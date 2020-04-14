from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import (create_access_token
                                , jwt_required
                                , get_raw_jwt)
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

class Usuario(Resource):

    def get(self, id):
        usuario = UsuarioModel.find_by_id(id)
        
        if usuario:
            return usuario.convertToDictionary()
        return {'Message': 'Usuario not found'}, 404

    @jwt_required
    def post(self, id):
        usuario = UsuarioModel.find_by_id(id)
        if usuario:
            return {'Message': 'Usuario already exists'}, 400

        dados = Usuario.argumento.parse_args()
        usuario = UsuarioModel(id, **dados)
        
        try:
            usuario.save_hotel()
            return usuario.convertToDictionary(), 201
        except:
            return {'Message': 'An internal error ocurred while attempting to save the data'}, 500

    @jwt_required 
    def delete(self, id):
        usuario = UsuarioModel.find_by_id(id)
        
        if usuario:
            try:
                usuario.save_hotel()
                return { 'hoteis': [hotel.convertToDictionary() for hotel in UsuarioModel.findAll_hotel() ] }
            except:
                return {'Message': 'An internal error ocurred while attempting to save the data'}, 500                

        return {'Message': 'Hotel not found'}, 404        

class UsuarioRegister(Resource):

    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('nome', type=str, required=True, help='The field nome must be filled')
        atributos.add_argument('usuario', type=str, required=True, help='The field usuario must be filled')
        atributos.add_argument('senha', type=str, required=True, help='The field senha must be filled')
        atributos.add_argument('email', type=str, required=True, help='The field email must be filled')
        dados = atributos.parse_args()

        if UsuarioModel.find_by_usuario(dados['usuario']):
            return {'Message': 'Usuario already exists'}, 500

        usuario = UsuarioModel(**dados)
        usuario.save_usuario()
        return {'Message': 'Usuario created with success'}, 201

class UsuarioLogin(Resource):

    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('usuario', type=str, required=True, help='The field usuario must be filled')
        atributos.add_argument('senha', type=str, required=True, help='The field senha must be filled')
        dados = atributos.parse_args()

        usuario = UsuarioModel.find_by_usuario(dados['usuario'])

        if usuario and safe_str_cmp(dados['senha'], usuario.senha):
            token_acesso = create_access_token(identity=usuario.id)
            return {'token': token_acesso}, 200
        return {'mensagem': 'Either the username or password are incorrect.'}, 401             
        
        return {'Message': 'Usuario not found'}, 404

class UsuarioLogout(Resource):

    @jwt_required
    def post(self):
        jti_id = get_raw_jwt()['jti']
        BLACKLIST.add(jti_id)
        return {'message': 'Logged out with success'}, 200