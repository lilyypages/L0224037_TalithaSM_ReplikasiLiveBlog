import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Rekomendasi Nusantara", layout="centered")

st.title("🗺️ Rekomendasi Nusantara")
st.markdown("*Live Blog Tempat Makan, Hotel, dan Kegiatan di Seluruh Indonesia*")

# --- SIDEBAR: PENDAFTARAN ---
with st.sidebar:
    st.header("🔑 Dapatkan Access ID")
    if 'my_id' not in st.session_state:
        with st.form("reg_form"):
            nama = st.text_input("Nama")
            umur = st.number_input("Umur", min_value=10)
            kota = st.text_input("Asal Kota")
            if st.form_submit_button("Daftar"):
                res = requests.post(f"{API_URL}/register", json={"nama":nama, "umur":umur, "asal_kota":kota})
                if res.status_code == 200:
                    st.session_state['my_id'] = res.json()['your_id']
                    st.success(f"ID Kamu: {st.session_state['my_id']}")
    else:
        st.info(f"ID Kamu: **{st.session_state['my_id']}**")
        if st.button("Hapus ID (Logout)"):
            del st.session_state['my_id']
            st.rerun()

# --- INPUT REKOMENDASI ---
st.subheader("Bagikan Rekomendasimu")
with st.container(border=True):
    u_id = st.text_input("Masukkan ID Kamu", value=st.session_state.get('my_id', ''))
    col1, col2 = st.columns(2)
    with col1:
        kat = st.selectbox("Kategori", ["🍴 Kuliner", "🏨 Hotel", "🌴 Wisata", "🏃 Kegiatan"])
    with col2:
        lok = st.text_input("Lokasi (Contoh: Salatiga, Surabaya)")
    
    isi = st.text_area("Apa rekomendasinya?", placeholder="Tuliskan pengalamanmu di sini...")
    
    if st.button("Kirim Rekomendasi"):
        if u_id and kat and lok and isi:
            payload = {
                "user_id": u_id, 
                "kategori": kat, 
                "lokasi": lok, 
                "konten": isi
            }
            
            # Melakukan request ke Backend
            res = requests.post(f"{API_URL}/rekomendasi", json=payload)
            
            if res.status_code == 200:
                st.success("✅ Rekomendasi berhasil dipublikasikan!")
                st.balloons() # Efek perayaan
                # Beri jeda sebentar lalu refresh
                import time
                time.sleep(1)
                st.rerun()
            elif res.status_code == 401:
                # Ini notifikasi jika ID tidak ditemukan di database
                st.error("🚫 ID Tidak Terdaftar! Silakan daftar di sidebar terlebih dahulu untuk mendapatkan Access ID.")
            else:
                st.error(f"❌ Terjadi kesalahan: {res.json().get('detail', 'Error tidak diketahui')}")
        else:
            # Notifikasi jika ada form yang kosong
            st.warning("⚠️ Mohon lengkapi semua data (ID, Kota, dan Isi Rekomendasi)!")

st.divider()

# --- TAMPILAN FEED ---
try:
    feed = requests.get(f"{API_URL}/feed").json()
    for p in feed:
        with st.container(border=True):
            st.markdown(f"### {p['kategori']} di {p['lokasi']}")
            st.write(p['konten'])
            st.caption(f"Oleh: **{p['nama_pengirim']}** | 🕒 {p['waktu']}")
except:
    st.info("Belum ada rekomendasi. Jadilah yang pertama!")