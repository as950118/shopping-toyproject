from typing import List, Optional

from sqlalchemy.orm import Session

from product.adapter.outbound.db_models import (
    ProductEntity,
    CouponEntity,
    DiscountType,
    CouponType,
)
from product.domain.models import Product
from product.domain.policy import (
    DiscountPolicy,
    CouponPolicy,
    RateDiscountPolicy,
    AmountDiscountPolicy,
    RateCouponPolicy,
    AmountCouponPolicy,
)
from product.port.outbound.repository import ProductRepository


def to_discount_policy(discount_orm: Optional[ProductEntity]) -> Optional[DiscountPolicy]:
    if not discount_orm:
        return None
    if discount_orm.type == DiscountType.RATE:
        return RateDiscountPolicy(discount_orm.value)
    elif discount_orm.type == DiscountType.AMOUNT:
        # value가 float이므로 int로 변환
        return AmountDiscountPolicy(int(discount_orm.value))
    return None


def to_coupon_policy(coupon_orm: CouponEntity) -> CouponPolicy:
    if coupon_orm.type == CouponType.RATE:
        return RateCouponPolicy(coupon_orm.value)
    elif coupon_orm.type == CouponType.AMOUNT:
        # value가 float이므로 int로 변환
        return AmountCouponPolicy(int(coupon_orm.value))
    raise ValueError("Unknown coupon type")


def to_domain(product_orm: ProductEntity) -> Product:
    discount_policy = to_discount_policy(product_orm.discount)
    coupon_policies = [to_coupon_policy(c) for c in product_orm.coupons]
    return Product(
        product_id=product_orm.id,
        name=product_orm.name,
        price=product_orm.price,
        discount_policy=discount_policy,
        coupon_policies=coupon_policies,
    )


class SQLAlchemyProductRepository(ProductRepository):
    """
    SQLAlchemy 기반 ProductRepository 구현체
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        products = self.db.query(ProductEntity).all()
        return [to_domain(p) for p in products]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        # 경고 띄워서 타입 힌트 추가
        product: Optional[ProductEntity] = self.db.query(ProductEntity).filter(ProductEntity.id == product_id).first()
        if product:
            return to_domain(product)
        return None

    def save(self, product: Product) -> Product:
        # 단순 예시: 새 Product만 저장 (업데이트 미구현)
        product_orm = ProductEntity(
            name=product.name,
            price=product.price,
        )
        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return to_domain(product_orm)
