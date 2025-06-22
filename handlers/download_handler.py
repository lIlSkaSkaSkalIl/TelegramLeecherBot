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
        await message.reply_document(filename)
        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Error:\n`{e}`")
