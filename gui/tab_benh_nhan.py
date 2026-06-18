# gui/tab_benh_nhan.py

# TabBenhNhan — Tab quản lý Bệnh Nhân (CRUD)
# Phụ trách: Kiều Anh Bằng

import tkinter as tk
from tkinter import messagebox
from gui.base_tab import BaseTab
from main import (
    BenhNhan,
    doc_danh_sach_benh_nhan,
    ghi_file, tao_ma_tu_dong,
    FILE_BENH_NHAN
)
from cau_truc_du_lieu import chuan_hoa_ten, chuoi_co_so, chuoi_sang_so, kiem_tra_sdt


class TabBenhNhan(BaseTab):
    """Tab quản lý danh sách Bệnh Nhân."""

    def __init__(self, frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo):
        super().__init__(frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo)
        self.ma_dang_chon = ""
        self._thiet_lap_giao_dien()

    
    def _thiet_lap_giao_dien(self):
        khung_nhap = tk.Frame(self.frame)
        khung_nhap.pack(fill="x", pady=10, padx=10)

        self.e_ten, self.e_ns, self.e_sdt = self.tao_form(khung_nhap, [
            ("Ho ten:",   20),
            ("Nam sinh:", 10),
            ("SDT:",      15),
        ])

        self.tao_khung_nut(khung_nhap, [
            ("Them", self._xu_ly_them, 8),
            ("Sua",  self._xu_ly_sua,  8),
            ("Xoa",  self._xu_ly_xoa,  8),
        ], hang=0, cot_bat_dau=6)

        self.bang = self.tao_bang(
            columns=("ma", "ten", "ns", "sdt"),
            headings=("Ma BN", "Ho Ten", "Nam Sinh", "So Dien Thoai")
        )
        self.bang.bind("<<TreeviewSelect>>", self._chon_hang)
        self._tai_du_lieu()

    
    def _chon_hang(self, event):
        chon = self.bang.selection()
        if chon:
            gv = self.bang.item(chon[0])['values']
            self.ma_dang_chon = gv[0]
            self.e_ten.delete(0, tk.END); self.e_ten.insert(0, gv[1])
            self.e_ns.delete(0, tk.END);  self.e_ns.insert(0, gv[2])
            sdt_str = str(gv[3])
            self.e_sdt.delete(0, tk.END)
            self.e_sdt.insert(0, sdt_str if sdt_str.startswith("0") else "0" + sdt_str)

    
    def _kiem_tra(self, ten, ns, sdt):
        if ten == "" or ns == "" or sdt == "":
            messagebox.showwarning("Canh bao", "Vui long nhap du thong tin!")
            return False
        if not chuoi_co_so(ns):
            messagebox.showerror("Loi", "Nam sinh phai la so!"); return False
        n_so = chuoi_sang_so(ns)
        if n_so < 1900 or n_so > 2026:
            messagebox.showerror("Loi", "Nam sinh vo ly!"); return False
        if not kiem_tra_sdt(sdt):
            messagebox.showerror("Loi", "SDT khong hop le!"); return False
        return True

    
    def _xu_ly_them(self):
        ten = self.e_ten.get(); ns = self.e_ns.get(); sdt = self.e_sdt.get()
        if not self._kiem_tra(ten, ns, sdt): return
        ten = chuan_hoa_ten(ten)
        ds = doc_danh_sach_benh_nhan()
        ds.them_cuoi(BenhNhan(tao_ma_tu_dong(ds, "BN"), ten, ns, sdt))
        ghi_file(FILE_BENH_NHAN, ds)
        self._lam_moi()
        self._cap_nhat_trang_thai("Da them benh nhan: " + ten)

    def _xu_ly_sua(self):
        if self.ma_dang_chon == "": return
        ten = self.e_ten.get(); ns = self.e_ns.get(); sdt = self.e_sdt.get()
        if not self._kiem_tra(ten, ns, sdt): return
        ten = chuan_hoa_ten(ten)
        ds = doc_danh_sach_benh_nhan()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('benh_nhan', 'sua',
                BenhNhan(cu.ma, cu.ho_ten, cu.nam_sinh, cu.sdt))
        ds.cap_nhat_theo_dieu_kien(
            lambda x: x.ma == self.ma_dang_chon,
            BenhNhan(self.ma_dang_chon, ten, ns, sdt))
        ghi_file(FILE_BENH_NHAN, ds)
        self._lam_moi()

    def _xu_ly_xoa(self):
        if self.ma_dang_chon == "": return
        ds = doc_danh_sach_benh_nhan()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('benh_nhan', 'xoa',
                BenhNhan(cu.ma, cu.ho_ten, cu.nam_sinh, cu.sdt))
        ds.xoa_theo_dieu_kien(lambda x: x.ma == self.ma_dang_chon)
        ghi_file(FILE_BENH_NHAN, ds)
        self._lam_moi()

    
    def _lam_moi(self):
        self.ma_dang_chon = ""
        for e in (self.e_ten, self.e_ns, self.e_sdt): e.delete(0, tk.END)
        self._tai_du_lieu()

    def _tai_du_lieu(self):
        for row in self.bang.get_children(): self.bang.delete(row)
        for bn in doc_danh_sach_benh_nhan().duyet():
            sdt_str = bn.sdt if str(bn.sdt).startswith("0") else "0" + str(bn.sdt)
            self.bang.insert("", "end",
                values=(bn.ma, bn.ho_ten, bn.nam_sinh, sdt_str))

    def lam_tuoi(self):
        self._tai_du_lieu()
