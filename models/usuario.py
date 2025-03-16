from sql_alchemy import banco

# A herança do banco.Model permite o mapeamento dos atributos da classe como uma tabela SQL
class UserModel(banco.Model):
    __tablename__ = 'usuarios' # Indica ao SQL Alchemy que o nome da tabela

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    
    def __init__(self, login, senha) -> None:
        # Considerando que não há menção a chave primária (user_id), o SQL Alchemy assume o papel de 
        # atribuir os ids de forma incremental
        self.login = login
        self.senha = senha
    
    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login
        }
    
    # Não há necessidade de fazer referências ao objeto da classe, mas a métodos da classe pai, por isso o uso do classmethod
    @classmethod
    def find_user(cls, user_id):
        # O método "query" pertence a classe banco.Model. Por essa razão é necessário o classmethod
        # A instrução abaixo retorna o primeiro registro de acordo com a condição
        user = cls.query.filter_by(user_id=user_id).first() # SELECT * FROM usuarios WHERE user_id == <user_id> limit 1
        
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        # O método "query" pertence a classe banco.Model. Por essa razão é necessário o classmethod
        # A instrução abaixo retorna o primeiro registro de acordo com a condição
        user = cls.query.filter_by(login=login).first() # SELECT * FROM usuarios WHERE user_id == <user_id> limit 1
        
        if user:
            return user
        return None
    
    def save_user(self):
        # Salva o objeto criado no banco de dados
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

    


    
