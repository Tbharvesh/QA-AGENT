import os
import whisper # type: ignore
import subprocess
from pathlib import Path
from yt_dlp import YoutubeDL
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

def download_youtube_audio(youtube_url: str, output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "video_audio.%(ext)s")
    # Set path to your ffmpeg folder
    ffmpeg_path = "C:\\ffmpeg\\bin"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    final_path = os.path.join(output_dir, "video_audio.mp3")
    return final_path


def transcribe_audio(audio_path: str, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    # Step 1: Provide the Recruter.ai YouTube URL
    YT_URL = "https://www.youtube.com/watch?v=IK62Rk47aas"
    
    # Step 2: Download audio from YouTube video
    audio_path = download_youtube_audio(YT_URL)
    print(f"Downloaded audio to {audio_path}")

    # Step 3: Transcribe using Whisper
    transcript = transcribe_audio(audio_path)
    
    # Step 4: Save to file
    output_file = Path("assets/transcription.txt")
    output_file.write_text(transcript, encoding="utf-8") # type: ignore
    print(f"Transcript saved to {output_file}")
