from openai import OpenAI
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse

# Set your OpenAI API key securely

client = OpenAI()

#logger = logging.getLogger(__name__)
def index(request):
    return render(request, 'index.html')

def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # OpenAI ChatCompletion request
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            # Log the full response for debugging
            #logger.info(f"OpenAI response: {completion}")
            response_content = completion.choices[0].message.content

            return JsonResponse({"response": response_content.strip()})
            #return JsonResponse({"response": response['choices'][0]['message']['content'].strip()})

        except Exception as e:
            # Log generic error with traceback
            import traceback
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
