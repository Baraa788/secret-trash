from mysql.connector import Error
from database import get_db_connection


def get_random_bank():
    """DB سحب بنك وهمي واحد عشوائياً من"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM banks ORDER BY RAND() LIMIT 1")
        return cursor.fetchone()

    except Error as err:
        print(f"❌ Database Error (Fetching Bank): {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_player_stats(player_id, earned_reward, used_attempts):
    """تحديث نقاط اللاعب وعدد محاولاته من داتا بأما"""
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
        print(f" Database Error (Updating Stats): {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def generate_hint(secret_code, guess):

    exact_matches = []
    misplaced_digits = []

    # 1. فحص الأرقام الصحيحة في مكانها الصحيح، والأرقام الموجودة في مكان خاطئ
    for i in range(4):
        if guess[i] == secret_code[i]:
            exact_matches.append(
                f"Digit #{i+1} [{guess[i]}] -> EXACT MATCH (Locked in!)."
            )
        elif guess[i] in secret_code:
            misplaced_digits.append(
                f"Digit [{guess[i]}] -> PRESENT in PIN, but wrong position!"
            )

    # 2. تحليل البصمة الرقمية للكود السري (Metadata)
    digits_list = [int(d) for d in secret_code]
    total_sum = sum(digits_list)
    even_count = sum(1 for d in digits_list if d % 2 == 0)
    odd_count = 4 - even_count
    min_digit = min(digits_list)
    max_digit = max(digits_list)

    print("\n" + "-" * 50)
    print("🕵️‍♂️ [DECRYPTION ANALYZER - SYSTEM LEAK]:")

    # عرض تطابق الأرقام
    if exact_matches:
        for msg in exact_matches:
            print(f"   ✅ {msg}")
    if misplaced_digits:
        # استخدام set لمنع تكرار الرسالة لنفس الرقم
        for msg in set(misplaced_digits):
            print(f"   ⚠️ {msg}")
    if not exact_matches and not misplaced_digits:
        print("   ❌ Zero digits matched the firewall signature.")

    # عرض التلميحات الاستخباراتية الإضافية
    print("\n📡 [METADATA INTEL]:")
    print(f"   • Sum of all 4 digits   : {total_sum}")
    print(f"   • Even vs Odd digits    : {even_count} Even / {odd_count} Odd")
    print(f"   • Digit Range (Min-Max) : Between {min_digit} and {max_digit}")
    print("-" * 50)


def play_heist(player):
    """إدارة جولة الاختراق الكاملة مع لوب المحاولات الثلاث"""
    bank = get_random_bank()
    if not bank:
        print(" Unable to load target systems right now.")
        return player

    secret_code = bank["secret_code"]
    chances = 4
    attempts_used = 0

    print("\n" + "=" * 50)
    print(f"🎯 TARGET SYSTEM: {bank['bank_name']}")
    print(f"💰 BOUNTY REWARD: {bank['reward']} Points")
    print("🔐 SECURITY PROTOCOL: 4-digit numeric PIN (0-9 only).")
    print(f"⏳ ATTEMPTS AVAILABLE: You have {chances} chances to breach the vault!")
    print("=" * 50)

    while chances > 0:
        guess = input(f"\n[Chances Left: {chances}] Enter 4-digit PIN: ").strip()

        if not guess.isdigit() or len(guess) != 4:
            print(" INVALID INPUT! Please enter exactly 4 numeric digits (e.g., 1234).")
            continue

        attempts_used += 1
        chances -= 1

        if guess == secret_code:
            print(f"\n🎉 ACCESS GRANTED! You successfully hacked {bank['bank_name']}!")
            print(f"💵 {bank['reward']} Points have been added to your account.")

            update_player_stats(player["id"], bank["reward"], attempts_used)
            player["score"] += bank["reward"]
            player["attempts"] += attempts_used
            return player

        if chances > 0:
            print("❌ ACCESS DENIED! Incorrect PIN.")
            generate_hint(secret_code, guess)

    print("\n🚨 SYSTEM LOCKDOWN! Alarm triggered. You failed the heist.")
    print(f"🔑 The correct PIN was: {secret_code}")

    update_player_stats(player["id"], 0, attempts_used)
    player["attempts"] += attempts_used
    return player
