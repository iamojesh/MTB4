import tkinter as tk
from tkinter import font, messagebox
from datetime import datetime
import hashlib
import random
import os
import subprocess
import sys

# ================= CONFIG =================
MTB_VERSION = "AKASH-MTB v2.4.1"

CHECKSUM_FILES = [
    "Ex.py",
    "dasho.py",
    "pduo.py",
    "scale_factor.cfg"
]

# ================= COLORS =================
OK_BG  = "#064e3b"
OK_FG  = "#22c55e"
ERR_BG = "#7f1d1d"
ERR_FG = "#fecaca"

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB – INITIAL SYSTEM CHECK")
root.geometry("960x650")
root.configure(bg="#020c1b")
root.resizable(False, False)

# ================= FONTS =================
title_font  = font.Font(family="Times New Roman", size=26, weight="bold")
label_font  = font.Font(family="Times New Roman", size=14, weight="bold")
value_font  = font.Font(family="Times New Roman", size=13)
button_font = font.Font(family="Times New Roman", size=12, weight="bold")

# ================= CHECKSUM FUNCTIONS =================
def calculate_static_checksum(files):
    sha = hashlib.sha256()
    for file in files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                sha.update(f.read())
        else:
            sha.update(b"FILE_MISSING")
    return sha.hexdigest().upper()

def last_modified(files):
    times = []
    for f in files:
        if os.path.exists(f):
            times.append(os.path.getmtime(f))
    if not times:
        return "N/A"
    return datetime.fromtimestamp(max(times)).strftime("%d-%m-%Y %H:%M:%S")

STATIC_CHECKSUM = calculate_static_checksum(CHECKSUM_FILES)

# ================= HEADER =================
tk.Label(
    root,
    text="SYSTEM INTEGRITY CHECK",
    font=title_font,
    bg="#020c1b",
    fg="#00e5ff",
    pady=18
).pack()

# ================= BACK PANEL =================
back_panel = tk.Frame(root, bg="#0a192f", bd=2, relief=tk.GROOVE)
back_panel.pack(padx=30, pady=15, fill="both", expand=True)

main = tk.Frame(back_panel, bg="#0a192f")
main.pack(padx=35, pady=25, fill="both", expand=True)

# ================= ROW CREATOR =================
def create_row(text, wrap=False):
    row = tk.Frame(main, bg="#0a192f")
    row.pack(fill="x", pady=10)

    tk.Label(
        row,
        text=text,
        font=label_font,
        bg="#0a192f",
        fg="#00ff9c",
        width=32,
        anchor="w"
    ).pack(side="left", padx=(0, 10))

    val = tk.Label(
        row,
        text="---",
        font=value_font,
        bg="#112240",
        fg="white",
        anchor="w",
        justify="left",
        padx=12,
        pady=8,
        wraplength=520 if wrap else 0
    )
    val.pack(side="left", fill="both", expand=True)
    return val

# ================= FIELDS =================
version_val  = create_row("MTB VERSION")
date_val     = create_row("SYSTEM DATE / TIME")
modified_val = create_row("LAST FILE MODIFIED")
cgu_val      = create_row("CGU CALIBRATION VALUE")
rpf_val      = create_row("RPF CALIBRATION VALUE")
checksum_val = create_row("SYSTEM CHECKSUM ", wrap=True)

# ================= INITIAL VALUES =================
version_val.config(text=MTB_VERSION)
modified_val.config(text=last_modified(CHECKSUM_FILES))

checksum_val.config(
    text=STATIC_CHECKSUM,
    bg=OK_BG,
    fg=OK_FG
)

# ================= LIVE VALUES =================
cgu_value = 100.000
rpf_value = 200.000

def update_runtime_values():
    global cgu_value, rpf_value

    cgu_value += random.uniform(-0.03, 0.03)
    rpf_value += random.uniform(-0.05, 0.05)

    cgu_val.config(text=f"{cgu_value:.3f}")
    rpf_val.config(text=f"{rpf_value:.3f}")
    date_val.config(text=datetime.now().strftime("%d %B %Y | %H:%M:%S"))

    root.after(1000, update_runtime_values)

# ================= CHECKSUM VERIFICATION =================
def verify_checksum():
    current = calculate_static_checksum(CHECKSUM_FILES)

    if current != STATIC_CHECKSUM:
        checksum_val.config(
            text=current,
            bg=ERR_BG,
            fg=ERR_FG
        )
    else:
        checksum_val.config(
            text=current,
            bg=OK_BG,
            fg=OK_FG
        )

    root.after(3000, verify_checksum)

update_runtime_values()
verify_checksum()

# ================= BUTTON HOVER =================
def hover_on(btn, color):
    btn.config(bg=color)

def hover_off(btn, color):
    btn.config(bg=color)

# ================= BUTTONS =================
button_frame = tk.Frame(root, bg="#020c1b")
button_frame.pack(pady=22)

def continue_app():
    root.destroy()
    subprocess.Popen([sys.executable, "Ex.py"])

continue_btn = tk.Button(
    button_frame,
    text="CONTINUE ",
    font=button_font,
    bg="#2a4bd7",
    fg="white",
    width=20,
    height=2,
    cursor="hand2",
    command=continue_app
)
continue_btn.pack(side="left", padx=30)

continue_btn.bind("<Enter>", lambda e: hover_on(continue_btn, "#1e40af"))
continue_btn.bind("<Leave>", lambda e: hover_off(continue_btn, "#2a4bd7"))

exit_btn = tk.Button(
    button_frame,
    text="EXIT",
    font=button_font,
    bg="#b33939",
    fg="white",
    width=20,
    height=2,
    cursor="hand2",
    command=root.destroy
)
exit_btn.pack(side="right", padx=30)

exit_btn.bind("<Enter>", lambda e: hover_on(exit_btn, "#7f1d1d"))
exit_btn.bind("<Leave>", lambda e: hover_off(exit_btn, "#b33939"))

# ================= RUN =================
root.mainloop()
