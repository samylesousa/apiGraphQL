from typing import List, Type, Optional
import strawberry
from models import Empresa, Curso, Estagio, Bolsa, Professor, Plataforma, Endereco
import datetime
from dataclasses import asdict
from sqlalchemy.future import select
from database_config import get_session


# Criando um scalar para lidar com Date no GraphQL
DateScalar = strawberry.scalar(
    datetime.date,
    serialize=lambda v: v.isoformat(),
    parse_value=lambda v: datetime.date.fromisoformat(v)
)

async def get_estagios():
    async with get_session() as session:
        resultado = await session.execute(select(Estagio))
        item = resultado.scalars().all()

        return [EstagioType(
            id=row.id,
            nome=row.nome,
            vertente=row.vertente,
            salario=row.salario,
            empresa_id=row.empresa_id,
            horas_semanais=row.horas_semanais,
            remunerado=row.remunerado,
            descricao=row.descricao,
            data_inicio=row.data_inicio,
            data_fim=row.data_fim
            ) for row in item]

async def get_bolsas():
    async with get_session() as session:
        resultado = await session.execute(select(Bolsa))
        item = resultado.scalars().all()

        return [BolsaType(
            id=row.id,
            nome=row.nome,
            vertente=row.vertente,
            salario=row.salario,
            professor_id=row.professor_id,
            horas_semanais=row.horas_semanais,
            remunerado=row.remunerado,
            quantidade_vagas=row.quantidade_vagas,
            data_inicio=row.data_inicio,
            data_fim=row.data_fim,
            descricao=row.descricao
            ) for row in item]

async def get_professores():
    async with get_session() as session:
        resultado = await session.execute(select(Professor))
        item = resultado.scalars().all()

        return [ProfessorType(
            id=row.id,
            nome=row.nome,
            vertente=row.vertente,
            telefone=row.telefone,
            email=row.email,
            website=row.website,
            formacao=row.formacao,
            ) for row in item]

async def get_empresas():
    async with get_session() as session:
        resultado = await session.execute(select(Empresa))
        item = resultado.scalars().all()

        return [EmpresaType(
            id=row.id,
            nome=row.nome,
            vertente=row.vertente,
            telefone=row.telefone,
            email=row.email,
            website=row.website,
            CNPJ=row.CNPJ,
            status=row.status,
            endereco_id=row.endereco_id
            ) for row in item]

async def get_endereco():
    async with get_session() as session:
        resultado = await session.execute(select(Endereco))
        item = resultado.scalars().all()

        return [EnderecoType(
            id=row.id,
            rua=row.rua,
            numero=row.numero,
            bairro=row.bairro,
            cidade=row.cidade,
            estado=row.estado,
            cep=row.cep,
            ) for row in item]

async def get_plataforma():
    async with get_session() as session:
        resultado = await session.execute(select(Plataforma))
        item = resultado.scalars().all()

        return [PlataformaType(
            id=row.id,
            nome=row.nome,
            email=row.email,
            website=row.website,
            tipo=row.tipo,
            ) for row in item]

async def get_courses():
    async with get_session() as session:
        resultado = await session.execute(select(Curso))
        item = resultado.scalars().all()
        return [CursoType(
                id=row.id,
                nome=row.nome,
                categoria=row.categoria,
                preco= row.preco,
                plataforma_id=row.plataforma_id,
                nivel=row.nivel,
                vertente=row.vertente,
                data_inicio=row.data_inicio,
                data_fim=row.data_fim
                ) for row in item]


#criando os tipos para as queries
@strawberry.type
class EnderecoType:
	id: int
	rua: str
	numero: Optional[int] = None
	bairro: Optional[str] = None
	cidade: Optional[str] = None
	estado: Optional[str] = None
	cep: Optional[str] = None

@strawberry.type
class PlataformaType:
	id: int
	nome: str
	email: Optional[str] = None
	website: Optional[str] = None
	tipo: Optional[bool] = None

@strawberry.type
class ProfessorType:
	id: int
	nome: str
	vertente: Optional[str] = None
	telefone: Optional[str] = None
	email: Optional[str] = None
	website: Optional[str] = None
	formacao: Optional[str] = None

#a partir daqui começa as tabelas com relacionamentos
@strawberry.type
class EmpresaType:
	id: int
	nome: str
	vertente: Optional[str] = None
	CNPJ: Optional[str] = None
	endereco_id: Optional[int] = None
	telefone: Optional[str] = None
	email: Optional[str] = None
	website: Optional[str] = None
	status: Optional[bool] = None

@strawberry.type
class CursoType:
    id: int
    nome: str
    categoria: Optional[str] = None
    preco: Optional[float] = None
    plataforma_id: Optional[int] = None
    nivel: Optional[str] = None
    vertente: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None


@strawberry.type
class EstagioType:
    id: int
    nome: str
    vertente: Optional[str] = None
    salario: Optional[float] = None
    empresa_id: Optional[int] = None
    remunerado: Optional[bool] = None
    horas_semanais: Optional[int] = None
    descricao: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None

@strawberry.type
class BolsaType:
	id: int
	nome: str
	vertente: Optional[str] = None
	salario: Optional[float] = None
	remunerado: Optional[bool] = None
	horas_semanais: Optional[int] = None
	quantidade_vagas: Optional[int] = None
	descricao: Optional[str] = None
	data_inicio: Optional[datetime.date] = None
	data_fim: Optional[datetime.date] = None
	professor_id: Optional[int] = None

#criando os tipos para os gets e o delete com id
@strawberry.input
class GetIDType:
    id: int

async def getbyid_professor(self, input: GetIDType) -> ProfessorType:
    async with get_session() as session:
        resultado = await session.get(Professor, input.id)
        if not resultado:
            raise Exception("Professor não foi encontrado")

        return ProfessorType(
            id=resultado.id,
            nome=resultado.nome,
            vertente=resultado.vertente,
            telefone=resultado.telefone,
            email=resultado.email,
            website=resultado.website,
            formacao=resultado.formacao
        )

async def getbyid_curso(self, input: GetIDType) -> CursoType:
    async with get_session() as session:
        resultado = await session.get(Curso, input.id)
        if not resultado:
            raise Exception("Curso não foi encontrado")

        return CursoType(
            id=resultado.id,
            nome=resultado.nome,
            categoria=resultado.categoria,
            preco=resultado.preco,
            plataforma_id=resultado.plataforma_id,
            nivel=resultado.nivel,
            vertente=resultado.vertente,
            data_inicio=resultado.data_inicio,
            data_fim=resultado.data_fim,
        )

async def getbyid_plataforma(self, input: GetIDType) -> PlataformaType:
    async with get_session() as session:
        resultado = await session.get(Plataforma, input.id)
        if not resultado:
            raise Exception("Plataforma não foi encontrada")

        return PlataformaType(
            id=resultado.id,
            nome=resultado.nome,
            email=resultado.email,
            website=resultado.website,
            tipo=resultado.tipo
        )

async def getbyid_estagio(self, input: GetIDType) -> EstagioType:
    async with get_session() as session:
        resultado = await session.get(Estagio, input.id)
        if not resultado:
            raise Exception("Estágio não foi encontrado")
        return EstagioType(
            id=resultado.id,
            nome=resultado.nome,
            vertente=resultado.vertente,
            salario=resultado.salario,
            empresa_id=resultado.empresa_id,
            remunerado=resultado.remunerado,
            horas_semanais=resultado.horas_semanais,
            descricao=resultado.descricao,
            data_inicio=resultado.data_inicio,
            data_fim=resultado.data_fim
        )

async def getbyid_endereco(self, input: GetIDType) -> EnderecoType:
    async with get_session() as session:
        resultado = await session.get(Endereco, input.id)
        if not resultado:
            raise Exception("Endereco não foi encontrado")

        return EnderecoType(
            id=resultado.id,
            rua=resultado.rua,
            numero=resultado.numero,
            bairro=resultado.bairro,
            cidade=resultado.cidade,
            estado=resultado.estado,
            cep=resultado.cep
        )

async def getbyid_empresa(self, input: GetIDType) -> EmpresaType:
    async with get_session() as session:
        resultado = await session.get(Empresa, input.id)
        if not resultado:
            raise Exception("Empresa não foi encontrada")

        await session.commit()
        await session.refresh(resultado)
        return EmpresaType(
            id=resultado.id,
            nome=resultado.nome,
            vertente=resultado.vertente,
            CNPJ=resultado.CNPJ,
            endereco_id=resultado.endereco_id,
            telefone=resultado.telefone,
            email=resultado.email,
            website=resultado.website,
            status=resultado.status,
        )

async def getbyid_bolsa(self, input: GetIDType) -> BolsaType:
    async with get_session() as session:
        resultado = await session.get(Bolsa, input.id)
        if not resultado:
            raise Exception("Bolsa não foi encontrada")

        return BolsaType(
            id=resultado.id,
            nome=resultado.nome,
            vertente=resultado.vertente,
            salario=resultado.salario,
            remunerado=resultado.remunerado,
            horas_semanais=resultado.horas_semanais,
            quantidade_vagas=resultado.quantidade_vagas,
            descricao=resultado.descricao,
            data_inicio=resultado.data_inicio,
            data_fim=resultado.data_fim,
            professor_id=resultado.professor_id
        )

@strawberry.type
class Query:
    getCursos: List[CursoType] = strawberry.field(resolver=get_courses)
    getPlataformas: List[PlataformaType] = strawberry.field(resolver=get_plataforma)
    getEnderecos: List[EnderecoType] = strawberry.field(resolver=get_endereco)
    getEmpresas: List[EmpresaType] = strawberry.field(resolver=get_empresas)
    getProfessores: List[ProfessorType] = strawberry.field(resolver=get_professores)
    getBolsas: List[BolsaType] = strawberry.field(resolver=get_bolsas)
    getEstagios: List[EstagioType] = strawberry.field(resolver=get_estagios)
    getIdEstagios: EstagioType = strawberry.field(resolver=getbyid_estagio)
    getIdBolsas: BolsaType = strawberry.field(resolver=getbyid_bolsa)
    getIdEndereco: EnderecoType = strawberry.field(resolver=getbyid_endereco)
    getIdProfessor: ProfessorType = strawberry.field(resolver=getbyid_professor)
    getIdEmpresa: EmpresaType = strawberry.field(resolver=getbyid_empresa)
    getIdPlataforma: PlataformaType = strawberry.field(resolver=getbyid_plataforma)
    getIdCurso: CursoType = strawberry.field(resolver=getbyid_curso)


#criando os tipos para as mutations (criação)
@strawberry.input
class EnderecoInputCreate:
	rua: str
	numero: Optional[int] = None
	bairro: Optional[str] = None
	cidade: Optional[str] = None
	estado: Optional[str] = None
	cep: Optional[str] = None

@strawberry.input
class PlataformaInputCreate:
	nome: str
	email: Optional[str] = None
	website: Optional[str] = None
	tipo: Optional[bool] = None

@strawberry.input
class ProfessorInputCreate:
	nome: str
	vertente: Optional[str] = None
	telefone: Optional[str] = None
	email: Optional[str] = None
	website: Optional[str] = None
	formacao: Optional[str] = None


#a partir daqui começa as tabelas com relacionamentos
@strawberry.input
class EmpresaInputCreate:
	nome: str
	vertente: Optional[str] = None
	CNPJ: Optional[str] = None
	endereco_id: Optional[int] = None
	telefone: Optional[str] = None
	email: Optional[str] = None
	website: Optional[str] = None
	status: Optional[bool] = None

@strawberry.input
class CursoInputCreate:
    nome: str
    categoria: Optional[str] = None
    preco: Optional[float] = None
    plataforma_id: Optional[int] = None
    nivel: Optional[str] = None
    vertente: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None


@strawberry.input
class EstagioInputCreate:
    nome: str
    vertente: Optional[str] = None
    salario: Optional[float] = None
    empresa_id: Optional[int] = None
    remunerado: Optional[bool] = None
    horas_semanais: Optional[int] = None
    descricao: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None

@strawberry.input
class BolsaInputCreate:
	nome: str
	vertente: Optional[str] = None
	salario: Optional[float] = None
	remunerado: Optional[bool] = None
	horas_semanais: Optional[int] = None
	quantidade_vagas: Optional[int] = None
	descricao: Optional[str] = None
	data_inicio: Optional[datetime.date] = None
	data_fim: Optional[datetime.date] = None
	professor_id: Optional[int] = None



async def criar_professor(info, input: ProfessorInputCreate) -> ProfessorType:
    async with get_session() as session:
        try:
            novo_professor = Professor(
                nome=input.nome,
                vertente=input.vertente,
                telefone=input.telefone,
                email=input.email,
                website=input.website,
                formacao=input.formacao
            )
            session.add(novo_professor)
            await session.commit()
            await session.refresh(novo_professor)

            return ProfessorType(
                id=novo_professor.id,
                nome=novo_professor.nome,
                vertente=novo_professor.vertente,
                telefone=novo_professor.telefone,
                email=novo_professor.email,
                website=novo_professor.website,
                formacao=novo_professor.formacao,
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_bolsa(info, input: BolsaInputCreate) -> BolsaType:
    async with get_session() as session:
        try:
            nova_bolsa = Bolsa(
                nome=input.nome,
                vertente=input.vertente,
                salario=input.salario,
                remunerado=input.remunerado,
                horas_semanais=input.horas_semanais,
                quantidade_vagas=input.quantidade_vagas,
                descricao=input.descricao,
                data_inicio=input.data_inicio,
                data_fim=input.data_fim,
                professor_id=input.professor_id
            )
            session.add(nova_bolsa)
            await session.commit()
            await session.refresh(nova_bolsa)

            return BolsaType(
                id=nova_bolsa.id,
                nome=nova_bolsa.nome,
                vertente=nova_bolsa.vertente,
                salario=nova_bolsa.salario,
                remunerado=nova_bolsa.remunerado,
                horas_semanais=nova_bolsa.horas_semanais,
                quantidade_vagas=nova_bolsa.quantidade_vagas,
                descricao=nova_bolsa.descricao,
                data_inicio=nova_bolsa.data_inicio,
                data_fim=nova_bolsa.data_fim,
                professor_id=nova_bolsa.professor_id
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_endereco(info, input: EnderecoInputCreate) -> EnderecoType:
    async with get_session() as session:
        try:
            novo_endereco = Endereco(
                rua=input.rua,
                numero=input.numero,
                bairro=input.bairro,
                cidade=input.cidade,
                estado=input.estado,
                cep=input.cep
            )
            session.add(novo_endereco)
            await session.commit()
            await session.refresh(novo_endereco)

            return EnderecoType(
                id=novo_endereco.id,
                rua=novo_endereco.rua,
                numero=novo_endereco.numero,
                bairro=novo_endereco.bairro,
                cidade=novo_endereco.cidade,
                estado=novo_endereco.estado,
                cep=novo_endereco.cep
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_empresa(info, input: EmpresaInputCreate) -> EmpresaType:
    async with get_session() as session:
        try:
            nova_empresa = Empresa(
                nome=input.nome,
                vertente=input.vertente,
                CNPJ=input.CNPJ,
                endereco_id=input.endereco_id,
                telefone=input.telefone,
                email=input.email,
                website=input.website,
                status=input.status
            )
            session.add(nova_empresa)
            await session.commit()
            await session.refresh(nova_empresa)

            return EmpresaType(
                id=nova_empresa.id,
                nome=nova_empresa.nome,
                vertente=nova_empresa.vertente,
                CNPJ=nova_empresa.CNPJ,
                endereco_id=nova_empresa.endereco_id,
                telefone=nova_empresa.telefone,
                email=nova_empresa.email,
                website=nova_empresa.website,
                status=nova_empresa.status
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_curso(info, input: CursoInputCreate) -> CursoType:
    async with get_session() as session:
        try:
            novo_curso = Curso(
                nome=input.nome,
                vertente=input.vertente,
                categoria=input.categoria,
                preco=input.preco,
                plataforma_id=input.plataforma_id,
                nivel=input.nivel,
                data_inicio=input.data_inicio,
                data_fim=input.data_fim
            )
            session.add(novo_curso)
            await session.commit()
            await session.refresh(novo_curso)

            return CursoType(
                id=novo_curso.id,
                nome=novo_curso.nome,
                vertente=novo_curso.vertente,
                categoria=novo_curso.categoria,
                preco=novo_curso.preco,
                plataforma_id=novo_curso.plataforma_id,
                nivel=novo_curso.nivel,
                data_inicio=novo_curso.data_inicio,
                data_fim=novo_curso.data_fim
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_plataforma(info, input: PlataformaInputCreate) -> PlataformaType:
    async with get_session() as session:
        try:
            nova_plataforma = Plataforma(
                nome=input.nome,
                email=input.email,
                website=input.website,
                tipo=input.tipo
            )
            session.add(nova_plataforma)
            await session.commit()
            await session.refresh(nova_plataforma)

            return PlataformaType(
                id=nova_plataforma.id,
                nome=nova_plataforma.nome,
                email=nova_plataforma.email,
                website=nova_plataforma.website,
                tipo=nova_plataforma.tipo
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def criar_estagio(info, input: EstagioInputCreate) -> EstagioType:
    async with get_session() as session:
        try:
            novo_estagio = Estagio(
                nome=input.nome,
                vertente=input.vertente,
                salario=input.salario,
                empresa_id=input.empresa_id,
                remunerado=input.remunerado,
                horas_semanais=input.horas_semanais,
                descricao=input.descricao,
                data_inicio=input.data_inicio,
                data_fim=input.data_fim
            )
            session.add(novo_estagio)
            await session.commit()
            await session.refresh(novo_estagio)

            return EstagioType(
                id=novo_estagio.id,
                nome=novo_estagio.nome,
                vertente=novo_estagio.vertente,
                salario=novo_estagio.salario,
                empresa_id=novo_estagio.empresa_id,
                remunerado=novo_estagio.remunerado,
                horas_semanais=novo_estagio.horas_semanais,
                descricao=novo_estagio.descricao,
                data_inicio=novo_estagio.data_inicio,
                data_fim=novo_estagio.data_fim
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

#criando os tipos para as atualizações
@strawberry.input
class EnderecoUpdateInput:
    id: int
    rua: Optional[str] = None
    numero: Optional[int] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

@strawberry.input
class PlataformaUpdateInput:
    id: int
    nome: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    tipo: Optional[bool] = None

@strawberry.input
class ProfessorUpdateInput:
    id: int
    nome: Optional[str] = None
    vertente: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    formacao: Optional[str] = None

#a partir daqui começa as tabelas com relacionamentos
@strawberry.input
class EmpresaUpdateInput:
    id: int
    nome: Optional[str] = None
    vertente: Optional[str] = None
    CNPJ: Optional[str] = None
    endereco_id: Optional[int] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    status: Optional[bool] = None

@strawberry.input
class CursoUpdateInput:
    id: int
    nome: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = None
    plataforma_id: Optional[int] = None
    nivel: Optional[str] = None
    vertente: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None


@strawberry.input
class EstagioUpdateInput:
    id: int
    nome: Optional[str] = None
    vertente: Optional[str] = None
    salario: Optional[float] = None
    empresa_id: Optional[int] = None
    remunerado: Optional[bool] = None
    horas_semanais: Optional[int] = None
    descricao: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None

@strawberry.input
class BolsaUpdateInput:
    id: int
    nome: Optional[str] = None
    vertente: Optional[str] = None
    salario: Optional[float] = None
    remunerado: Optional[bool] = None
    horas_semanais: Optional[int] = None
    quantidade_vagas: Optional[int] = None
    descricao: Optional[str] = None
    data_inicio: Optional[datetime.date] = None
    data_fim: Optional[datetime.date] = None
    professor_id: Optional[int] = None

async def update_bolsa(self, input: BolsaUpdateInput) -> BolsaType:
    async with get_session() as session:
        try:
            resultado = await session.get(Bolsa, input.id)
            if not resultado:
                raise Exception("Bolsa não foi encontrada")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return BolsaType(
                id=resultado.id,
                nome=resultado.nome,
                vertente=resultado.vertente,
                salario=resultado.salario,
                remunerado=resultado.remunerado,
                horas_semanais=resultado.horas_semanais,
                quantidade_vagas=resultado.quantidade_vagas,
                descricao=resultado.descricao,
                data_inicio=resultado.data_inicio,
                data_fim=resultado.data_fim,
                professor_id=resultado.professor_id
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_curso(self, input: CursoUpdateInput) -> CursoType:
    async with get_session() as session:
        try:
            resultado = await session.get(Curso, input.id)
            if not resultado:
                raise Exception("Curso não foi encontrado")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return CursoType(
                id=resultado.id,
                nome=resultado.nome,
                categoria=resultado.categoria,
                preco=resultado.preco,
                plataforma_id=resultado.plataforma_id,
                nivel=resultado.nivel,
                vertente=resultado.vertente,
                data_inicio=resultado.data_inicio,
                data_fim=resultado.data_fim,
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_empresa(self, input: EmpresaUpdateInput) -> EmpresaType:
    async with get_session() as session:
        try:
            resultado = await session.get(Empresa, input.id)
            if not resultado:
                raise Exception("Empresa não foi encontrada")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return EmpresaType(
                id=resultado.id,
                nome=resultado.nome,
                vertente=resultado.vertente,
                CNPJ=resultado.CNPJ,
                endereco_id=resultado.endereco_id,
                telefone=resultado.telefone,
                email=resultado.email,
                website=resultado.website,
                status=resultado.status,
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_endereco(self, input: EnderecoUpdateInput) -> EnderecoType:
    async with get_session() as session:
        try:
            resultado = await session.get(Endereco, input.id)
            if not resultado:
                raise Exception("Endereco não foi encontrado")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return EnderecoType(
                id=resultado.id,
                rua=resultado.rua,
                numero=resultado.numero,
                bairro=resultado.bairro,
                cidade=resultado.cidade,
                estado=resultado.estado,
                cep=resultado.cep
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_estagio(self, input: EstagioUpdateInput) -> EstagioType:
    async with get_session() as session:
        try:
            resultado = await session.get(Estagio, input.id)
            if not resultado:
                raise Exception("Estágio não foi encontrado")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return EstagioType(
                id=resultado.id,
                nome=resultado.nome,
                vertente=resultado.vertente,
                salario=resultado.salario,
                empresa_id=resultado.empresa_id,
                remunerado=resultado.remunerado,
                horas_semanais=resultado.horas_semanais,
                descricao=resultado.descricao,
                data_inicio=resultado.data_inicio,
                data_fim=resultado.data_fim
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_plataforma(self, input: PlataformaUpdateInput) -> PlataformaType:
    async with get_session() as session:
        try:
            resultado = await session.get(Plataforma, input.id)
            if not resultado:
                raise Exception("Plataforma não foi encontrada")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return PlataformaType(
                id=resultado.id,
                nome=resultado.nome,
                email=resultado.email,
                website=resultado.website,
                tipo=resultado.tipo
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")

async def update_professor(self, input: ProfessorUpdateInput) -> ProfessorType:
    async with get_session() as session:
        try:
            resultado = await session.get(Professor, input.id)
            if not resultado:
                raise Exception("Professor não foi encontrado")

            input_elementos = asdict(input)
            for key, value in input_elementos.items():
                if key != "id" and value is not None:
                    setattr(resultado, key, value)

            await session.commit()
            await session.refresh(resultado)
            return ProfessorType(
                id=resultado.id,
                nome=resultado.nome,
                vertente=resultado.vertente,
                telefone=resultado.telefone,
                email=resultado.email,
                website=resultado.website,
                formacao=resultado.formacao
            )
        except Exception as e:
            await session.rollback()
            raise Exception(f"Erro: {str(e)}")


@strawberry.type
class MensagemInput:
    ok: Optional[bool]
    message: str

def delete_elementos(model_class: Type):
    async def resolver(info, input: GetIDType) -> MensagemInput:
        async with get_session() as session:
            try:
                resultado = await session.get(model_class, input.id)
                if not resultado:
                    raise Exception("Elemento não foi encontrado")

                await session.delete(resultado)
                await session.commit()
                return MensagemInput(ok=True, message="Elemento deletado com sucesso.")
            except Exception as e:
                await session.rollback()
                raise Exception(f"Erro: {str(e)}")


    return resolver

@strawberry.type
class Mutation:
    criarProfessor: ProfessorType = strawberry.field(resolver=criar_professor)
    criarBolsa: BolsaType = strawberry.field(resolver=criar_bolsa)
    criarEndereco: EnderecoType = strawberry.field(resolver=criar_endereco)
    criarEmpresa: EmpresaType = strawberry.field(resolver=criar_empresa)
    criarCurso: CursoType = strawberry.field(resolver=criar_curso)
    criarPlataforma: PlataformaType = strawberry.field(resolver=criar_plataforma)
    criarEstagio: EstagioType = strawberry.field(resolver=criar_estagio)
    updateBolsa: BolsaType = strawberry.field(resolver=update_bolsa)
    updateCurso: CursoType = strawberry.field(resolver=update_curso)
    updateEmpresa: EmpresaType = strawberry.field(resolver=update_empresa)
    updateEndereco: EnderecoType = strawberry.field(resolver=update_endereco)
    updateEstagio: EstagioType = strawberry.field(resolver=update_estagio)
    updatePlataforma: PlataformaType = strawberry.field(resolver=update_plataforma)
    updateProfessor: ProfessorType = strawberry.field(resolver=update_professor)
    deleteBolsa: MensagemInput = strawberry.field(resolver=delete_elementos(Bolsa))
    deleteCurso: MensagemInput = strawberry.field(resolver=delete_elementos(Curso))
    deleteEmpresa: MensagemInput = strawberry.field(resolver=delete_elementos(Empresa))
    deleteEndereco: MensagemInput = strawberry.field(resolver=delete_elementos(Endereco))
    deleteEstagio: MensagemInput = strawberry.field(resolver=delete_elementos(Estagio))
    deletePlataforma: MensagemInput = strawberry.field(resolver=delete_elementos(Plataforma))
    deleteProfessor: MensagemInput = strawberry.field(resolver=delete_elementos(Professor))


schema = strawberry.federation.Schema(query=Query, mutation=Mutation)