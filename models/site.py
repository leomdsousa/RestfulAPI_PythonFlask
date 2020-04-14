from sql_alchemy import banco 
from models.hotel import HotelModel

class SiteModel(banco.Model):
    __tablename__ = 'TB_SITES'

    id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(50))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url):
        self.url = url

    def convertToDictionary(self):
        return {
            'id': self.id
            , 'nota': self.url
            , 'hoteis': [ hotel.convertToDictionary() for hotel in self.hoteis ]
        }

    @classmethod
    def find_all(cls):
        sites = cls.query.all()
        if sites:
            return sites
        return None

    @classmethod
    def find_by_id(cls, id):
        site = cls.query.filter_by(id=id).first()
        if site:
            return site
        return None

    @classmethod
    def find_by_url(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hoteis()]

        banco.session.delete(self)
        banco.session.commit()

    def update_site(self, url):
        self.url = url