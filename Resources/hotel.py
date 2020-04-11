from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return { 'hoteis': [hotel.convertToDictionary() for hotel in HotelModel.find_all() ] }

class Hotel(Resource):

    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True, help='The field nome must be filled')
    argumento.add_argument('nota', type=float, required=True, help='The field nota must be filled')
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')

    def get(self, id):
        hotel = HotelModel.find_by_id(id)
        
        if hotel:
            return hotel.convertToDictionary()
        return {'Message': 'Hotel not found'}, 404

    @jwt_required
    def post(self, id):
        hotel = HotelModel.find_by_id(id)
        if hotel:
            return {'Message': 'Hotel already exists'}, 400

        dados = Hotel.argumento.parse_args()
        hotel = HotelModel(id, **dados)
        
        try:
            hotel.save_hotel()
            return hotel.convertToDictionary(), 201
        except:
            return {'Message': 'An internal error ocurred while attempting to save the data'}, 500
        
    @jwt_required
    def put(self, id):
        dados = Hotel.argumento.parse_args()
        
        hotel_encontrado = HotelModel.find_by_id(id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'Message': 'An internal error ocurred while attempting to save the data'}, 500

            return hotel_encontrado.convertToDictionary(), 200

        return {'Message': 'Hotel not found'}, 404

    @jwt_required
    def delete(self, id):
        hotel = HotelModel.find_by_id(id)
        
        if hotel:
            try:
                hotel.save_hotel()
                return { 'hoteis': [hotel.convertToDictionary() for hotel in HotelModel.find_all() ] }
            except:
                return {'Message': 'An internal error ocurred while attempting to save the data'}, 500                

        return {'Message': 'Hotel not found'}, 404        

