# gui/tab_hang_cho.py
# TabHangCho — Tab Hàng Chờ Khám (Queue FIFO)

import tkinter as tk
from tkinter import ttk, messagebox
from gui.base_tab import BaseTab


class TabHangCho(BaseTab):

    def __init__(self, frame, hang_cho, fn_cap_nhat_trang_thai, fn_nut_undo):
        # Tab này không cần undo_stack nên truyền None
        super().__init__(frame, None, fn_cap_nhat_trang_thai, fn_nut_undo)
        self.hang_cho = hang_cho   # Queue dùng chung từ app.py
        self._thiet_lap_giao_dien()

  
    def _thiet_lap_giao_dien(self):
        # Khung nhập liệu
        khung_tren = tk.LabelFrame(self.frame,
                                   text="Xep benh nhan vao hang cho",
                                   padx=8, pady=8)
        khung_tren.pack(fill="x", padx=15, pady=12)

        tk.Label(khung_tren, text="Ma BN:").grid(row=0, column=0, padx=6, pady=5)
        self.e_ma = tk.Entry(khung_tren, width=12)
        self.e_ma.grid(row=0, column=1, padx=6, pady=5)

        tk.Label(khung_tren, text="Ten BN:").grid(row=0, column=2, padx=6, pady=5)
        self.e_ten = tk.Entry(khung_tren, width=22)
        self.e_ten.grid(row=0, column=3, padx=6, pady=5)

        tk.Button(
            khung_tren, text="Them vao hang cho",
            command=self._xu_ly_them,
            bg="#5cb85c", fg="white", relief=tk.FLAT, padx=8
        ).grid(row=0, column=4, padx=12, pady=5)

        # Bảng danh sách chờ 
        khung_bang = tk.LabelFrame(
            self.frame,
            text="Danh sach dang cho",
            padx=8, pady=8)
        khung_bang.pack(fill="both", expand=True, padx=15, pady=5)

        cot     = ("stt", "ma", "ten")
        tieu_de = ("STT", "Ma BN", "Ten Benh Nhan")
        self.bang = ttk.Treeview(khung_bang, columns=cot, show="headings", height=12)
        for c, hd in zip(cot, tieu_de):
            self.bang.heading(c, text=hd)
            self.bang.column(c, anchor="center")
        self.bang.pack(fill="both", expand=True)

        # Khung dưới: nút gọi + nhãn trạng thái
        khung_duoi = tk.Frame(self.frame)
        khung_duoi.pack(fill="x", padx=15, pady=10)

        tk.Button(
            khung_duoi, text="Goi benh nhan tiep theo",
            command=self._xu_ly_goi_tiep,
            bg="#d9534f", fg="white", font=("Arial", 11, "bold"),
            relief=tk.FLAT, padx=12, pady=6
        ).pack(side=tk.LEFT, padx=6)

        self.nhan_dang_kham = tk.Label(
            khung_duoi, text="Dang goi: ---",
            font=("Arial", 13, "bold"), fg="#d9534f"
        )
        self.nhan_dang_kham.pack(side=tk.LEFT, padx=20)

        self.nhan_so_cho = tk.Label(
            khung_duoi, text="So nguoi cho: 0",
            font=("Arial", 11), fg="#555"
        )
        self.nhan_so_cho.pack(side=tk.RIGHT, padx=10)

   
    def _cap_nhat_bang(self):
        """Vẽ lại bảng từ Queue hiện tại."""
        for row in self.bang.get_children(): self.bang.delete(row)
        stt = 1
        for nguoi in self.hang_cho.duyet():
            self.bang.insert("", "end", values=(stt, nguoi['ma'], nguoi['ten']))
            stt += 1
        self.nhan_so_cho.config(text="So nguoi cho: " + str(self.hang_cho.kich_thuoc()))

    def _xu_ly_them(self):
        """Enqueue: thêm BN vào cuối hàng đợi."""
        ma  = self.e_ma.get().strip()
        ten = self.e_ten.get().strip()
        if ma == "" or ten == "":
            messagebox.showwarning("Canh bao", "Vui long nhap du Ma BN va Ten BN!")
            return
        self.hang_cho.enqueue({'ma': ma, 'ten': ten})
        self.e_ma.delete(0, tk.END)
        self.e_ten.delete(0, tk.END)
        self._cap_nhat_bang()
        self._cap_nhat_trang_thai("Da xep [" + ten + "] vao hang cho.")

    def _xu_ly_goi_tiep(self):
        """Dequeue: lấy BN đầu hàng ra và thông báo."""
        if self.hang_cho.is_empty():
            messagebox.showinfo("Hang cho", "Hang cho hien dang trong!")
            self.nhan_dang_kham.config(text="Dang goi: ---")
            return
        nguoi = self.hang_cho.dequeue()
        ten = nguoi['ten']; ma = nguoi['ma']
        self.nhan_dang_kham.config(text="Dang goi: " + ten + " (" + ma + ")")
        self._cap_nhat_bang()
        messagebox.showinfo("Moi vao kham", "Moi benh nhan: " + ten + " [" + ma + "] vao kham!")
        self._cap_nhat_trang_thai("Da goi [" + ten + "] vao kham.")

    def lam_tuoi(self):
        self._cap_nhat_bang()
