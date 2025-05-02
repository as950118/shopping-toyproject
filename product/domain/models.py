from typing import Optional, List

from product.adapter.outbound.db_models import DiscountType
from product.application.schemas import ProductResponseSchema, DiscountSchema, CouponSchema
from product.domain.policy import DiscountPolicy, CouponPolicy, RateDiscountPolicy, AmountDiscountPolicy, \
    RateCouponPolicy, AmountCouponPolicy


class Product:
    """
    순수 도메인 엔티티: 상품
    - 할인/쿠폰 정책은 전략 패턴으로 확장 가능하게 설계
    - 가격 계산 비즈니스 로직 포함
    """

    def __init__(
            self,
            product_id: Optional[int],
            name: str,
            price: int,
            discount_policy: Optional[DiscountPolicy] = None,
            coupon_policies: Optional[List[CouponPolicy]] = None,
    ):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.discount_policy = discount_policy
        self.coupon_policies = coupon_policies or []

    def calculate_final_price(self) -> int:
        """
        할인 및 쿠폰 정책을 순차적으로 적용하여 최종 가격을 계산
        """
        price = self.price
        if self.discount_policy:
            price = self.discount_policy.apply(price)
        for coupon in self.coupon_policies:
            price = coupon.apply(price)
        return max(price, 0)


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
        id=product.product_id,
        name=product.name,
        price=product.price,
        discount=discount,
        coupons=coupons,
        final_price=product.calculate_final_price()
    )
