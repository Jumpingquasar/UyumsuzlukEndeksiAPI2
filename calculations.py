from __future__ import print_function
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

def to_dict(self):
    return {
        'id': self.id,
        'osgb_bolge': self.osgb_bolge,
        "isim": self.isim,
        "sertifika": self.sertifika,
        "toplam_atama_suresi": self.toplam_atama_suresi,
        "ikamet_il": self.ikamet_il,
        "ikamet_ilce": self.ikamet_ilce,
        "firma_unvan": self.firma_unvan,
        "tehlike_sinifi": self.tehlike_sinifi,
        "lokasyon": self.lokasyon,
        "ana_isveren": self.ana_isveren,
        "hizmet_tipi": self.hizmet_tipi,
        "atama_sekli": self.atama_sekli,
        "sgk_no": self.sgk_no,
        "atama_suresi": self.atama_suresi,
        "sgk_il": self.sgk_il,
        "sgk_ilce": self.sgk_ilce,
        "sgk_il_isim": self.sgk_il_isim
    }

def df_creator(json):
    arr = []
    used_arr = []
    for obj in json:
        if str(obj.id)+obj.isim not in used_arr:
            used_arr.append(str(obj.id) + obj.isim)
            arr.append(to_dict(obj))
    df = pd.DataFrame(arr)
    return df

# Yasal çalışma saati sınırı
maksimum_saat = 195

ana_kisi = {
    "gorev_yeri": "",
    "ikamet_yeri": "",
    "seviye": "",
    "isyeri_seviye": "",
    "kisi_saat": "",
    "gorevi": ""
}
diger_kisi = {
    "gorev_yeri": "",
    "ikamet_yeri": "",
    "seviye": "",
    "isyeri_seviye": "",
    "kisi_saat": "",
    "gorevi": ""
}

# İller arası mesafe tablosunu çek
df_distance = pd.read_excel("venv/Lib/Excel/ilmesafe.xlsx")

# Kişi index'ine göre saat puanı hesabı
def saat_hesabi(kisi):
    kisi_saat = kisi["kisi_saat"]
    X = 1 - (kisi_saat / maksimum_saat)
    Y = (1 + X) ** 2
    saat_puan = 250 / Y
    return saat_puan

# Kişi index'ine göre mesafe puanı hesabı
def mesafe_hesabi(kisi):
    ikamet_list = df_distance[kisi["ikamet_yeri"]]
    gorev_yeri = kisi["gorev_yeri"]
    il_list = df_distance["İL_ADI"].tolist()
    gorev_index = il_list.index(gorev_yeri)
    mesafe = ikamet_list[gorev_index]
    if 0 < mesafe <= 100:
        return 200
    elif mesafe >= 100:
        return 100
    else:
        return 250

# Kişi index'ine göre uzmanlık puanı hesabı
def uzmanlik_hesabi(kisi):
    seviye = kisi["seviye"]
    isyeri_seviye = kisi["isyeri_seviye"]
    if type(seviye) != int or type(isyeri_seviye) != int:
        return 500
    fark = seviye - isyeri_seviye
    uzmanlik_puan = 500 - 150 * abs(fark)
    return uzmanlik_puan

# Kişi index'ine göre toplam puan hesabı
def puan_hesabi(kisi):
    saat_puan = saat_hesabi(kisi)
    uzmanlik_puan = uzmanlik_hesabi(kisi)
    mesafe_puan = mesafe_hesabi(kisi)
    return saat_puan + uzmanlik_puan + mesafe_puan

# diger_kisi'ye ana_kisi'nin "gorev_yeri" ve "isyeri_seviye"'sini verirsek çıkan yüzdelik puan hesabı
def puan_karsilastirma(ana_kisi, diger_kisi):
    onceki_puan = puan_hesabi(diger_kisi)
    diger_kisi["gorev_yeri"] = ana_kisi["gorev_yeri"]
    diger_kisi["isyeri_seviye"] = ana_kisi["isyeri_seviye"]
    sonraki_puan = puan_hesabi(diger_kisi)
    return (sonraki_puan-onceki_puan)*100/onceki_puan

def hizmet_tipi_degistirici(hizmet_tipi):
    if hizmet_tipi == "A SINIFI UZMAN":
        return "3"
    if hizmet_tipi == "B SINIFI UZMAN":
        return "2"
    if hizmet_tipi == "C SINIFI UZMAN":
        return "1"
    return hizmet_tipi

def sirket_tipi_degistirici(tehlike_sinifi):
    if tehlike_sinifi == "Çok Tehlikeli":
        return "3"
    if tehlike_sinifi == "Tehlikeli":
        return "2"
    if tehlike_sinifi == "Az Tehlikeli":
        return "1"
    return tehlike_sinifi

# Puan karsilaştırmadan gelen yüzdelik verilerin DataFrame'e aktarımı
def yuzde_DF(p_table):
    counter = 0
    karsilastirma_listoflists = []
    kisi_index = 0
    while kisi_index < len(p_table):
        karsilastirma_list = []
        kisi_index_ = 0
        ana_kisi["ikamet_yeri"] = p_table.iloc[kisi_index]["ikamet_il"]
        ana_kisi["gorev_yeri"] = p_table.iloc[kisi_index]["sgk_il_isim"]
        ana_kisi["seviye"] = hizmet_tipi_degistirici(p_table.iloc[kisi_index]["hizmet_tipi"])
        ana_kisi["isyeri_seviye"] = sirket_tipi_degistirici(p_table.iloc[kisi_index]["tehlike_sinifi"])
        ana_kisi["kisi_saat"] = p_table.iloc[kisi_index]["toplam_atama_suresi"]
        ana_kisi["gorevi"] = p_table.iloc[kisi_index]["hizmet_tipi"]
        kisi_index += 1
        while kisi_index_ < len(p_table):
            diger_kisi["ikamet_yeri"] = p_table.iloc[kisi_index_]["ikamet_il"]
            diger_kisi["gorev_yeri"] = p_table.iloc[kisi_index_]["sgk_il_isim"]
            diger_kisi["seviye"] = hizmet_tipi_degistirici(p_table.iloc[kisi_index_]["hizmet_tipi"])
            diger_kisi["isyeri_seviye"] = sirket_tipi_degistirici(p_table.iloc[kisi_index_]["tehlike_sinifi"])
            diger_kisi["kisi_saat"] = p_table.iloc[kisi_index_]["toplam_atama_suresi"]
            diger_kisi["gorevi"] = p_table.iloc[kisi_index_]["hizmet_tipi"]
            kisi_index_ += 1
            karsilastirma_list.append(puan_karsilastirma(ana_kisi, diger_kisi)-puan_karsilastirma(diger_kisi, ana_kisi))
            counter += 1
            if counter%1000 == 0:
                print("Total Operations =", counter)
        karsilastirma_listoflists.append(karsilastirma_list)
    return pd.DataFrame(karsilastirma_listoflists)

def intermediate_yuzde_DF(main_DF, p_table, index_location):
    counter = 0
    i = 0
    row = index_location[2]
    column = index_location[1]
    while i < len(p_table):
        ana_kisi["ikamet_yeri"] = p_table.iloc[row]["İKAMETİ"]
        ana_kisi["gorev_yeri"] = p_table.iloc[row]["GÖREV YERİ"]
        ana_kisi["seviye"] = p_table.iloc[row]["SEVİYE"]
        ana_kisi["isyeri_seviye"] = p_table.iloc[row]["İŞYERİ"]
        ana_kisi["kisi_saat"] = p_table.iloc[row]["ÇALIŞILAN SAAT"]
        ana_kisi["gorevi"] = p_table.iloc[row]["GÖREVİ"]
        diger_kisi["ikamet_yeri"] = p_table.iloc[i]["İKAMETİ"]
        diger_kisi["gorev_yeri"] = p_table.iloc[i]["GÖREV YERİ"]
        diger_kisi["seviye"] = p_table.iloc[i]["SEVİYE"]
        diger_kisi["isyeri_seviye"] = p_table.iloc[i]["İŞYERİ"]
        diger_kisi["kisi_saat"] = p_table.iloc[i]["ÇALIŞILAN SAAT"]
        diger_kisi["gorevi"] = p_table.iloc[i]["GÖREVİ"]
        main_DF.iloc[row][i] = puan_karsilastirma(ana_kisi, diger_kisi)-puan_karsilastirma(diger_kisi, ana_kisi)
        i += 1
        counter += 1
        if counter % 1000 == 0:
            print("Total Operations =", counter)
    j = 0
    while j < len(p_table):
        ana_kisi["ikamet_yeri"] = p_table.iloc[j]["İKAMETİ"]
        ana_kisi["gorev_yeri"] = p_table.iloc[j]["GÖREV YERİ"]
        ana_kisi["seviye"] = p_table.iloc[j]["SEVİYE"]
        ana_kisi["isyeri_seviye"] = p_table.iloc[j]["İŞYERİ"]
        ana_kisi["kisi_saat"] = p_table.iloc[j]["ÇALIŞILAN SAAT"]
        ana_kisi["gorevi"] = p_table.iloc[j]["GÖREVİ"]
        diger_kisi["ikamet_yeri"] = p_table.iloc[column]["İKAMETİ"]
        diger_kisi["gorev_yeri"] = p_table.iloc[column]["GÖREV YERİ"]
        diger_kisi["seviye"] = p_table.iloc[column]["SEVİYE"]
        diger_kisi["isyeri_seviye"] = p_table.iloc[column]["İŞYERİ"]
        diger_kisi["kisi_saat"] = p_table.iloc[column]["ÇALIŞILAN SAAT"]
        diger_kisi["gorevi"] = p_table.iloc[column]["GÖREVİ"]
        main_DF.iloc[j][column] = puan_karsilastirma(ana_kisi, diger_kisi)
        j += 1
        counter += 1
        if counter % 1000 == 0:
            print("Total Operations =", counter)
    return main_DF

def matrix_summation(matrix):
    return matrix.values.sum()/len(matrix)**2

def average_puan(p_table):
    kisi_index = 0
    all_points = []
    while kisi_index < len(p_table):
        ana_kisi["ikamet_yeri"] = p_table.iloc[kisi_index]["ikamet_il"]
        ana_kisi["gorev_yeri"] = p_table.iloc[kisi_index]["sgk_il_isim"]
        ana_kisi["seviye"] = hizmet_tipi_degistirici(p_table.iloc[kisi_index]["hizmet_tipi"])
        ana_kisi["isyeri_seviye"] = sirket_tipi_degistirici(p_table.iloc[kisi_index]["tehlike_sinifi"])
        ana_kisi["kisi_saat"] = p_table.iloc[kisi_index]["toplam_atama_suresi"]
        ana_kisi["gorevi"] = p_table.iloc[kisi_index]["hizmet_tipi"]
        kisi_index += 1
        all_points.append(puan_hesabi(ana_kisi))
    return sum(all_points)/len(all_points)

def switcher(uzmanDF, uzman_ids_list):
    indexes = []
    for switch_id in uzman_ids_list:
        i=0
        while i < len(uzmanDF):
            if uzmanDF.iloc[i]["id"] == int(switch_id):
                indexes.append(i)
            i+=1
    gy_cache = uzmanDF.loc[indexes[0], "sgk_il_isim"]
    s_cache = uzmanDF.loc[indexes[0], "tehlike_sinifi"]
    uzmanDF.loc[indexes[0], "sgk_il_isim"] = uzmanDF.loc[indexes[1], "sgk_il_isim"]
    uzmanDF.loc[indexes[0], "tehlike_sinifi"] = uzmanDF.loc[indexes[1], "tehlike_sinifi"]
    uzmanDF.loc[indexes[1], "sgk_il_isim"] = gy_cache
    uzmanDF.loc[indexes[1], "tehlike_sinifi"] = s_cache
    return uzmanDF
