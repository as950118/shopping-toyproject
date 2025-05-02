from product.domain.model import Product
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
            product = Product(product_id=1, name="상품A", price=10000)
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 10000

    def context_with_single_rate_discount():
        def it_applies_single_rate_discount():
            # Given
            product = Product(
                product_id=2,
                name="상품B",
                price=20000,
                discount_policies=[RateDiscountPolicy(0.1)]  # 10% 할인
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 18000

    def context_with_multiple_discounts():
        def it_applies_multiple_discounts_in_order():
            # Given
            product = Product(
                product_id=3,
                name="상품C",
                price=30000,
                discount_policies=[
                    RateDiscountPolicy(0.1),      # 10% 할인: 30,000 -> 27,000
                    AmountDiscountPolicy(2000),   # 2,000원 할인: 27,000 -> 25,000
                    RateDiscountPolicy(0.2),      # 20% 할인: 25,000 -> 20,000
                ]
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 30,000 -> 27,000 (10%) -> 25,000 (-2,000) -> 20,000 (20%)
            assert final_price == 20000

    def context_with_multiple_discounts_and_coupons():
        def it_applies_multiple_discounts_and_coupons_in_order():
            # Given
            product = Product(
                product_id=4,
                name="상품D",
                price=50000,
                discount_policies=[
                    AmountDiscountPolicy(5000),   # 50,000 -> 45,000
                    RateDiscountPolicy(0.1),      # 45,000 -> 40,500
                ],
                coupon_policies=[
                    RateCouponPolicy(0.05),       # 40,500 -> 38,475
                    AmountCouponPolicy(3000),     # 38,475 -> 35,475
                ]
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 50,000 -> 45,000 (-5,000) -> 40,500 (10%) -> 38,475 (5% 쿠폰) -> 35,475 (-3,000)
            assert final_price == 35475

    def context_with_multiple_discounts_and_multiple_coupons():
        def it_applies_all_discounts_and_coupons_in_order():
            # Given
            product = Product(
                product_id=5,
                name="상품E",
                price=100000,
                discount_policies=[
                    RateDiscountPolicy(0.2),      # 100,000 -> 80,000
                    AmountDiscountPolicy(10000),  # 80,000 -> 70,000
                ],
                coupon_policies=[
                    RateCouponPolicy(0.1),        # 70,000 -> 63,000
                    AmountCouponPolicy(5000),     # 63,000 -> 58,000
                    RateCouponPolicy(0.05),       # 58,000 -> 55,100
                ]
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            # 100,000 -> 80,000 (20%) -> 70,000 (-10,000) -> 63,000 (10%) -> 58,000 (-5,000) -> 55,100 (5%)
            assert final_price == 55100

    def context_final_price_never_negative():
        def it_never_returns_negative_price():
            # Given
            product = Product(
                product_id=6,
                name="상품F",
                price=1000,
                discount_policies=[
                    AmountDiscountPolicy(2000),   # 1,000 -> 0
                    RateDiscountPolicy(0.5),      # 0 -> 0
                ],
                coupon_policies=[
                    AmountCouponPolicy(5000),     # 0 -> 0
                    RateCouponPolicy(0.5),        # 0 -> 0
                ]
            )
            # When
            final_price = product.calculate_final_price()
            # Then
            assert final_price == 0