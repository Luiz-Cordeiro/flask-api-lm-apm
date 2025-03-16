# Função responsável por definir os parâmetros de acordo com o payload recebido. São definidos os valores padrão caso não seja especificado na requisição
# NOTA IMPORTANTE: Essa função usa o comportamento da associação entre os argumentos com valores pré-definidos e o kwargs recebido
# Dessa forma, é atribuído o valor da chave do kwargs ao parâmetro correspondente. 
# Exemplo: Se dados[cidade] = "São Paulo", então cidade deixa de ser None e assume o valor "São Paulo"
def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrela_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset,
        }
    
    return {
        'estrelas_min': estrelas_min,
        'estrela_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset,
    }

consulta_sem_cidade = "SELECT * FROM hoteis \
                WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM hoteis \
                WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                and cidade = ? LIMIT ? OFFSET ?"