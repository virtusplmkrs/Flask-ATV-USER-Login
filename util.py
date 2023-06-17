"""importando os models.py"""
from models import Pessoas, Usuarios, db_session

"""função para incluir pessoas"""
def insere_pessoas():
    pessoa = Pessoas(nome='Yuri', idade=50)
    print(pessoa)
    db_session.add(pessoa)
    db_session.commit()

"""função para listar pessoas"""
def lista_pessoas():
    pessoa = db_session.query(Pessoas).all()
    '''loop para verificação de pessoa'''
    #for i in pessoa:
    #    print(i.nome)
    '''fim para verificação de pessoa'''
    print(pessoa)

"""função para consulta especifica de pessoas"""
def consulta_pessoas():
    pessoa = db_session.query(Pessoas).filter(Pessoas.nome == 'Yuri').first()
    print(pessoa)

"""função para alterar registro de pessoas"""
def altera_pessoas():
    pessoa = db_session.query(Pessoas).filter(Pessoas.nome == 'Yuri').first()
    pessoa.idade = 48
    #pessoa.save foi criado no models
    pessoa.save()
    print(pessoa.nome, pessoa.idade)

"""função para excluir registro de pessoas"""    
def excluir_pessoas():
    pessoa = db_session.query(Pessoas).filter(Pessoas.nome == 'Yuri').first()
    #pessoa.delete foi criado no models
    pessoa.delete()

"""função para incluir pessoas"""
def insere_usuarios(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    print(usuario)
    db_session.add(usuario)
    db_session.commit()
    #usuario.save()

"""função para listar pessoas"""
def lista_usuarios():
    usuario = db_session.query(Usuarios).all()
    '''fim para verificação de pessoa'''
    print(usuario)



    

if __name__=='__main__':
    #insere_pessoas()
    #altera_pessoas()
    #consulta_pessoas()
    #lista_pessoas()
    #excluir_pessoas()
    insere_usuarios('Fabio', '2272')
    insere_usuarios('Yuri', '8572')
    lista_usuarios()