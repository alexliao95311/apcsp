import tkinter as tk

root = tk.Tk()

root.rowconfigure((0, 1), weight=1)
root.columnconfigure((0, 1), weight=1)

tk.Frame(root, bg="blue").grid(row=0, column=0, sticky="nsew")
tk.Frame(root, bg="lime").grid(row=0, column=1, sticky="nsew")
tk.Frame(root, bg="red").grid(row=1, column=0, sticky="nsew")
tk.Frame(root, bg="yellow").grid(row=1, column=1, sticky="nsew")

root.mainloop()
