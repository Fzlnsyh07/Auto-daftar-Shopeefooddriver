import requests, re, time
from bs4 import BeautifulSoup
from lxml import html
from fake_useragent import UserAgent

ua = UserAgent()
r = requests.Session()

def daftar():
    # Baca data dari file
    try:
        with open("data.txt", "r") as f:
            line = f.readline().strip()
            datas = line.split(":")
        if len(datas) < 6:
            print("❌ Format data.txt tidak lengkap. Format: nama:nohp:jkkode:email:domisili:tahun")
            return
    except Exception as e:
        print("❌ Gagal membaca data.txt:", e)
        return

    nama, nohp, jkkode, email, domisili, tahun = datas

    url = "https://survey.alchemer.com/s3/6406341/Formulir-Pendaftaran-Driver-ShopeeFood"
    headers = {
        "user-agent": ua.random,
        "referer": url,
        "origin": "https://survey.alchemer.com"
    }

    # --- Page 1
    data1 = {
        "sg_currentpageid": "3",
        "sgE-6406341-3-3": nama,
        "sgE-6406341-3-4": nohp,
        "sgE-6406341-3-5": jkkode,
        "sgE-6406341-3-6": email,
        "sgE-6406341-3-7": "10056",  # Domisili (kode)
        "sGizmoNextButton": "Next"
    }

    res1 = r.post(url, headers=headers, data=data1)
    soup1 = BeautifulSoup(res1.text, 'html.parser')
    try:
        script = next(s for s in soup1.find_all('script') if '"session":' in s.text)
        session = re.search(r'"session":\s*"(.*?)"', script.text).group(1)
        survey_id = re.search(r'"id":\s*(\d+)', script.text).group(1)
    except Exception as e:
        print("❌ Gagal ambil session/ID:", e)
        return

    # --- Page 2
    data2 = {
        "sg_currentpageid": "4",
        "sgE-6406341-3-3": nama,
        "sgE-6406341-3-4": nohp,
        "sgE-6406341-3-5": jkkode,
        "sgE-6406341-3-6": email,
        "sgE-6406341-3-7": "10056",
        "sGizmoNextButton": "Next",
        "sg_surveyident": survey_id,
        "sg_sessionid": session,
        "sgE-6406341-4-9": domisili,
        "sgE-6406341-4-8": tahun,
        "sGizmoSubmitButton": "Submit"
    }

    res2 = r.post(url, headers=headers, data=data2)

    tree = html.fromstring(res2.content)
    texts = tree.xpath("//text()")
    cek = next((t for t in texts if "Terima kasih atas ketertarikanmu" in t), None)

    if cek:
        print("✅ Berhasil mendaftar!")
        print(f"📩 Pesan: {cek}")
    else:
        print("❌ Gagal membaca pesan sukses dari server.")
        with open("hasil_submit.html", "w", encoding="utf-8") as f:
            f.write(res2.text)
        print("📄 Hasil disimpan ke hasil_submit.html untuk dicek manual.")


# Jalankan
print("=== AUTO DAFTAR SHOPEEFOOD DRIVER ===")
daftar()
