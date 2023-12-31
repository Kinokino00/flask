from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)
books = {1: "Python book", 2: "Java book", 3: "Flask book"}
url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
counties = None
ascending = True
df = None


@app.route("/")  # app可隨意取名，/代表首頁
# @app.route("/index")  # /index代表index頁
def index():
    today = get_now()
    print(today)  # print只能在終端機看到
    return render_template("index.html", today=today)


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route("/pm25-chart")
def pm25_chart():
    global counties
    df = pd.read_csv(url).dropna()
    counties = list(set(df["county"]))
    # counties = [counties for county in counties if county != six_county[0]]  #把不是新北市的先留下
    # counties.insert(0, six_county[0])  #再塞入新北市到第一位
    lowest = df.sort_values("pm25").iloc[0][["site", "pm25"]].values
    highest = df.sort_values("pm25").iloc[-1][["site", "pm25"]].values
    return render_template(
        "/pm25-charts-bulma.html",
        datetime=get_now(),
        counties=counties,
        lowest=lowest,
        highest=highest,
    )


@app.route("/pm25-json")  # 當API用，pm25-chart.html會呼叫他
def get_pm25_json():
    global df, counties  # 表示這邊的df是可拉到全域給大家用
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
    df = pd.read_csv(url).dropna()

    six_county = ["新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市"]
    six_data = {}
    for county in six_county:
        six_data[county] = round(
            df.groupby("county").get_group(county)["pm25"].mean(), 2
        )

    json_data = {
        "title": "PM2.5數據",
        "xData": df["site"].tolist(),
        "yData": df["pm25"].tolist(),
        "six_data": six_data,
        "county": counties[0],  # 預設選到的縣市是第一個縣市
    }
    return json.dumps(json_data, ensure_ascii=False)  # 轉成json


@app.route("/county-pm25-json/<county>")
def get_county_pm25_json(county):
    global df  # 呼叫全域
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
    pm25 = {}
    try:
        if df is None:
            df = pd.read_csv(url).dropna()
        pm25 = (
            df.groupby("county")
            .get_group(county)[["site", "pm25"]]
            .set_index("site")
            .to_dict()["pm25"]
        )
        success = True
        message = "資料取得成功!"
    except Exception as e:
        print(e)
        success = False
        message = str(e)
    json_data = {
        "datetime": get_now(),
        "success": success,
        "title": county,
        "pm25": pm25,
        "message": message,
    }
    return json.dumps(json_data, ensure_ascii=False)


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    global ascending
    now = get_now()
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
    return render_template("books.html", books=books, today=get_now())


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
