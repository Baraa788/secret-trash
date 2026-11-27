from database import get_connection


def set_budget(amount):
    """تحديث الحد الأقصى للميزانية الشهرية"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE budget SET monthly_limit = %s WHERE id = 1", (amount,))
    conn.commit()
    cursor.close()
    conn.close()


def add_expense(amount, category, description):
    """إضافة عملية صرف جديدة إلى قاعدة البيانات"""
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (amount, category, description) VALUES (%s, %s, %s)"
    cursor.execute(query, (amount, category, description))
    conn.commit()
    cursor.close()
    conn.close()


def delete_expense(expense_id):
    """حذف مصروف معين باستخدام رقم المعرف (ID)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_dashboard_data():
    """جلب البيانات وحساب الملخص المالي وحالة الميزانية"""
    conn = get_connection()
    # dictionary=True تخلي النتائج ترجع كـ قاموس (Key: Value) بدل Tuple لسهولة التعامل
    cursor = conn.cursor(dictionary=True)

    # 1. جلب الميزانية
    cursor.execute("SELECT monthly_limit FROM budget WHERE id = 1")
    budget_row = cursor.fetchone()
    monthly_limit = float(budget_row["monthly_limit"]) if budget_row else 0.0

    # 2. جلب جميع المصاريف مرتبة من الأحدث للأقدم
    cursor.execute("SELECT * FROM expenses ORDER BY created_at DESC")
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    # 3. منطق الحسابات ببايثون
    total_spent = sum(float(item["amount"]) for item in expenses)
    remaining = monthly_limit - total_spent

    # 4. تحديد حالة التنبيه بناءً على نسبة الصرف
    alert_status = "safe"
    alert_message = "wad3ak el mali moumtaz w demn el mizeniyeh"

    if monthly_limit > 0:
        usage_percent = (total_spent / monthly_limit) * 100
        if usage_percent >= 100:
            alert_status = "danger"
            alert_message = "lakad ta5atayt el mizanieh el chahriye el mou7adadeh!"
        elif usage_percent >= 80:
            alert_status = "warning"
            alert_message = f"lakad ist5damta   {usage_percent:.0f}%  mn al mizeniyeh."

    return {
        "monthly_limit": monthly_limit,
        "total_spent": total_spent,
        "remaining": remaining,
        "expenses": expenses,
        "alert_status": alert_status,
        "alert_message": alert_message,
    }


# اختبار سريع للمنطق قبل ربطه بـ Flask
if __name__ == "__main__":
    set_budget(1000)
    add_expense(150, "food", "lunch with freind")
    data = get_dashboard_data()
    print("📊  experience summary:", data)
