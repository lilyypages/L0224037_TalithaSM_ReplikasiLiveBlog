from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI()
DB_FILE = "rekomendasi_db.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": [], "posts": []}, f)

def load_db():
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- MODELS ---
class UserProfile(BaseModel):
    nama: str
    umur: int
    asal_kota: str

class PostRekomendasi(BaseModel):
    user_id: str
    kategori: str # Kuliner, Hotel, Wisata, Kegiatan
    lokasi: str   # Nama Kota (Solo, Salatiga, Jakarta, dll)
    konten: str

# --- ENDPOINTS ---

@app.post("/register")
def register(profile: UserProfile):
    db = load_db()
    new_id = f"ID-{len(db['users']) + 101}" # Mulai dari ID-101 agar terlihat keren
    user_data = {
        "user_id": new_id,
        "nama": profile.nama,
        "umur": profile.umur,
        "asal_kota": profile.asal_kota
    }
    db['users'].append(user_data)
    save_db(db)
    return {"message": "Selamat bergabung!", "your_id": new_id}

@app.post("/rekomendasi")
def create_post(post: PostRekomendasi):
    db = load_db()
    user = next((u for u in db['users'] if u['user_id'] == post.user_id), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="ID Kamu tidak terdaftar!")

    new_post = {
        "post_id": len(db['posts']) + 1,
        "nama_pengirim": user['nama'],
        "kategori": post.kategori,
        "lokasi": post.lokasi,
        "konten": post.konten,
        "waktu": datetime.now().strftime("%d %b %Y, %H:%M")
    }
    db['posts'].append(new_post)
    save_db(db)
    return {"status": "Success", "data": new_post}

@app.get("/feed")
def get_feed():
    db = load_db()
    return db['posts'][::-1]

@app.put("/rekomendasi/{post_id}")
def update_post(post_id: int, updated: PostRekomendasi):
    db = load_db()
    
    for p in db['posts']:
        if p['post_id'] == post_id:
            p['kategori'] = updated.kategori
            p['lokasi'] = updated.lokasi
            p['konten'] = updated.konten
            save_db(db)
            return {"message": "Post berhasil diupdate", "data": p}
    
    raise HTTPException(status_code=404, detail="Post tidak ditemukan")

@app.delete("/rekomendasi/{post_id}")
def delete_post(post_id: int):
    db = load_db()
    
    for i, p in enumerate(db['posts']):
        if p['post_id'] == post_id:
            deleted = db['posts'].pop(i)
            save_db(db)
            return {"message": "Post berhasil dihapus", "data": deleted}
    
    raise HTTPException(status_code=404, detail="Post tidak ditemukan")