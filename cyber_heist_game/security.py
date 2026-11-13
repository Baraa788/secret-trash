import hashlib
import secrets
import mysql.connector
from mysql.connector import Error
from database import get_db_connection


def hash_password(password):
    """OWASP"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
    return f"{salt}:{pwd_hash}"


def verify_password(stored_password, provided_password):
    """التحقق ب تطابق كلمة المرور المدخلة مع المشفرة"""
    try:
        salt, original_hash = stored_password.split(":")
        new_hash = hashlib.pbkdf2_hmac(
            "sha256", provided_password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return secrets.compare_digest(original_hash, new_hash)
    except ValueError:
        return False


def register_player(username, password):
    """تسجيل لاعب جديد في db"""
    # التحقق من أن الحقول ليست فارغة
    if not username.strip() or not password.strip():
        print("enter information ..not null")
        return False

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        hashed_pwd = hash_password(password)

        # استعلام مجهزة (%s) لمنع الـ SQL Injection تماماً
        query = "INSERT INTO players (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_pwd))
        connection.commit()

        print(
            f"The player account '{username}' has been successfully and securely created!"
        )
        return True

    except mysql.connector.IntegrityError:
        print("This username is already in use, choose another one.")
        return False
    except Error as err:
        print(f"error in data base :{err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def login_player(username, password):
    """التحقق من بيانات دخول اللاعب وإرجاع بياناته كامله"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        # dictionary=True تجعل النتيجة تعود كقاموس يسهل قراءة أعمدته بالاسم
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM players WHERE username = %s"
        cursor.execute(query, (username,))
        player = cursor.fetchone()

        if player and verify_password(player["password"], password):
            print(f"\n Welcome back, hacker'{username}'!")
            return player
        else:
            print("\nIncorrect username or password")
            return None

    except Error as err:
        print(f" Login error {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
