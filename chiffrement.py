import customtkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import PhotoImage


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("green")

        self.title("Chiffr3ment")
        self.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.geometry("260x300")
        self.resizable(False, False)
        self.focus_force()

        self.lbl_title = tk.CTkLabel(self, text="Chiffr3ment",
                                     font=("arial", 18, "bold"))
        self.lbl_title.pack(side="top", anchor="center", pady=(10, 0))

        self.lbl_open_file = tk.CTkLabel(
            self, text="Cliquer pour ouvrir un fichier", font=("arial", 14))
        self.lbl_open_file.pack(side="top", anchor="center", padx=10,
                                pady=(0, 10))

        self.btn_file = tk.CTkButton(self, text="+", font=("arial", 50),
                                     command=self.open_file)
        self.btn_file.pack(fill="both", anchor="center", side="top", padx=10,
                           pady=(10, 50), expand="true")

    def open_file(self):
        file = askopenfile()
        print(file)
        print(file.name)


class Encrypt(tk.CTkFrame):
    def __init__(self, master, file_name):
        super().__init__(self, master)


class Decrypt(tk.CTkFrame):
    def __init__(self, master, file_name):
        super().__init__(self, master)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
