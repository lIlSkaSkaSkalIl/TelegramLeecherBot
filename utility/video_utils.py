import subprocess
import mimetypes

def is_video(filename: str) -> bool:
    """
    Cek apakah file termasuk jenis video berdasarkan MIME type.
    """
    mtype, _ = mimetypes.guess_type(filename)
    return mtype and mtype.startswith("video")

def convert_to_mp4(input_file: str, output_file: str = "converted_output.mp4"):
    """
    Konversi file video ke format .mp4 agar bisa diputar di Telegram.
    """
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        "-movflags", "+faststart",
        output_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
