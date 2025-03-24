# Python chat
> Examples to work with context
> Upload file and transcript with elevenlabs

## install

```bash
pip install starlette fastapi uvicorn python-multipart requests
```

## .env file

```bash
    OPENAI_KEY=YOUR-OPENAI-KEY
    OPENAI_MODEL=gpt-3.5-turbo
    TRANSCRIPTION_MODEL=whisper-1
```

## execute

```bash
    uvicorn main:app --reload
```

## swagger

```bash
    http://127.0.0.1:8000/docs
```

## voice recorder

```bash
> https://online-voice-recorder.com/es/
> https://elevenlabs.io/
```
