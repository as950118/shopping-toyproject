from typing import List, Optional
from abc import ABC, abstractmethod
from product.domain.models import Product


# 입력 포트: 상품 유스케이스 인터페이스
class ProductUseCase(ABC):
    @abstractmethod
    def list_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_product_detail(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def calculate_final_price(self, product_id: int) -> Optional[int]:
        pass
