from sql_alchemy import banco


# A herança do banco.Model permite o mapeamento dos atributos da classe como uma tabela SQL
class SiteModel(banco.Model):
    __tablename__ = 'sites' # Indica ao SQL Alchemy que o nome da tabela

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    # Define o relacionamento entre tabelas do banco
    # Considerando que a entidade hotel possui uma chave estrangeira de site (site_id), o sql_alchemy assume a cardinalidade de vários hoteis para um site
    hoteis = banco.relationship('HotelModel') # Retorna uma lista de hoteis
    


    def __init__(self, url) -> None:
        self.url = url
    
    def json(self):
        return{
            'site_id': self.site_id,
            'url': self.url,
            'hoteis':[hotel.json() for hotel in self.hoteis]
        }
    

    # Não há necessidade de fazer referências ao objeto da classe, mas a métodos da classe pai, por isso o uso do classmethod
    @classmethod
    def find_site(cls, url):
        # O método "query" pertence a classe banco.Model. Por essa razão é necessário o classmethod
        # A instrução abaixo retorna o primeiro registro de acordo com a condição
        site = cls.query.filter_by(url=url).first() # SELECT * FROM hoteis WHERE hotel_id == <hotel_id> limit 1
        
        if site:
            return site
        return None
    
    def save_site(self):
        # Salva o objeto criado no banco de dados
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()


    
