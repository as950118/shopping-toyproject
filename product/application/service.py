from typing import List, Optional
from product.domain.models import Product
from product.port.inbound.use_case import ProductUseCase
from product.port.outbound.repository import ProductRepository


class ProductService(ProductUseCase):
    """
    상품 관련 유스케이스(비즈니스 로직) 구현체.
    ProductRepository(출력 포트)에 의존하여 데이터 접근.
    """

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self) -> List[Product]:
        return self.repository.get_all()

    def get_product_detail(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def calculate_final_price(self, product_id: int) -> Optional[int]:
        product = self.repository.get_by_id(product_id)
        if product is None:
            return None
        return product.calculate_final_price()