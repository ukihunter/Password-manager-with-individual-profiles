import customtkinter as ctk
from PIL import Image, ImageTk
# Set appearance mode to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
import tkinter.ttk as ttk
from passdb import save_pass, load_pass

def create_passmen_window(parent=None, username=""):
    if parent is None:
        parent = ctk.CTk()
    passman_win = ctk.CTkToplevel(parent)
    passman_win.overrideredirect(True)
    passman_win.geometry("700x500")

    # Close button
    import sys
    close_button = ctk.CTkButton(
        passman_win, text="X", width=30, height=30,
        corner_radius=32, fg_color="red", command=sys.exit
    )
    close_button.place(x=640, y=8)

    # Welcome label
    welcome_text = f"Hello, {username}!"
    call = ctk.CTkLabel(
        passman_win, text=welcome_text,
        font=("arial", 20, "bold"), text_color="black"
    )
    call.place(x=20, y=30)

    # Treeview using ttk
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=25)

    treeview = ttk.Treeview(
        passman_win,
        columns=("web", "email_username", "password", "create_update_date"),
        show="headings"
    )
    treeview.heading("web", text="Web")
    treeview.heading("email_username", text="Email/Username")
    treeview.heading("password", text="Password")
    treeview.heading("create_update_date", text="Create/Update Date")
    treeview.column("web", width=150, anchor="center")
    treeview.column("email_username", width=150, anchor="center")
    treeview.column("password", width=150, anchor="center")
    treeview.column("create_update_date", width=150, anchor="center")
    treeview.place(x=20, y=100, width=660, height=300)

    # Load and show existing data for user
    passwords = load_pass(username)
    for entry in passwords:
        website = entry.get("website")
        email = entry.get("email")
        password = entry.get("password")
        date = entry.get("date")
        treeview.insert("", "end", values=(website, email, password, date))

    # Add button popup
    def open_add_popup():
        popup = ctk.CTkToplevel(passman_win)
        popup.geometry("400x300")
        popup.title("Add New Entry")

        # Entry fields
        ctk.CTkLabel(popup, text="Website:").pack(pady=(10, 0))
        website_entry = ctk.CTkEntry(popup, width=300)
        website_entry.pack()

        ctk.CTkLabel(popup, text="Username/Email:").pack(pady=(10, 0))
        email_entry = ctk.CTkEntry(popup, width=300)
        email_entry.pack()

        ctk.CTkLabel(popup, text="Password:").pack(pady=(10, 0))
        password_entry = ctk.CTkEntry(popup, show="*", width=300)
        password_entry.pack()

        def add_data():
            from datetime import datetime
            website = website_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            date = datetime.now().strftime("%Y-%m-%d %H:%M")

            if website and email and password:
                save_pass(username, website, email, password, date)
                treeview.insert("", "end", values=(website, email, "******", date))
                popup.destroy()
            else:
                ctk.CTkLabel(popup, text="Please fill all fields!", text_color="red").pack(pady=10)

        ctk.CTkButton(popup, text="Add", command=add_data).pack(pady=20)

    # Add button
    add_button = ctk.CTkButton(
        passman_win, text=" + Add", width=100, height=30,
        corner_radius=32, fg_color="green", command=open_add_popup
    )
    add_button.place(x=570, y=50)

    # Window drag functionality
    def start_move(event):
        passman_win._offsetx = event.x
        passman_win._offsety = event.y

    def do_move(event):
        x = passman_win.winfo_x() + event.x - passman_win._offsetx
        y = passman_win.winfo_y() + event.y - passman_win._offsety
        passman_win.geometry(f"+{x}+{y}")

    passman_win.bind("<ButtonPress-1>", start_move)
    passman_win.bind("<B1-Motion>", do_move)

    return passman_win