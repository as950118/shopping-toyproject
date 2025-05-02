from typing import List

from product.adapter.outbound.db_models import DiscountType
from product.application.schemas import (
    ProductResponseSchema,
    DiscountSchema,
    CouponSchema,
    ProductCreateSchema
)
from product.domain.model import Product
from product.domain.policy import (
    RateDiscountPolicy,
    RateCouponPolicy, AmountDiscountPolicy,
    AmountCouponPolicy,
    CouponPolicy, DiscountPolicy
)


def to_product_response_schema_from_product(product: Product) -> ProductResponseSchema:
    # Discount 변환
    discounts: List[DiscountSchema] = []
    for discount_policy in product.discount_policies:
        if isinstance(discount_policy, RateDiscountPolicy):
            discounts.append(DiscountSchema(type=DiscountType.RATE, value=discount_policy.rate))
        elif isinstance(discount_policy, AmountDiscountPolicy):
            discounts.append(DiscountSchema(type=DiscountType.AMOUNT, value=discount_policy.amount))

    # Coupon 변환
    coupons: List[CouponSchema] = []
    for coupon in product.coupon_policies:
        if isinstance(coupon, RateCouponPolicy):
            coupons.append(CouponSchema(type=DiscountType.RATE, value=coupon.rate))
        elif isinstance(coupon, AmountCouponPolicy):
            coupons.append(CouponSchema(type=DiscountType.AMOUNT, value=coupon.amount))
    return ProductResponseSchema(
        id=product.product_id,
        name=product.name,
        price=product.price,
        discounts=discounts,
        coupons=coupons,
        final_price=product.calculate_final_price()
    )


def to_domain_from_product_create_schema(schema: ProductCreateSchema) -> Product:
    # Discount 변환
    discount_policies: List[DiscountPolicy] = []
    for discount in schema.discounts:
        if discount.type == DiscountType.RATE:
            discount_policies.append(RateDiscountPolicy(discount.value))
        elif discount.type == DiscountType.AMOUNT:
            discount_policies.append(AmountDiscountPolicy(int(discount.value)))

    # Coupon 변환
    coupon_policies: List[CouponPolicy] = []
    for coupon in schema.coupons:
        if coupon.type == DiscountType.RATE:
            coupon_policies.append(RateCouponPolicy(coupon.value))
        elif coupon.type == DiscountType.AMOUNT:
            coupon_policies.append(AmountCouponPolicy(int(coupon.value)))
    # id는 None 또는 0으로 생성(저장 시 DB에서 할당)
    return Product(
        product_id=None,
        name=schema.name,
        price=schema.price,
        discount_policies=discount_policies,
        coupon_policies=coupon_policies,
    )
