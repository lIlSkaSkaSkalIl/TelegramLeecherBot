import subprocess
import mimetypes
import json
import time

def is_video(filename: str) -> bool:
    mtype, _ = mimetypes.guess_type(filename)
    return mtype and mtype.startswith("video")

def get_codec_info(filename: str) -> dict:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=codec_name", "-of", "json", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        video_codec = json.loads(result.stdout)["streams"][0]["codec_name"]

        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
             "stream=codec_name", "-of", "json", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        audio_codec = json.loads(result.stdout)["streams"][0]["codec_name"]

        return {"video": video_codec, "audio": audio_codec}

    except Exception:
        return {"video": None, "audio": None}

def smart_convert_to_mp4(input_file: str, output_file: str = "converted_output.mp4") -> float:
    codec_info = get_codec_info(input_file)
    is_compatible = (
        codec_info["video"] == "h264" and
        codec_info["audio"] == "aac" and
        input_file.endswith(".mp4")
    )

    if is_compatible:
        cmd = ["ffmpeg", "-y", "-i", input_file, "-c", "copy", "-movflags", "+faststart", output_file]
        print("⚡ Melakukan remux cepat (tanpa encode)...")
    else:
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "ultrafast",
            "-movflags", "+faststart",
            output_file
        ]
        print("🔧 Melakukan re-encode karena codec tidak cocok...")

    start = time.time()
    subprocess.run(cmd, check=True)
    end = time.time()

    print(f"✅ Konversi selesai dalam {end - start:.2f} detik")
    return end - start
