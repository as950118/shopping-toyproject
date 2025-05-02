-- 상품 데이터
INSERT INTO products (id, name, price) VALUES
                                           (1, '에어컨', 500000),
                                           (2, '노트북', 1200000),
                                           (3, '커피머신', 250000);

-- 할인 정책 데이터
INSERT INTO discounts (id, type, value, is_active, description)
VALUES
    (1, 'rate', 0.10, TRUE, '여름맞이 10% 할인'),
    (2, 'amount', 50000, TRUE, '노트북 5만원 할인'),
    (3, 'rate', 0.20, TRUE, '커피머신 20% 할인');

-- 쿠폰 데이터
INSERT INTO coupons (id, type, value, is_active, description)
VALUES
    (1, 'amount', 20000, TRUE, '신규회원 2만원 쿠폰'),
    (2, 'rate', 0.05, TRUE, '5% 추가 할인 쿠폰'),
    (3, 'amount', 10000, TRUE, '커피머신 1만원 쿠폰');

-- 상품-할인 관계 (N:M)
INSERT INTO product_discount (product_id, discount_id) VALUES
                                                           (1, 1), -- 에어컨에 10% 할인
                                                           (2, 2), -- 노트북에 5만원 할인
                                                           (3, 3); -- 커피머신에 20% 할인

-- 상품-쿠폰 관계 (N:M)
INSERT INTO product_coupon (product_id, coupon_id) VALUES
                                                       (1, 1), -- 에어컨에 신규회원 쿠폰
                                                       (1, 2), -- 에어컨에 5% 쿠폰
                                                       (2, 1), -- 노트북에 신규회원 쿠폰
                                                       (2, 2), -- 노트북에 5% 쿠폰
                                                       (3, 3), -- 커피머신에 1만원 쿠폰
                                                       (3, 2); -- 커피머신에 5% 쿠폰

-- (옵션) 할인/쿠폰 속성 테이블은 필요시 추가로 삽입

-- 이제 이 데이터로 전체 API/서비스/엔드포인트 통합 테스트가 가능합니다.