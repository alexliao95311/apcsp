import tkinter as tk

current_password = "sigmaalpha123"

def test_my_button():
    '''check password and continue depending on correct or not'''
    entered_pass = ent_password.get()

    if entered_pass == current_password:
        lbl_auth_status.config(text=f"Success! Password '{entered_pass}' is correct.")
        frame_auth.tkraise()
    else:
        lbl_fail_status.config(text="Invalid Password. Access Denied.")
        frame_fail.tkraise()

def go_to_login():
    ent_username.delete(0, tk.END)
    ent_password.delete(0, tk.END)
    frame_login.tkraise()

def change_password_logic():
    global current_password
    new_p = ent_new_password.get()
    if new_p:
        current_password = new_p
        ent_new_password.delete(0, tk.END)
        go_to_login()

root = tk.Tk()
root.wm_geometry("350x450")
root.title("Authentication System")

# Create the frames and stack them in the same grid position
for f in (tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)):
    f.grid(row=0, column=0, sticky="news")

# Assign frames to variables
frame_login, frame_auth, frame_fail, frame_change = root.winfo_children()

# --- Login Frame UI ---
tk.Label(frame_login, text='Username:', font="Arial").pack(pady=5)
ent_username = tk.Entry(frame_login, bd=3)
ent_username.pack(pady=5)

tk.Label(frame_login, text="Password:", font="Arial").pack(pady=5)
ent_password = tk.Entry(frame_login, bd=3, show='*')
ent_password.pack(pady=5)

btn_login = tk.Button(frame_login, text="Login", command=test_my_button)
btn_login.pack(pady=20)

# --- Success (Auth) Frame UI ---
lbl_auth_status = tk.Label(frame_auth, text="", font=("Arial", 10, "bold"), fg="green")
lbl_auth_status.pack(pady=20)

btn_exit = tk.Button(frame_auth, text="Exit (Logout)", command=go_to_login)
btn_exit.pack(pady=5)

btn_reset = tk.Button(frame_auth, text="Change Password", command=lambda: frame_change.tkraise())
btn_reset.pack(pady=5)

# --- Failure Frame UI ---
lbl_fail_status = tk.Label(frame_fail, text="", font=("Arial", 10), fg="red")
lbl_fail_status.pack(pady=20)

btn_retry = tk.Button(frame_fail, text="Retry", command=go_to_login)
btn_retry.pack(pady=5)

# --- Change Password Frame UI ---
tk.Label(frame_change, text="Enter New Password:", font="Arial").pack(pady=20)
ent_new_password = tk.Entry(frame_change, bd=3, show='*')
ent_new_password.pack(pady=10)

btn_confirm_change = tk.Button(frame_change, text="Update Password", command=change_password_logic)
btn_confirm_change.pack(pady=5)

# Show the login frame first
frame_login.tkraise()

root.mainloop()
