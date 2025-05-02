import pytest

from product.application.service import ProductService
from product.domain.models import Product
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
                discount_policy=RateDiscountPolicy(0.1)),
        Product(product_id=3, name="상품C", price=15000,
                discount_policy=AmountDiscountPolicy(3000)),
        Product(product_id=4, name="상품D", price=30000,
                discount_policy=RateDiscountPolicy(0.2),
                coupon_policies=[AmountCouponPolicy(5000)]),
        Product(product_id=5, name="상품E", price=50000,
                discount_policy=AmountDiscountPolicy(10000),
                coupon_policies=[RateCouponPolicy(0.1), AmountCouponPolicy(2000)]),
        Product(product_id=6, name="상품F", price=1000,
                discount_policy=AmountDiscountPolicy(2000),
                coupon_policies=[AmountCouponPolicy(5000)]),
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
    assert price == 18000


def test_calculate_final_price_with_amount_discount(service):
    price = service.calculate_final_price(3)
    assert price == 12000


def test_calculate_final_price_with_discount_and_coupon(service):
    price = service.calculate_final_price(4)
    assert price == 19000


def test_calculate_final_price_with_multiple_coupons(service):
    price = service.calculate_final_price(5)
    assert price == 34000


def test_calculate_final_price_never_negative(service):
    price = service.calculate_final_price(6)
    assert price == 0


def test_calculate_final_price_product_not_found(service):
    price = service.calculate_final_price(999)
    assert price is None
