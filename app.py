# gui/app.py

# QuanLyLichKhamApp — Class chính lắp ráp toàn bộ ứng dụng
# Phụ trách: Đỗ Tùng Dương

import tkinter as tk
from tkinter import ttk, messagebox
from cau_truc_du_lieu import Stack, Queue
from main import (
    doc_danh_sach_bac_si, doc_danh_sach_benh_nhan,
    doc_danh_sach_lich_hen, doc_danh_sach_benh_an,
    ghi_file,
    FILE_BAC_SI, FILE_BENH_NHAN, FILE_LICH_HEN, FILE_BENH_AN
)
from gui.tab_bac_si    import TabBacSi
from gui.tab_benh_nhan import TabBenhNhan
from gui.tab_lich_hen  import TabLichHen
from gui.tab_benh_an   import TabBenhAn
from gui.tab_hang_cho  import TabHangCho
from gui.tab_bao_cao   import TabBaoCao


class QuanLyLichKhamApp:
    """
    Class chính của ứng dụng.
    Chịu trách nhiệm:
      - Tạo cửa sổ và Notebook
      - Khởi tạo shared state (undo_stack, hang_cho)
      - Tạo từng Tab và truyền shared state vào
      - Quản lý thanh trạng thái và logic Undo
    """

    def __init__(self, root):
        self.root = root
        self.root.title("He Thong Quan Ly Lich Kham")
        self.root.geometry("1150x700")

        # Shared state
        self.undo_stack = Stack()   # Dùng chung cho mọi tab CRUD
        self.hang_cho   = Queue()   # Dùng riêng cho TabHangCho

        # Notebook 
        nb = ttk.Notebook(root)
        nb.pack(expand=True, fill="both")

        # Tạo Frame cho từng tab
        f_bs  = tk.Frame(nb)
        f_bn  = tk.Frame(nb)
        f_lh  = tk.Frame(nb)
        f_ba  = tk.Frame(nb)
        f_hc  = tk.Frame(nb)
        f_bc  = tk.Frame(nb)

        nb.add(f_bs,  text="  Bac Si  ")
        nb.add(f_bn,  text="  Benh Nhan  ")
        nb.add(f_lh,  text="  Lich Hen  ")
        nb.add(f_ba,  text="  Benh An  ")
        nb.add(f_hc,  text="  Hang Cho Kham  ")
        nb.add(f_bc,  text="  Bao Cao  ")

        # Khởi tạo từng Tab, truyền shared state 
        self.tab_bs = TabBacSi(
            f_bs, self.undo_stack,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        self.tab_bn = TabBenhNhan(
            f_bn, self.undo_stack,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        self.tab_lh = TabLichHen(
            f_lh, self.undo_stack,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        self.tab_ba = TabBenhAn(
            f_ba, self.undo_stack,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        self.tab_hc = TabHangCho(
            f_hc, self.hang_cho,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        self.tab_bc = TabBaoCao(
            f_bc,
            self._cap_nhat_trang_thai, self._set_nut_undo)

        # Map loai -> tab (để Undo biết refresh tab nào) 
        self._tab_map = {
            'bac_si':    self.tab_bs,
            'benh_nhan': self.tab_bn,
            'lich_hen':  self.tab_lh,
            'benh_an':   self.tab_ba,
        }

        # Thanh trạng thái + nút Undo
        self._thiet_lap_thanh_duoi()

   
    # THANH DƯỚI: trạng thái + nút Undo
    
    def _thiet_lap_thanh_duoi(self):
        thanh = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        thanh.pack(side=tk.BOTTOM, fill=tk.X)

        self.nhan_trang_thai = tk.Label(thanh, text="San sang.", anchor="w", padx=8)
        self.nhan_trang_thai.pack(side=tk.LEFT, expand=True, fill=tk.X)



    def _cap_nhat_trang_thai(self, thong_bao):
        self.nhan_trang_thai.config(text=thong_bao)

    def _set_nut_undo(self, bat):
        pass  # Nút Undo đã bị xoá

    
    # LOGIC UNDO: Pop Stack và phục hồi dữ liệu
   
    def _xu_ly_undo(self):
        ban_ghi = self.undo_stack.pop()
        if ban_ghi is None:
            self._set_nut_undo(False)
            return

        loai      = ban_ghi['loai']
        hanh_dong = ban_ghi['hanh_dong']
        doi_tuong = ban_ghi['du_lieu_cu']

        # Ánh xạ loại → file và hàm đọc
        _FILE = {
            'bac_si':    FILE_BAC_SI,
            'benh_nhan': FILE_BENH_NHAN,
            'lich_hen':  FILE_LICH_HEN,
            'benh_an':   FILE_BENH_AN,
        }
        _DOC = {
            'bac_si':    doc_danh_sach_bac_si,
            'benh_nhan': doc_danh_sach_benh_nhan,
            'lich_hen':  doc_danh_sach_lich_hen,
            'benh_an':   doc_danh_sach_benh_an,
        }

        ds = _DOC[loai]()
        if hanh_dong == 'xoa':
            ds.them_cuoi(doi_tuong)
        elif hanh_dong == 'sua':
            ds.cap_nhat_theo_dieu_kien(lambda x: x.ma == doi_tuong.ma, doi_tuong)
        ghi_file(_FILE[loai], ds)

        # Làm mới đúng tab bị ảnh hưởng
        self._tab_map[loai].lam_tuoi()

        if self.undo_stack.is_empty():
            self._set_nut_undo(False)

        self._cap_nhat_trang_thai("Da hoan tac: [" + hanh_dong + " " + loai + "].")
        messagebox.showinfo("Hoan tac", "Da hoan tac thanh cong!")
