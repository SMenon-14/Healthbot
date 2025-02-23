from openai import OpenAI
import json
import pandas as pd
import logging
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import requests

from healthbot.models import MedicalCondition

# Set your OpenAI API key securely

client = OpenAI(api_key=":)")
csv_data = pd.read_csv('/UHCFormularyData.csv')  # Update with your file path


def get_drug_info(query):
    # Convert the query to title case to match the drug names in a case-insensitive manner
    query = query.strip().title()
    # Filter the DataFrame for rows that match the drug name
    drug_info = csv_data[csv_data['Drug Name'].str.contains(query, case=False, na=False)]

    if drug_info.empty:
        print("returning empty")
        return 0

    # Extract the relevant columns
    relevant_columns = ['Drug Name', 'Brand or Generic', 'Drug Tier', 'Coverage Rules or Limits on Use']
    return drug_info[relevant_columns].to_dict(orient='records')

def rag_drug_info(query):
    # Step 1: Retrieve relevant drug information
    drug_info = get_drug_info(query)  # Assuming `get_drug_info` fetches data from DB
    if drug_info is 0:
        print("Found this")
        return f"""You are a healthcare assistant, answer the user inputted question: {query}"""
    if drug_info:
        first_drug = drug_info[0]
        name = first_drug['Drug Name']
        drug_tier = first_drug['Drug Tier']
        brand_or_generic = first_drug['Brand or Generic']
        coverage_rules = first_drug['Drug Tier']
        # Step 2: Construct the prompt using the retrieved information
        prompt = f"""
        You are a healthcare assistant. Below is some information about a drug:
        Name: {name}
        Drug Tier: {drug_tier}
        Brand or Generic: {brand_or_generic}
        Coverage Rules Under United Healthcare: {coverage_rules}

        User asked: "{query}"
        Provide a detailed, helpful response based on the above information and your own knowledge and TELL THE USER WHAT THE UNITED HEALTH CARE COVERAGE RULES ARE!!!!!
        """
    return prompt

def index(request):
    return render(request, 'index.html')

def page1(request):
    return render(request, 'medications.html')

def page2(request):
    return render(request, 'conditions.html')

def page3(request):
    return render(request, 'other.html')

def home(request):
    return render(request, 'home.html')

def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            # Check if there's a message
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # If there's no history, initialize it
            if 'conversation_history' not in request.session:
                request.session['conversation_history'] = []

            # Add the new user message to the conversation history
            conversation_history = request.session['conversation_history']
            conversation_history.append({"role": "user", "content": user_message})
            rag_prompt = rag_drug_info(user_message)
            conversation_history.append({"role": "system", "content": rag_prompt})

            # OpenAI ChatCompletion request with full conversation history
            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # You can use a larger model if needed
                store=True,
                messages=conversation_history  # Send the entire conversation history
            )

            # Extract the bot's response
            response_content = completion.choices[0].message.content.strip()

            # Add the bot's response to the conversation history
            conversation_history.append({"role": "assistant", "content": response_content})

            # Save the updated conversation history back to the session
            request.session['conversation_history'] = conversation_history

            return JsonResponse({"response": format_response(response_content)})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
def format_response(response_content):
    """
    Function to format the content returned by the OpenAI API into a more structured format
    """
    # Example: Split content by newlines, and format headings and lists
    lines = response_content.split('\n')
    formatted_content = ""

    for line in lines:
        if line.startswith("###"):  # Example for subheading (like ### Subheading)
            formatted_content += f"<h3>{line[3:].strip()}</h3>"
        elif line.startswith("##"):  # Example for main heading (like ## Heading)
            formatted_content += f"<h2>{line[2:].strip()}</h2>"
        elif line.startswith("*"):  # Example for list item (like * Item)
            formatted_content += f"<ul><li>{line[1:].strip()}</li></ul>"
        else:
            formatted_content += f"<p>{line.strip()}</p>"

    return formatted_content