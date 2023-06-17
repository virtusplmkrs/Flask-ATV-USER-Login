"""
Para realizar o teste de login via postman
barra de endereço: http://http://127.0.0.1:5000/pessoa/
opção Authorization: Basic Auth
na caixa informe: usuario e senha
"""
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios, db_session
"""import para usar a autenticação básica HTTP para proteger a rota '/'"""
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

"""
lista de usuário para autenticação/ ideal usar uma tabela 
de banco de dados - usar somente para teste sem banco
users = {
    "Alex": generate_password_hash("7171"),
    "Yuri": generate_password_hash("8572"),
}

@auth.verify_password
def verify_password(login, senha):
    if login in Usuarios and \
            check_password_hash(Usuarios.get(login), senha):
        return login
"""
@auth.verify_password
def verify_password(login, senha):
    if not (login, senha):
        return False
    
    #if login in Usuarios and \
    #        check_password_hash(Usuarios.get(login), senha):
    return db_session.query(Usuarios).filter_by(login=login, senha=senha).first()
    
"""classe api-restful Pessoa"""
class Pessoa(Resource):
    #esse decorador obriga realizar a autenticação
    @auth.login_required
    #metodo get busca de pessoas por nome
    def get(self, nome):
        """retorna um dicionário"""
        pessoa = db_session.query(Pessoas).filter_by(nome=nome).first()
        try:
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Pessoa nao encontrada',
            }
        return response

    """metodo put alterar de pessoas por nome"""
    def put(self, nome):
        pessoa = db_session.query(Pessoas).filter_by(nome=nome).first()
        dados = request.json
        """ permite alterar o nome"""
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        """ permite alterar a idade"""
        if 'idade' in dados:
            pessoa.idade = dados['idade']
            
        pessoa.save()

        response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade,
            }
        
        print(dados)
        return response

    """metodo delete Excluir de pessoas por nome"""
    def delete(self, nome):
        pessoa = db_session.query(Pessoas).filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida'.format(pessoa.nome)
        pessoa.delete()
        return {'status': 'success', 'message':mensagem}


"""classe api-restful listando pessoas"""
class Lista_Pessoas(Resource):
    #esse decorador obriga realizar a autenticação
    @auth.login_required
    #metodo get lista todas pessoas 
    def get(self):
        """busca todas as pessoas no banco"""
        pessoa = db_session.query(Pessoas).all()
        """retorna em um dicionário com todas as pessoas"""
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoa]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade,
        }
        return response


"""classe api-restful listando pessoas"""
class Lista_Atividades(Resource):
    #esse decorador obriga realizar a autenticação
    @auth.login_required
    #metodo get lista todas atividades das pessoas
    def get(self):
        """busca todas as pessoas no banco"""
        ativividades = db_session.query(Atividades).all()
        """retorna em um dicionário com todas as atividades das pessoas/for in line"""
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoas.nome} for i in ativividades]
        return response

    def post(self):
        dados = request.json
        pessoa = db_session.query(Pessoas).filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoas=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoas.nome,
            'nome': atividade.nome,
            'id': atividade.id,
        }
        return response

        
        

"""rotas pessoa"""
api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(Lista_Pessoas, '/pessoa/')
api.add_resource(Lista_Atividades, '/atividade/')


"""star do app"""
if __name__ == '__main__':
    app.run(debug=True)