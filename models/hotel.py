from sql_alchemy import banco


# A herança do banco.Model permite o mapeamento dos atributos da classe como uma tabela SQL
class HotelModel(banco.Model):
    __tablename__ = 'hoteis' # Indica ao SQL Alchemy que o nome da tabela

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    # Chave estrangeira que permite relacionar os sites com os hotéis
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))
    #site = banco.relationship('SiteModel') # Indica a relação entre as tabelas site e hoteis
    


    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id) -> None:
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id
    
    def json(self):
        return{
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }
    

    # Não há necessidade de fazer referências ao objeto da classe, mas a métodos da classe pai, por isso o uso do classmethod
    @classmethod
    def find_hotel(cls, hotel_id):
        # O método "query" pertence a classe banco.Model. Por essa razão é necessário o classmethod
        # A instrução abaixo retorna o primeiro registro de acordo com a condição
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # SELECT * FROM hoteis WHERE hotel_id == <hotel_id> limit 1
        
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        # Salva o objeto criado no banco de dados
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, **dados):
        self.nome = dados['nome']
        self.estrelas = dados['estrelas']
        self.diaria = dados['diaria']
        self.cidade = dados['cidade']

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()


    
