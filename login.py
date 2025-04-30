from customtkinter import *
from PIL import Image
import signup_window
from database import validate_user
import passmen

set_appearance_mode("light")

def create_login_window(parent):
    login_win = CTkToplevel(parent)
    login_win.overrideredirect(True)
    login_win.geometry("700x500")

    # Close button
    import sys
    close_button = CTkButton(login_win, text="X", width=30, height=30, 
                           corner_radius=32, fg_color="red", command=sys.exit)
    close_button.place(x=640, y=8)

    # Frame setup
    frame = CTkFrame(login_win, fg_color="white", border_color="gray", 
                   border_width=1, height=500, width=400)
    frame.place(x=0, y=0)

    # Image setup
    image = CTkImage(dark_image=Image.open("img/image.png"), size=(400, 600))
    image_label = CTkLabel(
        frame,
        image=image,
        text="Welcome \nBack XD,",
        font=("Terminal", 48, "bold"),
        text_color="#F5F5F5",
        compound="center",
        padx=10,
        pady=20   
    )
    image_label.place(relx=0.5, rely=0.5, anchor="center")

    # Login form
    CTkLabel(login_win, text="Login", font=("Terminal", 48, "bold"), text_color="black").place(x=450, y=100)
    
    username_entry = CTkEntry(login_win, placeholder_text="Username", width=180, text_color="#FFCC70")
    username_entry.place(x=450, y=180)
    
    password_entry = CTkEntry(login_win, placeholder_text="Password", width=180, 
                            text_color="#FFCC70", show="*")
    password_entry.place(x=450, y=230)

    error_label = CTkLabel(login_win, text="", font=("Arial", 12))
    error_label.place(x=450, y=270)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            error_label.configure(text="Please fill in all fields", text_color="red")
            return
        
        if validate_user(username, password):
            error_label.configure(text="Login successful!", text_color="green")
            def return_to_passmen():

                login_win.destroy()
                passmen.create_passmen_window(username=username)
                

            login_win.after(1500, return_to_passmen)

        else:
            error_label.configure(text="Invalid username or password", text_color="red")

    CTkButton(login_win, text="LOG IN", width=190, height=50, corner_radius=32,
            fg_color="red", hover_color="green", command=attempt_login).place(x=450, y=310)

    # Signup link
    def open_signup():
        login_win.withdraw()
        signup_win = signup_window.create_signup_window(login_win)
        signup_win.protocol("WM_DELETE_WINDOW", lambda: login_win.deiconify())

    link_label = CTkLabel(login_win, text="Click Here to Sign Up", 
                        font=("DaunPenh", 10, "underline"), text_color="gray")
    link_label.place(x=480, y=380)
    link_label.bind("<Button-1>", lambda e: open_signup())

    # Drag functionality
    def start_move(event):
        login_win._offsetx = event.x
        login_win._offsety = event.y

    def do_move(event):
        x = login_win.winfo_x() + event.x - login_win._offsetx
        y = login_win.winfo_y() + event.y - login_win._offsety
        login_win.geometry(f"+{x}+{y}")

    login_win.bind("<ButtonPress-1>", start_move)
    login_win.bind("<B1-Motion>", do_move)

    return login_win

if __name__ == "__main__":
    root = CTk()
    root.withdraw()
    login_window = create_login_window(root)
    root.mainloop()