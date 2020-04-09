from flask_restful import Resource, reqparse
from models.HotelModel import HotelModel

hoteis = [
    {
    'id': '1',
    'nome': 'Alpha Hotel',
    'nota': 3,
    'diaria': 250.00,
    'cidade': 'Santa Catarina',
    },
    {
    'id': '2',
    'nome': 'Beta Hotel',
    'nota': 2,
    'diaria': 80.00,
    'cidade': 'Santa Catarina',
    },
    {
    'id': '3',
    'nome': 'Zeta Hotel',
    'nota': 4,
    'diaria': 350.00,
    'cidade': 'Santa Catarina',
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):

    @staticmethod
    def find_hotel(id):
        for hotel in hoteis:
            if hotel['id'] == id:
                return hotel
        return None

    argumento = reqparse.RequestParser()
    argumento.add_argument('nome')
    argumento.add_argument('nota')
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')

    def get(self, id):
        hotel = Hotel.find_hotel(id)

        if hotel:
            return hotel
        return {'Erro': 'Hotel não encontrado'}, 404

    def post(self, id):
        dados = Hotel.argumento.parse_args()
        hotel_modelo = HotelModel(id, **dados)
        novo_hotel = hotel_modelo.convertToDictionary()
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def put(self, id):
        dados = Hotel.argumento.parse_args()
        hotel_modelo = HotelModel(id, **dados)
        hotel_atualizado = hotel_modelo.convertToDictionary()
        hotel = Hotel.find_hotel(id)
        if hotel:
            hotel.update(hotel_atualizado)
            return hotel, 200
        return {'Erro': 'Erro'}, 404  
        return hoteis, 200

    def delete(self, id):
        hotel = Hotel.find_hotel(id)
        
        if hotel:
            indice = 0
            for hotel in hoteis:
                if hotel['id'] == id:
                    hoteis.pop(indice)
                    return hoteis, 200    
                indice += 1

        return {'Erro': 'Hotel não encontrado'}, 404        

