import mysql.connector
from mysql.connector import Error


def get_db_connection():

    return mysql.connector.connect(
        host="localhost", user="root", password="", database="cyber_heist_db"
    )


def init_db():

    connection = None
    cursor = None
    try:
        # 1. الاتصال بالسيرفر المحلي
        connection = mysql.connector.connect(host="localhost", user="root", password="")

        if connection.is_connected():
            cursor = connection.cursor()

            # 2. إنشاء قاعدة البيانات والدخول إليها
            cursor.execute("CREATE DATABASE IF NOT EXISTS cyber_heist_db")
            cursor.execute("USE cyber_heist_db")

            # 3 (Players)
            create_players_table = """
            CREATE TABLE IF NOT EXISTS players (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                score INT DEFAULT 0,
                attempts INT DEFAULT 0
            )
            """
            cursor.execute(create_players_table)

            # 4.(Banks)
            create_banks_table = """
            CREATE TABLE IF NOT EXISTS banks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bank_name VARCHAR(100) UNIQUE NOT NULL,
                secret_code VARCHAR(4) NOT NULL,
                reward INT NOT NULL
            )
            """
            cursor.execute(create_banks_table)

            # 5. إضافة بنوك وهمية افتراضية للبدء (INSERT IGNORE يمنع التكرار عند إعادة التشغيل)
            insert_banks_query = """
            INSERT IGNORE INTO banks (bank_name, secret_code, reward) 
            VALUES (%s, %s, %s)
            """
            sample_banks = [
                ("البنك السويسري الرقمي", "4829", 500),
                ("خزنة البنك المركزي", "1094", 1000),
                ("بنك المستقبل الافتراضي", "7351", 300),
                ("محفظة التشفير الكبرى", "9026", 1500),
            ]
            cursor.executemany(insert_banks_query, sample_banks)

            connection.commit()
            print("✅ The database, tables, and fake banks were prepared successful")

    except Error as err:
        print(f"❌ : {err}")

    finally:

        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# تشغيل التهيئة عند تنفيذ الملف مباشرة
if __name__ == "__main__":
    init_db()
