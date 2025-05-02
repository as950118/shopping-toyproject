from abc import ABC, abstractmethod


# 정책의 최상위 인터페이스
class Policy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int:
        pass


# 할인 정책 인터페이스. 추후 확장 고려.
class DiscountPolicy(Policy, ABC):
    pass


# 쿠폰 정책 인터페이스. 추후 확장 고려.
class CouponPolicy(Policy, ABC):
    pass


# 퍼센트 할인 정책 예시
class RateDiscountPolicy(DiscountPolicy):
    def __init__(self, rate: float):
        if not (0.0 <= rate <= 1.0):
            raise ValueError("rate must be between 0.0 and 1.0")
        self.rate = rate  # 0.0 ~ 1.0

    def apply(self, price: int) -> int:
        return int(price * (1 - self.rate))


# 금액 할인 정책 예시
class AmountDiscountPolicy(DiscountPolicy):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, price: int) -> int:
        return max(price - self.amount, 0)


# 퍼센트 쿠폰 정책 예시
class RateCouponPolicy(CouponPolicy):
    def __init__(self, rate: float):
        if not (0.0 <= rate <= 1.0):
            raise ValueError("rate must be between 0.0 and 1.0")
        self.rate = rate  # 0.0 ~ 1.0

    def apply(self, price: int) -> int:
        return int(price * (1 - self.rate))


# 금액 쿠폰 정책 예시
class AmountCouponPolicy(CouponPolicy):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, price: int) -> int:
        return max(price - self.amount, 0)