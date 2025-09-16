from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql

browser = webdriver.Chrome()

link_list = [
    "https://kream.co.kr/search?tab=44", # 신발
    "https://kream.co.kr/search?tab=46", # 패션잡화
    "https://kream.co.kr/search?tab=50", # 상의
    "https://kream.co.kr/search?tab=51" # 하의
]

products = []

for link in link_list:
    browser.get(link)
    time.sleep(2)

    # 카테고리 확인
    category = browser.find_element(By.CSS_SELECTOR, "a.tab.active").find_element(By.CLASS_NAME, "tab_name").text
    print("*"*10, "현재 수집중인 카테고리:", category, "*"*10)

    # 제품 전체 불러오기
    product_cards = browser.find_elements(By.CLASS_NAME, "product_card")

    for card in product_cards:
        brand = card.find_element(By.CSS_SELECTOR, "p.product_info_brand > span.brand-name").text
        product_name = card.find_element(By.CSS_SELECTOR, "div.product_info_product_name > p.name").text
        price = card.find_element(By.CSS_SELECTOR, "p.amount > span").text

        products.append({
            "카테고리": category,
            "브랜드": brand,
            "제품명": product_name,
            "가격": price
        })

browser.quit()  # 브라우저 종료
print("크롤링 완료, 총 수집 제품 수:", len(products))


# 데이터 베이스 연동 후 -> 수집한 데이터를 DB에 저장

# DB 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cur:
    cur.execute("CREATE DATABASE IF NOT EXISTS Kream")
    cur.execute("USE Kream")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS kream_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        brand VARCHAR(150),
        product_name VARCHAR(300),
        price VARCHAR(50)
    )
    """)

    sql = """
    INSERT INTO kream_products (category, brand, product_name, price)
    VALUES (%s, %s, %s, %s)
    """
    for item in products:
        cur.execute(sql, (
            item['카테고리'],
            item['브랜드'],
            item['제품명'],
            item['가격']
        ))

conn.commit()
conn.close()
print("DB 저장 완료")