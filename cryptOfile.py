import customtkinter as tk
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showerror, showinfo
from tkinter import PhotoImage

import base64
import os
import sys
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")

        self.title("Crypt0file")
        self.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.geometry("260x300")
        self.resizable(False, False)
        self.focus_force()

        self.lbl_title = tk.CTkLabel(self, text="Crypt0file",
                                     font=("arial", 18, "bold"))
        self.lbl_title.pack(side="top", anchor="center", pady=(10, 0))
        self.get_file = GetFile(self)

    def open_file(self):
        file = askopenfile()
        if file is None:
            ...
        else:
            return file.name

    def __open_file(self, file):
        """Retrieves the path of the file to open and returns the path, file
        name, and file type."""
        dirname, basename = os.path.split(file)
        extension = os.path.splitext(basename)[1]
        basename = os.path.splitext(file)[0]

        return {
            'dirname': dirname,
            'basename': basename,
            'extension': extension
        }

    def __generate_key(self, password):
        """Generate a key from password"""
        password = password.encode()  # Convert to type bytes
        salt = b'\xff\xb6\x9cH\xc7\xf4\x1b\x9ea%Z\xa8+\xeek\x94'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def encrypt(self, password, file):
        key = self.__generate_key(password)
        file_name = self.__open_file(file)
        encrypted_file = os.path.join(
            file_name['dirname'], file_name['basename'] + '.ch3')

        with open(file, 'rb') as f:
            data = f.read()

        f = Fernet(key)
        encrypt_data = f.encrypt(data)
        extension = f.encrypt(
            bytes(file_name['extension'], encoding='utf8'))

        with open(encrypted_file, 'wb') as f:
            f.write(encrypt_data + b'#' + extension)

        return "Votre fichier a été chiffré"

    def decrypt(self, password, file):
        key = self.__generate_key(password)
        file_name = self.__open_file(file)

        with open(file, 'rb') as f:
            data = f.read()
            data, extension = data.split(b'#')

        f = Fernet(key)
        decrypted_data = f.decrypt(data)
        extension = f.decrypt(extension)
        decrypted_file = os.path.join(
            file_name['dirname'],
            file_name['basename'] + extension.decode())

        with open(decrypted_file, 'wb') as f:
            f.write(decrypted_data)

        return "Votre fichier a été déchiffré"


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
                                     command=self.open_file,
                                     fg_color="#404548",
                                     hover_color="#2F3335")
        self.btn_file.pack(fill="both", anchor="center", side="top", padx=10,
                           pady=(10, 50), expand="true")
        self.pack(fill="both", expand="true")

    def open_file(self):
        file = self.master.open_file()
        if file is not None:
            self.pack_forget()
            Form(self.master, file)


class Form(tk.CTkFrame):
    def __init__(self, master, file):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.pack(side="top", fill="both", expand="true", padx=10,
                  pady=(0, 10))

        file_extension = os.path.splitext(file)[-1]
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file)/1024

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
                                       fg_color="#404548",
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
            fg_color=self.btn_cancel.cget("fg_color"))
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
            self.ent_confirm.bind("<Return>",
                                  lambda event:
                                  self.encrypt(self.ent_pwd.get(),
                                               self.ent_confirm.get(),
                                               file))
            self.ent_confirm.pack(fill="x")

            self.btn_crypt.configure(command=lambda:
                                     self.encrypt(self.ent_pwd.get(),
                                                  self.ent_confirm.get(),
                                                  file))

        else:
            self.ent_pwd.bind("<Return>",
                              lambda event: self.decrypt(self.ent_pwd.get(),
                                                         file))
            self.btn_crypt.configure(text="Déchiffrer",
                                     command=lambda:
                                     self.decrypt(self.ent_pwd.get(), file))

        self.check_var = tk.StringVar(value="off")
        self.ckb_pwd = tk.CTkCheckBox(self, text="voir mot de passe",
                                      fg_color=self.ent_pwd.cget("fg_color"),
                                      command=self.show_password,
                                      variable=self.check_var,
                                      onvalue="on", offvalue="off",
                                      checkbox_width=10, checkbox_height=10)
        self.ckb_pwd.pack(fill="x")

    def show_password(self):
        if self.check_var.get() == "on":
            self.ent_pwd.configure(show="")
            try:
                self.ent_confirm.configure(show="")
            except AttributeError:
                ...
        else:
            self.ent_pwd.configure(show="*")
            try:
                self.ent_confirm.configure(show="*")
            except AttributeError:
                ...

    def cancel(self, event=False):
        self.pack_forget()
        self.master.get_file.pack(fill="both", expand="true")
        self.destroy()

    def encrypt(self, password1, password2, file):
        if len(password1) < 6:
            showerror("Attention",
                      "Le mot de passe saisis doit faire plus de 6 caractères")
        elif password1 != password2:
            showerror("Attention",
                      "Les mots de passe saisis ne sont pas identiques")
        else:
            showinfo("succès", self.master.encrypt(password1, file))
            dirname = os.path.split(file)
            if sys.platform == "win32":
                os.system(f"start {dirname[0]}")
            else:
                os.system(f"open {dirname[0]}")
            self.cancel()

    def decrypt(self, password, file):
        try:
            showinfo("succès", self.master.decrypt(password, file))
            dirname = os.path.split(file)
            if sys.platform == "win32":
                os.system(f"start {dirname[0]}")
            else:
                os.system(f"open {dirname[0]}")
            self.cancel()
        except InvalidToken:
            return showinfo("Erreur", "Le mot de passe saisis est incorrect")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
