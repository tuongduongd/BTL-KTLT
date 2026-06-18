# gui.py — Entry point
# Chạy: python gui.py
import tkinter as tk
from gui.app import QuanLyLichKhamApp

if __name__ == "__main__":
    root = tk.Tk()
    QuanLyLichKhamApp(root)
    root.mainloop()
