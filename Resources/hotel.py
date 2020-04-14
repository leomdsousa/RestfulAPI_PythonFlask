from models.hotel import HotelModel
from models.site import SiteModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token
                                , jwt_required
                                , get_raw_jwt)
from Resources.filters import consulta_hotel_com_cidade, consulta_hotel_sem_cidade, normalizePathParams 
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('nota_min', type=float)
path_params.add_argument('nota_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()


    def get(self):
        params = path_params.parse_args()
        params_valids = { valor:params[valor] for valor in params if params[valor] is not None } 
        parameters = normalizePathParams(**params_valids)

        if parameters.get('cidade'):
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta_hotel_com_cidade, tupla)
        else:
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta_hotel_sem_cidade, tupla)

        hoteis = []
        for linha in result:
            hoteis.append({
                'id': linha[0]
                , 'nome': linha[1]
                , 'nota': linha[2]
                , 'diaria': linha[3]
                , 'cidade': linha[4]  
                , 'site_id': linha[5]                
            })

        return { 'hoteis': hoteis }

class Hotel(Resource):

    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True, help='The field nome must be filled')
    argumento.add_argument('nota', type=float, required=True, help='The field nota must be filled')
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')
    argumento.add_argument('site_id', type=int, required=True, help='Missing site id. Every hotel has to be linked to a site')

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

