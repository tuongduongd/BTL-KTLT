class Node:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.tiep = None
class DanhSachLienKet:
    def __init__(self):
        self.dau = None
        self.kich_thuoc = 0

    def them_cuoi(self, du_lieu):
        node_moi = Node(du_lieu)
        if self.dau is None:
            self.dau = node_moi
        else:
            hien_tai = self.dau
            while hien_tai.tiep is not None:
                hien_tai = hien_tai.tiep
            hien_tai.tiep = node_moi
        self.kich_thuoc += 1

    def lay(self, vi_tri):
        if vi_tri < 0 or vi_tri >= self.kich_thuoc:
            return None
        hien_tai = self.dau
        dem = 0
        while dem < vi_tri:
            hien_tai = hien_tai.tiep
            dem += 1
        return hien_tai.du_lieu

    def do_dai(self):
        return self.kich_thuoc

    def tim_kiem(self, dieu_kien):
        hien_tai = self.dau
        while hien_tai is not None:
            if dieu_kien(hien_tai.du_lieu):
                return hien_tai.du_lieu
            hien_tai = hien_tai.tiep
        return None

    def tim_kiem_tat_ca(self, dieu_kien):
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau
        while hien_tai is not None:
            if dieu_kien(hien_tai.du_lieu):
                ket_qua.them_cuoi(hien_tai.du_lieu)
            hien_tai = hien_tai.tiep
        return ket_qua

    def dem(self, dieu_kien):
        so_luong = 0
        hien_tai = self.dau
        while hien_tai is not None:
            if dieu_kien(hien_tai.du_lieu):
                so_luong += 1
            hien_tai = hien_tai.tiep
        return so_luong

    def duyet(self):
        hien_tai = self.dau
        while hien_tai is not None:
            yield hien_tai.du_lieu
            hien_tai = hien_tai.tiep

    def xoa_theo_dieu_kien(self, dieu_kien):
        if self.dau is None:
            return False
            
        if dieu_kien(self.dau.du_lieu):
            self.dau = self.dau.tiep
            self.kich_thuoc -= 1
            return True
            
        hien_tai = self.dau
        while hien_tai.tiep is not None:
            if dieu_kien(hien_tai.tiep.du_lieu):
                hien_tai.tiep = hien_tai.tiep.tiep
                self.kich_thuoc -= 1
                return True
            hien_tai = hien_tai.tiep
        return False
        
    def cap_nhat_theo_dieu_kien(self, dieu_kien, du_lieu_moi):
        hien_tai = self.dau
        while hien_tai is not None:
            if dieu_kien(hien_tai.du_lieu):
                hien_tai.du_lieu = du_lieu_moi
                return True
            hien_tai = hien_tai.tiep
        return False

    def sap_xep(self, ham_so_sanh):
        if self.kich_thuoc <= 1:
            return
        da_doi_cho = True
        while da_doi_cho:
            da_doi_cho = False
            hien_tai = self.dau
            while hien_tai.tiep is not None:
                if ham_so_sanh(hien_tai.du_lieu, hien_tai.tiep.du_lieu):
                    # Đổi chỗ dữ liệu
                    tam = hien_tai.du_lieu
                    hien_tai.du_lieu = hien_tai.tiep.du_lieu
                    hien_tai.tiep.du_lieu = tam
                    da_doi_cho = True
                hien_tai = hien_tai.tiep

# CÁC HÀM TIỆN ÍCH

def chia_chuoi(chuoi_goc, ky_tu_phan_cach):

    ket_qua = DanhSachLienKet()
    tu_hien_tai = ""
    i = 0
    chieu_dai = 0

    for c in chuoi_goc:
        chieu_dai += 1
        
    while i < chieu_dai:
        ky_tu = chuoi_goc[i]
        if ky_tu == ky_tu_phan_cach:
            ket_qua.them_cuoi(tu_hien_tai)
            tu_hien_tai = ""
        else:
            tu_hien_tai += ky_tu
        i += 1

    ket_qua.them_cuoi(tu_hien_tai)
    return ket_qua

def loai_bo_khoang_trang(chuoi_goc):

    if chuoi_goc == "":
        return ""
    
    bat_dau = 0
    chieu_dai = 0
    for c in chuoi_goc:
        chieu_dai += 1
        
    while bat_dau < chieu_dai and (chuoi_goc[bat_dau] == " " or chuoi_goc[bat_dau] == "\n" or chuoi_goc[bat_dau] == "\t" or chuoi_goc[bat_dau] == "\r"):
        bat_dau += 1
        
    ket_thuc = chieu_dai - 1
    while ket_thuc >= 0 and (chuoi_goc[ket_thuc] == " " or chuoi_goc[ket_thuc] == "\n" or chuoi_goc[ket_thuc] == "\t" or chuoi_goc[ket_thuc] == "\r"):
        ket_thuc -= 1
        
    if bat_dau > ket_thuc:
        return ""
        
    ket_qua = ""
    i = bat_dau
    while i <= ket_thuc:
        ket_qua += chuoi_goc[i]
        i += 1
    return ket_qua

def chuoi_sang_so(chuoi):

    so_nguyen = 0
    i = 0
    chieu_dai = 0
    for c in chuoi:
        chieu_dai += 1
    
    while i < chieu_dai:
        ky_tu = chuoi[i]
        # Lấy giá trị mã ascii (ord) trừ đi ascii của '0'
        if '0' <= ky_tu <= '9':
            gia_tri = ord(ky_tu) - ord('0')
            so_nguyen = so_nguyen * 10 + gia_tri
        i += 1
    return so_nguyen

def chuoi_co_so(chuoi):
    for ky_tu in chuoi:
        if not ('0' <= ky_tu <= '9'):
            return False
    return True if chuoi != "" else False

def so_ngay_trong_thang(thang):
    if thang == 2:
        return 29
    if thang == 4 or thang == 6 or thang == 9 or thang == 11:
        return 30
    return 31

def kiem_tra_dinh_dang_ngay(chuoi_ngay):

    chieu_dai = 0
    for c in chuoi_ngay:
        chieu_dai += 1
        
    if chieu_dai != 10:
        return False

    if chuoi_ngay[4] != '-' or chuoi_ngay[7] != '-':
        return False
        
    chuoi_nam = chuoi_ngay[0] + chuoi_ngay[1] + chuoi_ngay[2] + chuoi_ngay[3]
    chuoi_thang = chuoi_ngay[5] + chuoi_ngay[6]
    chuoi_ngay_le = chuoi_ngay[8] + chuoi_ngay[9]
    
    if not (chuoi_co_so(chuoi_nam) and chuoi_co_so(chuoi_thang) and chuoi_co_so(chuoi_ngay_le)):
        return False
        
    nam = chuoi_sang_so(chuoi_nam)
    thang = chuoi_sang_so(chuoi_thang)
    ngay = chuoi_sang_so(chuoi_ngay_le)
    
    if nam < 1900 or nam > 2100:
        return False
    if thang < 1 or thang > 12:
        return False
    if ngay < 1 or ngay > so_ngay_trong_thang(thang):
        return False
        
    return True

def kiem_tra_dinh_dang_gio(chuoi_gio):
    chieu_dai = 0
    for c in chuoi_gio:
        chieu_dai += 1
        
    if chieu_dai != 5:
        return False
        
    if chuoi_gio[2] != ':':
        return False
        
    chuoi_h = chuoi_gio[0] + chuoi_gio[1]
    chuoi_m = chuoi_gio[3] + chuoi_gio[4]
    
    if not (chuoi_co_so(chuoi_h) and chuoi_co_so(chuoi_m)):
        return False
        
    h = chuoi_sang_so(chuoi_h)
    m = chuoi_sang_so(chuoi_m)
    
    if h < 0 or h > 23:
        return False
    if m < 0 or m > 59:
        return False
        
    return True

def kiem_tra_sdt(chuoi_sdt):
    if not chuoi_co_so(chuoi_sdt):
        return False
    chieu_dai = 0
    for c in chuoi_sdt:
        chieu_dai += 1
    if chieu_dai < 9 or chieu_dai > 11:
        return False
    return True

def chuan_hoa_ten(chuoi):

    ket_qua = ""
    chieu_dai = 0
    for c in chuoi:
        chieu_dai += 1
        
    dau_tu = True
    i = 0
    while i < chieu_dai:
        ky_tu = chuoi[i]

        if ky_tu == ' ':
            ket_qua += ky_tu
            dau_tu = True
            i += 1
            continue
            
        ma_ascii = ord(ky_tu)
        
        if dau_tu:
            if 97 <= ma_ascii <= 122:
                ket_qua += chr(ma_ascii - 32)
            else:
                ket_qua += ky_tu
            dau_tu = False
        else:
            # Nếu là chữ in hoa (A-Z: 65-90), chuyển thành chữ thường (+32)
            if 65 <= ma_ascii <= 90:
                ket_qua += chr(ma_ascii + 32)
            else:
                ket_qua += ky_tu
                
        i += 1
        
    return ket_qua