from customtkinter import *
from PIL import Image
from database import save_user, load_users

def create_signup_window(parent):
    signup_win = CTkToplevel(parent)
    signup_win.overrideredirect(True)
    signup_win.geometry("700x500")

    # Close button
    import sys
    close_button = CTkButton(signup_win, text="X", width=30, height=30, 
                           corner_radius=32, fg_color="red", command=sys.exit)
    close_button.place(x=640, y=8)

    # Frame setup
    frame = CTkFrame(signup_win, fg_color="white", border_color="gray", 
                   border_width=1, height=500, width=400)
    frame.place(x=0, y=0)

    # Image setup
    image = CTkImage(dark_image=Image.open("img/image.png"), size=(400, 600))
    image_label = CTkLabel(
        frame,
        image=image,
        text="Join \nwith us XD,",
        font=("Terminal", 48, "bold"),
        text_color="#F5F5F5",
        compound="center",
        padx=10,
        pady=20   
    )
    image_label.place(relx=0.5, rely=0.5, anchor="center")

    # Signup form
    CTkLabel(signup_win, text="Sign Up", font=("Terminal", 48, "bold"), text_color="black").place(x=450, y=100)

    username_entry = CTkEntry(signup_win, placeholder_text="Username", width=180, text_color="#FFCC70")
    username_entry.place(x=450, y=180)
    
    password_entry = CTkEntry(signup_win, placeholder_text="Password", width=180, 
                            text_color="#FFCC70", show="*")
    password_entry.place(x=450, y=230)
    
    confirm_entry = CTkEntry(signup_win, placeholder_text="Confirm Password", width=180, 
                           text_color="#FFCC70", show="*")
    confirm_entry.place(x=450, y=280)

    error_label = CTkLabel(signup_win, text="", font=("Arial", 12))
    error_label.place(x=450, y=310)

    def attempt_signup():
        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()
        
        if not all([username, password, confirm]):
            error_label.configure(text="Please fill all fields", text_color="red")
            return
            
        if password != confirm:
            error_label.configure(text="Passwords don't match", text_color="red")
            return
            
        if username in load_users():
            error_label.configure(text="Username already exists", text_color="red")
            return
            
        save_user(username, password)
        error_label.configure(text="Signup successful!", text_color="green")
        signup_win.after(1500, return_to_login)

    CTkButton(signup_win, text="SIGN UP", width=190, height=50, corner_radius=32,
            fg_color="red", hover_color="green", command=attempt_signup).place(x=450, y=340)

    # Login link
    def return_to_login():
        signup_win.destroy()
        parent.deiconify()

    link_label = CTkLabel(
        signup_win,
        text="Already have an account? Log In",
        font=("DaunPenh", 10, "underline"),
        text_color="gray",
    )
    link_label.place(x=480, y=400)
    link_label.bind("<Button-1>", lambda e: return_to_login())

    # Drag functionality
    def start_move(event):
        signup_win._offsetx = event.x
        signup_win._offsety = event.y

    def do_move(event):
        x = signup_win.winfo_x() + event.x - signup_win._offsetx
        y = signup_win.winfo_y() + event.y - signup_win._offsety
        signup_win.geometry(f"+{x}+{y}")

    signup_win.bind("<ButtonPress-1>", start_move)
    signup_win.bind("<B1-Motion>", do_move)

    return signup_win