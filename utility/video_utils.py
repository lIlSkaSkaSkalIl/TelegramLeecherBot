import os
import subprocess
import asyncio
import re
import time
from utility.status_utils import format_status

def is_video(file_path: str) -> bool:
    video_extensions = ['.mp4', '.mkv', '.webm', '.mov', '.avi']
    ext = os.path.splitext(file_path)[1].lower()
    return ext in video_extensions

def smart_convert_to_mp4(input_file: str, output_file: str) -> bool:
    try:
        # Cek video codec
        probe_v = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=codec_name",
             "-of", "default=noprint_wrappers=1:nokey=1", input_file],
            capture_output=True, text=True
        )
        video_codec = probe_v.stdout.strip()

        # Cek audio codec
        probe_a = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=codec_name",
             "-of", "default=noprint_wrappers=1:nokey=1", input_file],
            capture_output=True, text=True
        )
        audio_codec = probe_a.stdout.strip()

        if video_codec == "h264" and audio_codec == "aac":
            cmd = ["ffmpeg", "-i", input_file, "-c", "copy", output_file]
        else:
            cmd = ["ffmpeg", "-i", input_file, "-c:v", "libx264", "-c:a", "aac", output_file]

        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Konversi gagal: {e}")
        return False

async def download_m3u8_video(url, output_path, status_message, client):
    try:
        filename = os.path.basename(output_path)
        start_time = time.time()

        process = await asyncio.create_subprocess_exec(
            "ffmpeg", "-i", url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        duration = None
        last_update = 0

        while True:
            line = await process.stderr.readline()
            if not line:
                break

            if "Duration" in line and duration is None:
                match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)
                if match:
                    h, m, s = map(float, match.groups())
                    duration = h * 3600 + m * 60 + s

            if "time=" in line:
                match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                if match and duration:
                    h, m, s = map(float, match.groups())
                    current = h * 3600 + m * 60 + s

                    percent = (current / duration) * 100
                    now = time.time()
                    if now - last_update > 5:
                        elapsed = now - start_time
                        status_text = format_status(
                            "📥 Mengunduh dari .m3u8",
                            filename,
                            done=int(current * 1024 * 512),
                            total=int(duration * 1024 * 512),
                            elapsed=elapsed
                        )
                        await status_message.edit_text(status_text)
                        last_update = now

        await process.wait()
        return process.returncode == 0

    except Exception as e:
        await status_message.edit(f"❌ Gagal parsing: `{e}`")
        return False
