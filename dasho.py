import tkinter as tk
from tkinter import font, messagebox
import time
from datetime import datetime
import subprocess
import sys

LOG_FILE = "akash_mtb_dashm.txt"

# ================= LOGGING =================
def write_log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {event}\n")

write_log("Dashboard Started")

# ================= FUNCTIONS =================
def button_hover(e):
    e.widget['background'] = e.widget.hover_color

def button_leave(e):
    e.widget['background'] = e.widget.original_color

def button_click(name):
    write_log(f"Button Clicked: {name}")
    messagebox.showinfo("Operation", f"{name} executed")

# ✅ OPEN PDU CHECKS
def open_pduo():
    write_log("Opening PDU Checks")
    root.destroy()
    subprocess.Popen([sys.executable, "pduo.py"])

def show_help():
    write_log("Help Opened")
    messagebox.showinfo(
        "Help",
        "AKASH MTB CHECKOUT\n\n"
        "• Select checks from dashboard\n"
        "• Monitor status at bottom\n"
        "• Use menu for navigation"
    )

def change_mode():
    write_log("Change Mode Selected")
    root.destroy()
    subprocess.Popen([sys.executable, "dashboard_updated.py"])

def open_login():
    write_log("Login Screen Opened")
    root.destroy()
    subprocess.Popen([sys.executable, "login.py"])

def exit_app():
    if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
        write_log("Application Exited")
        root.destroy()

def update_clock():
    clock_label.config(text=time.strftime("%d %B %Y | %H:%M:%S"))
    clock_label.after(1000, update_clock)

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB CHECKOUT – COMMAND CENTER")
root.geometry("900x720")
root.configure(bg="#0a192f")
root.resizable(True, True)

# ================= FONTS =================
title_font = font.Font(family="Segoe UI", size=32, weight="bold")
subtitle_font = font.Font(family="Segoe UI", size=16, weight="bold")
button_font = font.Font(family="Segoe UI", size=12, weight="bold")
menu_font = font.Font(family="Segoe UI", size=16, weight="bold")
clock_font = font.Font(family="Consolas", size=11)

# ================= HEADER =================
title_label = tk.Label(
    root,
    text="AKASH MTB CHECKOUT",
    font=title_font,
    bg="#0a192f",
    fg="#00e5ff",
    pady=20
)
title_label.pack()

subtitle_label = tk.Label(
    root,
    text="WELCOME TO OPERATOR MODE",
    font=subtitle_font,
    bg="#0a192f",
    fg="#00ff9c"
)
subtitle_label.pack(pady=(0, 25))

# ================= SHINING EFFECT =================
def shine_text(label, colors, index=0):
    label.config(fg=colors[index])
    label.after(500, shine_text, label, colors, (index + 1) % len(colors))

shine_text(title_label, ["#00e5ff", "#33f6ff", "#66ffff", "#33f6ff"])
shine_text(subtitle_label, ["#00ff9c", "#33ffcc", "#66ffcc", "#33ffcc"])

# ================= BUTTON DATA =================
button_data = [
    ("START PDU CHECKS", "#1f4068", "#4ecca3"),
    ("START SPU CHECKS", "#1b6ca8", "#00bcd4"),
    ("START SCU/ACTUATOR CHECKS", "#4b7bec", "#a5b1ff"),
    ("START CGU CHECKS", "#6d214f", "#ff6f91"),
    ("START RPF CHECKS", "#3c6382", "#60a3bc"),
    ("START PYRO CHECKS", "#b33939", "#ff5252")
]

# ================= BUTTONS =================
for text, color, hover in button_data:
    frame = tk.Frame(root, bg="#0a192f")
    frame.pack(pady=10)

    # 🔹 Conditional routing
    if text == "START PDU CHECKS":
        cmd = open_pduo
    else:
        cmd = lambda t=text: button_click(t)

    btn = tk.Button(
        frame,
        text=f"{text}  >>",
        font=button_font,
        bg=color,
        fg="white",
        relief=tk.RAISED,
        bd=3,
        width=32,
        height=2,
        cursor="hand2",
        command=cmd
    )

    btn.original_color = color
    btn.hover_color = hover
    btn.bind("<Enter>", button_hover)
    btn.bind("<Leave>", button_leave)
    btn.pack()

# ================= STATUS BAR =================
status_frame = tk.Frame(root, bg="#020c1b", height=40)
status_frame.pack(side=tk.BOTTOM, fill=tk.X)

tk.Label(
    status_frame,
    text="System Status: READY | All subsystems nominal",
    font=clock_font,
    bg="#020c1b",
    fg="#00ff9c"
).pack(side=tk.LEFT, padx=20)

clock_label = tk.Label(
    status_frame,
    font=clock_font,
    bg="#020c1b",
    fg="#8892b0"
)
clock_label.pack(side=tk.RIGHT, padx=20)
update_clock()

# ================= OPTIONS MENU =================
options_btn = tk.Menubutton(
    root,
    text="☰",
    font=menu_font,
    bg="#020c1b",
    fg="#00e5ff",
    relief=tk.FLAT,
    cursor="hand2"
)

options_menu = tk.Menu(
    options_btn,
    tearoff=0,
    bg="#112240",
    fg="white",
    activebackground="#00e5ff",
    activeforeground="#020c1b"
)

options_menu.add_command(label="Help", command=show_help)
options_menu.add_command(label="Change Mode", command=change_mode)
options_menu.add_command(label="Open Login", command=open_login)
options_menu.add_separator()
options_menu.add_command(label="Exit", command=exit_app)

options_btn.config(menu=options_menu)
options_btn.place(relx=0.99, rely=0.92, anchor="se")

# ================= RUN =================
root.mainloop()
