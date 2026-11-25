import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "connection_timeout": 5,
}


def init_db():

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker_db")
    cursor.close()
    conn.close()

    # 2. الاتصال بقاعدة البيانات الجديدة لإنشاء الجداول
    conn = get_connection()
    cursor = conn.cursor()

    # جدول المصاريف
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            description VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # جدول الميزانية
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INT PRIMARY KEY DEFAULT 1,
            monthly_limit DECIMAL(10, 2) NOT NULL DEFAULT 0.00
        )
    """)

    # إدخال ميزانية افتراضية (0) إذا كان الجدول فاضي
    cursor.execute("INSERT IGNORE INTO budget (id, monthly_limit) VALUES (1, 0.00)")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ tmm tajhiz DB bnaja7 !")


def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database="expense_tracker_db",
        connection_timeout=5,
    )


if __name__ == "__main__":
    init_db()
