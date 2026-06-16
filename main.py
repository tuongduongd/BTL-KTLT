from cau_truc_du_lieu import (
    DanhSachLienKet, chia_chuoi, loai_bo_khoang_trang,
    chuoi_sang_so, chuoi_co_so
)class BacSi:
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
