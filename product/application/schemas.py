from typing import Optional, List
from pydantic import BaseModel, Field

from product.domain.models import Product, CouponPolicy
from product.domain.policy import RateDiscountPolicy, AmountDiscountPolicy, RateCouponPolicy, AmountCouponPolicy
from product.adapter.outbound.db_models import DiscountType


class DiscountSchema(BaseModel):
    type: DiscountType = Field(..., description="할인 타입: rate(할인률), amount(정액)")
    value: float = Field(..., description="할인 값: 정률(0.0~1.0), 정액(정수)")


class CouponSchema(BaseModel):
    type: DiscountType = Field(..., description="쿠폰 타입: rate(할인률), amount(정액)")
    value: float = Field(..., description="쿠폰 값: 정률(0.0~1.0), 정액(정수)")


class ProductCreateSchema(BaseModel):
    name: str = Field(..., description="상품명")
    price: int = Field(..., description="상품 가격")
    discount: Optional[DiscountSchema] = Field(None, description="할인 정책")
    coupons: Optional[List[CouponSchema]] = Field(default_factory=list, description="쿠폰 목록")


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: int
    discount: Optional[DiscountSchema] = None
    coupons: List[CouponSchema] = []
    final_price: Optional[int] = Field(None, description="최종 판매가 (할인/쿠폰 적용 후)")

    class Config:
        orm_mode = True
