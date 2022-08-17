from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class uzman_list(Base):
    __tablename__ = 'uzman_list'
    id = Column(Integer, primary_key=True, index=True)
    osgb_bolge = Column(String)
    isim = Column(String)
    sertifika = Column(String)
    toplam_atama_suresi = Column(Integer)
    ikamet_il = Column(String)
    ikamet_ilce = Column(String)
    firma_unvan = Column(String)
    tehlike_sinifi = Column(String)
    lokasyon = Column(String)
    ana_isveren = Column(String)
    hizmet_tipi = Column(String)
    atama_sekli = Column(String)
    sgk_no = Column(String)
    atama_suresi = Column(String)
    sgk_il = Column(Integer)
    sgk_ilce = Column(Integer)
    sgk_il_isim = Column(String)