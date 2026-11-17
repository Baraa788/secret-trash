import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from security import register_player, login_player
from game_logic import (
    get_random_bank,
    update_player_stats,
    get_player_by_id,
    analyze_guess,
)

app = Flask(__name__)
# مفتاح سري عشوائي لتشفير جلسات المستخدمين وحمايتها من التلاعب
app.secret_key = secrets.token_hex(24)

init_db()


def start_new_mission():
    """تهيئة جولة اختراق جديدة وحفظ تفاصيلها في جلسة اللاعب"""
    bank = get_random_bank()
    if bank:
        session["current_bank"] = {
            "name": bank["bank_name"],
            "reward": bank["reward"],
            "secret_code": bank["secret_code"],  # محفوظة في السيرفر فقط ولا ترسل للـ
        }
        session["chances"] = 4
        session["attempts_used"] = 0
        session["last_hint"] = None
        session["game_over"] = False
        session["status_message"] = None


@app.route("/", methods=["GET"])
def index():
    """الصفحة الرئيسية.. توجه اللاعب للوحة التحكم إذا كان مسجل أو لصفحة الدخول"""
    if "player_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/auth", methods=["POST"])
def auth():
    """معالجة تسجيل الحساب الجديد والدخول التلقائي.. أو تسجيل الدخول للعائدين"""
    action = request.form.get("action")
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        flash("⚠️ Please enter both username and password.", "error")
        return redirect(url_for("index"))

    if action == "register":
        if register_player(username, password):
            # دخول فور نجاح التسجيل
            player = login_player(username, password)
            if player:
                session["player_id"] = player["id"]
                start_new_mission()
                flash(
                    f" Welcome Agent {player['username']}! Account created & logged in.",
                    "success",
                )
                return redirect(url_for("dashboard"))
        else:
            flash(" Registration failed: Username may already exist.", "error")
            return redirect(url_for("index"))

    elif action == "login":
        player = login_player(username, password)
        if player:
            session["player_id"] = player["id"]
            start_new_mission()
            flash(
                f" Access Granted. Welcome back, Agent {player['username']}!", "success"
            )
            return redirect(url_for("dashboard"))
        else:
            flash(" Access Denied: Incorrect username or password.", "error")
            return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """شاشة اللعب الرئيسية ..ومعالجة محاولات الاختراق"""
    if "player_id" not in session:
        return redirect(url_for("index"))

    player = get_player_by_id(session["player_id"])
    if not player:
        session.clear()
        return redirect(url_for("index"))

    if "current_bank" not in session:
        start_new_mission()

    if request.method == "POST":
        # إذا طلب اللاعب بدء مهمة جديدة
        if "new_mission" in request.form:
            start_new_mission()
            return redirect(url_for("dashboard"))

        # معالجة تخمين الكود السري
        if not session.get("game_over", False):
            guess = request.form.get("guess", "").strip()

            # التحقق من صحة المدخلات (4 أرقام فقط)
            if not guess.isdigit() or len(guess) != 4:
                flash(" INVALID INPUT: Enter exactly 4 numeric digits (0-9).", "error")
                return redirect(url_for("dashboard"))

            session["attempts_used"] += 1
            session["chances"] -= 1
            secret_code = session["current_bank"]["secret_code"]
            #  الفوز
            if guess == secret_code:
                reward = session["current_bank"]["reward"]
                update_player_stats(player["id"], reward, session["attempts_used"])
                session["game_over"] = True
                session["last_hint"] = None
                session["status_message"] = {
                    "type": "win",
                    "text": f"🎉 ACCESS GRANTED! You breached {session['current_bank']['name']} and earned +{reward} Points!",
                }
                return redirect(url_for("dashboard"))

            #  الخطأ مع بقاء محاولات
            if session["chances"] > 0:
                session["last_hint"] = analyze_guess(secret_code, guess)
                flash(
                    " ACCESS DENIED! Incorrect PIN. Check the Decryption Analyzer below.",
                    "error",
                )
            else:
                #  (الخسارة)
                update_player_stats(player["id"], 0, session["attempts_used"])
                session["game_over"] = True
                session["last_hint"] = None
                session["status_message"] = {
                    "type": "lose",
                    "text": f"SYSTEM LOCKDOWN! Alarm triggered. The correct PIN was [{secret_code}].",
                }

            return redirect(url_for("dashboard"))

    return render_template(
        "dashboard.html",
        player=player,
        bank=session.get("current_bank"),
        chances=session.get("chances"),
        hint=session.get("last_hint"),
        game_over=session.get("game_over"),
        status=session.get("status_message"),
    )


@app.route("/logout")
def logout():
    """تسجيل الخروج.. ومسح الجلسة بأمان"""
    session.clear()
    flash(" Securely disconnected from server.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
