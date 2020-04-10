from sql_alchemy import banco 

class HotelModel(banco.Model):
    __tablaname__ = 'TB_HOTEL'

    id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    nota = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, id, nome, nota, diaria, cidade):
        self.id = id
        self.nome = nome
        self.nota = nota
        self.diaria = diaria
        self.cidade = cidade

    def convertToDictionary(self):
        return {
            'id': self.id
            , 'nome': self.nome
            , 'nota': self.nota
            , 'diaria': self.diaria
            , 'cidade': self.cidade
        }

    @classmethod
    def findAll_hotel(cls):
        hoteis = cls.query.all()
        if hoteis:
            return hoteis
        return None

    @classmethod
    def find_hotelById(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

    def update_hotel(self):
        banco.session.update(self)
        banco.session.commit()
