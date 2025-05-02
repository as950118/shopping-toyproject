from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from product.adapter.outbound.repository import SQLAlchemyProductRepository
from product.application.mapper import to_product_response_schema_from_product
from product.application.schemas import (
    ProductCreateSchema,
    ProductResponseSchema,
)
from product.application.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = SQLAlchemyProductRepository(db)
    return ProductService(repo)


@router.get("/", response_model=List[ProductResponseSchema])
def list_products(service: ProductService = Depends(get_product_service)):
    products = service.list_products()
    return [to_product_response_schema_from_product(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_detail(product_id: int, service: ProductService = Depends(get_product_service)):
    product = service.get_product_detail(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return to_product_response_schema_from_product(product)


@router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
def create_product(
        product_in: ProductCreateSchema,
        service: ProductService = Depends(get_product_service)
):
    saved_product = service.create_product(product_in)
    return ProductResponseSchema.from_domain(saved_product)


@router.get("/{product_id}/final-price", response_model=int)
def calculate_final_price(product_id: int, service: ProductService = Depends(get_product_service)):
    final_price = service.calculate_final_price(product_id)
    if final_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return final_price

# TODO 변환함수 도메인으로 분리
