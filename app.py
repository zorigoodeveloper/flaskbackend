import os, json
import psycopg2
from flask import Flask, request, jsonify


app = Flask(__name__)

connection = psycopg2.connect(user = 'postgres',
    password = 'dbpass',
    host = '127.0.0.1',
    port = '5433',
    database = 'db_employee')

# buh salariin medeelel haruulah
@app.route('/api/branch', methods=['GET'])
def get_branches():
    with connection:
        with connection.cursor() as cur:
            cur.execute("""
                SELECT * FROM public.tbl_branch
            """)
            result = cur.fetchall()
            keys = [i[0] for i in cur.description]
            rows = [dict(zip(keys, values)) for values in result]
    return jsonify(branches=rows)

# 1 salbariin medeelel haruulah
@app.route('/api/branch/<int:id>', methods=['GET'])
def get_branch(id):
    with connection:
        with connection.cursor() as cur:
            cur.execute(f"""
            SELECT * FROM public.tbl_branch WHERE bid = {id} """)
            result = cur.fetchall()
            keys = [i[0] for i in cur.description]
            rows = [dict(zip(keys, values)) for values in result]
    return jsonify(rows)

# shine salbar nemeh
@app.route('/api/branch/create', methods=['POST'])
def create_branch():
    with connection:
        with connection.cursor() as cur:
            bname = request.get_json()['bname']
            cur.execute(f"""INSERT INTO tbl_branch (bname) VALUES ('{bname}') """)
            try:
                connection.commit()
                return {"message": "Салбар амжилттай нэмлээ"}
            except:
                connection.rollback()
                return {"message": "Алдаа гарлаа"}

# salbar n medeellig zasah
@app.patch('/api/branch/edit/<int:id>')
def edit_branch(id):
    with connection:
        with connection.cursor() as cur:
            bname = request.get_json()['bname']
            cur.execute(f"""UPDATE tbl_branch SET bname ='{bname}' WHERE bid={id} """)
            try:
                connection.commit()
                return {"message": "Салбар амжилттай заслаа"}
            except:
                connection.rollback()
                return {"message": "Алдаа гарлаа"}

# salbar n medeelel ustgah
@app.put('/api/branch/delete/<int:id>')
def delete_branch(id):
    with connection:
        with connection.cursor() as cur:
            cur.execute(f"""DELETE FROM tbl_branch WHERE bid={id} """)
            try:
                connection.commit()
                return {"message": "Салбар амжилттай устгалаа"}
            except:
                connection.rollback()
                return {"message": "Алдаа гарлаа"}

if __name__ == '__main__':
    app.run(debug=True)
