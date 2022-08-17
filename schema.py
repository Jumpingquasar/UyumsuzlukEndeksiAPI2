from pydantic import BaseModel

class Item(BaseModel):
    id: int
    osgb_bolge: str
    isim: str
    sertifika: str
    toplam_atama_suresi: int
    ikamet_il: str
    ikamet_ilce: str
    firma_unvan: str
    tehlike_sinifi: str
    lokasyon: str
    ana_isveren: str
    hizmet_tipi: str
    atama_sekli: str
    sgk_no: str
    atama_suresi: str
    sgk_il: int
    sgk_ilce: int
    sgk_il_isim: str

    class Config:
        orm_mode = True
