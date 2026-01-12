import tkinter as tk
from tkinter import font, messagebox
from datetime import datetime
import subprocess
import sys

LOG_FILE = "pdu_manual_logs.txt"

# ================= LOGGING =================
def write_log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {event}\n")

write_log("PDU CHECKS OPENED")

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB – PDU MANUAL INPUT")
root.geometry("900x550")
root.configure(bg="#0b1220")

# ================= FONTS =================
title_font  = font.Font(family="Segoe UI", size=26, weight="bold")
label_font  = font.Font(family="Segoe UI", size=13, weight="bold")
input_font  = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Segoe UI", size=11, weight="bold")

# ================= HEADER =================
header = tk.Frame(root, bg="#020817", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="PDU CHECKS",
    font=title_font,
    bg="#020817",
    fg="#38bdf8"
).pack(pady=20)

# ================= FORM =================
form = tk.Frame(root, bg="#0b1220")
form.pack(pady=40, padx=60, fill="x")

# ================= ENTRY WITH HIGHLIGHT =================
def create_row(text):
    row = tk.Frame(form, bg="#0b1220")
    row.pack(fill="x", pady=18)

    tk.Label(
        row,
        text=text,
        font=label_font,
        bg="#0b1220",
        fg="#7dd3fc",
        width=18,
        anchor="w"
    ).pack(side=tk.LEFT, padx=(0, 15))

    # 🔲 Border frame
    border = tk.Frame(row, bg="#38bdf8", height=45)
    border.pack(side=tk.LEFT, fill="x", expand=True)
    border.pack_propagate(False)

    inner = tk.Frame(border, bg="#020817")
    inner.pack(fill="both", expand=True, padx=2, pady=2)

    entry = tk.Entry(
        inner,
        font=input_font,
        bg="#020817",
        fg="#22c55e",
        relief=tk.FLAT,
        insertbackground="#22c55e"
    )
    entry.pack(fill="both", expand=True, padx=12, pady=8)

    # ✨ Highlight events
    def on_focus_in(e):
        border.config(bg="#22c55e")   # green glow

    def on_focus_out(e):
        border.config(bg="#38bdf8")   # normal blue

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry

# ================= INPUT FIELDS =================
serial_entry = create_row("PDU SERIAL NO")
make_entry   = create_row("MAKE")

# ================= SUBMIT =================
def submit():
    s = serial_entry.get().strip()
    m = make_entry.get().strip()

    if not s or not m:
        messagebox.showwarning("Required", "Please fill all fields")
        return

    write_log(f"Submitted: {s}, {m}")
    messagebox.showinfo("Saved", "PDU Data Saved Successfully")

    serial_entry.delete(0, tk.END)
    make_entry.delete(0, tk.END)
    serial_entry.focus()

tk.Button(
    root,
    text="SUBMIT",
    font=button_font,
    bg="#2563eb",
    fg="white",
    width=18,
    height=2,
    command=submit
).pack(pady=30)

# ================= FOOTER =================
footer = tk.Frame(root, bg="#020817", height=50)
footer.pack(side=tk.BOTTOM, fill=tk.X)

def back_to_dash():
    write_log("Back to DashM")
    root.destroy()
    subprocess.Popen([sys.executable, "dashm.py"])

tk.Button(
    footer,
    text="BACK TO DASHBOARD",
    font=button_font,
    bg="#2563eb",
    fg="white",
    command=back_to_dash
).pack(side=tk.LEFT, padx=20, pady=10)

tk.Button(
    footer,
    text="EXIT",
    font=button_font,
    bg="#dc2626",
    fg="white",
    command=root.destroy
).pack(side=tk.RIGHT, padx=20, pady=10)

# ================= START =================
serial_entry.focus()
root.mainloop()
