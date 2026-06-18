# gui/tab_bac_si.py

# TabBacSi — Tab quản lý Bác Sĩ (CRUD)
# Phụ trách: Đỗ Tùng Dương

import tkinter as tk
from tkinter import messagebox
from gui.base_tab import BaseTab
from main import (
    BacSi,
    doc_danh_sach_bac_si,
    ghi_file, tao_ma_tu_dong,
    FILE_BAC_SI
)
from cau_truc_du_lieu import chuan_hoa_ten


class TabBacSi(BaseTab):
    """Tab quản lý danh sách Bác Sĩ."""

    def __init__(self, frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo):
        super().__init__(frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo)
        self.ma_dang_chon = ""
        self._thiet_lap_giao_dien()

    
    def _thiet_lap_giao_dien(self):
        """Xây dựng toàn bộ giao diện của tab."""
        khung_nhap = tk.Frame(self.frame)
        khung_nhap.pack(fill="x", pady=10, padx=10)

        # Dùng tao_form() thay vì viết Label+Entry thủ công
        self.e_ten, self.e_ck, self.e_gio = self.tao_form(khung_nhap, [
            ("Ho ten:",      20),
            ("Chuyen khoa:", 15),
            ("Khung gio:",   20),
        ])

        # Dùng tao_khung_nut() thay vì viết Button thủ công
        self.tao_khung_nut(khung_nhap, [
            ("Them", self._xu_ly_them, 8),
            ("Sua",  self._xu_ly_sua,  8),
            ("Xoa",  self._xu_ly_xoa,  8),
        ], hang=0, cot_bat_dau=6)

        # Bảng hiển thị
        self.bang = self.tao_bang(
            columns=("ma", "ten", "ck", "gio"),
            headings=("Ma BS", "Ho Ten", "Chuyen Khoa", "Khung Gio")
        )
        self.bang.bind("<<TreeviewSelect>>", self._chon_hang)
        self._tai_du_lieu()

    
    def _chon_hang(self, event):
        chon = self.bang.selection()
        if chon:
            gv = self.bang.item(chon[0])['values']
            self.ma_dang_chon = gv[0]
            self.e_ten.delete(0, tk.END); self.e_ten.insert(0, gv[1])
            self.e_ck.delete(0, tk.END);  self.e_ck.insert(0, gv[2])
            self.e_gio.delete(0, tk.END); self.e_gio.insert(0, gv[3])

   
    def _xu_ly_them(self):
        ten = self.e_ten.get(); ck = self.e_ck.get(); gio = self.e_gio.get()
        if ten == "" or ck == "" or gio == "":
            messagebox.showwarning("Canh bao", "Vui long nhap du thong tin!")
            return
        ten = chuan_hoa_ten(ten)
        ds = doc_danh_sach_bac_si()
        ds.them_cuoi(BacSi(tao_ma_tu_dong(ds, "BS"), ten, ck, gio))
        ghi_file(FILE_BAC_SI, ds)
        self._lam_moi()
        self._cap_nhat_trang_thai("Da them bac si: " + ten)

    def _xu_ly_sua(self):
        if self.ma_dang_chon == "":
            messagebox.showwarning("Canh bao", "Vui long chon bac si de sua!")
            return
        ten = chuan_hoa_ten(self.e_ten.get())
        ck  = self.e_ck.get()
        gio = self.e_gio.get()
        ds  = doc_danh_sach_bac_si()
        cu  = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('bac_si', 'sua',
                BacSi(cu.ma, cu.ho_ten, cu.chuyen_khoa, cu.khung_gio))
        ds.cap_nhat_theo_dieu_kien(
            lambda x: x.ma == self.ma_dang_chon,
            BacSi(self.ma_dang_chon, ten, ck, gio))
        ghi_file(FILE_BAC_SI, ds)
        self._lam_moi()
        messagebox.showinfo("Thanh cong", "Da cap nhat!")

    def _xu_ly_xoa(self):
        if self.ma_dang_chon == "":
            messagebox.showwarning("Canh bao", "Vui long chon bac si de xoa!")
            return
        ds  = doc_danh_sach_bac_si()
        cu  = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('bac_si', 'xoa',
                BacSi(cu.ma, cu.ho_ten, cu.chuyen_khoa, cu.khung_gio))
        ds.xoa_theo_dieu_kien(lambda x: x.ma == self.ma_dang_chon)
        ghi_file(FILE_BAC_SI, ds)
        self._lam_moi()
        messagebox.showinfo("Thanh cong", "Da xoa!")

    
    def _lam_moi(self):
        self.ma_dang_chon = ""
        for e in (self.e_ten, self.e_ck, self.e_gio):
            e.delete(0, tk.END)
        self._tai_du_lieu()

    def _tai_du_lieu(self):
        for row in self.bang.get_children(): self.bang.delete(row)
        for bs in doc_danh_sach_bac_si().duyet():
            self.bang.insert("", "end",
                values=(bs.ma, bs.ho_ten, bs.chuyen_khoa, bs.khung_gio))

    # Hàm public để app.py gọi khi cần refresh (vd: sau Undo)
    def lam_tuoi(self):
        self._tai_du_lieu()
