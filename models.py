from sqlalchemy.orm import DeclarativeBase, Mapped, scoped_session, sessionmaker, mapped_column, relationship
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

"""
cria um banco de dados sqLite com o nome atividades use
'convert_unicode' pra fazer uso de acentuação no banco.
"""
engine = create_engine('sqlite:///atividades.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                            bind=engine))


"""
Classe base usada para definições de classe declarativa 
permitindo a criação de novas bases de forma compatível 
com os verificadores de tipos e pode ser usada como base 
para novos mapeamentos declarativos. referencia: 
https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase
"""
class Base(DeclarativeBase):
    pass

"""classe para criar tabela atividades no banco"""
class Pessoas(Base):
    __tablename__ = "pessoas"

    """criação dos camos da tabelas."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(40), index=True) #index=true, vai permitir tornar mais rapida a consulta nesta coluna
    idade:Mapped[int] = mapped_column(Integer)

    """
    função para imprimir o retorno do que
    vai ser exibido da consulta de um objeto
    """
    def __repr__(self):
        return '<Pessoas {}>'.format(self.nome)
    
    """função ou metodo para salvar registro na tabela pessoas"""
    def save(self):
        db_session.add(self)
        db_session.commit()

    """função ou metodo para excluir registro na tabela pessoas"""
    def delete(self):
        db_session.delete(self)
        db_session.commit()

"""classe para criar tabela atividades no banco"""
class Atividades(Base):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    pessoa_id:Mapped[int] = mapped_column(ForeignKey("pessoas.id"), nullable=False)
    pessoas: Mapped["Pessoas"] = relationship("Pessoas")

    """
    função para imprimir o retorno do que
    vai ser exibido da consulta de um objeto
    """
    def __repr__(self):
        return '<Atividades {}>'.format(self.nome)

    """função ou metodo para salvar registro atividades"""
    def save(self):
        db_session.add(self)
        db_session.commit()

    """função ou metodo para excluir registro"""
    def delete(self):
        db_session.delete(self)
        db_session.commit()


"""classe para criar a tabela de usuários"""
class Usuarios(Base):
    __tablename__="usuarios"
    """criação dos camos da tabelas."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(20), unique=True) #index=true, vai permitir tornar mais rapida a consulta nesta coluna
    senha:Mapped[int] = mapped_column(String(20))

    """
    função para imprimir o retorno do que
    vai ser exibido da consulta de um objeto
    """
    def __repr__(self):
        return '<Usuarios {}>'.format(self.login)

    #função ou metodo para salvar usuarios"""
    def save(self):
        db_session.add(self)
        db_session.commit()

    #função ou metodo para excluir usuarios"""
    def delete(self):
        db_session.delete(self)
        db_session.commit()


    

"""função ou metodo para criar o banco de dados"""
def init_db():
    Base.metadata.create_all(bind=engine)

"""
proteção para evitar chamada externa
para criaçãodo Banco e tabelas
"""
if __name__ == '__main__':
    init_db()