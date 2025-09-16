from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# DB에서 제품 데이터 가져오기 함수
def get_products():
    conn = sqlite3.connect("kream_products.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT category, brand, product_name,price FROM kream_products")
    rows = cur.fetchall()
    conn.close()
    # rows를 dict 형태로 변환하여 반환
    return [dict(row) for row in rows]

# admin 페이지 route
@app.route("/")
def admin():
    return render_template("adminpage.html")

# signup 페이지 route
@app.route("/signup")
def signup():
    return render_template("signup.html")

# products API route (db에서 데이터 가져오기)
@app.route("/products")
def products_api(): 
    return jsonify(get_products())

if __name__ == "__main__":
    app.run(debug=True)