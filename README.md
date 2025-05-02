# 쇼핑몰 상품 관리 API

## 1. 프로젝트 개요

**쇼핑몰 상품 관리 API**는 상품 리스트 조회, 상세 페이지에서의 가격 계산(할인/쿠폰/최종가 적용) 등 핵심 기능을 제공하는 API입니다.  
비즈니스 로직과 프레젠테이션 로직의 분리, 도메인 중심 설계, 확장성, API 응답 구조의 유연성에 중점을 두었습니다.

---

## 2. 주요 기능
- **상품 리스트 조회**
- **상품 상세 조회 및 가격 계산**
  - 할인율/정액 할인 정책 적용 (여러 개 가능)
  - 쿠폰 정책 적용 (여러 개 가능)
  - 위 조건들에 따른 최종 판매가 계산

---

## 3. 설계 의도 및 구조 설명

### 3.1 비즈니스 로직과 프레젠테이션 로직 분리

- **도메인/비즈니스 로직**: `product/domain`, `product/application`
- **포트**: `product/port`
- **어뎁터**: `product/adapter`
- **매퍼/스키마**: `product/application/schemas.py`, `product/application/mapper.py`

### 3.2 확장 가능성

- **정책 패턴(Strategy Pattern)**을 활용하여 할인/쿠폰 정책을 추상화
- 할인/쿠폰 정책은 N:N(다대다) 구조로 여러 상품에 적용 가능
- 정책별 다양한 속성(조건, 한도, 기간, 타겟 등) 확장 가능 (EAV 구조 지원)
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
│ │ ├── domain/
│ │ │ ├── model.py # 현재 도메인의 모델. product
│ │ │ └── policy.py
│ │ ├── application/
│ │ │ ├── service.py
│ │ │ ├── schemas.py
│ │ │ └── mapper.py
│ │ ├── adapter/
│ │ │ ├── inbound/
│ │ │ │ └── router.py
│ │ │ ├── outbound/
│ │ │ │ ├── db_models.py
│ │ │ └─└── repository.py
│ │ ├── port/
│ │ │ ├── inbound/
│ │ │ │ └── router.py
│ │ │ ├── outbound/
│ │ │ │ ├── db_models.py
│ │ └─└─└── repository.py
├── tests/
│ ├── test_product_service.py
│ └── test_product_api.py
└── README.md # 프로젝트 설명 (본 파일)
```

### 핵심 코드 설명

- **domain/models.py**: Product 등 순수 도메인 엔티티 정의
- **domain/policy.py**: 할인/쿠폰 정책 인터페이스 및 구현체
- **application/service.py**: 비즈니스 유스케이스(상품 조회, 가격 계산 등)
- **application/schemas.py**: Pydantic 기반 API 요청/응답 스키마
- **application/mapper.py**: 도메인 ↔ 스키마 변환 함수
- **adapter/outbound/db_models.py**: SQLAlchemy ORM 모델 (N:N, EAV 구조)
- **adapter/outbound/repository.py**: DB 접근 및 도메인 객체 변환
- **adapter/inbound/router.py**: FastAPI 라우터(엔드포인트)
- **tests/**: 서비스/도메인/엔드포인트 단위 및 통합 테스트

---

## 5. 도메인 모델링

- **Product**: 상품의 고유 ID, 이름, 가격, 여러 할인/쿠폰 정책을 보유
- **DiscountPolicy/CouponPolicy**: 할인/쿠폰 정책의 추상화 및 구현체(정률, 정액 등), N:N 구조
- **정책 적용 순서**: 여러 할인 → 여러 쿠폰(순차 적용) → 최종가 산출
- **정책 속성 확장**: 조건, 한도, 기간, 타겟 등 EAV 구조로 유연하게 확장 가능

---

## 6. API 명세서

| 메서드 | 경로                       | 설명                  | 요청/응답 스키마         |
|--------|----------------------------|-----------------------|--------------------------|
| GET    | `/products/`               | 상품 리스트 조회      | ProductResponseSchema[]  |
| GET    | `/products/{id}`           | 상품 상세 조회        | ProductResponseSchema    |
| POST   | `/products/`               | 상품 생성             | ProductCreateSchema      |
| GET    | `/products/{id}/final-price` | 상품 최종가 계산     | int                      |

---

## 7. 테스트 코드

- **서비스/도메인 통합 테스트**:
  - `tests/test_product_service.py`
  - BDD 스타일(`describe_`, `context_`, `it_`) 및 다양한 정책 조합 케이스 검증
- **API 엔드포인트 통합 테스트**:
  - `tests/test_product_api.py`
  - FastAPI TestClient로 실제 HTTP 요청/응답 검증
- **pytest-describe, pytest-spec** 등 BDD 지원 플러그인 사용

---

## 8. 기술 스택

- **언어**: Python 3.9+
- **프레임워크**: FastAPI
- **DB**: MySQL 8.0 (SQLAlchemy ORM, N:M/EAV 구조)
- **테스트**: pytest, pytest-describe, pytest-spec (BDD 지원)
- **기타**: Pydantic v2, Uvicorn, Docker

---

## 9. 실행 방법

의존성 설치
```bash
pip install -r requirements.txt
```

DB 및 앱 컨테이너 실행 (Docker)
```bash
docker-compose up --build
```
서버 실행 (로컬 개발)
```bash
uvicorn main:app --reload
```
테스트 실행
```bash
pytest
```
## 10. 기타
- DB 초기 데이터: initdb/init.sql에서 샘플 상품/정책/쿠폰 데이터 자동 삽입
- 확장성: 정책/쿠폰/상품 그룹/유저 조건 등 실무 이커머스 시나리오에 맞게 유연하게 확장 가능
- 정책/쿠폰 N:M 구조, EAV(Entity Attribute Value) 속성, BDD 테스트, Docker 기반 개발환경 등 실무 패턴 반영
- 여러 상품에 여러 할인이 존재할 수 있는지에 대한 고민이 있었으나, 우선은 확장성 위주로 고려하여 여러 할인 적용 가능