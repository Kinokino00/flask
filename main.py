from flask import Flask
from datetime import datetime

app = Flask(__name__)
books = {1: "Python book", 2: "Java book", 3: "Flask book"}


@app.route("/")  # app可隨意取名，/代表首頁
@app.route("/index")  # /index代表index頁
def index():
    today = datetime.now()
    print(today)  # print只能在終端機看到
    return f"<h1>HELLO! {today}</h1>"


@app.route("/books")
def get_all_books():
    return books


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
    # try:
    # input("name=")
    # input("height=")
    # input("weight=")
    bmi = round(eval(weight) / (eval(height) / 100) ** 2, 2)
    return {"name": name, "height": height, "weight": weight, "bmi": bmi}


#     return f"{name} BMI:{bmi}"
# except Exception as e:
#     return "參數錯誤"


if __name__ == "__main__":
    app.run(debug=True)  # 運行，正式發布時debug=True要拿掉
