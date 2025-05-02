from product.domain.models import Product
from product.domain.policy import (
    RateDiscountPolicy,
    AmountDiscountPolicy,
    RateCouponPolicy,
    AmountCouponPolicy,
)

def describe_product_price_calculation():

    def context_no_discount_and_no_coupon():
        def it_returns_original_price():
            # Given
            product = Product(id=1, name="상품A", price=10000)
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 10000

    def context_with_rate_discount():
        def it_applies_rate_discount():
            # Given
            product = Product(
                id=2,
                name="상품B",
                price=20000,
                discount_policy=RateDiscountPolicy(0.1)  # 10% 할인
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 18000

    def context_with_amount_discount():
        def it_applies_amount_discount():
            # Given
            product = Product(
                id=3,
                name="상품C",
                price=15000,
                discount_policy=AmountDiscountPolicy(3000)  # 3,000원 할인
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 12000

    def context_with_discount_and_single_coupon():
        def it_applies_discount_then_coupon():
            # Given
            product = Product(
                id=4,
                name="상품D",
                price=30000,
                discount_policy=RateDiscountPolicy(0.2),  # 20% 할인
                coupon_policies=[AmountCouponPolicy(5000)]  # 5,000원 쿠폰
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 30,000 -> 24,000(20% 할인) -> 19,000(쿠폰)
            assert final_price == 19000

    def context_with_multiple_coupons():
        def it_applies_discount_and_multiple_coupons_in_order():
            # Given
            product = Product(
                id=5,
                name="상품E",
                price=50000,
                discount_policy=AmountDiscountPolicy(10000),  # 10,000원 할인
                coupon_policies=[
                    RateCouponPolicy(0.1),    # 10% 쿠폰
                    AmountCouponPolicy(2000)  # 2,000원 쿠폰
                ]
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 50,000 -> 40,000(할인) -> 36,000(10% 쿠폰) -> 34,000(2,000원 쿠폰)
            assert final_price == 34000

    def context_final_price_never_negative():
        def it_never_returns_negative_price():
            # Given
            product = Product(
                id=6,
                name="상품F",
                price=1000,
                discount_policy=AmountDiscountPolicy(2000),  # 2,000원 할인
                coupon_policies=[AmountCouponPolicy(5000)]   # 5,000원 쿠폰
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 1,000 -> 0(할인) -> 0(쿠폰, 음수 방지)
            assert final_price == 0