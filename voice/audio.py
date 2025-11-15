from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from groq import Groq
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post('/transcribe')
async def transcribe_audio(file: UploadFile = File(None)):
    if not file:
        raise HTTPException(
            status_code=400, 
            detail='No file part in the request or the field name is incorrect. The field name must be "file".'
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Create a temporary file-like object for Groq API
        from io import BytesIO
        audio_file = BytesIO(file_content)
        audio_file.name = file.filename or "audio.m4a"
        
        # Transcribe using Groq Whisper API
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",  # or "whisper-large-v3-turbo" for faster processing
            file=audio_file,
            response_format="json"  # Options: json, text, verbose_json
        )
        
        return JSONResponse(content={"transcription": transcript.text})
    
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during transcription")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)