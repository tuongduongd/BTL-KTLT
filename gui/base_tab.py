# gui/base_tab.py

# BaseTab — Class cha dùng chung cho tất cả các Tab
# Cung cấp:
#   - tao_bang()       : tạo Treeview + scrollbar
#   - tao_form()       : tạo hàng Label+Entry từ danh sách config
#   - tao_khung_nut()  : tạo hàng nút bấm từ danh sách config
#   - _push_undo()     : đẩy thao tác vào Stack Undo

import tkinter as tk
from tkinter import ttk


class BaseTab:
    """
    Class cha mà tất cả các Tab kế thừa.
    Nhận vào frame gốc, undo_stack, và callback cập nhật trạng thái.
    """

    def __init__(self, frame, undo_stack, fn_cap_nhat_trang_thai, fn_nut_undo):
        """
        frame                  : tk.Frame của tab này (đã được tạo bởi app.py)
        undo_stack             : Stack dùng chung
        fn_cap_nhat_trang_thai : hàm callback cập nhật thanh trạng thái bên dưới
        fn_nut_undo            : hàm callback bật,tắt nút Undo
        """
        self.frame = frame
        self.undo_stack = undo_stack
        self._cap_nhat_trang_thai = fn_cap_nhat_trang_thai
        self._set_nut_undo = fn_nut_undo

    
    # HELPER 1: Tạo bảng Treeview có thanh cuộn dọc
    
    def tao_bang(self, columns, headings, chieu_cao=14):
        """
        Tạo và trả về Treeview widget đã được đặt vào self.frame.
        columns  : tuple tên cột nội bộ, vd: ("ma", "ten", "ck")
        headings : tuple tiêu đề hiển thị, vd: ("Ma BS", "Ho Ten", "Chuyen Khoa")
        """
        khung = tk.Frame(self.frame)
        khung.pack(fill="both", expand=True, padx=10, pady=5)

        tree = ttk.Treeview(khung, columns=columns, show="headings", height=chieu_cao)
        scrollbar = ttk.Scrollbar(khung, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for i, hd in enumerate(headings):
            tree.heading(columns[i], text=hd)
            tree.column(columns[i], anchor="center")

        tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return tree

    
    # HELPER 2: Tạo hàng Label + Entry từ danh sách config
    
    def tao_form(self, khung_cha, danh_sach_truong, hang=0):
        """
        Tạo các cặp Label + Entry và đặt vào khung_cha bằng grid().
        danh_sach_truong : list of (label_text, entry_width)
                           vd: [("Ho ten:", 20), ("Chuyen khoa:", 15)]
        hang             : grid row để đặt các widget (mặc định 0)
        Trả về           : list các Entry widget theo đúng thứ tự
        """
        entries = []
        for i, (label_text, entry_width) in enumerate(danh_sach_truong):
            col_label = i * 2
            col_entry = i * 2 + 1
            tk.Label(khung_cha, text=label_text).grid(
                row=hang, column=col_label, padx=5, pady=5, sticky="e")
            e = tk.Entry(khung_cha, width=entry_width)
            e.grid(row=hang, column=col_entry, padx=5, pady=5)
            entries.append(e)
        return entries

    
    # HELPER 3: Tạo hàng nút bấm từ danh sách config
    
    def tao_khung_nut(self, khung_cha, danh_sach_nut, hang=0, cot_bat_dau=None, colspan=None):
        """
        Tạo các nút bấm và đặt vào khung_cha.
        danh_sach_nut : list of (text, command, width)
                        vd: [("Them", self.xu_ly_them, 8), ("Sua", ..., 8)]
        hang          : grid row
        cot_bat_dau   : cột bắt đầu đặt khung nút (None = tự tính = sau entries)
        Trả về        : Frame chứa các nút
        """
        if cot_bat_dau is None:
            # Đặt sau tất cả entry (mỗi entry chiếm 2 cột: label + entry)
            cot_bat_dau = len(danh_sach_nut) * 2  # fallback tạm
        khung_nut = tk.Frame(khung_cha)
        kw_grid = {"row": hang, "column": cot_bat_dau, "padx": 10, "pady": 5}
        if colspan:
            kw_grid["columnspan"] = colspan
        khung_nut.grid(**kw_grid)
        for (text, command, width) in danh_sach_nut:
            tk.Button(khung_nut, text=text, command=command, width=width).pack(
                side="left", padx=2)
        return khung_nut

   
    # HELPER 4: Đẩy thao tác vào Stack Undo
    
    def _push_undo(self, loai, hanh_dong, du_lieu_cu):
        """
        Lưu trạng thái cũ vào undo_stack trước khi sửa/xóa.
        loai       : 'bac_si' | 'benh_nhan' | 'lich_hen' | 'benh_an'
        hanh_dong  : 'xoa' | 'sua'
        du_lieu_cu : bản sao đối tượng trước khi thay đổi
        """
        self.undo_stack.push({
            'loai': loai,
            'hanh_dong': hanh_dong,
            'du_lieu_cu': du_lieu_cu
        })
        self._set_nut_undo(True)   # bật nút Undo
        self._cap_nhat_trang_thai(
            "Da thuc hien: [" + hanh_dong.upper() + " " + loai + "]. Nhan Undo de hoan tac."
        )
