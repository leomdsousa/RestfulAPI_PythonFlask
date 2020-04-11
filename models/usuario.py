from sql_alchemy import banco 

class UsuarioModel(banco.Model):
    __tablename__ = 'TB_USUARIO'

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(50))
    usuario = banco.Column(banco.String(20))
    senha = banco.Column(banco.String(50))
    email = banco.Column(banco.String(40))

    def __init__(self, nome, usuario, senha, email):
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
        self.email = email

    def convertToDictionary(self):
        return {
            'id': self.id
            , 'nome': self.nome
            , 'usuario': self.usuario
            , 'email': self.email
        }

    @classmethod
    def find_by_id(cls, id):
        usuario = cls.query.filter_by(id=id).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_by_usuario(cls, usuario):
        usuario = cls.query.filter_by(usuario=usuario).first()
        if usuario:
            return usuario
        return None

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
