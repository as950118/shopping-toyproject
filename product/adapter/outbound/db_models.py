from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Enum, Table, Text, DateTime, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


# 정책 적용 대상 타입
class PolicyTargetType(enum.Enum):
    ALL = "all"
    USER = "user"
    GROUP = "group"
    PRODUCT = "product"
    CATEGORY = "category"
    BRAND = "brand"
    # 필요시 추가


class DiscountType(enum.Enum):
    RATE = "rate"
    AMOUNT = "amount"
    # 기타 정책 타입 추가 가능


class CouponType(enum.Enum):
    RATE = "rate"
    AMOUNT = "amount"
    # 기타 정책 타입 추가 가능


# Product-Discount N:M 관계 테이블
product_discount_table = Table(
    "product_discount",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("discount_id", Integer, ForeignKey("discounts.id"), primary_key=True),
)

# Product-Coupon N:M 관계 테이블 (기존과 동일)
product_coupon_table = Table(
    "product_coupon",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("coupon_id", Integer, ForeignKey("coupons.id"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)

    # N:M 관계로 변경
    discounts = relationship(
        "Discount",
        secondary=product_discount_table,
        back_populates="products"
    )
    coupons = relationship(
        "Coupon",
        secondary=product_coupon_table,
        back_populates="products"
    )


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(DiscountType), nullable=False)
    value = Column(Float, nullable=False)  # rate(0.0~1.0) 또는 amount(정수)

    # 정책 적용 대상
    target_type = Column(Enum(PolicyTargetType), nullable=True)  # 예: "user", "category", "all"
    target_value = Column(String(100), nullable=True)  # 예: user_id, category_id 등

    # 자주 쓰는 정책 속성 컬럼화
    is_active = Column(Boolean, default=True)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
    min_purchase_amount = Column(Integer, nullable=True)
    max_discount_amount = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    # EAV 구조 확장
    attributes = relationship("DiscountAttribute", back_populates="discount")

    # N:M 관계
    products = relationship(
        "Product",
        secondary=product_discount_table,
        back_populates="discounts"
    )


class DiscountAttribute(Base):
    __tablename__ = "discount_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=False)
    name = Column(String(50), nullable=False)  # 예: "rate", "amount", "start_date", "target_user"
    value = Column(Text, nullable=False)  # 문자열로 저장, 필요시 파싱

    discount = relationship("Discount", back_populates="attributes")


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(CouponType), nullable=False)
    value = Column(Float, nullable=False)  # rate(0.0~1.0) 또는 amount(정수)

    # 정책 적용 대상
    target_type = Column(Enum(PolicyTargetType), nullable=True)
    target_value = Column(String(100), nullable=True)

    # 자주 쓰는 정책 속성 컬럼화
    is_active = Column(Boolean, default=True)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)
    min_purchase_amount = Column(Integer, nullable=True)
    max_discount_amount = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    # EAV 구조 확장
    attributes = relationship("CouponAttribute", back_populates="coupon")

    # N:M 관계
    products = relationship(
        "Product",
        secondary=product_coupon_table,
        back_populates="coupons"
    )


class CouponAttribute(Base):
    __tablename__ = "coupon_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False)
    name = Column(String(50), nullable=False)  # 예: "rate", "amount", "start_date", "target_user"
    value = Column(Text, nullable=False)

    coupon = relationship("Coupon", back_populates="attributes")
