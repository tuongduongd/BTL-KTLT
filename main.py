import os
from cau_truc_du_lieu import (
    DanhSachLienKet, chia_chuoi, loai_bo_khoang_trang,
    chuoi_sang_so, chuoi_co_so
)

THU_MUC_DU_LIEU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FILE_BAC_SI = os.path.join(THU_MUC_DU_LIEU, "bacsi.txt")
FILE_BENH_NHAN = os.path.join(THU_MUC_DU_LIEU, "benhnhan.txt")
FILE_LICH_HEN = os.path.join(THU_MUC_DU_LIEU, "lichhen.txt")
FILE_BENH_AN = os.path.join(THU_MUC_DU_LIEU, "benhan.txt")

class BacSi:
    def __init__(self, ma, ho_ten, chuyen_khoa, khung_gio):
        self.ma = ma
        self.ho_ten = ho_ten
        self.chuyen_khoa = chuyen_khoa
        self.khung_gio = khung_gio

    def to_str(self):
        return self.ma + "|" + self.ho_ten + "|" + self.chuyen_khoa + "|" + self.khung_gio


class BenhNhan:
    def __init__(self, ma, ho_ten, nam_sinh, sdt):
        self.ma = ma
        self.ho_ten = ho_ten
        self.nam_sinh = nam_sinh
        self.sdt = sdt

    def to_str(self):
        return self.ma + "|" + self.ho_ten + "|" + self.nam_sinh + "|" + self.sdt


class LichHen:
    def __init__(self, ma, ma_benh_nhan, ma_bac_si, ngay_kham, gio_kham, trang_thai):
        self.ma = ma
        self.ma_benh_nhan = ma_benh_nhan
        self.ma_bac_si = ma_bac_si
        self.ngay_kham = ngay_kham
        self.gio_kham = gio_kham
        self.trang_thai = trang_thai

    def to_str(self):
        return (self.ma + "|" + self.ma_benh_nhan + "|" + self.ma_bac_si + "|" + 
                self.ngay_kham + "|" + self.gio_kham + "|" + self.trang_thai)


class BenhAn:
    def __init__(self, ma, ma_lich_hen, trieu_chung, ket_luan):
        self.ma = ma
        self.ma_lich_hen = ma_lich_hen
        self.trieu_chung = trieu_chung
        self.ket_luan = ket_luan

    def to_str(self):
        return self.ma + "|" + self.ma_lich_hen + "|" + self.trieu_chung + "|" + self.ket_luan

#SỬ LÝ FILE

def tao_thu_muc_data():
    if not os.path.exists(THU_MUC_DU_LIEU):
        os.makedirs(THU_MUC_DU_LIEU)

def doc_file(duong_dan):
    ds_dong = DanhSachLienKet()
    if not os.path.exists(duong_dan):
        return ds_dong
    f = open(duong_dan, "r", encoding="utf-8")
    for dong in f:
        dong_sach = loai_bo_khoang_trang(dong)
        if dong_sach != "":
            ds_dong.them_cuoi(dong_sach)
    f.close()
    return ds_dong

def ghi_file(duong_dan, ds_doi_tuong):
    tao_thu_muc_data()
    f = open(duong_dan, "w", encoding="utf-8")
    for doi_tuong in ds_doi_tuong.duyet():
        f.write(doi_tuong.to_str() + "\n")
    f.close()

def doc_danh_sach_bac_si():
    ds_bac_si = DanhSachLienKet()
    ds_dong = doc_file(FILE_BAC_SI)
    for dong in ds_dong.duyet():
        phan = chia_chuoi(dong, "|")
        if phan.do_dai() >= 4:
            ma = loai_bo_khoang_trang(phan.lay(0))
            ten = loai_bo_khoang_trang(phan.lay(1))
            ck = loai_bo_khoang_trang(phan.lay(2))
            gio = loai_bo_khoang_trang(phan.lay(3))
            ds_bac_si.them_cuoi(BacSi(ma, ten, ck, gio))
    return ds_bac_si

def doc_danh_sach_benh_nhan():
    ds_benh_nhan = DanhSachLienKet()
    ds_dong = doc_file(FILE_BENH_NHAN)
    for dong in ds_dong.duyet():
        phan = chia_chuoi(dong, "|")
        if phan.do_dai() >= 4:
            ma = loai_bo_khoang_trang(phan.lay(0))
            ten = loai_bo_khoang_trang(phan.lay(1))
            ns = loai_bo_khoang_trang(phan.lay(2))
            sdt = loai_bo_khoang_trang(phan.lay(3))
            ds_benh_nhan.them_cuoi(BenhNhan(ma, ten, ns, sdt))
    return ds_benh_nhan

def doc_danh_sach_lich_hen():
    ds_lich_hen = DanhSachLienKet()
    ds_dong = doc_file(FILE_LICH_HEN)
    for dong in ds_dong.duyet():
        phan = chia_chuoi(dong, "|")
        if phan.do_dai() >= 6:
            ma = loai_bo_khoang_trang(phan.lay(0))
            mbn = loai_bo_khoang_trang(phan.lay(1))
            mbs = loai_bo_khoang_trang(phan.lay(2))
            ngay = loai_bo_khoang_trang(phan.lay(3))
            gio = loai_bo_khoang_trang(phan.lay(4))
            tt = loai_bo_khoang_trang(phan.lay(5))
            ds_lich_hen.them_cuoi(LichHen(ma, mbn, mbs, ngay, gio, tt))
    return ds_lich_hen

def doc_danh_sach_benh_an():
    ds_benh_an = DanhSachLienKet()
    ds_dong = doc_file(FILE_BENH_AN)
    for dong in ds_dong.duyet():
        phan = chia_chuoi(dong, "|")
        if phan.do_dai() >= 4:
            ma = loai_bo_khoang_trang(phan.lay(0))
            mlh = loai_bo_khoang_trang(phan.lay(1))
            tc = loai_bo_khoang_trang(phan.lay(2))
            kl = loai_bo_khoang_trang(phan.lay(3))
            ds_benh_an.them_cuoi(BenhAn(ma, mlh, tc, kl))
    return ds_benh_an

# LOGIC NGHIỆP VỤ

def chuoi_cat_bo_tien_to(chuoi, tien_to):
    chieu_dai_tien_to = 0
    for c in tien_to:
        chieu_dai_tien_to += 1
        
    ket_qua = ""
    i = chieu_dai_tien_to
    
    chieu_dai_chuoi = 0
    for c in chuoi:
        chieu_dai_chuoi += 1
        
    while i < chieu_dai_chuoi:
        ket_qua += chuoi[i]
        i += 1
    return ket_qua

def tao_ma_tu_dong(danh_sach, tien_to):
    so_lon_nhat = 0
    for phan_tu in danh_sach.duyet():

        chuoi_so = chuoi_cat_bo_tien_to(phan_tu.ma, tien_to)
        if chuoi_co_so(chuoi_so):
            gia_tri_so = chuoi_sang_so(chuoi_so)
            if gia_tri_so > so_lon_nhat:
                so_lon_nhat = gia_tri_so
                
    so_moi = so_lon_nhat + 1

    chuoi_kq = ""
    if so_moi < 10:
        chuoi_kq = "00"
    elif so_moi < 100:
        chuoi_kq = "0"

    chuoi_tam = ""
    so_tam = so_moi
    if so_tam == 0:
        chuoi_tam = "0"
    else:
        while so_tam > 0:
            chu_so = so_tam % 10
            ky_tu = chr(chu_so + ord('0'))
            chuoi_tam_moi = ky_tu
            for c in chuoi_tam:
                chuoi_tam_moi += c
            chuoi_tam = chuoi_tam_moi
            so_tam = so_tam // 10
            
    return tien_to + chuoi_kq + chuoi_tam

def kiem_tra_trung_lich(ds_lich_hen, ma_bac_si, ngay, gio):
    """Kiểm tra xem bác sĩ đã bị đặt lịch hẹn giờ đó chưa."""
    for lh in ds_lich_hen.duyet():
        if lh.ma_bac_si == ma_bac_si:
            if lh.ngay_kham == ngay:
                if lh.gio_kham == gio:
                    if lh.trang_thai != "Da huy":
                        return True
    return False

def hien_thi_gio_trong(bac_si, ds_lich_hen, ngay):
    ds_gio_trong = DanhSachLienKet()

    cac_gio = chia_chuoi(bac_si.khung_gio, ",")
    
    for gio_chua_trim in cac_gio.duyet():
        gio = loai_bo_khoang_trang(gio_chua_trim)
        if gio != "":
            da_trung = kiem_tra_trung_lich(ds_lich_hen, bac_si.ma, ngay, gio)
            if da_trung == False:
                ds_gio_trong.them_cuoi(gio)
                
    return ds_gio_trong


# MENU CONSOLE

def nhap(thong_bao):
    print(thong_bao, end="")
    chuoi = input()
    return loai_bo_khoang_trang(chuoi)

def xuat_duong_ke():
    print("-" * 50)

def cls():
    # Xoá màn hình đơn giản
    print("\n" * 2)

def menu_bac_si():
    ds_bs = doc_danh_sach_bac_si()
    while True:
        cls()
        xuat_duong_ke()
        print("QUẢN LÝ BÁC SĨ")
        print("1. Xem danh sách")
        print("2. Thêm bác sĩ")
        print("0. Quay lại")
        xuat_duong_ke()
        chon = nhap("Chọn chức năng: ")
        if chon == "1":
            print("\n--- DANH SÁCH BÁC SĨ ---")
            for bs in ds_bs.duyet():
                print(bs.to_str())
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "2":
            ten = nhap("Nhập tên BS: ")
            ck = nhap("Chuyên khoa: ")
            gio = nhap("Khung giờ (VD: 08:00, 09:00): ")
            ma = tao_ma_tu_dong(ds_bs, "BS")
            ds_bs.them_cuoi(BacSi(ma, ten, ck, gio))
            ghi_file(FILE_BAC_SI, ds_bs)
            print("Thêm thành công!")
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "0":
            break

def menu_benh_nhan():
    ds_bn = doc_danh_sach_benh_nhan()
    while True:
        cls()
        xuat_duong_ke()
        print("QUẢN LÝ BỆNH NHÂN")
        print("1. Xem danh sách")
        print("2. Thêm bệnh nhân")
        print("0. Quay lại")
        xuat_duong_ke()
        chon = nhap("Chọn chức năng: ")
        if chon == "1":
            print("\n--- DANH SÁCH BỆNH NHÂN ---")
            for bn in ds_bn.duyet():
                print(bn.to_str())
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "2":
            ten = nhap("Nhập tên BN: ")
            ns = nhap("Năm sinh (4 chữ số): ")
            if not chuoi_co_so(ns):
                print("LỖI: Năm sinh phải là số!")
                nhap("Nhấn Enter để tiếp tục...")
                continue
                
            nam_sinh_so = chuoi_sang_so(ns)
            if nam_sinh_so < 1900 or nam_sinh_so > 2026:
                print("LỖI: Năm sinh không hợp lý!")
                nhap("Nhấn Enter để tiếp tục...")
                continue
                
            sdt = nhap("SDT: ")
            # Lấy hàm kiểm tra SDT tự code từ thư viện
            from cau_truc_du_lieu import kiem_tra_sdt
            if not kiem_tra_sdt(sdt):
                print("LỖI: Số điện thoại không đúng định dạng (9-11 số)!")
                nhap("Nhấn Enter để tiếp tục...")
                continue
                
            ma = tao_ma_tu_dong(ds_bn, "BN")
            ds_bn.them_cuoi(BenhNhan(ma, ten, ns, sdt))
            ghi_file(FILE_BENH_NHAN, ds_bn)
            print("Thêm thành công!")
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "0":
            break

def menu_lich_hen():
    ds_lh = doc_danh_sach_lich_hen()
    while True:
        cls()
        xuat_duong_ke()
        print("QUẢN LÝ LỊCH HẸN")
        print("1. Xem danh sách")
        print("2. Đặt lịch mới")
        print("0. Quay lại")
        xuat_duong_ke()
        chon = nhap("Chọn chức năng: ")
        if chon == "1":
            print("\n--- DANH SÁCH LỊCH HẸN ---")
            for lh in ds_lh.duyet():
                print(lh.to_str())
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "2":
            mbn = nhap("Mã BN: ")
            mbs = nhap("Mã BS: ")
            ngay = nhap("Ngày khám (YYYY-MM-DD): ")
            
            from cau_truc_du_lieu import kiem_tra_dinh_dang_ngay, kiem_tra_dinh_dang_gio
            
            if not kiem_tra_dinh_dang_ngay(ngay):
                print("LỖI: Ngày không hợp lệ hoặc sai định dạng!")
                nhap("Nhấn Enter để tiếp tục...")
                continue
                
            gio = nhap("Giờ khám (HH:MM): ")
            if not kiem_tra_dinh_dang_gio(gio):
                print("LỖI: Giờ không hợp lệ hoặc sai định dạng!")
                nhap("Nhấn Enter để tiếp tục...")
                continue
            
            # Logic check trùng lịch
            if kiem_tra_trung_lich(ds_lh, mbs, ngay, gio):
                print("LỖI: Bác sĩ này đã bận vào giờ đó!")
            else:
                ma = tao_ma_tu_dong(ds_lh, "LH")
                ds_lh.them_cuoi(LichHen(ma, mbn, mbs, ngay, gio, "Da dat"))
                ghi_file(FILE_LICH_HEN, ds_lh)
                print("Đặt lịch thành công!")
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "0":
            break

def menu_benh_an():
    ds_ba = doc_danh_sach_benh_an()
    while True:
        cls()
        xuat_duong_ke()
        print("QUẢN LÝ BỆNH ÁN")
        print("1. Xem danh sách")
        print("2. Ghi bệnh án")
        print("0. Quay lại")
        xuat_duong_ke()
        chon = nhap("Chọn chức năng: ")
        if chon == "1":
            print("\n--- DANH SÁCH BỆNH ÁN ---")
            for ba in ds_ba.duyet():
                print(ba.to_str())
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "2":
            mlh = nhap("Mã Lịch hẹn: ")
            tc = nhap("Triệu chứng: ")
            kl = nhap("Kết luận: ")
            ma = tao_ma_tu_dong(ds_ba, "BA")
            ds_ba.them_cuoi(BenhAn(ma, mlh, tc, kl))
            ghi_file(FILE_BENH_AN, ds_ba)
            print("Ghi thành công!")
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "0":
            break

def menu_chinh():
    while True:
        cls()
        print("=" * 40)
        print("HỆ THỐNG QUẢN LÝ LỊCH KHÁM - CONSOLE")
        print("=" * 40)
        print("1. Bác sĩ")
        print("2. Bệnh nhân")
        print("3. Lịch hẹn")
        print("4. Bệnh án")
        print("5. Mở Giao diện Đồ họa (GUI)")
        print("0. Thoát")
        print("=" * 40)
        chon = nhap("Mời chọn: ")
        
        if chon == "1":
            menu_bac_si()
        elif chon == "2":
            menu_benh_nhan()
        elif chon == "3":
            menu_lich_hen()
        elif chon == "4":
            menu_benh_an()
        elif chon == "5":
            print("Đang bật giao diện đồ hoạ...")
            gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.py")
            if os.path.exists(gui_path):
                import subprocess
                subprocess.call([sys.executable, gui_path])
            else:
                print("Lỗi: Không tìm thấy gui.py")
            nhap("Nhấn Enter để tiếp tục...")
        elif chon == "0":
            print("Tạm biệt!")
            break

if __name__ == "__main__":
    tao_thu_muc_data()
    # Chạy giao diện đồ họa (GUI)
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.py")
    if os.path.exists(gui_path):
        import subprocess
        subprocess.call(["python", gui_path])
    else:
        print("Lỗi: Không tìm thấy gui.py")
