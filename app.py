from flask import Flask, jsonify
from flask_restful import Api
from Resources.hotel import Hoteis, Hotel
from Resources.usuario import Usuario, UsuarioRegister, UsuarioLogin, UsuarioLogout
from flask_jwt_extended import JWTManager
from BLACKLIST import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_SECRET_KEY'] = 'IDontKnow'
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:id>')
api.add_resource(Usuario, '/usuarios/<int:id>')
api.add_resource(UsuarioRegister, '/register')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalido():
    return jsonify({'message': 'You have been logged out with success'}), 401

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)