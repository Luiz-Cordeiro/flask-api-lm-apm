import hmac
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST


# reqparse permite receber e tratar as requisições encaminhadas ao backend

atributos = reqparse.RequestParser()
atributos.add_argument('login',type=str,required=True,help="The field 'login' cannot be left blank")
atributos.add_argument('senha',type=str,required=True,help="The field 'senha' cannot be left blank")

class User(Resource):
    
    def get(self, user_id):
        dados = atributos.parse_args()
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message':'User not found'}, 404  # Forma de declarar o código HTTP a ser retornado  

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user'}, 500
            return {'message':'User deleted'}, 200       
        return {'message':'User not found'}, 404   
    
class UserRegister(Resource):
    
    def post(self):
        dados = atributos.parse_args()
        print(dados['login'])

        if UserModel.find_by_login(dados['login']):
            return {'message':"The login '{}' already exists.".format(dados['login'])}
        
        user = UserModel(**dados)
        user.save_user()

        return {'message':"User created successfully!"}, 201
    
class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        # safe_str_cmp é um modo seguro de comparar strings, como senhas.
        #if user and safe_str_cmp(user.senha, dados['senha']):
        if user and hmac.compare_digest(str(user.senha).encode("utf-8"),str(dados['senha']).encode("utf-8")):
            #token_de_acesso = create_access_token(identity=user.user_id)
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token':token_de_acesso}, 200
        
        return {'message':'The username or password is incorrect'}, 401
    
class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # Captura o ID do JWT - JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
    

        
