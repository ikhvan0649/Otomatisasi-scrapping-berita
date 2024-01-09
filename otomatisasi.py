import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

def baca_api_key(file_path="api_key.txt"):
    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        return None

def cari_berita(keyword, api_key, jumlah_hasil=5, bahasa='id'):
    base_url = "https://newsapi.org/v2/everything"
    parameters = {
        'q': keyword,
        'apiKey': api_key,
        'pageSize': jumlah_hasil,
        'language': bahasa
    }

    try:
        response = requests.get(base_url, params=parameters)
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'ok':
            articles = data.get('articles')
            links = [article['url'] for article in articles]
            return links
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def cari_berita_gui():
    keyword = entry_keyword.get()
    api_key = baca_api_key()

    if not keyword or not api_key:
        messagebox.showwarning("Peringatan", "Keyword atau API Key tidak ditemukan.")
        return

    hasil_pencarian = cari_berita(keyword, api_key, bahasa='id')
    
    if hasil_pencarian:
        for i, link in enumerate(hasil_pencarian, start=1):
            hasil_text.insert(tk.END, f"{i}. {link}\n")
    else:
        messagebox.showerror("Error", "Gagal melakukan pencarian.")

# Membuat GUI
window = tk.Tk()
window.title("Pencarian Berita")

# Label dan Entry untuk Keyword
label_keyword = tk.Label(window, text="Keyword:")
label_keyword.grid(row=0, column=0, padx=5, pady=5)
entry_keyword = tk.Entry(window)
entry_keyword.grid(row=0, column=1, padx=5, pady=5)

# Tombol Pencarian
tombol_cari = tk.Button(window, text="Cari Berita", command=cari_berita_gui)
tombol_cari.grid(row=1, column=0, columnspan=2, pady=10)

# Hasil Pencarian
hasil_text = scrolledtext.ScrolledText(window, width=50, height=10, wrap=tk.WORD)
hasil_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
