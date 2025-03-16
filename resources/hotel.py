from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from flask_jwt_extended import jwt_required # Permite definir as operações que requerem login
import sqlite3




# Definição dos argumentos na URL
# reqparse permite receber e tratar as requisições encaminhadas ao backend
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float) # Número de itens na consulta
path_params.add_argument('offset', type=float) # Salto de itens

class Hoteis(Resource):

    def get(self):
        connection = sqlite3.connect('./instance/banco_app.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        
        # Extração de dados válidos
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        # Usar o "get" oferece uma forma de consulta que, mesmo na ausência da chave, retorna o valor null nas atribuições. Usar a consulta direta dicionario[chave] pode resultar em erro
        if not parametros.get('cidade'):
            # Obtenção da tupla com os valores do dicionário usando compreensão de listas na extração
            tupla = tuple(parametros[chave] for chave in parametros)
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple(parametros[chave] for chave in parametros)
            resultado = cursor.execute(consulta_com_cidade, tupla)
            #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
        
        hoteis=[]

        # Formatação do retorno em json para o resultado do banco
        # A extração respeita a ordem das colunas do banco
        for linha in resultado:
            hoteis.append({
                'hotel_id':linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'hotel_id': linha[5]
            })
        
        return {'hoteis':hoteis}
        
        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
   
    argumentos = reqparse.RequestParser() # Instancia um RequestParser
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be blank") # Define os atributos que serão aceitos no corpo da requisição
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be blank")
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")

    # def find_hotel(hotel_id):
    #     for hotel in hoteis:
    #         if(hotel['hotel_id'] == hotel_id):
    #             return hotel
    #     return None
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message':'Hotel not found'}, 404  # Forma de declarar o código HTTP a ser retornado

    @jwt_required() # Indica a necessidade de um token de acesso para realizar a operação
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args() # Consolida as informações recebidas no formato chave-valor 
        hotel = HotelModel(hotel_id, **dados) # Permite referenciar os pares chave-valor do dicionário "dados" (**kwargs)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 201

    @jwt_required()    
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args() # Consolida as informações recebidas no formato chave-valor
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel() # Aparentemente o SQLAlchemy atualiza o DB com base no objeto alterado
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados) # Permite referenciar os pares chave-valor do dicionário "dados" (**kwargs)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 201
        
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel'}, 500
            return {'message':'Hotel deleted'}, 200       
        return {'message':'Hotel not found'}, 404   
    


    

        
