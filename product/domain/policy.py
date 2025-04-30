from abc import ABC, abstractmethod

# 할인 정책 인터페이스
class DiscountPolicy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int:
        pass

# 쿠폰 정책 인터페이스
class CouponPolicy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int:
        pass

# 퍼센(%) 할인 정책 예시
class RateDiscountPolicy(DiscountPolicy):
    def __init__(self, rate: float):
        self.rate = rate  # 0.0 ~ 1.0

    def apply(self, price: int) -> int:
        return int(price * (1 - self.rate))

# 정액(고정금액) 할인 정책 예시
class AmountDiscountPolicy(DiscountPolicy):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, price: int) -> int:
        return max(price - self.amount, 0)

# 퍼센트(%) 쿠폰 정책 예시
class RateCouponPolicy(CouponPolicy):
    def __init__(self, rate: float):
        self.rate = rate  # 0.0 ~ 1.0

    def apply(self, price: int) -> int:
        return int(price * (1 - self.rate))

# 정액(고정금액) 쿠폰 정책 예시
class AmountCouponPolicy(CouponPolicy):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, price: int) -> int:
        return max(price - self.amount, 0)