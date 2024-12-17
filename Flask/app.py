from flask import Flask, jsonify, request
import sqlite3

DB_PATH = "cinema/cinema.db"
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        genre TEXT,
        poster TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        session_time TEXT NOT NULL,
        price REAL NOT NULL,
        tickets INTEGER NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        session_id INTEGER NOT NULL,
        tickets INTEGER NOT NULL,
        profit  INTEGER NOT NULL,
        seat_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE

    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        seat_id TEXT,
        available BOOL,
        FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()

app = Flask(__name__)



# АУТЕНТИФИКАЦИЯ ----------------------------------------------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        return jsonify({"message": "Login successful", "user_id": result[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# ПОЛЬЗОВАТЕЛИ ---------------------------------------------------------------------------

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    users_list = [{"id": user[0], "username": user[1], "password": user[2]} for user in users]
    return jsonify(users_list), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Удаление пользователя по ID
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "User not found"}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# ФИЛЬМЫ ------------------------------------------------------------------------------------

@app.route('/add_movie', methods=['POST'])
def add_movie():
    try:
        data = request.get_json()

        title = data.get('title')
        description = data.get('description', '')
        genre = data.get('genre', '')
        poster = data.get('poster')

        if not title or not poster:
            return jsonify({"error": "Invalid input. All fields are required."}), 400

        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO movies (title, description, genre, poster)
            VALUES (?, ?, ?, ?)
        """, (title, description, genre, poster))

        conn.commit()
        conn.close()

        return jsonify({"message": "Movie and sessions added successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()

        movie_list = []
        for movie in movies:
            movie_id, title, description, genre, poster = movie

            movie_list.append({
                "id": movie_id,
                "title": title,
                "description": description,
                "genre": genre,
                "poster": poster
            })

        conn.close()
        return jsonify(movie_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Movie deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# СЕАНСЫ ----------------------------------------------------------------------------------------

def calculate_rows_and_seats(total_seats, seats_per_row=10):
    rows = (total_seats // seats_per_row) + (1 if total_seats % seats_per_row != 0 else 0)
    return rows, seats_per_row

def create_seats_for_session(session_id, total_seats):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    rows, seats_per_row = calculate_rows_and_seats(total_seats)

    for row in range(rows):
        row_label = chr(65 + row)  # Логика для получения буквы для ряда (A, B, C...)
        for seat_number in range(1, seats_per_row + 1):
            # Генерируем seat_id для каждого места
            seat_id = f"{row_label}{seat_number}"
            cursor.execute("INSERT INTO seats (session_id, seat_id, available) VALUES (?, ?, ?)",
                           (session_id, seat_id, True))

    conn.commit()
    conn.close()


@app.route('/add_session', methods=['POST'])
def add_session():
    try:
        data = request.get_json()
        movie_id = data.get('movie_id')
        session_time = data.get('session_time')
        price = data.get('price')
        tickets = data.get('tickets')

        # Проверяем, что все необходимые данные предоставлены
        if not all([movie_id, session_time, price, tickets]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Подключаемся к базе данных
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Проверяем, существует ли фильм с указанным ID
        cursor.execute("SELECT id FROM movies WHERE id = ?", (movie_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Movie not found'}), 404

        # Добавляем сеанс
        cursor.execute("""
            INSERT INTO sessions (movie_id, session_time, price, tickets)
            VALUES (?, ?, ?, ?)
        """, (movie_id, session_time, price, tickets))
        session_id = cursor.lastrowid
        conn.commit()
        create_seats_for_session(session_id, tickets)
        conn.close()


        return jsonify({'message': 'Session added successfully'}), 201

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_sessions/<int:movie_id>', methods=['GET'])
def load_sessions(movie_id):
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Проверяем, существует ли фильм с указанным ID
        cursor.execute("SELECT id FROM movies WHERE id = ?", (movie_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Movie not found'}), 404

        # Получаем все сеансы для данного фильма
        cursor.execute("""
            SELECT id, session_time, price, tickets
            FROM sessions
            WHERE movie_id = ?
        """, (movie_id,))
        sessions = cursor.fetchall()

        conn.close()

        # Форматируем результат
        session_list = [
            {
                'session_id': session[0],
                'session_time': session[1],
                'price': session[2],
                'tickets': session[3]
            }
            for session in sessions
        ]

        return jsonify(session_list), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_session/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Delete session
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Session not found."}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": "Session deleted successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 501


# ПОКУПКИ ----------------------------------------------------------------------------

@app.route('/purchase/total', methods=['GET'])
def get_total_sales():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Получаем все продажи
        cursor.execute("""
            SELECT SUM(tickets), SUM(profit)
            FROM purchase
        """)
        result = cursor.fetchone()

        total_tickets = result[0] if result[0] else 0
        total_profit = result[1] if result[1] else 0

        conn.close()

        return jsonify({
            "total_tickets": total_tickets,
            "total_profit": total_profit
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/purchase/movie/<int:movie_id>', methods=['GET'])
def get_movie_sales(movie_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Получаем все продажи для конкретного фильма
        cursor.execute("""
            SELECT SUM(tickets), SUM(profit)
            FROM purchase
            WHERE movie_id = ?
        """, (movie_id,))
        result = cursor.fetchone()

        total_tickets = result[0] if result[0] else 0
        total_profit = result[1] if result[1] else 0

        conn.close()

        return jsonify({
            "total_tickets": total_tickets,
            "total_profit": total_profit
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/purchase/session/<int:session_id>', methods=['GET'])
def get_session_sales(session_id):
    report_type = request.args.get('report_type', 'summary')  # Получаем параметр report_type из запроса

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        if report_type == 'summary':
            # Получаем общую информацию по проданным билетам и прибыли
            cursor.execute("""
                SELECT SUM(tickets), SUM(profit)
                FROM purchase
                WHERE session_id = ?
            """, (session_id,))
            result = cursor.fetchone()

            total_tickets = result[0] if result[0] else 0
            total_profit = result[1] if result[1] else 0

            conn.close()

            return jsonify({
                "total_tickets": total_tickets,
                "total_profit": total_profit
            }), 200

        elif report_type == 'users':
            # Получаем информацию о пользователях, купивших билеты на сеанс
            cursor.execute("""
                SELECT
                    u.username,
                    SUM(p.tickets) AS total_tickets,
                    SUM(p.profit) AS total_profit,
                    GROUP_CONCAT(p.seat_name, ', ') AS seat_names
                FROM
                    purchase p
                JOIN
                    users u ON p.user_id = u.id
                WHERE
                    p.session_id = ?
                GROUP BY
                    u.username
            """, (session_id,))
            result = cursor.fetchall()

            if not result:
                return jsonify({"error": "No users found for this session"}), 404

            # Формируем список пользователей с количеством билетов и прибылью
            users_data = [
                {
                    "username": user[0],
                    "ticket_count": user[1],
                    "profit": user[2],
                    "seat_name": user[3]
                }
                for user in result
            ]

            conn.close()

            return jsonify({
                "users": users_data
            }), 200

        else:
            return jsonify({"error": "Invalid report_type. Use 'summary' or 'users'."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/purchase/tickets_by_movie', methods=['GET'])
def get_tickets_by_movie():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.title AS movie_title, SUM(p.tickets) AS tickets_sold
            FROM movies m
            LEFT JOIN sessions s ON m.id = s.movie_id
            LEFT JOIN purchase p ON s.id = p.session_id
            GROUP BY m.id
            ORDER BY tickets_sold DESC
        """)
        result = cursor.fetchall()
        conn.close()

        # Форматируем данные в список словарей
        data = [{"movie_title": row[0], "tickets_sold": row[1] or 0} for row in result]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_seats', methods=['GET'])
def get_seats():
    try:
        session_id = request.args.get('session_id')

        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT seat_id, available FROM seats WHERE session_id = ?", (session_id,))
        seats = cursor.fetchall()

        seats_data = [{"seat_id": seat[0], "available": seat[1]} for seat in seats]

        conn.close()

        return jsonify({"seats": seats_data}), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/purchase_ticket', methods=['POST'])
def purchase_ticket():
    try:
        data = request.get_json()
        username = data.get('username')
        seat_ids = data.get('seat_ids')  # Изменено: принимаем список seat_ids
        session_id = data.get('session_id')

        if not all([username, seat_ids, session_id]) or not isinstance(seat_ids, list) or not seat_ids:
            return jsonify({'error': 'Missing required fields or invalid seat_ids'}), 400

        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Получаем user_id по username
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()
        if not user_id:
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        user_id = user_id[0]

        # Проверяем, существует ли session_id
        cursor.execute("SELECT movie_id, price FROM sessions WHERE id = ?", (session_id,))
        session_data = cursor.fetchone()
        if not session_data:
            conn.close()
            return jsonify({'error': 'Session not found'}), 404
        movie_id, price = session_data

        tickets = 0
        profit = 0
        purchased_seats = []
        # Проверяем доступность каждого места и добавляем покупку
        for seat_id in seat_ids:
            cursor.execute("SELECT available FROM seats WHERE seat_id = ? AND session_id = ?", (seat_id, session_id))
            seat = cursor.fetchone()
            if not seat:
                conn.close()
                return jsonify({'error': f'Seat {seat_id} not found'}), 404
            if not seat[0]:  # Если место уже занято
                conn.close()
                return jsonify({'error': f'Seat {seat_id} is already booked'}), 400

            # Обновляем статус места на "занято"
            cursor.execute(
                "UPDATE seats SET available = ? WHERE seat_id = ? AND session_id = ?",
                (False, seat_id, session_id)
            )
            purchased_seats.append(seat_id)

            # Добавляем запись о покупке
            cursor.execute(
                """
                INSERT INTO purchase (user_id, movie_id, session_id, tickets, profit, seat_name)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, movie_id, session_id, 1, price, seat_id)
            )
            tickets += 1
            profit += price

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Tickets purchased successfully',
            'tickets': tickets,
            'purchased_seats': purchased_seats,
            'total_profit': profit
        }), 201

    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

@app.route('/user/purchases', methods=['GET'])
def get_user_purchases():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]

        # Получаем данные о покупках пользователя
        cursor.execute("""
            SELECT
                m.title AS movie_title,
                s.session_time AS session_time,
                SUM(p.tickets) AS ticket_count,
                SUM(p.profit) AS total_profit,
                GROUP_CONCAT(p.seat_name, ', ') AS seat_names
            FROM
                purchase p
            JOIN
                sessions s ON p.session_id = s.id
            JOIN
                movies m ON s.movie_id = m.id
            WHERE
                p.user_id = ?
            GROUP BY
                p.session_id
        """, (user_id,))

        purchases = cursor.fetchall()

        if not purchases:
            conn.close()
            return jsonify({"message": "No purchases found for this user"}), 200

        # Формируем ответ
        user_purchases = []
        for purchase in purchases:
            user_purchases.append({
                "movie_title": purchase[0],
                "session_time": purchase[1],
                "ticket_count": purchase[2],
                "total_profit": purchase[3],
                "seat_names": purchase[4]
            })

        conn.close()

        return jsonify({
            "username": username,
            "purchases": user_purchases
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500



@app.route('/')
def home():
    return 'Блять я заебался сука нахуй!'

if __name__ == '__main__':
    app.run(debug=True)
