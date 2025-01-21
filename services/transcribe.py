from flask import Flask, request, jsonify
import whisper


model = whisper.load_model("base")

def transcribe(video_file):
    try:
        #merged video file is now send thru whisper ai
        result = model.transcribe(video_file)

        return result['text']

    except Exception as e:
        return RuntimeError("Error during transcription: {str(e)}")