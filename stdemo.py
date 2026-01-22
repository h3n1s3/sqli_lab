import random
from flask import Flask , request
import string
import pyodbc

app = Flask(__name__)
SERVER = "DESKTOP-81QF8E8\SQLEXPRESS"
DB_NAME = "lab_sqli"
CONN_STR = (
    "DRIVER={SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
)

def init_db():
    #connect sever
    conn_server = pyodbc.connect(
        f"DRIVER={{SQL Server}};"
        f"SERVER={SERVER};",
        autocommit=True
    )
    cursor_server = conn_server.cursor()
    #tạo db
    cursor_server.execute(f"""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_NAME}')
    BEGIN
        CREATE DATABASE {DB_NAME}
    END
    """)
    cursor_server.close()
    conn_server.close()
    

    #connect db
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    # tạo bảng users
    cursor.execute("""
    IF NOT EXISTS (
        SELECT * FROM sysobjects WHERE name='users' AND xtype='U'
    )
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50),
        password NVARCHAR(50),
        role NVARCHAR(20)
    )
    """)
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count < 100:
        for i in range(1, 121):
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                f"user{i}",
                f"pass{i}",
                "admin" if i == 1 else "user"
            )
        conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def index():
    return """
    <h2>Danh sách tra cứu người dùng </h2>
    <p>Nhập bất kì điều gì bạn muốn</p>

    <form action="/user" method="get">
        <input type="text" name="id" placeholder="e.g. 1">
        <button type="submit">Search</button>
    </form>

    <p>Hint</p>
    <ul>
        <li>Hãy thử gì đó ở input</li>
    </ul>
    """
@app.route("/user")
def get_user():
    uid = request.args.get("id")

    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        query = f"SELECT username FROM users WHERE id = {uid}"
        cursor.execute(query)
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        if not row:
            return "Not found!"
        result = "<br>".join([str(r[0]) for r in row])
        return result

    except Exception as e:
        return f"SQL Error: {e}"
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0" , port = 5001 , debug=True)





