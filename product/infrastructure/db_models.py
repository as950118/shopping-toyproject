from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class DiscountType(enum.Enum):
    RATE = "rate"      # 정률 할인
    AMOUNT = "amount"  # 정액 할인

class CouponType(enum.Enum):
    RATE = "rate"
    AMOUNT = "amount"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)

    # 1:1 관계 (상품별 할인 정책)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=True)
    discount = relationship("Discount", back_populates="product", uselist=False)

    # 1:N 관계 (상품별 여러 쿠폰)
    coupons = relationship("Coupon", back_populates="product")

class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(DiscountType), nullable=False)
    value = Column(Float, nullable=False)  # rate(0.0~1.0) 또는 amount(정수)

    # 역참조
    product = relationship("Product", back_populates="discount", uselist=False)

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(CouponType), nullable=False)
    value = Column(Float, nullable=False)  # rate(0.0~1.0) 또는 amount(정수)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="coupons")