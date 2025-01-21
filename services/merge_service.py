import os
import requests
from tempfile import NamedTemporaryFile
import ffmpeg

from services import transcribe

def process_and_merge_urls(chunk_urls, output_file_path="merged_video.mp4"):
    try:
        # Download chunks and save them
        downloaded_chunks = download_chunks(chunk_urls)

        # Merge chunks into a single file
        merge_chunks(downloaded_chunks, output_file_path)

        audio_file = extract_audio(output_file_path)

        return transcribe(audio_file)
    except Exception as e:
        raise RuntimeError(f"Error during video merging: {e}")

# Downloads all chunks and saves them as temporary files
def download_chunks(chunk_urls):
    temp_files = []

    for i, chunk_url in enumerate(chunk_urls):
        print(f"Downloading chunk {i + 1}/{len(chunk_urls)}: {chunk_url}")

        try:
            # Send GET request
            response = requests.get(chunk_url, stream=True)
            response.raise_for_status()

            # Save to a temporary file
            temp_file = NamedTemporaryFile(delete=False)
            with temp_file as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            temp_files.append(temp_file.name)
            print(f"Chunk {i + 1} saved to: {temp_file.name}")

        except requests.RequestException as e:
            print(f"Failed to download chunk {i + 1}. Error: {e}")

    return temp_files

# Merges all chunk files into a single output file
def merge_chunks(chunk_files, output_file_path):
    with open(output_file_path, "wb") as output_file:
        for chunk_file in chunk_files:
            print(f"Merging chunk: {chunk_file}")
            with open(chunk_file, "rb") as input_file:
                output_file.write(input_file.read())

    # Clean up temporary files
    for chunk_file in chunk_files:
        os.remove(chunk_file)
        print(f"Deleted temporary file: {chunk_file}")

    print("All chunks merged and temporary files cleaned up.")

def extract_audio(video_path, audio_path="temp_audio.wav"):
    ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)
    return audio_path