import tkinter as tk
from gui_main_app import MainApplication


def main():
    # Open GUI Window
    main_window = tk.Tk()
    main_window.title('FSCV GUI')
    main_app = MainApplication(main_window)
    main_app.grid(row=0, column=0)

    main_window.mainloop()


if __name__ == "__main__":
    main()
