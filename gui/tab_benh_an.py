# gui/tab_benh_an.py
# TabBenhAn — Tab quản lý Bệnh Án (CRUD)

import tkinter as tk
from tkinter import messagebox
from gui.base_tab import BaseTab
from main import (
    BenhAn,
    doc_danh_sach_benh_an,
    ghi_file, tao_ma_tu_dong,
    FILE_BENH_AN
)


class TabBenhAn(BaseTab):
    """tab quản lý bệnh án."""

    def __init__(self, frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo):
        super().__init__(frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo)
        self.ma_dang_chon = ""
        self._thiet_lap_giao_dien()

   
    def _thiet_lap_giao_dien(self):
        khung_nhap = tk.Frame(self.frame)
        khung_nhap.pack(fill="x", pady=10, padx=10)

        self.e_lh, self.e_tc, self.e_kl = self.tao_form(khung_nhap, [
            ("Ma Lich hen:", 15),
            ("Trieu chung:", 25),
            ("Ket luan:",    25),
        ])

        self.tao_khung_nut(khung_nhap, [
            ("Ghi Moi", self._xu_ly_them, 8),
            ("Sua An",  self._xu_ly_sua,  8),
            ("Xoa An",  self._xu_ly_xoa,  8),
        ], hang=0, cot_bat_dau=6)

        self.bang = self.tao_bang(
            columns=("ma", "lh", "tc", "kl"),
            headings=("Ma Benh An", "Ma Lich Hen", "Trieu Chung", "Ket Luan")
        )
        self.bang.bind("<<TreeviewSelect>>", self._chon_hang)
        self._tai_du_lieu()

   
    def _chon_hang(self, event):
        chon = self.bang.selection()
        if chon:
            gv = self.bang.item(chon[0])['values']
            self.ma_dang_chon = gv[0]
            self.e_lh.delete(0, tk.END); self.e_lh.insert(0, gv[1])
            self.e_tc.delete(0, tk.END); self.e_tc.insert(0, gv[2])
            self.e_kl.delete(0, tk.END); self.e_kl.insert(0, gv[3])


    def _xu_ly_them(self):
        lh = self.e_lh.get(); tc = self.e_tc.get(); kl = self.e_kl.get()
        if lh == "" or tc == "" or kl == "":
            messagebox.showwarning("Canh bao", "Vui long nhap du thong tin!")
            return
        ds = doc_danh_sach_benh_an()
        ds.them_cuoi(BenhAn(tao_ma_tu_dong(ds, "BA"), lh, tc, kl))
        ghi_file(FILE_BENH_AN, ds)
        self._lam_moi()
        self._cap_nhat_trang_thai("Da ghi benh an moi.")

    def _xu_ly_sua(self):
        if self.ma_dang_chon == "": return
        lh = self.e_lh.get(); tc = self.e_tc.get(); kl = self.e_kl.get()
        ds = doc_danh_sach_benh_an()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('benh_an', 'sua',
                BenhAn(cu.ma, cu.ma_lich_hen, cu.trieu_chung, cu.ket_luan))
        ds.cap_nhat_theo_dieu_kien(
            lambda x: x.ma == self.ma_dang_chon,
            BenhAn(self.ma_dang_chon, lh, tc, kl))
        ghi_file(FILE_BENH_AN, ds)
        self._lam_moi()

    def _xu_ly_xoa(self):
        if self.ma_dang_chon == "": return
        ds = doc_danh_sach_benh_an()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('benh_an', 'xoa',
                BenhAn(cu.ma, cu.ma_lich_hen, cu.trieu_chung, cu.ket_luan))
        ds.xoa_theo_dieu_kien(lambda x: x.ma == self.ma_dang_chon)
        ghi_file(FILE_BENH_AN, ds)
        self._lam_moi()

    
    def _lam_moi(self):
        self.ma_dang_chon = ""
        for e in (self.e_lh, self.e_tc, self.e_kl): e.delete(0, tk.END)
        self._tai_du_lieu()

    def _tai_du_lieu(self):
        for row in self.bang.get_children(): self.bang.delete(row)
        for ba in doc_danh_sach_benh_an().duyet():
            self.bang.insert("", "end",
                values=(ba.ma, ba.ma_lich_hen, ba.trieu_chung, ba.ket_luan))

    def lam_tuoi(self):
        self._tai_du_lieu()
