# 📤 Telegram Uploader Bot

Versi: **1.02.06**  
Bot Telegram untuk mengunduh file dari direct download link (HTTP/HTTPS) dan mengunggahnya kembali ke Telegram (chat pribadi).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/lIlSkaSkaSkalIl/TelegramLeecherBot/blob/main/run_bot_colab.ipynb)

---

## 🔧 Fitur

- 📥 Unduh dari direct link (misalnya `https://example.com/file.zip`)
- 📤 Upload otomatis ke Telegram
- 📊 Status download tampil dengan:
  - Nama file
  - Ukuran
  - Kecepatan
  - Estimasi waktu selesai (ETA)
  - Ekstensi
- 🔄 Status diperbarui setiap 5 detik
- ✅ Terstruktur dengan refactor:
  - `main.py` → alur utama
  - `handlers/download_handler.py` → logika download/upload
  - `utility/status_format.py` → fungsi status & ETA

---

## 📁 Struktur Folder

```
TelegramLeecherBot/
├── main.py
├── handlers/
│   ├── __init__.py
│   └── download_handler.py
├── utility/
│   ├── __init__.py
│   └── status_format.py
├── requirements.txt
└── run_bot_colab.ipynb
```

---

## ▶️ Cara Menjalankan

### 🔹 Google Colab:
1. Masukkan `API_ID`, `API_HASH`, dan `BOT_TOKEN`
2. Jalankan sel
3. Kirim link ke bot via Telegram

### 🔹 VPS / Replit / Lokal:
```bash
export API_ID=123456
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token
python main.py
```

---

## 💡 Catatan

- Bot hanya bekerja untuk **direct HTTP/HTTPS links**
- Tidak mendukung Google Drive, Mega, YouTube (untuk sekarang)
- Upload maksimal 2GB (batas Telegram Bot API)

---

## 🤝 Kontribusi

Struktur disesuaikan dari [@lIlSkaSkaSkalIl/TelegramLeecherBot](https://github.com/lIlSkaSkaSkalIl/TelegramLeecherBot)

