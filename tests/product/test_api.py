from fastapi.testclient import TestClient
from main import app  # FastAPI 앱 인스턴스

client = TestClient(app)


def test_list_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # 추가 검증: 상품 개수, 필드 등


def test_get_product_detail():
    pass
    # TODO 현재는 데이터 없음
    # response = client.get("/products/1")
    # assert response.status_code == 200
    # data = response.json()
    # assert data["id"] == 1
    # assert "final_price" in data


def test_get_product_detail_not_found():
    response = client.get("/products/0")
    assert response.status_code == 404
