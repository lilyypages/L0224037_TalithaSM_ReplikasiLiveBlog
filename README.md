# 📌 Rekomendasi Nusantara (FastAPI + Streamlit)

Aplikasi **Live Blog Rekomendasi** berbasis:

* ⚡ **FastAPI** (Backend API)
* 🎨 **Streamlit** (Frontend UI)

User bisa:

* Register untuk mendapatkan **Access ID**
* Membagikan rekomendasi (Kuliner, Hotel, Wisata, Kegiatan)
* Mengedit & menghapus rekomendasi (**FULL CRUD**)
* Melihat feed rekomendasi dari user lain

---

## 📁 Struktur Project

```
liveblog_replika-fastapi/
│
├── main.py                # Backend FastAPI
├── app.py                 # Frontend Streamlit
├── rekomendasi_db.json    # Database sederhana (JSON)
└── __pycache__/           # Cache Python (abaikan)
```

---

## ⚙️ Requirements

Pastikan sudah install:

* Python 3.8+
* pip

Install dependencies:

```bash
pip install fastapi uvicorn streamlit requests
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Jalankan Backend (FastAPI)

Masuk ke folder project:

```bash
cd D:\Praktikum-IPBD\liveblog_replika-fastapi
```

Jalankan server:

```bash
uvicorn main:app --reload
```

Jika berhasil:

```
Uvicorn running on http://127.0.0.1:8000
```

Cek API di browser:

```
http://127.0.0.1:8000/docs
```

---

### 2. Jalankan Frontend (Streamlit)

Buka terminal baru (jangan matikan backend), lalu jalankan:

```bash
streamlit run app.py
```

Akan terbuka di browser:

```
http://localhost:8501
```

---

## 🧠 Cara Menggunakan (Frontend)

### 1. Register

* Isi nama, umur, dan kota di sidebar
* Klik **Daftar**
* Simpan **Access ID**

### 2. Post Rekomendasi

* Masukkan ID
* Pilih kategori
* Isi lokasi & konten
* Klik **Kirim Rekomendasi**

### 3. Lihat Feed

* Semua postingan tampil di halaman utama

---

## 🧪 Testing API dengan Postman

Pastikan backend sudah berjalan:

```bash
uvicorn main:app --reload
```

Base URL:

```
http://127.0.0.1:8000
```

---

### 🔑 1. Register User

**Method:** `POST`
**URL:**

```
http://127.0.0.1:8000/register
```

**Body → raw JSON:**

```json
{
  "nama": "Lia",
  "umur": 20,
  "asal_kota": "Solo"
}
```

**Response:**

```json
{
  "message": "Selamat bergabung!",
  "your_id": "ID-101"
}
```

📌 Simpan `your_id` untuk langkah berikutnya

---

### 📝 2. Tambah Rekomendasi

**Method:** `POST`
**URL:**

```
http://127.0.0.1:8000/rekomendasi
```

**Body → raw JSON:**

```json
{
  "user_id": "ID-101",
  "kategori": "🍴 Kuliner",
  "lokasi": "Solo",
  "konten": "Nasi liwet di sini enak banget!"
}
```

**Response berhasil:**

```json
{
  "status": "Success",
  "data": {
    "post_id": 1,
    "nama_pengirim": "Lia",
    "kategori": "🍴 Kuliner",
    "lokasi": "Solo",
    "konten": "Nasi liwet di sini enak banget!",
    "waktu": "08 Apr 2026, 14:00"
  }
}
```

**Jika ID tidak valid:**

```json
{
  "detail": "ID Kamu tidak terdaftar!"
}
```

---

### 📡 3. Ambil Feed

**Method:** `GET`
**URL:**

```
http://127.0.0.1:8000/feed
```

**Response:**

```json
[
  {
    "post_id": 1,
    "nama_pengirim": "Lia",
    "kategori": "🍴 Kuliner",
    "lokasi": "Solo",
    "konten": "Nasi liwet di sini enak banget!",
    "waktu": "08 Apr 2026, 14:00"
  }
]
```

---

### ✏️ 4. Update Rekomendasi

**Method:** `PUT`
**URL:**

```
http://127.0.0.1:8000/rekomendasi/1
```

**Body:**

```json
{
  "user_id": "ID-101",
  "kategori": "🌴 Wisata",
  "lokasi": "Bali",
  "konten": "Pantainya bagus banget!"
}
```

**Response:**

```json
{
  "message": "Post berhasil diupdate",
  "data": {
    "post_id": 1,
    "nama_pengirim": "Lia",
    "kategori": "🌴 Wisata",
    "lokasi": "Bali",
    "konten": "Pantainya bagus banget!",
    "waktu": "08 Apr 2026, 14:00"
  }
}
```

---

### 🗑️ 5. Delete Rekomendasi

**Method:** `DELETE`
**URL:**

```
http://127.0.0.1:8000/rekomendasi/1
```

**Response:**

```json
{
  "message": "Post berhasil dihapus",
  "data": {
    "post_id": 1,
    "nama_pengirim": "Lia",
    "kategori": "🌴 Wisata",
    "lokasi": "Bali",
    "konten": "Pantainya bagus banget!",
    "waktu": "08 Apr 2026, 14:00"
  }
}
```

---

## ⚠️ Tips Pakai Postman

* Pilih:

  * **Body → raw → JSON**
* Jangan gunakan `form-data`
* Pastikan backend masih running
* Pastikan URL benar (`127.0.0.1:8000`)
* Pastikan method sesuai (POST / GET)

---

## 🔍 Alternatif Tanpa Postman

Gunakan Swagger UI:

```
http://127.0.0.1:8000/docs
```

Bisa langsung klik endpoint dan coba API tanpa Postman 👍

---

## 🗄️ Sistem Database

Menggunakan file JSON:

```
rekomendasi_db.json
```

Struktur:

```json
{
  "users": [],
  "posts": []
}
```

---

## ⚠️ Catatan Penting

* Backend harus dijalankan terlebih dahulu sebelum frontend
* Jangan ubah API URL di `main.py`:

```python
API_URL = "http://127.0.0.1:8000"
```

* Jika muncul error ID → pastikan sudah register dulu

---