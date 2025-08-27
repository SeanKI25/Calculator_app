import tkinter as tk
from tkinter import messagebox

ALLOWED_CHARS = set("0123456789+-*/().% ")

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(padx=8, pady=8)
        self.minsize(320, 420)

        #The Display
        self.var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var, font=("Segoe UI", 22), bd=6, relief="solid", justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=8)
        self.entry.focus_set()

        #Layout
        self.grid_rowconfigure(0, weight=0)
        for r in range(1, 6):
            self.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.grid_columnconfigure(c, weight=1)
        

        self._build_menu()

    #Menu
    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Alt+F4")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear", command=self.clear, accelerator="Esc")
        edit_menu.add_command(label="Backspace", command=self.backspace, accelerator="Backspace")
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy", command=self.copy_display, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_display, accelerator="Ctrl+V")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)


        buttons = [
            ("C", 1, 0, self.clear), ("←", 1, 1, self.backspace), ("/", 1, 2, lambda: self.add("/")), ("*", 1, 3, lambda: self.add("*")),
            ("7", 2, 0, lambda: self.add("7")), ("8", 2, 1, lambda: self.add("8")), ("9", 2, 2, lambda: self.add("9")), ("-", 2, 3, lambda: self.add("-")),
            ("4", 3, 0, lambda: self.add("4")), ("5", 3, 1, lambda: self.add("5")), ("6", 3, 2, lambda: self.add("6")), ("+", 3, 3, lambda: self.add("+")),
            ("1", 4, 0, lambda: self.add("1")), ("2", 4, 1, lambda: self.add("2")), ("3", 4, 2, lambda: self.add("3")), ("=", 4, 3, self.equals),
            ("0", 5, 0, lambda: self.add("0")), (".", 5, 1, lambda: self.add(".")), ("(", 5, 2, lambda: self.add("(")), (")", 5, 3, lambda: self.add(")")),
        ]
        for (txt, r, c, cmd) in buttons:
            tk.Button(self, text=txt, command=cmd, font=("Segoe UI", 18), bd=2)\
                .grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            

        #Keyboard bindings
        self.bind("<Key>", self.on_key)
        self.bind("<Return>", lambda e:self.equals())
        self.bind("=",        lambda e: self.equals())    
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())
        self.bind("<KP_Enter>", lambda e: self.equals())
        self.bind("c", lambda e: self.clear())
        self.bind("C", lambda e: self.clear())

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Calculator\nBuilt with Python + Tkinter\n 2025 Sean Kelly Iroanya"
        )


    #The Calculator Logic

    def add(self, s: str):
        self.var.set(self.var.get() +s)

    def clear(self):
        self.var.set("")

    def backspace(self):
        self.var.set(self.var.get()[:-1])

    def equals(self):
        expr = (self.var.get().replace("x", "*").replace("÷", "/"))

        if not set(expr) <= ALLOWED_CHARS:
            self.var.set("Error");return
        try:
            result = eval(expr, {"__builtins__": None}, {})
            self.var.set(str(result))
        except Exception:
            self.var.set("Error")

    def copy_display(self):
        text = self.var.get()
        self.clipboard_clear()
        self.clipboard_append(text)
    
    def paste_display(self):
        try:
            clip = self.clipboard_get()
        except tk.TclError:
            clip = ""
        #Filter to allowed characters only
        clip = "".join(ch for ch in clip if ch in ALLOWED_CHARS or ch in "xX÷")
        #normalize  x/÷ to * and /
        clip = clip.replace("x", "*").replace("X", "*").replace("÷", "/")
        self.add(clip)


    def on_key(self, event: tk.Event):
        ch = event.char
        if ch in ("x", "X"):
            self.add("*"); return "break"
        if ch == "÷":
            self.add("/"); return "break"
        if ch in ALLOWED_CHARS:
            self.add(ch); return "break"
    
if __name__ == "__main__":
    Calculator().mainloop()
