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


def product_create_schema_to_domain(schema: ProductCreateSchema) -> Product:
    # Discount 변환
    discount_policy = None
    if schema.discount:
        if schema.discount.type == DiscountType.RATE:
            discount_policy = RateDiscountPolicy(schema.discount.value)
        elif schema.discount.type == DiscountType.AMOUNT:
            discount_policy = AmountDiscountPolicy(int(schema.discount.value))
    # Coupon 변환
    coupon_policies: List[CouponPolicy] = []
    for coupon in schema.coupons or []:
        if coupon.type == DiscountType.RATE:
            coupon_policies.append(RateCouponPolicy(coupon.value))
        elif coupon.type == DiscountType.AMOUNT:
            coupon_policies.append(AmountCouponPolicy(int(coupon.value)))
    # id는 None 또는 0으로 생성(저장 시 DB에서 할당)
    return Product(
        product_id=None,
        name=schema.name,
        price=schema.price,
        discount_policy=discount_policy,
        coupon_policies=coupon_policies,
    )
