from mysql.connector import Error
from database import get_db_connection


def get_random_bank():
    """سحب بنك وهمي  عشوائياً db"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM banks ORDER BY RAND() LIMIT 1")
        return cursor.fetchone()
    except Error as err:
        print(f"Database Error (Fetching Bank): {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_player_stats(player_id, earned_reward, used_attempts):
    """تحديث نقاط اللاعب وعدد محاولاته ب قاعدة البيانات بأمان"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        UPDATE players 
        SET score = score + %s, attempts = attempts + %s 
        WHERE id = %s
        """
        cursor.execute(query, (earned_reward, used_attempts, player_id))
        connection.commit()
    except Error as err:
        print(f"Database Error (Updating Stats): {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_player_by_id(player_id):
    """جلب أحدث بيانات اللاعب لتحديث الواجهة"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, score, attempts FROM players WHERE id = %s",
            (player_id,),
        )
        return cursor.fetchone()
    except Error as err:
        print(f"Database Error (Fetching Player): {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def analyze_guess(secret_code, guess):
    """تحليل تخمين اللاعب وإرجاع التلميحات كبيانات"""
    exact_matches = []
    misplaced_digits = []

    for i in range(4):
        if guess[i] == secret_code[i]:
            exact_matches.append(
                f"Digit #{i+1} [{guess[i]}] -> EXACT MATCH (Locked in!)"
            )
        elif guess[i] in secret_code:
            misplaced_digits.append(
                f"Digit [{guess[i]}] -> PRESENT in PIN, wrong position!"
            )

    digits_list = [int(d) for d in secret_code]

    return {
        "exact": exact_matches,
        "misplaced": list(set(misplaced_digits)),
        "sum": sum(digits_list),
        "even": sum(1 for d in digits_list if d % 2 == 0),
        "odd": 4 - sum(1 for d in digits_list if d % 2 == 0),
        "min": min(digits_list),
        "max": max(digits_list),
    }
