import getpass
from database import init_db
from security import register_player, login_player
from game_logic import play_heist


def show_player_dashboard(player):
    """القائمة الداخلية للاعب بعد تسجيل الدخول بنجاح"""
    while True:
        print("\n" + "=" * 50)
        print(
            f"🕵️‍♂️ AGENT: {player['username']} | 💰 SCORE: {player['score']} | 🎯 ATTEMPTS: {player['attempts']}"
        )
        print("=" * 50)
        print("1. 🚀 Start New Bank Heist")
        print("2. 📊 View My Stats")
        print("3. 🔒 Logout (Return to Main Menu)")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            player = play_heist(player)

        elif choice == "2":
            print("\n--- 📊 AGENT PROFILE ---")
            print(f"Username       : {player['username']}")
            print(f"Total Score    : {player['score']} Points")
            print(f"Total Attempts : {player['attempts']}")
            print("------------------------")

        elif choice == "3":
            print(f"\n👋 Logging out... Stay safe, Agent {player['username']}!")
            break

        else:
            print("⚠️ Invalid choice! Please enter 1, 2, or 3.")


def main():
    """نقطة الانطلاق الرئيسية للعبة"""
    print("🔄 Initializing Cyber Heist Security Systems...")
    init_db()

    while True:
        print("\n" + "*" * 50)
        print("💻 WELCOME TO CYBER HEIST: THE VAULT BREAKER 💻")
        print("*" * 50)
        print("1. 🆕 New Player? Create Account & Play Immediately")
        print("2. 🔑 Returning Player? Login to Your Account")
        print("3. ❌ Exit Game")

        choice = input("\nChoose an action (1-3): ").strip()

        if choice == "1":
            print("\n--- 🆕 NEW AGENT REGISTRATION ---")
            username = input("Choose a Username: ").strip()
            password = getpass.getpass(
                "Choose a Password (hidden while typing): "
            ).strip()

            # إذا تم إنشاء الحساب بنجاح، نسجل دخوله تلقائياً وننقله للوحة اللعب فوراً
            if register_player(username, password):
                print("⚡ Auto-logging into your new agent dashboard...")
                player = login_player(username, password)
                if player:
                    show_player_dashboard(player)

        elif choice == "2":
            print("\n--- 🔑 RETURNING AGENT LOGIN ---")
            username = input("Username: ").strip()
            password = getpass.getpass("Password (hidden while typing): ").strip()

            player = login_player(username, password)
            if player:
                show_player_dashboard(player)

        elif choice == "3":
            print("\n🔌 Disconnecting from server. Goodbye!")
            break

        else:
            print("⚠️ Invalid option! Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
