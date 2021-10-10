from flask import Flask, render_template, request, g
from flask_paginate import Pagination, get_page_parameter
import sqlite3

app = Flask(__name__)


# DBと接続
def connect_db():
    conn = sqlite3.connect('./ex/chinook.db')
    return conn


@app.route("/ex0/")
def hello_world():
    return "Hello, World!"


@app.route('/ex1/', methods=["GET", "POST"])
def table():
    conn = connect_db()
    cur = conn.cursor()

    # 渡す変数
    items = []
    column_names = []
    column_count = 0
    table_names = []
    current_table = ''

    # データベース中のテーブル名を取得
    cur.execute(
        "SELECT name FROM sqlite_master WHERE TYPE='table'")
    result = cur.fetchall()
    for table_name in result:
        table_names.append(str(table_name).replace(
            '(', '').replace(')', '').replace(',', '').replace('"', '').replace("'", ""))

    # テーブル名取得
    if request.method == 'GET':
        first_table = table_names[0]
        current_table = request.args.get('table_name', '%s' % (first_table))
        # テーブルデータの取得
        cur.execute("SELECT * FROM %s" % (current_table))
        items = cur.fetchall()
        column_names = list(map(lambda x: x[0], cur.description))
        column_count = len(column_names)

    return render_template('index.html', items=items, column_names=column_names, column_count=column_count, current_table=current_table, table_names=table_names)


@app.route('/ex2/', methods=["GET", "POST"])
def paging():
    conn = connect_db()
    cur = conn.cursor()

    # 渡す変数
    items = []
    column_names = []
    column_count = 0
    table_names = []
    current_table = ''

    # データベース中のテーブル名を取得
    cur.execute(
        "SELECT name FROM sqlite_master WHERE TYPE='table'")
    tables = cur.fetchall()
    for table_name in tables:
        table_names.append(str(table_name).replace(
            '(', '').replace(')', '').replace(',', '').replace('"', '').replace("'", ""))

    # テーブル名取得
    if request.method == 'GET':
        first_table = table_names[0]
        current_table = request.args.get('table_name', '%s' % (first_table))

    # テーブルデータの取得
    cur.execute("SELECT * FROM %s" % (current_table))
    result = cur.fetchall()
    column_names = list(map(lambda x: x[0], cur.description))
    column_count = len(column_names)

    per_page = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)
    items = result[(page - 1)*per_page: page*per_page]
    pagination = Pagination(page=page, total=len(
        result),  per_page=per_page, css_framework='bootstrap4')

    print(page)
    print(items)
    print(column_names)

    return render_template('paging.html', items=items, pagination=pagination, column_names=column_names, column_count=column_count, current_table=current_table, table_names=table_names)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
