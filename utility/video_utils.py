import subprocess
import mimetypes
import time

def is_video(filename: str) -> bool:
    """
    Deteksi apakah file adalah video berdasarkan MIME type.
    """
    mtype, _ = mimetypes.guess_type(filename)
    return mtype and mtype.startswith("video")

def convert_to_mp4(input_file: str, output_file: str = "converted_output.mp4") -> float:
    """
    Konversi video ke MP4 agar bisa diputar di Telegram.
    - Preset ultrafast agar lebih cepat.
    - Menampilkan log ffmpeg.
    - Mengembalikan waktu eksekusi dalam detik.
    """
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "ultrafast",
        "-movflags", "+faststart",
        output_file
    ]

    print(f"🚀 Memulai konversi video: {input_file}")
    start = time.time()

    subprocess.run(cmd, check=True)

    end = time.time()
    duration = end - start
    print(f"✅ Konversi selesai dalam {duration:.2f} detik")

    return duration
