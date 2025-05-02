from typing import Optional, List

from product.domain.policy import DiscountPolicy, CouponPolicy


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

