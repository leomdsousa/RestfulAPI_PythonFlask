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
        return { 'hoteis': [hotel.convertToDictionary() for hotel in HotelModel.findAll_hotel() ] }

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
        hotel = HotelModel.find_hotelById(id)
        
        if hotel:
            return hotel.convertToDictionary()
        return {'Erro': 'Hotel não encontrado'}, 404

    def post(self, id):
        hotel = HotelModel.find_hotelById(id)
        if hotel:
            return {'Erro': 'Hotel já existente'}, 400

        dados = Hotel.argumento.parse_args()
        hotel = HotelModel(id, **dados)
        hotel.save_hotel()
        return hotel.convertToDictionary(), 201

    def put(self, id):
        hotel = HotelModel.find_hotelById(id)

        if hotel:
            dados = Hotel.argumento.parse_args()
            hotel_model = HotelModel(id, **dados)
            hotel_model.update_hotel()
            return hotel_model.convertToDictionary(), 200

        return {'Erro': 'Hotel não encontrado'}, 404

    def delete(self, id):
        hotel = HotelModel.find_hotelById(id)
        
        if hotel:
            hotel.delete_hotel()
            return { 'hoteis': [hotel.convertToDictionary() for hotel in HotelModel.findAll_hotel() ] }

        return {'Erro': 'Hotel não encontrado'}, 404        

