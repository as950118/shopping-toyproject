from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from product.api.schemas import (
    ProductCreateSchema,
    ProductResponseSchema,
    DiscountSchema,
    CouponSchema,
)
from product.application.service import ProductService
from product.infrastructure.db_models import DiscountType
from product.infrastructure.repository import SQLAlchemyProductRepository
from database import get_db
from product.domain.models import Product
from product.domain.policy import (
    RateDiscountPolicy,
    AmountDiscountPolicy,
    RateCouponPolicy,
    AmountCouponPolicy,
    CouponPolicy,
)

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = SQLAlchemyProductRepository(db)
    return ProductService(repo)

@router.get("/", response_model=List[ProductResponseSchema])
def list_products(service: ProductService = Depends(get_product_service)):
    products = service.list_products()
    return [to_response_schema(p) for p in products]

@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_detail(product_id: int, service: ProductService = Depends(get_product_service)):
    product = service.get_product_detail(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return to_response_schema(product)

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
def to_response_schema(product: Product) -> ProductResponseSchema:
    # Discount 변환
    discount = None
    if product.discount_policy:
        if isinstance(product.discount_policy, RateDiscountPolicy):
            discount = DiscountSchema(type=DiscountType.RATE, value=product.discount_policy.rate)
        elif isinstance(product.discount_policy, AmountDiscountPolicy):
            discount = DiscountSchema(type=DiscountType.AMOUNT, value=product.discount_policy.amount)
    # Coupon 변환
    coupons: List[CouponSchema] = []
    for c in getattr(product, "coupon_policies", []):
        if isinstance(c, RateCouponPolicy):
            coupons.append(CouponSchema(type=DiscountType.RATE, value=c.rate))
        elif isinstance(c, AmountCouponPolicy):
            coupons.append(CouponSchema(type=DiscountType.AMOUNT, value=c.amount))
    return ProductResponseSchema(
        id=product.id,
        name=product.name,
        price=product.price,
        discount=discount,
        coupons=coupons,
        final_price=product.calculate_final_price() if hasattr(product, "calculate_final_price") else None
    )