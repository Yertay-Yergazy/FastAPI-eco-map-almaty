from sqlalchemy import Column, Integer, String, Numeric
from app.db import Base

class Lake(Base):
    __tablename__ = "lakes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    
    # Параметры для формулы озера
    Z = Column(Integer)         # Географическая зона
    H = Column(Integer)         # Высота над уровнем моря
    G = Column(Integer)         # Генезис котловин
    A = Column(Integer)         # Площадь
    D = Column(Integer)         # Глубина
    W = Column(Integer)         # Водный баланс
    T = Column(Integer)         # Температурный режим
    Tw = Column(Integer)        # Прозрачность
    pH = Column(Integer)        # Водородный показатель
    O = Column(Integer)         # Кислородный режим
    I = Column(String)          # Ионный состав (можно хранить как "2(3)")
    M = Column(Integer)         # Минерализация
    Thw = Column(Integer)       # Общая жесткость воды
    Ka = Column(Integer)        # Коэффициент Х.Стеблера
    SAR = Column(Integer)       # Натриевое абсорбционное отношение
    IIWP_Dc = Column(Integer)   # КИЗВ (оценочные показатели загрязнения)
    Tr = Column(Integer)        # Трофический статус
    Fl = Column(Integer)        # Флора
    Fa = Column(Integer)        # Фауна

    # Для удобства можно добавить метод генерации формулы
    def formula(self):
        return f"Z{self.Z} H{self.H} G{self.G} A{self.A} D{self.D} W{self.W} T{self.T} Tw{self.Tw} pH{self.pH} O{self.O} I{self.I} M{self.M} Thw{self.Thw} Ka{self.Ka} SAR{self.SAR} IIWP Dc{self.IIWP_Dc} Tr{self.Tr} Fl{self.Fl} Fa{self.Fa}"
