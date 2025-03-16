from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco_app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False # Evita a emissão de alertas do Flask Alchemy
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone' # String para criptografia do JWT
app.config['JWT_BLACKLIST_ENABLED'] = True # Ativa o recurso de blacklist
api = Api(app)
# JWT gerencia a autenticação da aplicação
jwt = JWTManager(app)

# @app.before_first_request # Decorador que permite uma ação antes da primeira requisição -- DECORADOR DESATUALIZADO
@app.before_request # Permite 
# A função cria um novo banco caso ainda não exista no início da aplicação
def criar_banco():
    app.before_request_funcs[None].remove(criar_banco)
    banco.create_all() # Cria automaticamente o banco e tabelas conforme as definições

# Valida se o token está presente na BLACKLIST
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

# Trata os casos de tokens inválido por encerramento da sessão do usuário
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message':'You have been logged out'}), 401


## Permite definir os endpoints
#api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') # Define a rota com o tipo de dado a ser recebido via URL
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(Sites,'/sites')


if __name__ == '__main__':
    # A importação foi declarada aqui garantir que o banco só seja importado apenas quando o arquivo principal for executado
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

