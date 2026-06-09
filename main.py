
import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3
from datetime import datetime
from urllib.parse import quote
import random
import time

# ---------- DATABASE ----------
conn = sqlite3.connect("history.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS searches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    search_time TEXT
)
""")
conn.commit()

# ---------- FUNCTIONS ----------

def save_search(topic):
    cursor.execute(
        "INSERT INTO searches(topic, search_time) VALUES (?, ?)",
        (topic, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

def search_information():
    topic = search_entry.get().strip()

    if not topic:
        messagebox.showwarning("Input Required", "Please enter a topic.")
        return

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "🚀 Searching...\n")
    root.update()

    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
        headers = {"User-Agent": "AI Galaxy Bot/1.0"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            result_box.delete("1.0", tk.END)
            result_box.insert(tk.END, f"Wikipedia returned status code {response.status_code}")
            return

        data = response.json()

        result_box.delete("1.0", tk.END)

        if data.get("extract"):
            result_box.insert(tk.END, data["extract"])
            save_search(topic)
        else:
            result_box.insert(tk.END, "No information found for this topic.")

    except Exception as e:
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, f"Error:\n{e}")

def clear_data():
    search_entry.delete(0, tk.END)
    result_box.delete("1.0", tk.END)

def show_history():
    win = tk.Toplevel(root)
    win.title("Search History")
    win.geometry("600x400")
    win.configure(bg="#050A30")

    txt = tk.Text(win, bg="#09122C", fg="white", font=("Consolas", 11))
    txt.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM searches ORDER BY id DESC")
    rows = cursor.fetchall()

    if not rows:
        txt.insert(tk.END, "No history found.")
        return

    for row in rows:
        txt.insert(
            tk.END,
            f"Topic: {row[1]}\nTime: {row[2]}\n{'-'*50}\n"
        )

def update_clock():
    clock_label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_clock)

# ---------- GUI ----------

root = tk.Tk()
root.title("AI Galaxy Bot")
root.geometry("1100x700")
root.configure(bg="#050A30")

canvas = tk.Canvas(root, bg="#050A30", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

stars = []
for _ in range(180):
    x = random.randint(0, 1100)
    y = random.randint(0, 700)
    star = canvas.create_oval(x, y, x+2, y+2, fill="white", outline="")
    stars.append(star)

def animate_stars():
    for star in stars:
        canvas.move(star, 0, 1)
        c = canvas.coords(star)

        if c[1] > 700:
            x = random.randint(0, 1100)
            canvas.coords(star, x, 0, x+2, 2)

    root.after(40, animate_stars)

animate_stars()

title = tk.Label(
    root,
    text="✦ AI GALAXY BOT ✦",
    font=("Arial", 28, "bold"),
    bg="#050A30",
    fg="#00FFFF"
)
title.pack(pady=15)
title.lift()

clock_label = tk.Label(
    root,
    font=("Arial", 12, "bold"),
    bg="#050A30",
    fg="white"
)
clock_label.pack()
clock_label.lift()
update_clock()

search_frame = tk.Frame(root, bg="#050A30")
search_frame.pack(pady=15)
search_frame.lift()

search_entry = tk.Entry(
    search_frame,
    width=45,
    font=("Arial", 14),
    bg="#0B1F3A",
    fg="white",
    insertbackground="white"
)
search_entry.grid(row=0, column=0, padx=10)

search_btn = tk.Button(
    search_frame,
    text="🚀 Search",
    bg="#00FFFF",
    fg="black",
    font=("Arial", 11, "bold"),
    command=search_information
)
search_btn.grid(row=0, column=1, padx=5)

clear_btn = tk.Button(
    search_frame,
    text="🛰 Clear",
    bg="#FF006E",
    fg="white",
    font=("Arial", 11, "bold"),
    command=clear_data
)
clear_btn.grid(row=0, column=2, padx=5)

history_btn = tk.Button(
    search_frame,
    text="🌌 History",
    bg="#7B2CBF",
    fg="white",
    font=("Arial", 11, "bold"),
    command=show_history
)
history_btn.grid(row=0, column=3, padx=5)

result_frame = tk.Frame(root, bg="#050A30")
result_frame.pack(fill="both", expand=True, padx=20, pady=20)
result_frame.lift()

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(
    result_frame,
    bg="#09122C",
    fg="#00FFAA",
    insertbackground="white",
    font=("Consolas", 13),
    wrap="word",
    yscrollcommand=scrollbar.set
)

result_box.pack(fill="both", expand=True)
scrollbar.config(command=result_box.yview)

footer = tk.Label(
    root,
    text="Artificial Intelligence Mini Project | Galaxy Theme",
    bg="#050A30",
    fg="gray"
)
footer.pack(pady=8)
footer.lift()

root.mainloop()
conn.close()
