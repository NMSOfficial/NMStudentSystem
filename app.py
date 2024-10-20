import tkinter as tk
import sqlite3
import bcrypt
from tkinter import messagebox
from tkinter import ttk

def veritabanı_oluştur():
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanici (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anahtar TEXT UNIQUE,
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ogrenci (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anahtar TEXT,
                        okul TEXT,
                        okul_no TEXT,
                        telefon TEXT,
                        kulup TEXT,
                        sinif TEXT,
                        adsoyad TEXT,
                        dogum_tarihi TEXT)''')
    conn.commit()
    conn.close()

def kaydet_kullanici(anahtar, sifre):
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    random_tuz = 12
    hashed_password = bcrypt.hashpw(sifre.encode('utf-8'), bcrypt.gensalt(random_tuz))
    try:
        cursor.execute('INSERT INTO kullanici (anahtar, password) VALUES (?, ?)', (anahtar, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Anahtar zaten kayıtlı.")
    conn.close()

def giris_yap(anahtar, sifre):
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM kullanici WHERE anahtar = ?', (anahtar,))
    result = cursor.fetchone()
    conn.close()
    if result and bcrypt.checkpw(sifre.encode('utf-8'), result[0]):
        return True
    else:
        return False

def kaydet_ogrenci(anahtar, okul, okul_no, telefon, kulup, sinif, adsoyad, dogum_tarihi):
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ogrenci (anahtar, okul, okul_no, telefon, kulup, sinif, adsoyad, dogum_tarihi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (anahtar, okul, okul_no, telefon, kulup, sinif, adsoyad, dogum_tarihi))
    conn.commit()
    conn.close()

def ogrencileri_goster(anahtar):
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute('SELECT okul, okul_no, telefon, kulup, sinif, adsoyad, dogum_tarihi FROM ogrenci WHERE anahtar = ?', (anahtar,))
    ogrenciler = cursor.fetchall()
    conn.close()
    
    if not ogrenciler:
        messagebox.showinfo("Bilgi", "Kayıtlı öğrenci yok.")
    else:
        for widget in frame.winfo_children():
            widget.destroy()

        for i, ogrenci in enumerate(ogrenciler, start=1):
            lbl_ogrenci = tk.Label(frame, text=f"Öğrenci {i}: {ogrenci}", font=("SF Pro Display", 14), bg="#fff")
            lbl_ogrenci.pack(pady=5)

        btn_geri = tk.Button(frame, text="Geri Dön", font=("SF Pro Display", 14), command=ekran_giris)
        btn_geri.pack(pady=10)

def ekran_giris():
    for widget in frame.winfo_children():
        widget.destroy()

    label_logo = tk.Label(frame, text="NMStudentSystem", font=("SF Pro Display", 24), bg="#fff")
    label_logo.pack(pady=10)

    lbl_anahtar = tk.Label(frame, text="Anahtar:", font=("SF Pro Display", 14), bg="#fff")
    lbl_anahtar.pack(pady=5)
    entry_anahtar = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_anahtar.pack(pady=5)

    lbl_sifre = tk.Label(frame, text="Şifre:", font=("SF Pro Display", 14), bg="#fff")
    lbl_sifre.pack(pady=5)
    entry_sifre = tk.Entry(frame, font=("SF Pro Display", 14), show="*")
    entry_sifre.pack(pady=5)

    def giris_buton():
        anahtar = entry_anahtar.get()
        sifre = entry_sifre.get()
        if giris_yap(anahtar, sifre):
            ekran_kayit(anahtar)
        else:
            messagebox.showerror("Hata", "Giriş başarısız.")

    btn_giris = tk.Button(frame, text="Giriş Yap", font=("SF Pro Display", 14), command=giris_buton)
    btn_giris.pack(pady=10)

    btn_kayit = tk.Button(frame, text="Kayıt Ol", font=("SF Pro Display", 14), command=ekran_kayit_ol)
    btn_kayit.pack(pady=10)

def ekran_kayit(anahtar):
    for widget in frame.winfo_children():
        widget.destroy()

    label_ogrenci = tk.Label(frame, text="Öğrenci Bilgileri", font=("SF Pro Display", 20), bg="#fff")
    label_ogrenci.pack(pady=10)

    lbl_okul = tk.Label(frame, text="Okul:", font=("SF Pro Display", 14), bg="#fff")
    lbl_okul.pack(pady=5)
    entry_okul = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_okul.pack(pady=5)

    lbl_okul_no = tk.Label(frame, text="Okul Numarası:", font=("SF Pro Display", 14), bg="#fff")
    lbl_okul_no.pack(pady=5)
    entry_okul_no = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_okul_no.pack(pady=5)

    lbl_telefon = tk.Label(frame, text="Telefon Numarası:", font=("SF Pro Display", 14), bg="#fff")
    lbl_telefon.pack(pady=5)
    entry_telefon = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_telefon.pack(pady=5)

    lbl_kulup = tk.Label(frame, text="Kulüp:", font=("SF Pro Display", 14), bg="#fff")
    lbl_kulup.pack(pady=5)
    entry_kulup = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_kulup.pack(pady=5)

    lbl_sinif = tk.Label(frame, text="Sınıf:", font=("SF Pro Display", 14), bg="#fff")
    lbl_sinif.pack(pady=5)
    entry_sinif = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_sinif.pack(pady=5)

    lbl_adsoyad = tk.Label(frame, text="Ad Soyad:", font=("SF Pro Display", 14), bg="#fff")
    lbl_adsoyad.pack(pady=5)
    entry_adsoyad = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_adsoyad.pack(pady=5)

    lbl_dogum_tarihi = tk.Label(frame, text="Doğum Tarihi:", font=("SF Pro Display", 14), bg="#fff")
    lbl_dogum_tarihi.pack(pady=5)
    entry_dogum_tarihi = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_dogum_tarihi.pack(pady=5)

    def kaydet_buton():
        okul = entry_okul.get()
        okul_no = entry_okul_no.get()
        telefon = entry_telefon.get()
        kulup = entry_kulup.get()
        sinif = entry_sinif.get()
        adsoyad = entry_adsoyad.get()
        dogum_tarihi = entry_dogum_tarihi.get()
        kaydet_ogrenci(anahtar, okul, okul_no, telefon, kulup, sinif, adsoyad, dogum_tarihi)
        messagebox.showinfo("Başarılı", "Öğrenci kaydedildi.")

    btn_kaydet = tk.Button(frame, text="Kaydet", font=("SF Pro Display", 14), command=kaydet_buton)
    btn_kaydet.pack(pady=10)

    btn_goster = tk.Button(frame, text="Öğrencileri Göster", font=("SF Pro Display", 14), command=lambda: ogrencileri_goster(anahtar))
    btn_goster.pack(pady=10)

def ekran_kayit_ol():
    for widget in frame.winfo_children():
        widget.destroy()

    label_logo = tk.Label(frame, text="NMStudentSystem", font=("SF Pro Display", 24), bg="#fff")
    label_logo.pack(pady=10)

    lbl_anahtar = tk.Label(frame, text="Anahtar:", font=("SF Pro Display", 14), bg="#fff")
    lbl_anahtar.pack(pady=5)
    entry_anahtar = tk.Entry(frame, font=("SF Pro Display", 14))
    entry_anahtar.pack(pady=5)

    lbl_sifre = tk.Label(frame, text="Şifre:", font=("SF Pro Display", 14), bg="#fff")
    lbl_sifre.pack(pady=5)
    entry_sifre = tk.Entry(frame, font=("SF Pro Display", 14), show="*")
    entry_sifre.pack(pady=5)

    def kayit_buton():
        anahtar = entry_anahtar.get()
        sifre = entry_sifre.get()
        kaydet_kullanici(anahtar, sifre)
        ekran_giris()

    btn_kayit = tk.Button(frame, text="Kayıt Ol", font=("SF Pro Display", 14), command=kayit_buton)
    btn_kayit.pack(pady=10)

root = tk.Tk()
root.geometry("1366x768")
root.title("NMStudentSystem")
canvas = tk.Canvas(root, bg="#ffffff")
canvas.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)
frame = tk.Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=frame, anchor="nw")
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

veritabanı_oluştur()
ekran_giris()

root.mainloop()
