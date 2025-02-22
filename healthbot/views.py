import openai
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse

# Set your OpenAI API key securely
openai.api_key = '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'  # Replace with environment variable if needed

logger = logging.getLogger(__name__)
print(f"Using OpenAI API Key: {openai.api_key}")
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
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Or whichever model you are using
                messages=[{"role": "user", "content": user_message}],
                max_tokens=150
            )

            # Log the full response for debugging
            logger.info(f"OpenAI response: {response}")

            return JsonResponse({"response": response['choices'][0]['message']['content'].strip()})

        except openai.error.OpenAIError as e:
            # Log detailed OpenAI error
            logger.error(f"OpenAI API error: {e}")
            logger.error(f"Error response: {e.http_body}")
            return JsonResponse({"error": f"OpenAI API error: {e}"}, status=500)

        except Exception as e:
            # Log generic error with traceback
            import traceback
            logger.error(f"An error occurred: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
