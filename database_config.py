from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


DATABASE_URL = "mysql+asyncmy://root:issoechatopracaralho@localhost:3306/dadosGerais"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        yield session