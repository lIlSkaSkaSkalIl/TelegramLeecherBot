import os, requests, time
from utility.status_format import format_status

async def process_link(client, message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Link tidak valid.")
        return

    msg = await message.reply("🔄 Menyiapkan download...")

    try:
        filename = url.split("/")[-1].split("?")[0] or "downloaded_file"
        r = requests.get(url, stream=True, timeout=60)
        if r.status_code != 200:
            return await msg.edit("❌ Gagal mengunduh.")

        total = int(r.headers.get("content-length", 0))
        done, start, last = 0, time.time(), 0

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024*1024):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    if time.time() - last > 5 or done == total:
                        await msg.edit(format_status("📥 Mengunduh", filename, done, total, time.time() - start))
                        last = time.time()

        await msg.edit("📤 Mengunggah ke Telegram...")
        upload_start = time.time()
        await client.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption="✅ File berhasil diunggah.",
            progress=upload_progress,
            progress_args=(msg, filename, os.path.getsize(filename), upload_start)
        )
        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Error:\n`{e}`")

def upload_progress(current, total, msg, filename, size, start_time):
    now = time.time()
    if now - start_time >= 0 and (current == total or (now - upload_progress.last_edit_time) >= 5):
        status = format_status("📤 Mengunggah", filename, current, total, now - start_time)
        try:
            msg.edit(status)
        except:
            pass
        upload_progress.last_edit_time = now

upload_progress.last_edit_time = 0
