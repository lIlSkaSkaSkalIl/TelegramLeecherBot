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
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    now = time.time()
                    if now - last > 5 or done == total:
                        await msg.edit(format_status("📥 Mengunduh", filename, done, total, now - start))
                        last = now

        await msg.edit("📤 Mengunggah ke Telegram...")
        upload_start = time.time()

        async def upload_progress(current, total):
            now = time.time()
            if now - upload_progress.last_update > 5 or current == total:
                try:
                    await msg.edit(format_status("📤 Mengunggah", filename, current, total, now - upload_start))
                    upload_progress.last_update = now
                except:
                    pass

        upload_progress.last_update = 0

        await client.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption="✅ File berhasil diunggah.",
            progress=upload_progress
        )

        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Error:\n`{e}`")
