# 🤖 Telegram Leecher Bot — Versi 1.02,04

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lIlSkaSkaSkalIl/TelegramLeecherBot/blob/main/run_bot_colab.ipynb)

Bot Telegram ini dirancang untuk menerima direct download link (seperti dari Google Drive, MediaFire, Zippyshare, dll), mengunduh file tersebut, dan kemudian mengunggahnya kembali ke Telegram — secara otomatis melalui Google Colab.

---

## 🔧 Fitur Utama

- 🔗 Menerima link direct download
- 📥 Mengunduh file dari internet
- 📤 Mengunggah ulang file ke chat Telegram secara otomatis
- 📲 Bisa dijalankan langsung dari **Google Colab** tanpa perlu VPS atau perangkat lokal
- 🔐 Input token menggunakan form `getpass()` (tidak disimpan di file publik)

---

## 🚀 Cara Menjalankan

### 1. Siapkan Bot Telegram
- Buat bot baru melalui [@BotFather](https://t.me/BotFather)
- Catat `BOT_TOKEN` yang diberikan

### 2. Ambil API ID dan HASH
- Kunjungi [my.telegram.org](https://my.telegram.org)
- Login dan dapatkan `API_ID` dan `API_HASH`

### 3. Jalankan Bot dari Colab
- Klik tombol **"Open in Colab"** di atas
- Masukkan:
  - API ID
  - API HASH
  - BOT TOKEN
- Jalankan semua sel

---

## 📁 Struktur Proyek

```
Telegram_Uploader_Bot/
├── main.py                # Kode utama bot
├── requirements.txt       # Dependensi
├── run_bot_colab.ipynb    # File peluncur dari Google Colab
└── README.md              # Penjelasan proyek
```

---

## 🔒 Keamanan

- Token bot dan API ID tidak disimpan di file
- Semua data sensitif dimasukkan saat runtime lewat input form
- Aman untuk digunakan di repo publik

---

## 📌 Versi Saat Ini

> Versi: **v1.02,04**  
> Status: **Stabil & Aman**  
> Mode: **Google Colab (mobile friendly)**

---

## 🛠️ Pengembangan Selanjutnya (Roadmap)

- [ ] Modularisasi kode (`utils`, `handlers`)
- [ ] UI status upload/download realtime
- [ ] Tampilan Colab lebih interaktif dan informatif
