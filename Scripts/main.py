import tkinter as tk
from tkinter import messagebox as mbox
from model import Model


def resource_path(relative_path: str) -> str:
    """
    This function returns the absolute path of the given relative path
    :param relative_path: The relative path
    :return: This returns the absolute path
    """
    import sys
    import os
    from typing import Any

    try:
        base_path: Any = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)

class PasswordValidater:
    """
    The main app
    """
    def __init__(self) -> None:
        """
        This contains the window and some customizations and the Model class instance
        """
        self.window: tk.Tk = tk.Tk()
        self.window.resizable(False, False)
        self.window.title("Password Validator")
        self.window.iconphoto(True, tk.PhotoImage(file=resource_path("Assets/icon.png")))

        self.model: Model = Model.load()
        self.window.deiconify()
        self.instructions_details()

    def instructions_details(self) -> None:
        """
        Here, we display the instructions and details about the app
        :return: This doesn't return anything
        """
        toplevel: tk.Toplevel = tk.Toplevel(self.window)
        toplevel.resizable(False, False)
        toplevel.title("Instructions & Details")

        frame: tk.Frame = tk.Frame(toplevel)
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Welcome to Password Validator!", font=("Arial", 35, "bold")).grid(row=0, column=0)
        tk.Label(frame, text="This app is made for rating your passwords.", font=("Arial", 20)).grid(row=1, column=0)
        tk.Label(frame, text="Note: This app doesn't save any of\nyour passwords!", font=("Arial", 20, "bold")).grid(row=2, column=0)
        tk.Label(frame, text="This app has 3 levels of password rating:\n"
                             "0 - Weak\n"
                             "1 - Decent\n"
                             "2 - Strong\n"
                             "As well as a note for common passwords.", font=("Arial", 20)).grid(row=3, column=0, pady=10)
        tk.Label(frame, text="To use it, enter your password into the given entry\n"
                             "and press evaluate. That how simple it is!", font=("Arial", 20)).grid(row=4, column=0)

    def run(self) -> None:
        """
        This is the main code for the app.
        :return: This doesn't return anything
        """
        tk.Label(self.window, text="Password Validator", font=("Arial", 35, "bold")).pack(padx=10)

        frame: tk.Frame = tk.Frame(self.window)
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Enter password: ", font=("Arial", 20)).grid(row=0, column=0)
        p_entry: tk.Entry = tk.Entry(frame, bg="#333333")
        p_entry.grid(row=0, column=1)

        def result() -> None:
            """
            Here, we display the results in a messagebox
            :return: This doesn't return anything
            """
            password: str = p_entry.get()
            p_entry.delete(0, tk.END)
            strength: str = self.model.evaluate(password)
            mbox.showinfo(title="Password strength", message=strength)

        evaluate: tk.Button = tk.Button(frame, text="evaluate", command=result)
        evaluate.grid(row=0, column=2)

        tk.Button(self.window, text="info", command=self.instructions_details).pack(pady=10)

        self.window.mainloop()


def main() -> None:
    """
    This runs the app
    :return: This doesn't return anything
    """
    pv: PasswordValidater = PasswordValidater()
    pv.run()


if __name__ == '__main__':
    main()