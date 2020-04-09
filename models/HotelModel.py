class HotelModel():
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
