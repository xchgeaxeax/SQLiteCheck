from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# 鉴权密码
AUTH_PASSWORD = "password"

# SQLite数据库连接
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()


# 查询密码
def get_passwords(username):
    c.execute("SELECT PASSWORD FROM access where USERNAME = ?", (username,))
    # passwords = [row[0] for row in c.fetchall()]
    passwords = c.fetchall()
    return passwords


# 主页路由
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 检查鉴权密码
        password = request.form.get("password")
        if password == AUTH_PASSWORD:
            # 查询用户名和密码
            username = request.form.get("username")
            passwords = get_passwords(username)
            return render_template("result.html", username=username, passwords=passwords)
        else:
            return render_template("index.html", error="Invalid password")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
