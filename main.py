from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)
books = {1: "Python book", 2: "Java book", 3: "Flask book"}
ascending = True


@app.route("/")  # app可隨意取名，/代表首頁
# @app.route("/index")  # /index代表index頁
def index():
    today = datetime.now()
    print(today)  # print只能在終端機看到
    return render_template("index.html", today=today)


@app.route("/pm25-json")  # 當API用，pm25-chart.html會呼叫他
def get_pm25_json():
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
    df = pd.read_csv(url).dropna()
    json_data = {
        "title": "PM2.5數據",
        "xData": df["site"].tolist(),
        "yData": df["pm25"].tolist(),
    }
    return json.dumps(json_data, ensure_ascii=False)  # 轉成json


@app.route("/pm25-chart")
def pm25_chart():
    return render_template("/pm25-chart.html")


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    global ascending
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sort = False
    # 確定回傳方式
    if request.method == "POST":
        # 判斷在html點的是否為排序鈕，要用request要記得import
        print(request.form)
        if request.form.get("sort"):
            sort = True
    print(sort)
    try:
        df = pd.read_csv(url).dropna()
        # 升降序功能
        if sort:
            df = df.sort_values("pm25", ascending=ascending)
            ascending = not ascending
        else:
            ascending = True
        columns = df.columns.tolist()
        values = df.values.tolist()
        lowest = df.sort_values("pm25").iloc[0][["site", "pm25"]].values
        highest = df.sort_values("pm25").iloc[-1][["site", "pm25"]].values
        message = "取得資料成功"
        print(df["pm25"].max())
    except Exception as e:
        print(e)
        message = "取得 PM 2.5 資料失敗，請稍後再試..."
    return render_template("pm25.html", **locals())


@app.route("/books")
def get_all_books():
    today = datetime.now()
    books = {
        1: {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
        },
        2: {
            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
        },
        3: {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
        },
    }
    return render_template("books.html", books=books, today=today)


# id為變數，URL上的都是字串用int轉型成數字
# 預設方法為GET，可不寫
@app.route("/books/id=<int:id>", methods=["GET"])
def get_book(id):
    try:
        return f"<h1>{books[id]}<h1>"
    except Exception as e:
        print(e)
    return "<h1>書籍編號不正確</h1>"


@app.route("/bmi/name=<name>&height=<height>&weight=<weight>")
def get_bmi(name, height, weight):
    bmi = round(eval(weight) / (eval(height) / 100) ** 2, 2)
    return {"name": name, "height": height, "weight": weight, "bmi": bmi}


if __name__ == "__main__":
    app.run(debug=True)  # 運行，正式發布時debug=True要拿掉
