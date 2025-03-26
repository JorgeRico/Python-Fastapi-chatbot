from functions.context import reset_context
from functions.chat import SYSTEM_ROLE
from fastapi import FastAPI, HTTPException, File, UploadFile
from functions.errors import notFound
from starlette.middleware.cors import CORSMiddleware
from functions.codes import HTTP_200, HTTP_204, HTTP_500
from functions.chat import init_client, add_chat_message, add_assistant_chat_message
from time import time
from functions.elevenlabs import send_file_to_elevenlabs

app = FastAPI(exception_handlers={
    404: notFound
})

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/health", status_code=HTTP_200, description="Health endpoint")
def index():
    return { "message": "It works !!!!" }

@app.post("/reset-context", status_code=HTTP_200, description="Reset context endpoint")
def reset_chat_context(context="Talk like a pirate. Max 2 paragraphs"):
    try:
        reset_context(SYSTEM_ROLE, context)
    except: 
        raise HTTPException(status_code=HTTP_500, detail="Context reset error")

    return ({"message" : "context reset"})

@app.post("/send-message", status_code=HTTP_204, description="Send user role message")
async def send_message(message):
    try:
        client   = init_client()
        response = add_chat_message(client, message)
        add_assistant_chat_message(response)
    except:
        raise HTTPException(status_code=HTTP_500, detail="Assistant error")

    return ({"message" : response})

@app.post("/audio-file", status_code=HTTP_200, description="Transcribe audio file")
def upload_file(file: UploadFile = File(...)):
    try:
        milliseconds = int(time() * 1000)
        filename     = str(milliseconds) + '.mp3'
        mp3_folder   = './mp3/upload/'
        file_path    = mp3_folder + filename

        # save on a folder
        with open(file_path , "wb") as buffer:
            buffer.write(file.file.read())

        response = send_file_to_elevenlabs(filename, file_path)
    except:
        raise HTTPException(status_code=HTTP_500, detail="Upload File error")

    return ({"message" : response})
    