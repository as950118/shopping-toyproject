from contextlib import asynccontextmanager

from fastapi import FastAPI
from product.adapter.inbound.router import router as product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행
    print("Creating database tables...")
    # Base.metadata.create_all(bind=engine)
    yield
    # 애플리케이션 종료 시 실행
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(product_router)