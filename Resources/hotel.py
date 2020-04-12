from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalizePathParams(cidade=None
                        , nota_min=0
                        , nota_max=5
                        , diaria_min=0
                        , diaria_max=10000
                        , limit=50
                        , offset = 0
                        , **dados):
    if cidade:
        return {
            "cidade": cidade
            , "nota_min": nota_min
            , "nota_max": nota_max
            , "diaria_min": diaria_min
            , "diaria_max": diaria_max
            , "limit": limit
            , "offset": offset
        }
    return {
        "nota_min": nota_min
        , "nota_max": nota_max
        , "diaria_min": diaria_min
        , "diaria_max": diaria_max
        , "limit": limit
        , "offset": offset
    }


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
            consulta = "SELECT * FROM TB_HOTEIS \
                        WHERE CIDADE = ? \
                        AND NOTA >= ? AND NOTA <= ? \
                        AND DIARIA >= ? AND DIARIA <= ? \
                        AND LIMIT > ? \
                        AND OFFSET < ?"
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM TB_HOTEIS \
                        WHERE AND NOTA >= ? AND NOTA <= ? \
                        AND DIARIA >= ? AND DIARIA <= ? \
                        AND LIMIT > ? \
                        AND OFFSET < ?"
            tupla = tuple({parameters[chave] for chave in parameters})
            result = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in result:
            hoteis.append({
                'id': linha[0]
                , 'nome': linha[1]
                , 'nota': linha[2]
                , 'diaria': linha[3]
                , 'cidade': linha[4]                
            })

        return { 'hoteis': hoteis }

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

