# 쇼핑몰 상품 관리 API

## 1. 프로젝트 개요

**쇼핑몰 상품 관리 API**는 상품의 리스트 조회, 상세 페이지에서의 가격 계산(할인/쿠폰/최종가 적용) 등 핵심 기능을 제공하는 API입니다.  
비즈니스 로직과 프레젠테이션 로직의 분리, 도메인 중심 설계, 확장성, API 응답 구조의 유연성에 중점을 두었습니다.

---

## 2. 주요 기능

- **상품 리스트 조회**
- **상품 상세 조회 및 가격 계산**
    - 할인율 적용
    - 쿠폰 적용
    - 위 조건들에 따른 최종 판매가 계산

---

## 3. 설계 의도 및 구조 설명

### 3.1 비즈니스 로직과 프레젠테이션 로직 분리

- **헥사고날(클린) 아키텍처**를 적용하여 아래와같이 분리하였습니다.
    - 도메인/비즈니스 로직(`product/domain`, `product/application`)
    - 프레젠테이션(API, `product/api`)
    - 인프라스트럭처(DB, `product/infrastructure`)

### 3.2 확장 가능성

- **정책 패턴(Strategy Pattern)**을 활용하여 할인/쿠폰 정책을 추상화
- 새로운 할인/쿠폰 정책이 추가될 때 도메인 정책 클래스만 추가하면 됨
- 도메인 객체와 정책 객체의 결합도를 낮춰, 정책 변경/확장에 유연하게 대응

### 3.3 도메인 중심 설계

- **Product(상품)**, **Discount(할인)**, **Coupon(쿠폰)** 등 핵심 도메인 모델을 명확히 식별
- 도메인 객체는 ORM, API 스키마와 분리된 **순수 Python 클래스**로 구현
- 할인/쿠폰 정책은 각각의 Policy 인터페이스 및 구현체로 분리

### 3.4 API 응답 구조와 버전 관리

- API 응답은 Pydantic 스키마로 명확히 정의
- Enum, Optional 필드 등을 활용해 정책 변경 시에도 클라이언트 호환성 유지
- 추후 버전 관리(v1, v2 등) 및 정책 확장에 유연하게 대응할 수 있는 구조

---

## 4. 폴더 구조 및 핵심 코드 설명

```
shopping-toyproject/
├── main.py # FastAPI 앱 실행 및 라우터 등록 
├── database.py # DB 연결 및 세션 관리
│ ├── product/
│ ├── domain/ # 도메인 엔티티, 정책(Strategy) 등
│ │ ├── models.py
│ │ └── policy.py
│ ├── application/ # 서비스(유스케이스), 포트(인터페이스)
│ │ ├── service.py
│ │ └── port.py
│ ├── infrastructure/ # DB 모델, 리포지토리 구현
│ │ ├── db_models.py
│ │ └── repository.py
│ ├── api/ # FastAPI 라우터, Pydantic 스키마
│ │ ├── router.py
│ │ └── schemas.py
│ ├── tests/ # 단위/통합 테스트
│ │ ├── test_product_service.py
│ │ └── schemas.py
│ └── README.md # 프로젝트 설명 (본 파일)
```

### 핵심 코드 설명

- **domain/models.py**: Product 등 순수 도메인 엔티티 정의
- **domain/policy.py**: 할인/쿠폰 정책 인터페이스 및 구현체
- **application/service.py**: 비즈니스 유스케이스(상품 조회, 가격 계산 등)
- **application/port.py**: 입력/출력 포트(서비스/리포지토리 인터페이스)
- **infrastructure/db_models.py**: SQLAlchemy ORM 모델
- **infrastructure/repository.py**: DB 접근 및 도메인 객체 변환
- **api/schemas.py**: Pydantic 기반 API 요청/응답 스키마
- **api/router.py**: FastAPI 라우터(엔드포인트)
- **tests/**: 서비스/도메인/엔드포인트 단위 테스트

---

## 5. 도메인 모델링

- **Product**: 상품의 고유 ID, 이름, 가격, 할인/쿠폰 정책을 보유
- **DiscountPolicy/CouponPolicy**: 할인/쿠폰 정책의 추상화 및 구현체(정률, 정액 등)
- **정책 적용 순서**: 할인 → 쿠폰(여러 개 순차 적용) → 최종가 산출

---

## 6. API 명세서 (예시)

| 메서드 | 경로                       | 설명                  | 요청/응답 스키마         |
|--------|----------------------------|-----------------------|--------------------------|
| GET    | `/products/`               | 상품 리스트 조회      | ProductResponseSchema[]  |
| GET    | `/products/{id}`           | 상품 상세 조회        | ProductResponseSchema    |
| POST   | `/products/`               | 상품 생성             | ProductCreateSchema      |
| GET    | `/products/{id}/final-price` | 상품 최종가 계산     | int                      |

---

## 7. 테스트 코드

- **핵심 비즈니스 로직(가격 계산 등)은 서비스/도메인 단위 테스트로 검증**
- **API 엔드포인트는 FastAPI TestClient로 통합 테스트 가능**
- BDD 스타일 테스트도 지원

---

## 8. 기술 스택

- **언어**: Python 3.9
- **프레임워크**: FastAPI
- **DB**: MySQL 8.0 (SQLAlchemy ORM)
- **테스트**: pytest, pytest-describe (BDD 지원)
- **기타**: Pydantic, Uvicorn

---

## 9. 실행 방법

의존성 설치
```bash
pip install -r requirements.txt
```
DB 설정 및 마이그레이션
(예: Alembic, 직접 테이블 생성 등)
서버 실행
```bash
uvicorn main:app --reload
```
테스트 실행
```bash
pytest
```