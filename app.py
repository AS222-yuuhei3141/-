from crypt import methods
from flask import Flask, render_template, request
from cs50 import SQL
import random

app = Flask("__name__")
db = SQL("sqlite:///foodname.db")

@app.route("/", methods=["GET","POST"])
def index():
    if (request.method == "GET"):
        return render_template("input.html")
    else:
        # 一人当たりの必要摂取カロリー
        age = request.form.get("age")
        intAge = int(age)
        weight = request.form.get("weight")
        intWeight = int(weight)
        height = request.form.get("height")
        intHeight = int(height)
        budget = request.form.get("budget")
        intBudget = int(budget)
        # 性別
        sex = request.form.get("sex")
        # 活動レベル
        level = request.form.get("level")
        # 目的
        activity = request.form.get("activity")


    #とりあえず、仮で決める。
        # 朝で摂取したエネルギー + 昼で摂取したエネルギー
        # 男性:1800 (kcal)
        # 女性:1350 (kcal)

# --------------------------------------------------------------------
# 一人当たりの必要摂取カロリー
# act = b * o * g [kcal]
# --------------------------------------------------------------------
        # 基礎代謝(B)の計算
            # 男性： 10×体重kg＋6.25×身長cmー5×年齢＋5
            # 女性： 10×体重kg+6.25×身長cmー５×年齢-16
        b = 0
        # 「活動量を入れた代謝量」を求めるために掛ける値
        oDict = {"one":1.2,"two":1.55,"three":1.725}
        # G(食事の目的)
        gDict ={"増量":1.2,"現状維持":1.0,"減量":0.8}
        # bo: b * o　のこと
        bo = 0

        if (sex == "男"):
            b = 10 * intWeight + 6.25 * intHeight - 5 * intAge + 5
            # boを計算する
            if (level == "one"):
                bo = b * oDict["one"]
            elif (level == "two"):
                bo = b * oDict["two"]
            elif (level == "three"):
                bo = b * oDict["three"]
            # actを計算する。
            if (activity == "増量"):
                act = bo * gDict["増量"]
            elif (activity == "現状維持"):
                act = bo * gDict["現状維持"]
            elif (activity == "減量"):
                act = bo * gDict["減量"]


        if (sex == "女"):
            b = 10 * intWeight + 6.25 * intHeight - 5 * intAge - 16
            # boを計算する
            if (level == "one"):
                bo = b * oDict["one"]
            elif (level == "two"):
                bo = b * oDict["two"]
            elif (level == "three"):
                bo = b * oDict["three"]
            # actを計算する。
            if (activity == "増量"):
                act = bo * gDict["増量"]
            elif (activity == "現状維持"):
                act = bo * gDict["現状維持"]
            elif (activity == "減量"):
                act = bo * gDict["減量"]

#---------------------------------------------------------------------


# --------------------------------------------------------------------
# D = act - (朝で摂取したエネルギー + 昼で摂取したエネルギー) [kcal]
# --------------------------------------------------------------------

    #とりあえず、仮で決める。
    # 朝で摂取したエネルギー + 昼で摂取したエネルギー
        # 男性:1800 (kcal)
        # 女性:1350 (kcal)
        total = 0
        fDicts = request.form.getlist("select_food")
        for fDict in fDicts:
            total += int(fDict)

        if (sex == "男"):
            D = act - total

        elif (sex == "女"):
            D = act - total

# --------------------------------------------------------------------

        # return render_template("test.html", D=D)
        data = db.execute("SELECT * FROM foodnames WHERE カロリー < ?", D)

        return render_template("output.html", data = data)


@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    if request.method == "POST":
        breakfast = request.form.get("breakfast")
        lunch = request.form.get("lunch")
        snack = request.form.get("snack")
        sql = "SELECT * FROM 食品成分 WHERE 食品名 like ?"
        if len(breakfast) != 0:
            brName = db.execute(sql, "%" + breakfast + "%")
        else:
            brName = ''
        if len(lunch) != 0:
            luName = db.execute(sql, "%" + lunch + "%")
        else:
            luName = ''
        if len(snack) != 0:
            snName = db.execute(sql, "%" + snack + "%")
        else:
            snName = ''
        return render_template("input.html", breakfast=brName, lunch=luName, snack=snName)


@app.route("/select_item", methods=["GET", "POST"])
def select_item():
    if request.method == "POST":
        total = 0
        fDicts = request.form.getlist("select_food")
        for fDict in fDicts:
            total += fDict['エネルギー']
        return render_template("input.html")



@app.route("/back")
def back():
    return render_template("input.html")


