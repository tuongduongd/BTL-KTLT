# gui/tab_lich_hen.py
# TabLichHen — Tab quản lý Lịch Hẹn (CRUD + kiểm tra trùng)


import tkinter as tk
from tkinter import messagebox
from gui.base_tab import BaseTab
from main import (
    LichHen,
    doc_danh_sach_lich_hen,
    ghi_file, tao_ma_tu_dong, kiem_tra_trung_lich,
    FILE_LICH_HEN
)
from cau_truc_du_lieu import kiem_tra_dinh_dang_ngay, kiem_tra_dinh_dang_gio


class TabLichHen(BaseTab):
    """Tab quản lý Lịch Hẹn."""

    def __init__(self, frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo):
        super().__init__(frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo)
        self.ma_dang_chon = ""
        self._thiet_lap_giao_dien()


    def _thiet_lap_giao_dien(self):
        # Tab lịch hẹn có nhiều trường hơn nên dùng 2 hàng
        khung_nhap = tk.Frame(self.frame)
        khung_nhap.pack(fill="x", pady=10, padx=10)

        # Hàng 0: các trường nhập
        self.e_bn, self.e_bs, self.e_ngay, self.e_gio, self.e_tt = self.tao_form(
            khung_nhap, [
                ("Ma BN:",             12),
                ("Ma BS:",             12),
                ("Ngay (YYYY-MM-DD):", 14),
                ("Gio (HH:MM):",       10),
                ("Trang thai:",        12),
            ], hang=0
        )

        # Hàng 1: các nút (đặt giữa bằng columnspan)
        khung_nut = tk.Frame(khung_nhap)
        khung_nut.grid(row=1, column=0, columnspan=10, pady=8)
        tk.Button(khung_nut, text="Dat Lich", command=self._xu_ly_them, width=10).pack(side="left", padx=5)
        tk.Button(khung_nut, text="Sua Lich", command=self._xu_ly_sua,  width=10).pack(side="left", padx=5)
        tk.Button(khung_nut, text="Xoa Lich", command=self._xu_ly_xoa,  width=10).pack(side="left", padx=5)

        self.bang = self.tao_bang(
            columns=("ma", "bn", "bs", "ngay", "gio", "tt"),
            headings=("Ma LH", "Ma BN", "Ma BS", "Ngay", "Gio", "Trang Thai")
        )
        self.bang.bind("<<TreeviewSelect>>", self._chon_hang)
        self._tai_du_lieu()


    def _chon_hang(self, event):
        chon = self.bang.selection()
        if chon:
            gv = self.bang.item(chon[0])['values']
            self.ma_dang_chon = gv[0]
            self.e_bn.delete(0, tk.END);   self.e_bn.insert(0, gv[1])
            self.e_bs.delete(0, tk.END);   self.e_bs.insert(0, gv[2])
            self.e_ngay.delete(0, tk.END); self.e_ngay.insert(0, gv[3])
            gio_str = str(gv[4])
            if len(gio_str) == 4 and gio_str[1] == ':': gio_str = "0" + gio_str
            self.e_gio.delete(0, tk.END);  self.e_gio.insert(0, gio_str)
            self.e_tt.delete(0, tk.END);   self.e_tt.insert(0, gv[5])


    def _kiem_tra(self, bn, bs, ngay, gio, tt):
        if bn == "" or bs == "" or ngay == "" or gio == "" or tt == "":
            messagebox.showwarning("Canh bao", "Vui long nhap du thong tin!")
            return False
        if not kiem_tra_dinh_dang_ngay(ngay):
            messagebox.showerror("Loi", "Ngay khong hop le (YYYY-MM-DD)!"); return False
        if not kiem_tra_dinh_dang_gio(gio):
            messagebox.showerror("Loi", "Gio khong hop le (HH:MM)!"); return False
        return True

    
    def _xu_ly_them(self):
        bn = self.e_bn.get(); bs = self.e_bs.get(); ngay = self.e_ngay.get()
        gio = self.e_gio.get(); tt = self.e_tt.get()
        if not self._kiem_tra(bn, bs, ngay, gio, tt): return
        ds = doc_danh_sach_lich_hen()
        if kiem_tra_trung_lich(ds, bs, ngay, gio):
            messagebox.showerror("Loi", "Bac si da kin lich gio nay!"); return
        ds.them_cuoi(LichHen(tao_ma_tu_dong(ds, "LH"), bn, bs, ngay, gio, tt))
        ghi_file(FILE_LICH_HEN, ds)
        self._lam_moi()
        self._cap_nhat_trang_thai("Da dat lich hen thanh cong.")

    def _xu_ly_sua(self):
        if self.ma_dang_chon == "": return
        bn = self.e_bn.get(); bs = self.e_bs.get(); ngay = self.e_ngay.get()
        gio = self.e_gio.get(); tt = self.e_tt.get()
        if not self._kiem_tra(bn, bs, ngay, gio, tt): return
        ds = doc_danh_sach_lich_hen()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('lich_hen', 'sua', LichHen(
                cu.ma, cu.ma_benh_nhan, cu.ma_bac_si,
                cu.ngay_kham, cu.gio_kham, cu.trang_thai))
        ds.cap_nhat_theo_dieu_kien(
            lambda x: x.ma == self.ma_dang_chon,
            LichHen(self.ma_dang_chon, bn, bs, ngay, gio, tt))
        ghi_file(FILE_LICH_HEN, ds)
        self._lam_moi()

    def _xu_ly_xoa(self):
        if self.ma_dang_chon == "": return
        ds = doc_danh_sach_lich_hen()
        cu = ds.tim_kiem(lambda x: x.ma == self.ma_dang_chon)
        if cu:
            self._push_undo('lich_hen', 'xoa', LichHen(
                cu.ma, cu.ma_benh_nhan, cu.ma_bac_si,
                cu.ngay_kham, cu.gio_kham, cu.trang_thai))
        ds.xoa_theo_dieu_kien(lambda x: x.ma == self.ma_dang_chon)
        ghi_file(FILE_LICH_HEN, ds)
        self._lam_moi()

   
    def _lam_moi(self):
        self.ma_dang_chon = ""
        for e in (self.e_bn, self.e_bs, self.e_ngay, self.e_gio, self.e_tt):
            e.delete(0, tk.END)
        self._tai_du_lieu()

    def _tai_du_lieu(self):
        for row in self.bang.get_children(): self.bang.delete(row)
        for lh in doc_danh_sach_lich_hen().duyet():
            self.bang.insert("", "end", values=(
                lh.ma, lh.ma_benh_nhan, lh.ma_bac_si,
                lh.ngay_kham, lh.gio_kham, lh.trang_thai))

    def lam_tuoi(self):
        self._tai_du_lieu()
