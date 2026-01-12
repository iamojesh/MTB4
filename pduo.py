import tkinter as tk
from tkinter import font, messagebox, filedialog
import time
from datetime import datetime
import threading
import os
import subprocess
import sys

LOG_FILE = "pdu_checks_logs.txt"

# ================= LOGGING =================
def write_log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {event}\n")

write_log("PDU Checks Application Started")

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB – PDU CHECKS")
root.geometry("900x700")
root.configure(bg="#0a192f")
root.resizable(True, True)

# ================= FONTS =================
title_font = font.Font(family="Segoe UI", size=28, weight="bold")
subtitle_font = font.Font(family="Segoe UI", size=14, weight="bold")
log_font = font.Font(family="Consolas", size=10)
button_font = font.Font(family="Segoe UI", size=11, weight="bold")
menu_font_small = font.Font(family="Segoe UI", size=14, weight="bold")
clock_font = font.Font(family="Consolas", size=10)

# ================= HEADER =================
title_label = tk.Label(
    root,
    text="PDU CHECKS",
    font=title_font,
    bg="#0a192f",
    fg="#00e5ff",
    pady=15
)
title_label.pack()

# ================= ACTIVITY LOG BOX =================
log_label = tk.Label(
    root,
    text="Activity Log",
    font=subtitle_font,
    bg="#0a192f",
    fg="#00ff9c"
)
log_label.pack(anchor="w", padx=40, pady=(10, 5))

# Log text box with scrollbar
log_frame = tk.Frame(root, bg="#0a192f")
log_frame.pack(padx=40, pady=(0, 15), fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(
    log_frame,
    font=log_font,
    bg="#112240",
    fg="#00ff9c",
    height=15,
    width=80,
    relief=tk.RAISED,
    bd=2,
    yscrollcommand=scrollbar.set
)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=log_text.yview)
log_text.config(state=tk.DISABLED)

# ================= PROGRESS BAR =================
progress_label = tk.Label(
    root,
    text="Progress",
    font=subtitle_font,
    bg="#0a192f",
    fg="#00e5ff"
)
progress_label.pack(anchor="w", padx=40, pady=(10, 5))

progress_frame = tk.Frame(root, bg="#112240", height=30)
progress_frame.pack(padx=40, fill=tk.X, pady=(0, 10))
progress_frame.pack_propagate(False)

progress_bar = tk.Canvas(
    progress_frame,
    bg="#112240",
    highlightthickness=0,
    height=30
)
progress_bar.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

progress_text = tk.Label(
    root,
    text="0%",
    font=button_font,
    bg="#0a192f",
    fg="#00ff9c"
)
progress_text.pack(pady=(0, 20))

# ================= BUTTON FRAME =================
button_frame = tk.Frame(root, bg="#0a192f")
button_frame.pack(pady=10)

# Global variables
go_button = None
report_button = None
progress_value = 0
check_complete = False
test_results = []

# ================= FUNCTIONS =================
def add_log(message):
    """Add message to activity log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, f"[{timestamp}] {message}\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)
    root.update()

def update_progress(value):
    """Update progress bar"""
    global progress_value
    progress_value = min(100, value)
    
    # Clear previous bar
    progress_bar.delete("all")
    
    # Draw border
    progress_bar.create_rectangle(0, 0, 800, 30, outline="#00e5ff", width=2)
    
    # Draw filled portion
    fill_width = (progress_value / 100) * 795
    progress_bar.create_rectangle(2, 2, fill_width + 2, 28, fill="#00ff9c", outline="")
    
    # Update percentage text
    progress_text.config(text=f"{progress_value}%")
    root.update()

def run_pdu_checks():
    """Simulate PDU checks in background"""
    global check_complete, go_button, test_results
    
    write_log("PDU Checks Started")
    add_log("Initializing PDU Checks...")
    test_results = []
    
    checks = [
        "Power Supply Unit 1 Check",
        "Power Supply Unit 2 Check",
        "Voltage Regulation Test",
        "Current Monitoring Test",
        "Thermal Management Check",
        "Protection Circuit Test",
        "Cable Integrity Verification",
        "Load Testing",
        "Safety Protocol Validation",
        "Final System Diagnostics"
    ]
    
    for i, check in enumerate(checks):
        add_log(f"Running: {check}...")
        time.sleep(1)
        progress = int((i + 1) / len(checks) * 100)
        update_progress(progress)
        test_results.append({
            "name": check,
            "status": "PASSED",
            "duration": f"{round(1.0 + (i % 3) * 0.1, 1)}s"
        })
    
    add_log("All checks completed successfully!")
    write_log("PDU Checks Completed Successfully")
    check_complete = True
    
    # Show GO button
    go_button = tk.Button(
        button_frame,
        text="GO  →",
        font=button_font,
        bg="#4ecca3",
        fg="white",
        relief=tk.RAISED,
        bd=2,
        width=20,
        cursor="hand2",
        command=on_go_click
    )
    go_button.pack(pady=10)
    root.update()

def on_go_click():
    """Handle GO button click - wait 2 seconds then show Generate Report"""
    global go_button
    
    if go_button is not None:
        go_button.config(state=tk.DISABLED)
    add_log("Processing...")
    
    # Start timer to show report button after 2 seconds
    root.after(2000, show_report_button)

def show_report_button():
    """Display Generate Report button"""
    global report_button, go_button
    
    # Remove GO button
    if go_button is not None:
        go_button.destroy()
        go_button = None
    
    # Create Generate Report button
    if report_button is None:
        report_button = tk.Button(
            button_frame,
            text="GENERATE REPORT  →",
            font=button_font,
            bg="#2a4bd7",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            width=20,
            cursor="hand2",
            command=generate_report
        )
        report_button.pack(pady=10)
        add_log("Report ready for generation")
        root.update()

def generate_report():
    """Generate and save HTML report"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
        initialfile=f"PDU_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )
    
    if not file_path:
        return
    
    write_log(f"Report Generated: {file_path}")
    
    # Generate table rows from test results
    table_rows = ""
    for test in test_results:
        table_rows += f"""
                <tr>
                    <td>{test['name']}</td>
                    <td>[PASSED] Success</td>
                    <td>{test['duration']}</td>
                </tr>"""
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>PDU Checks Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #0a192f;
                color: #00e5ff;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background-color: #112240;
                padding: 30px;
                border-radius: 8px;
                border: 2px solid #00e5ff;
            }}
            h1 {{
                color: #00ff9c;
                text-align: center;
                border-bottom: 2px solid #00e5ff;
                padding-bottom: 15px;
            }}
            .report-info {{
                background-color: #0a192f;
                padding: 15px;
                border-left: 4px solid #00ff9c;
                margin: 20px 0;
            }}
            .status {{
                color: #00ff9c;
                font-weight: bold;
                font-size: 18px;
            }}
            .timestamp {{
                color: #8892b0;
                font-size: 14px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th {{
                background-color: #1f4068;
                color: #00e5ff;
                padding: 12px;
                text-align: left;
                border: 1px solid #00e5ff;
            }}
            td {{
                padding: 12px;
                border: 1px solid #00e5ff;
                color: #00ff9c;
            }}
            tr:nth-child(even) {{
                background-color: #0a192f;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #8892b0;
                border-top: 1px solid #00e5ff;
                padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AKASH MTB - PDU CHECKS REPORT</h1>
            
            <div class="report-info">
                <p class="status">[PASSED] Status: All Tests Passed</p>
                <p class="timestamp">Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</p>
            </div>
            
            <h2 style="color: #00e5ff;">Test Results</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration</th>
                </tr>
                {table_rows}
            </table>
            
            <div class="report-info">
                <p style="color: #00ff9c; font-weight: bold;">All subsystems nominal. PDU checks completed successfully.</p>
            </div>
            
            <div class="footer">
                <p>AKASH MTB - Defence Research and Development Organisation</p>
                <p>Confidential - For Official Use Only</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        with open(file_path, "w") as f:
            f.write(html_content)
        add_log(f"Report generated and saved successfully!")
        messagebox.showinfo("Success", f"Report generated successfully!\n\nSaved at: {file_path}")
        write_log(f"Report saved at: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
        write_log(f"Report generation failed: {str(e)}")

def start_checks():
    """Start PDU checks in a separate thread"""
    start_button.config(state=tk.DISABLED)
    thread = threading.Thread(target=run_pdu_checks, daemon=True)
    thread.start()

def go_to_dashboard():
    """Redirect to dasho.py"""
    write_log("Returning to Dashboard")
    root.destroy()
    subprocess.Popen([sys.executable, "dasho.py"])
    time.sleep(0.5)

def exit_app():
    """Exit the application"""
    if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
        write_log("Application Exited")
        root.destroy()

# Start Button
start_button = tk.Button(
    button_frame,
    text="START CHECKS  →",
    font=button_font,
    bg="#1f4068",
    fg="white",
    relief=tk.RAISED,
    bd=2,
    width=20,
    cursor="hand2",
    command=start_checks
)
start_button.pack(pady=10)

# ================= BOTTOM BAR =================
bottom_bar = tk.Frame(root, bg="#020c1b", height=50)
bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)
bottom_bar.pack_propagate(False)

# Go to Dashboard Button
dashboard_btn = tk.Button(
    bottom_bar,
    text="GO TO DASHBOARD  →",
    font=button_font,
    bg="#2a4bd7",
    fg="white",
    relief=tk.RAISED,
    bd=2,
    cursor="hand2",
    command=go_to_dashboard
)
dashboard_btn.pack(side=tk.LEFT, padx=15, pady=10)

# Exit Button
exit_btn = tk.Button(
    bottom_bar,
    text="EXIT",
    font=button_font,
    bg="#b33939",
    fg="white",
    relief=tk.RAISED,
    bd=2,
    cursor="hand2",
    command=exit_app
)
exit_btn.pack(side=tk.RIGHT, padx=15, pady=10)

# ================= RUN =================
root.mainloop()