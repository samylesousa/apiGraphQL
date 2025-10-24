from models import Empresa, Curso, Estagio, Bolsa, Professor, Plataforma, Endereco
import asyncio
from faker import Faker
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import random
from datetime import datetime

fake = Faker("pt_BR")

# URL do banco de dados MySQL com asyncmy
DATABASE_URL = "mysql+asyncmy://root:@localhost:3306/banco"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#funções que são usadas durante a construção do banco de dados
async def get_vertente(id: int, TableName):
    async with SessionLocal() as session:  #trabalha com uma instância da session
        query = select(TableName).where(TableName.id == id)
        result = await session.execute(query)
        return result.scalar()

async def get_number_of_elements(TableName):
    async with SessionLocal() as session:  
        query = sa.func.count(TableName.id)
        result = await session.execute(query)
        return result.scalar()

async def popular_banco():
    options = ["Telecomunicações", "Ciência da Computação", "Automação"]
    sufixos_academicos = ["PhD", "MSc", "BSc", "MD", "MBA", "DDS"]
    nivel = ["Básico", "Intermediário", "Avançado"]

    async with SessionLocal() as session:
        async with session.begin():

            professores = [
                Professor(
                    nome=fake.name(), 
                    email=fake.email(),
                    vertente=random.choice(options),
                    telefone=fake.phone_number()[:15],
                    website=fake.url(),
                    formacao=random.choice(sufixos_academicos)
                    ) 
                for _ in range(100)
            ]
            session.add_all(professores)

            plataformas = [
                Plataforma(
                    nome=fake.company(), 
                    email=fake.email(),
                    website=fake.url(),
                    tipo=fake.boolean()
                    ) 
                for _ in range(100)
            ]
            session.add_all(plataformas)

            enderecos = [
                Endereco(
                    rua=fake.street_name(), 
                    numero=fake.random_int(min=1, max=1000),
                    bairro=fake.bairro(),
                    cidade=fake.city(),
                    estado=fake.estado_sigla(),
                    cep=fake.postcode()
                    )
                for _ in range(100)
            ]
            session.add_all(enderecos)

            #Criando as bolsas (dependem dos professores, e da vertente deles)
            bolsas = []
            for _ in range(100):
                #definindo se a bolsa vai ser remunerada ou não
                remunerado = fake.boolean()
                if remunerado:
                    #se for o salario vai ser definido
                    salario = fake.pydecimal(left_digits=4, right_digits=2, positive=True)
                else:
                    salario = None
                
                #as bolsas tem o primeiro dia definido como hoje
                data_inicio = datetime.today().date()

                #verificando quantos professores existem para conectar um deles a bolsa
                num = await get_number_of_elements(Professor)
                id_professor = fake.random_int(min=0, max=num)
                #verificando a vertente do professor para que a mesma seja a da bolsa
                vertente = await get_vertente(id_professor, Professor)


                bolsas.append(
                    Bolsa(
                    professor_id = id_professor,
                    nome=fake.catch_phrase(),
                    descricao=fake.text(), 
                    horas_semanais=fake.random_int(min=10, max=80),
                    vertente=vertente.vertente,
                    quantidade_vagas=fake.random_int(min=1, max=100),
                    data_inicio=data_inicio,
                    salario=salario,
                    data_fim=fake.date_between(start_date=data_inicio, end_date='+2y'),
                    remunerado=remunerado
                    )
                )
            session.add_all(bolsas)

            #Criando os cursos (dependem da plataforma)
            cursos = []
            for _ in range(100):
                #escolhendo a categoria que o curso terá
                categoria = random.choice(["Pago", "Gratuito"])
                if categoria=="Pago":
                    #se ele for pago é definido o preço
                    preco=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                else:
                    preco = None

                #a data de início do curso é definida como a de hoje                
                data_inicio = datetime.today().date()

                #verificando quantas plataformas existem no banco para escolher a que vai ter o curso ofertado
                num = await get_number_of_elements(Plataforma)
                id_plataforma = fake.random_int(min=0, max=num)

                cursos.append(
                    Curso(
                    nome=fake.catch_phrase(), 
                    nivel=random.choice(nivel),
                    vertente=random.choice(options),
                    preco=preco,
                    data_inicio=data_inicio,
                    data_fim=fake.date_between(start_date=data_inicio, end_date='+2y'),
                    plataforma_id=id_plataforma,
                    categoria=categoria,
                    )
                )
            session.add_all(cursos)

            #Criando as empresas (dependem da endereco)
            empresas = []
            for _ in range(100):

                #verifica quantos endereços existem para escolher um aleatoriamente
                num = await get_number_of_elements(Endereco)
                id_endereco = fake.random_int(min=0, max=num)

                empresas.append(
                    Empresa(
                    nome=fake.company(), 
                    CNPJ=fake.cnpj()[:14],
                    telefone=fake.phone_number()[:15],
                    website=fake.url(),
                    email=fake.email(),
                    status=fake.boolean(),
                    endereco_id=id_endereco,
                    vertente=random.choice(options),
                    )
                )
            session.add_all(empresas)

            #Criando os estagios (dependem da empresa)
            estagios = []
            for _ in range(100):
                #escolhendo uma das empresas para ofertar o estágio
                num = await get_number_of_elements(Empresa)
                id_empresa = fake.random_int(min=1001, max=5000)
                vertente = await get_vertente(id_empresa, Empresa) #associando a mesma vertente para o estágio

                #todos os estágios vão começar a partir do dia atual
                data_inicio = datetime.today().date()

                #escolhendo se o estágio vai ser remunerado, e em caso positivo o salário é definido
                remunerado = fake.boolean()
                if remunerado:
                    salario = fake.pydecimal(left_digits=4, right_digits=2, positive=True)
                else:
                    salario = None

                estagios.append(
                    Estagio(
                    nome=fake.catch_phrase(), 
                    salario=salario,
                    empresa_id=id_empresa,
                    vertente=vertente.vertente,
                    horas_semanais=fake.random_int(min=10, max=80),
                    data_inicio=data_inicio,
                    data_fim=fake.date_between(start_date=data_inicio, end_date='+2y'),
                    descricao=fake.text(), 
                    remunerado=remunerado
                    )
                )
            session.add_all(estagios)

async def init_db():
    await popular_banco()

if __name__ == "__main__":
    asyncio.run(init_db())

