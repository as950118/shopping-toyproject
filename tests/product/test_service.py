import pytest

from product.application.service import ProductService
from product.domain.model import Product
from product.domain.policy import RateDiscountPolicy, AmountDiscountPolicy, RateCouponPolicy, AmountCouponPolicy
from product.port.outbound.repository import ProductRepository


# In-memory repository 구현
class InMemoryProductRepository(ProductRepository):
    def __init__(self, products=None):
        self._products = {p.product_id: p for p in (products or [])}

    def get_all(self):
        return list(self._products.values())

    def get_by_id(self, product_id):
        return self._products.get(product_id)

    def save(self, product):
        self._products[product.product_id] = product


@pytest.fixture
def sample_products():
    return [
        Product(product_id=1, name="상품A", price=10000),
        Product(product_id=2, name="상품B", price=20000,
                discount_policies=[RateDiscountPolicy(0.1)]),  # 10% 할인
        Product(product_id=3, name="상품C", price=15000,
                discount_policies=[AmountDiscountPolicy(3000)]),  # 3,000원 할인
        Product(product_id=4, name="상품D", price=30000,
                discount_policies=[RateDiscountPolicy(0.2)],
                coupon_policies=[AmountCouponPolicy(5000)]),  # 20% 할인 후 5,000원 쿠폰
        Product(product_id=5, name="상품E", price=50000,
                discount_policies=[AmountDiscountPolicy(10000)],
                coupon_policies=[RateCouponPolicy(0.1), AmountCouponPolicy(2000)]),  # 10,000원 할인 후 10% 쿠폰, 2,000원 쿠폰
        Product(product_id=6, name="상품F", price=1000,
                discount_policies=[AmountDiscountPolicy(2000)],
                coupon_policies=[AmountCouponPolicy(5000)]),  # 할인/쿠폰 합쳐서 음수 방지
        Product(product_id=7, name="상품G", price=30000,
                discount_policies=[RateDiscountPolicy(0.1), AmountDiscountPolicy(2000), RateDiscountPolicy(0.2)],
                coupon_policies=[RateCouponPolicy(0.05), AmountCouponPolicy(3000)]),  # 여러 할인/쿠폰 조합
    ]


@pytest.fixture
def service(sample_products):
    repo = InMemoryProductRepository(sample_products)
    return ProductService(repo)


def test_list_products(service, sample_products):
    products = service.list_products()
    assert len(products) == len(sample_products)
    assert {p.product_id for p in products} == {p.product_id for p in sample_products}


def test_get_product_detail(service):
    product = service.get_product_detail(2)
    assert product is not None
    assert product.name == "상품B"
    assert product.price == 20000


def test_calculate_final_price_no_discount_no_coupon(service):
    price = service.calculate_final_price(1)
    assert price == 10000


def test_calculate_final_price_with_rate_discount(service):
    price = service.calculate_final_price(2)
    assert price == 18000  # 20,000 * 0.9


def test_calculate_final_price_with_amount_discount(service):
    price = service.calculate_final_price(3)
    assert price == 12000  # 15,000 - 3,000


def test_calculate_final_price_with_discount_and_coupon(service):
    price = service.calculate_final_price(4)
    # 30,000 * 0.8 = 24,000, 24,000 - 5,000 = 19,000
    assert price == 19000


def test_calculate_final_price_with_multiple_coupons(service):
    price = service.calculate_final_price(5)
    # 50,000 - 10,000 = 40,000, 40,000 * 0.9 = 36,000, 36,000 - 2,000 = 34,000
    assert price == 34000


def test_calculate_final_price_never_negative(service):
    price = service.calculate_final_price(6)
    # 1,000 - 2,000 = 0, 0 - 5,000 = 0
    assert price == 0


def test_calculate_final_price_with_multiple_discounts_and_coupons(service):
    price = service.calculate_final_price(7)
    # 30,000 * 0.9 = 27,000, 27,000 - 2,000 = 25,000, 25,000 * 0.8 = 20,000
    # 20,000 * 0.95 = 19,000, 19,000 - 3,000 = 16,000
    assert price == 16000


def test_calculate_final_price_product_not_found(service):
    price = service.calculate_final_price(999)
    assert price is None