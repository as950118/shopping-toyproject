import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from product.adapter.inbound.router import router as product_router
from product.adapter.outbound.db_models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행
    logging.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    # 애플리케이션 종료 시 실행
    logging.info("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(product_router)