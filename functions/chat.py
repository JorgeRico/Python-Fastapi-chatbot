# from openai import OpenAI
import openai
from decouple import config
import os
from dotenv import load_dotenv
from functions.context import load_context, reset_context, update_context

SYSTEM_ROLE    = "system"
ASSISTANT_ROLE = "assistant"
USER_ROLE      = "user"

# init client
def init_client():
    load_dotenv(override = True)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    return openai.OpenAI(base_url = "https://models.inference.ai.azure.com", api_key = GITHUB_TOKEN)

# start chat - define system context
def start_chat():
    new_context = input("\n - Insert initial context: ")
    reset_context(SYSTEM_ROLE, new_context)

# add extra message conversation
def add_chat_message(client, message):
    update_context(USER_ROLE, message)
    context = load_context()

    return get_response(context, client)

# add assistant message to context
def add_assistant_chat_message(message):
    update_context(ASSISTANT_ROLE, message)

# chat response
def get_response(context, client):
    try:
        completion = client.chat.completions.create(
            model    = config("GITHUB_MODEL"),
            messages = context
        )

        return completion.choices[0].message.content
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e)

#  transcribe audio file
# async def transcribe_audio(client, audio_file):
#     try:
#         audio_file = open(audio_file, "rb")
        
#         transcript = await client.audio.transcriptions.create(
#             model = config("TRANSCRIPTION_MODEL"),
#             file  = audio_file, 
#         )
#         print(transcript.text)

#         return transcript.text
#     except openai.APIConnectionError as e:
#         print("The server could not be reached")
#         print(e.__cause__)  # an underlying Exception, likely raised within httpx.
#     except openai.RateLimitError as e:
#         print("A 429 status code was received; we should back off a bit.")
#     except openai.APIStatusError as e:
#         print("Another non-200-range status code was received")
#         print(e.status_code)
#         print(e)