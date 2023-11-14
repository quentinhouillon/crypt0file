import customtkinter as tk
import os
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
        self.get_file = GetFile(self)


class GetFile(tk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.lbl_open_file = tk.CTkLabel(
            self, text="Cliquer pour ouvrir un fichier", font=("arial", 13),
            text_color="#8E9596")
        self.lbl_open_file.pack(side="top", anchor="center", padx=10,
                                pady=(0, 10))

        self.btn_file = tk.CTkButton(self, text="+", font=("arial", 50),
                                     command=self.open_file)
        self.btn_file.pack(fill="both", anchor="center", side="top", padx=10,
                           pady=(10, 50), expand="true")
        self.pack(fill="both", expand="true")

    def open_file(self):
        file = askopenfile()
        if file is None:
            ...
        else:
            file_extension = os.path.splitext(file.name)[-1]
            file_name = os.path.basename(file.name)
            file_size = os.path.getsize(file.name)/1024
            self.pack_forget()
            Form(self.master, file_name, file_extension, file_size)


class Form(tk.CTkFrame):
    def __init__(self, master, file_name, file_extension, file_size):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.pack(side="top", fill="both", expand="true", padx=10,
                  pady=(0, 10))

        # FOOTER
        self.frm_footer = tk.CTkFrame(self, fg_color="transparent")
        self.frm_footer.pack(side="bottom", fill="x")

        self.btn_crypt = tk.CTkButton(self.frm_footer,
                                      text="Chiffrer", width=65,
                                      corner_radius=2)
        self.btn_crypt.pack(side="right", padx=5, pady=5)

        self.btn_cancel = tk.CTkButton(self.frm_footer,
                                       text="Annuler", width=65,
                                       corner_radius=2,
                                       fg_color="#343637",
                                       hover_color="#292C2D",
                                       command=self.cancel)
        self.btn_cancel.pack(side="right", padx=5, pady=5)
        # END FOOTER

        self.lbl_about_file = tk.CTkLabel(
            self, text=f"{file_name} - {file_size:.2f} MB", font=("arial", 13),
            text_color="#8E9596")
        self.lbl_about_file.pack(side="top", pady=(0, 10))

        self.lbl_pwd = tk.CTkLabel(
            self, text="Mot de passe",
            fg_color=self.btn_crypt.cget("fg_color"))
        self.lbl_pwd.pack(fill="x")

        self.ent_pwd = tk.CTkEntry(self, border_width=0, corner_radius=0,
                                   fg_color=self.lbl_pwd.cget("fg_color"),
                                   show="*", justify="center")
        self.ent_pwd.focus()
        self.ent_pwd.pack(fill="x")

        if file_extension != ".ch3":
            self.ent_pwd.bind(
                "<Return>", lambda event: self.ent_confirm.focus())
            self.lbl_confirm = tk.CTkLabel(
                self, text="confirmation",
                fg_color=self.lbl_pwd.cget("fg_color"))
            self.lbl_confirm.pack(fill="x")

            self.ent_confirm = tk.CTkEntry(
                self, border_width=0, corner_radius=0,
                fg_color=self.lbl_pwd.cget("fg_color"),
                show="*", justify="center")
            self.ent_confirm.pack(fill="x")

        else:
            self.ent_pwd.bind("<Return>", lambda event: ...)
            self.btn_crypt.configure(text="Déchiffrer")

    def cancel(self, event=False):
        self.pack_forget()
        self.master.get_file.pack(fill="both", expand="true")
        self.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
