# 🤖 Telegram Uploader Bot — Versi 1.02,03

Bot ini dibuat menggunakan Python dan berjalan di Google Colab.  
Fungsinya adalah untuk **mengunduh file dari direct download link (URL)** dan **mengunggahnya langsung ke Telegram**, baik sebagai file atau dokumen.

---

## 🧠 Fitur Utama

- 🔗 Terima link download langsung (http/https)
- 📥 Unduh file dari internet
- 📤 Upload otomatis ke obrolan Telegram pribadi
- 📡 Bisa dijalankan langsung dari Google Colab
- 🔐 Aman: API ID, HASH, dan BOT TOKEN dimasukkan lewat form input (tidak disimpan di kode)
- 🧪 Fokus stabilitas (belum dimodularisasi — akan dilakukan di versi selanjutnya)

---

## 🚀 Cara Menggunakan

### 📌 Persiapan
1. Buat Bot Telegram dari [@BotFather](https://t.me/BotFather)
2. Dapatkan:
   - API ID & API HASH dari [my.telegram.org](https://my.telegram.org)
   - BOT TOKEN dari BotFather

### ▶️ Jalankan dari Google Colab

1. Buka file [`run_bot_colab.ipynb`](run_bot_colab.ipynb)
2. Masukkan `API_ID`, `API_HASH`, dan `BOT_TOKEN` di form input
3. Jalankan semua sel
4. Bot akan aktif dan menunggu pesan link dari Telegram

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

## 🛡️ Keamanan

- Tidak ada token atau API yang disimpan dalam file publik
- Semua konfigurasi sensitif diinput manual saat runtime
- Aman untuk diupload ke GitHub secara publik

---

## 📌 Versi Saat Ini

> Versi: **v1.02,03**  
> Status: **Stabil & Aman**  
> Mode: Google Colab (belum modular)

---

## 🤝 Pengembangan Lanjutan

- [ ] Modularisasi handler & utilitas (v1.03)
- [ ] UI Colab lebih interaktif
- [ ] Pemrosesan status progres (upload/download)

---

Proyek ini dikelola dan dikembangkan untuk mempermudah pengelolaan file dari URL ke Telegram secara otomatis dan sederhana.
