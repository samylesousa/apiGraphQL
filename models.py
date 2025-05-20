import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#definindo as classes para as tabelas no banco de dados
class Endereco(Base):
    __tablename__ = 'endereco'
    def __str__(self):
        return f"""Rua: {self.rua},
            Número: {self.numero},
            Bairro: {self.bairro},
            Cidade: {self.cidade},
            Estado: {self.estado},
            Cep: {self.cep}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    rua = sa.Column(sa.String)
    numero = sa.Column(sa.Integer)
    bairro = sa.Column(sa.String) 
    cidade = sa.Column(sa.String)
    estado = sa.Column(sa.String)
    cep = sa.Column(sa.String)

    #relacionamento com a tabela empresa (one to one)
    empresa = sa.orm.relationship("Empresa", back_populates="endereco", uselist=False)


class Empresa(Base):
    __tablename__ = 'empresa'
    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            CNPJ: {self.CNPJ},
            Endereço: {self.endereco_id},
            Telefone: {self.telefone},
            Email: {self.email},
            Website: {self.website},
            Status: {"Ativa" if self.status else "Desativada"}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String) 
    vertente = sa.Column(sa.String) 
    CNPJ = sa.Column(sa.String)
    endereco_id = sa.Column(sa.Integer, sa.ForeignKey('endereco.id'))
    telefone = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    status = sa.Column(sa.Boolean)

    #relacionamento com a tabela endereço (one to one)
    endereco = sa.orm.relationship("Endereco", back_populates="empresa")

    #relacionamento com a tabela estagio (one to many)
    estagios = sa.orm.relationship("Estagio", back_populates="empresa")

class Plataforma(Base):
    __tablename__ = 'plataforma'
    def __str__(self):
        return f"""Nome: {self.nome},
            Email: {self.email},
            Website: {self.website},
            Tipo: {"Gratuita" if self.tipo else "Paga"}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    tipo  = sa.Column(sa.Boolean) #se é paga ou gratuita

    #relacionamento com a tabela curso (one to many)
    cursos = sa.orm.relationship("Curso", back_populates="plataforma")


class Curso(Base):
    __tablename__ = 'curso'
    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            Categoria: {self.categoria},
            Preço: {self.preco},
            Plataforma Id: {self.plataforma_id},
            Nível: {self.nivel},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    categoria = sa.Column(sa.String)   #se é pago ou não
    preco = sa.Column(sa.Float)
    plataforma_id =  sa.Column(sa.Integer, sa.ForeignKey('plataforma.id'))
    nivel = sa.Column(sa.String)    #as três opções são, iniciante, intermédiario e avançado
    vertente = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE) 

    #relacionamento com a tabela plataforma (many to one)
    plataforma = sa.orm.relationship("Plataforma", back_populates="cursos")

class Estagio(Base):
    __tablename__ = 'estagio'
    def __str__(self):
        return f'''Nome: {self.nome}, 
            Vertente: {self.vertente},
            Salário: {self.salario},
            Empresa Id: {self.empresa_id},
            Remunerado: {"Sim" if self.remunerado else "Não"},
            Horas Semanais: {self.horas_semanais},
            Descrição: {self.descricao},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim}
        '''

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    salario = sa.Column(sa.Float)
    empresa_id = sa.Column(sa.Integer, sa.ForeignKey('empresa.id'))
    remunerado  = sa.Column(sa.Boolean)
    horas_semanais = sa.Column(sa.Integer)
    descricao = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE)

    #relacionamento com a tabela empresa (many to one)
    empresa = sa.orm.relationship("Empresa", back_populates="estagios")

class Bolsa(Base):
    __tablename__ = 'bolsa'
    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            Salário: {self.salario},
            Remunerado: {self.remunerado},
            Horas Semanais: {self.horas_semanais},
            Quantidade de Vagas: {self.quantidade_vagas},
            Descrição: {self.descricao},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim},
            Professor Id: {self.professor_id}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    salario = sa.Column(sa.Float)
    remunerado  = sa.Column(sa.Boolean)
    horas_semanais = sa.Column(sa.Integer)
    quantidade_vagas = sa.Column(sa.Integer)
    descricao = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE) 
    professor_id = sa.Column(sa.Integer, sa.ForeignKey('professor.id'))

    #definindo o relacionamento com a tabela professor (many to one)
    professor = sa.orm.relationship("Professor", back_populates="bolsas")

class Professor(Base):
    __tablename__ = 'professor'
    
    def __str__(self):
        return f"""Nome: {self.nome}, 
            Vertente: {self.vertente},
            Telefone: {self.telefone},
            Email: {self.email},
            Website: {self.website},
            Formção: {self.formacao}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    telefone = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    formacao = sa.Column(sa.String)

    #relacionamento com a tabela bolsa (one to many)
    bolsas = sa.orm.relationship("Bolsa", back_populates="professor")