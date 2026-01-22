import sqlite3
import random
import string
from flask import Flask , request

MODE = "sqli_base"
# MODE = "bsqli"
# MODE = "safe"

app = Flask(__name__)
DB_NAME = "demo_sql.db"

#filter
def filter(user_id_input):
    if " " in user_id_input:
        return None
    return user_id_input

#Tạo database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor= conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    for i in range(1 , 101):
        ten_user = f"nhanvien_{i}"
        mat_khau = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{ten_user}', '{mat_khau}')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return '''
        <h1>HÃY NHẬP ID NHÂN VIÊN MÀ BẠN YÊU THÍCH <3</h1>
        <form action="/search" method="GET">
            Nhập ID nhân viên: <input type="text" name="id">
            <input type="submit" value="Tra cứu">
        </form>
    '''
#Tạo sqli
@app.route("/search")
def search():
    user_id_input = request.args.get('id', '')
    user_id_input = filter(user_id_input)
    if user_id_input is None:
        return "<h1> Định khai thác à , ko cóa đâu</h1>"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    def query_sqlbase( cursor , user_id_input):
        sql = f"SELECT * FROM users WHERE id = {user_id_input}" #cộng chuỗi trục tiếp
        cursor.execute(sql)
        return cursor.fetchall()
    def query_bsqlbase( cursor , user_id_input):
        sql = f"SELECT * FROM users WHERE id = {user_id_input}"
        cursor.execute(sql)
        return cursor.fetchone()
    def query_safe( cursor , user_id_input):
        
        cursor.execute(f"SELECT * FROM users WHERE id = ?" , (user_id_input,)) #sử dụng ? thế chỗ và input cho vào tuple
        return cursor.fetchall()
    try:
        if MODE == "sqli_base":
            ket_qua = query_sqlbase(cursor , user_id_input)
            html = f"<h3> Danh sách người dùng</h3>"
            if ket_qua:
                for user in ket_qua:
                    html += f"<p>ID : {user[0]} | username : {user[1]}</p>"
            else:
                    html += "<p>Not found</p>"
            return html
        elif MODE == "bsqli":
            ket_qua2 = query_bsqlbase( cursor , user_id_input)
            if ket_qua2:
                return "<h1>Welcome</h1>"
            else:
                return "<h1>khum cóa</h1>"
        else:
            ket_qua3 = query_safe( cursor , user_id_input)
            return "<h1> Làm gì có sqli haha</h1>"
        
        
            
    except Exception as e:
        return f"Lỗi {e}"
    finally:
        conn.close()
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
