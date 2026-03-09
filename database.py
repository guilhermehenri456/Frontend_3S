#importar as bibliotecas
from flask_login import UserMixin
from sqlalchemy import create_engine, String, Integer, func, Column, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash,check_password_hash

# base de dados
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/empresa_db')

#todos
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Funcionario(Base, UserMixin):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    cpf = Column(String, nullable=False)
    senha = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    criado_em = Column(DateTime, server_default=func.now())
    cargo = Column(String, nullable=False)
    salario = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Funcionario {self.nome}>'

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def save(self,db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            raise


