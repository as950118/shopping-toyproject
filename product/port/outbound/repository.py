from abc import ABC, abstractmethod
from typing import List, Optional

from product.domain.models import Product


# 출력 포트: 상품 저장소(Repository) 인터페이스
class ProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass
