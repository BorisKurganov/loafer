import sqlite3

def sql_request(sql_req, var={}):
    """Принимает запрос и параметр метода execute, 
       возвращает ответ на sql запрос"""
    with sqlite3.connect('db.db') as conn:
        #получаем объект курсора
        c = conn.cursor()
        #получаем объект ответа на запрос к базе
        c.execute(sql_req, var)
        result = c.fetchall()
        c.close()
        conn.commit()
    return result

def get_score(user_id):
    """Возвращает очки пользователя по id"""
    return sql_request("""SELECT scores
                          FROM users
                          WHERE id = :index""", {"index": user_id})[0][0]

def write_in_base(name, email, password, score):
    """Делает запись в базу данных"""
    user_data = (name, email, password, score)
    sql_request("""INSERT INTO users
                   (name, email, password, scores) 
                    values (?, ?, ?, ?)""", user_data)

def get_user(name, email, password):
    """Извлекает из базы данные о пользователе"""
    return sql_request("""SELECT *
                          FROM users
                          WHERE name = ? AND email = ? AND password = ?""",
                           (name, email, password))

def update_score(scores, user_id):
    sql_request("""UPDATE users SET scores = ? WHERE id = ?""",
                                                    (scores, user_id))

def get_top():
    """Возвращаёт топ 10 из базы"""
    return sql_request("""SELECT name, scores
                          FROM users
                          ORDER BY scores DESC LIMIT 10""")
