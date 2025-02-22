from openai import OpenAI
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse

# Set your OpenAI API key securely

client = OpenAI(
  api_key=":)"
)

#logger = logging.getLogger(__name__)
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