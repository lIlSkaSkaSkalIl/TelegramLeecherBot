import subprocess
import asyncio
import re
from utility.status_utils import format_eta

async def download_m3u8_video(url, output_path, status_message, client):
    try:
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
                match = re.search(r"Duration: (\d+):(\d+):(\d+.\d+)", line)
                if match:
                    h, m, s = map(float, match.groups())
                    duration = h * 3600 + m * 60 + s

            if "time=" in line:
                match = re.search(r"time=(\d+):(\d+):(\d+.\d+)", line)
                if match:
                    h, m, s = map(float, match.groups())
                    current = h * 3600 + m * 60 + s

                    if duration:
                        percent = (current / duration) * 100
                        eta = format_eta(duration - current)
                        now = asyncio.get_event_loop().time()
                        if now - last_update > 5:
                            await status_message.edit_text(
                                f"📥 Downloading: `{percent:.2f}%`\n⏳ ETA: `{eta}`"
                            )
                            last_update = now

        await process.wait()
        return process.returncode == 0

    except Exception as e:
        await status_message.edit(f"❌ Error: {str(e)}")
        return False
