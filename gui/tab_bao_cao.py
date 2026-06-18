# gui/tab_bao_cao.py
# TabBaoCao


import tkinter as tk
from gui.base_tab import BaseTab
from main import (
    doc_danh_sach_bac_si,
    doc_danh_sach_benh_nhan,
    doc_danh_sach_lich_hen,
)


class TabBaoCao(BaseTab):
    """Tab Báo Cáo: dùng tim_max và tim_min của DanhSachLienKet."""

    def __init__(self, frame, fn_cap_nhat_trang_thai, fn_nut_undo):
        super().__init__(frame, None, fn_cap_nhat_trang_thai, fn_nut_undo)
        self._thiet_lap_giao_dien()

   
    def _thiet_lap_giao_dien(self):
        khung_nhap = tk.Frame(self.frame)
        khung_nhap.pack(fill="x", pady=10, padx=10)

        tk.Label(khung_nhap, text="Nhap ngay (VD: 2026-06-15):").pack(side="left", padx=5)
        self.e_ngay = tk.Entry(khung_nhap, width=15)
        self.e_ngay.pack(side="left", padx=5)

        tk.Button(
            khung_nhap, text="Xuat Bao Cao",
            command=self._xuat_bao_cao,
            bg="#337ab7", fg="white", relief=tk.FLAT, padx=8, pady=3
        ).pack(side="left", padx=15)

        self.o_noi_dung = tk.Text(self.frame, font=("Consolas", 11))
        self.o_noi_dung.pack(fill="both", expand=True, padx=10, pady=10)


    def _xuat_bao_cao(self):
        self.o_noi_dung.delete(1.0, tk.END)
        ngay_chon = self.e_ngay.get()

        ds_lh = doc_danh_sach_lich_hen()
        ds_bs = doc_danh_sach_bac_si()
        ds_bn = doc_danh_sach_benh_nhan()

        # 1. Số cuộc hẹn trong ngày
        so_hen = ds_lh.dem(lambda lh: lh.ngay_kham == ngay_chon)
        self.o_noi_dung.insert(tk.END,
            "1. SO CUOC HEN TRONG NGAY " + ngay_chon + ": " + str(so_hen) + "\n\n")

        # 2. Bác sĩ nhiều lịch nhất — dùng DanhSachLienKet.tim_max()
        self.o_noi_dung.insert(tk.END, "2. BAC SI NHIEU LICH NHAT:\n")
        if ds_bs.do_dai() == 0:
            self.o_noi_dung.insert(tk.END, "   (Chua co du lieu)\n\n")
        else:
            bs_max, so_max = ds_bs.tim_max(
                lambda bs: ds_lh.dem(lambda lh: lh.ma_bac_si == bs.ma))
            if bs_max:
                self.o_noi_dung.insert(tk.END,
                    "   -> " + bs_max.ho_ten +
                    " | " + bs_max.chuyen_khoa +
                    " | " + str(so_max) + " lich\n\n")

        # 3. Thống kê số lần khám từng bệnh nhân
        self.o_noi_dung.insert(tk.END, "3. THONG KE LUOT KHAM TUNG BENH NHAN:\n")
        for bn in ds_bn.duyet():
            so_lan = ds_lh.dem(lambda lh: lh.ma_benh_nhan == bn.ma)
            self.o_noi_dung.insert(tk.END,
                "   - " + bn.ho_ten + ": " + str(so_lan) + " lan\n")

        # 4. Bác sĩ ít lịch nhất 
        self.o_noi_dung.insert(tk.END, "\n4. BAC SI IT LICH NHAT:\n")
        if ds_bs.do_dai() == 0:
            self.o_noi_dung.insert(tk.END, "   (Chua co du lieu)\n")
        else:
            bs_min, so_min = ds_bs.tim_min(
                lambda bs: ds_lh.dem(lambda lh: lh.ma_bac_si == bs.ma))
            if bs_min:
                self.o_noi_dung.insert(tk.END,
                    "   -> " + bs_min.ho_ten +
                    " | " + bs_min.chuyen_khoa +
                    " | " + str(so_min) + " lich\n")

        self._cap_nhat_trang_thai("Da xuat bao cao.")

    def lam_tuoi(self):
        pass  # Tab báo cáo không cần tự làm mới
