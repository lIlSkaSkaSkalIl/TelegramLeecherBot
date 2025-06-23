import subprocess
import asyncio
import re
import os
import time
from utility.status_utils import format_status

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
