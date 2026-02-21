import telebot
from telebot import types

TOKEN = "8377189184:AAEfSsEDH7TAeuBXbIXq4URtRh0O5kMl56I"
MY_ADMIN_ID = 5825392632
ALLOWED_USERS = [5825392632, 6724250074]

# ===== قنوات الاشتراك الإجباري =====
CHANNEL_1 = "@qZRuU5E_VVdhOWQ0"
CHANNEL_2 = "@le_Ghaith0000"

VIP_PRICE = "50 ليرة سورية"
CUSTOM_TABLE_PRICE = "حسب الطلب (حتى 500 ليرة سورية)"

PAYMENT_INFO = """
💳 طريقة الدفع:
سيرياتيل كاش

📱 الرقم:
0935949875

بعد التحويل اضغط زر الدفع ثم أرسل صورة الإيصال.
"""

bot = telebot.TeleBot(TOKEN)

waiting_for_receipt = {}

# =========================================
# ===== التحقق من الاشتراك =====
# =========================================

    # إذا المستخدم من الاستثناءات → يدخل فوراً
def check_subscription(user_id):

    # إذا المستخدم من الاستثناءات → يدخل فوراً
    if user_id in ALLOWED_USERS:
        return True

    try:
        ch1 = bot.get_chat_member(CHANNEL_1, user_id)
        ch2 = bot.get_chat_member(CHANNEL_2, user_id)

        if ch1.status in ["member", "administrator", "creator"] and \
           ch2.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except:
        return False


def send_force_sub(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📢 اشترك بالقناة الأولى",
            url="https://t.me/qZRuU5E_VVdhOWQ0"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "📢 اشترك بالقناة الثانية",
            url="https://t.me/le_Ghaith0000"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "✅ تحقق من الاشتراك",
            callback_data="check_sub"
        )
    )

    bot.send_message(
        chat_id,
        "🚫 تم إيقاف وصولك للبوت لأنك غير مشترك بإحدى القنوات.\n\nيرجى الاشتراك للمتابعة.",
        reply_markup=markup
    )


# =========================================
# ===== إرسال ملفات =====
# =========================================
def send_file(chat_id, file_path, file_type="document", caption=None):
    try:
        with open(file_path, "rb") as f:
            if file_type == "photo":
                bot.send_photo(chat_id, f, caption=caption)
            else:
                bot.send_document(chat_id, f, caption=caption)
    except Exception as e:
        bot.send_message(chat_id, "⚠️ حدث خطأ أثناء إرسال الملف.")
        print("ERROR:", e)


# =========================================
# ===== القائمة الرئيسية =====
# =========================================
def main_menu(chat_id, first_name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 متجر زاد")
    markup.add("📂 نماذج جداول مجانية")
    markup.add("💎 استشارة VIP")
    markup.add("🔄 إعادة تشغيل")

    bot.send_message(
        chat_id,
        f"أهلاً {first_name} 👋\n\nبوت التميز بخدمتك 🎓",
        reply_markup=markup
    )


# =========================================
# ===== start =====
# =========================================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    if check_subscription(user_id):
        main_menu(message.chat.id, message.from_user.first_name)
    else:
        send_force_sub(message.chat.id)


# =========================================
# ===== زر التحقق =====
# =========================================
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu(call.message.chat.id, call.from_user.first_name)
    else:
        bot.answer_callback_query(call.id, "❌ لم يتم الاشتراك بعد", show_alert=True)


# =========================================
# ===== منع الاستخدام إذا خرج من قناة =====
# =========================================
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id

    # تحقق بكل رسالة (إذا خرج من قناة ينمنع فوراً)
    if not check_subscription(user_id):
        send_force_sub(chat_id)
        return

    # إعادة تشغيل
    if text == "🔄 إعادة تشغيل":
        bot.send_message(chat_id, "♻️ تم تحديث البوت بنجاح!")
        main_menu(chat_id, message.from_user.first_name)

    # متجر
    elif text == "🛒 متجر زاد":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📝 دفتر الشهر")
        markup.add("📓 دفتر ملاحظات")
        markup.add("🔙 رجوع")
        bot.send_message(chat_id, "🛒 اختر منتج:", reply_markup=markup)

    elif text == "📝 دفتر الشهر":
        send_file(chat_id, "shahr1.jpg", "photo")
        send_file(chat_id, "shahr2.jpg", "photo")

    elif text == "📓 دفتر ملاحظات":
        send_file(chat_id, "molahathat.pdf")

    # الجداول
    elif text == "📂 نماذج جداول مجانية":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📅 جدول 20 يوم")
        markup.add("📅 جدول رمضان")
        markup.add("🧲 نوطة مغناطيسية")
        markup.add("📅 طلب جدول خاص")
        markup.add("🔙 رجوع")
        bot.send_message(chat_id, "📂 اختر جدول:", reply_markup=markup)

    elif text == "📅 جدول 20 يوم":
        send_file(chat_id, "schedule20.pdf")

    elif text == "📅 جدول رمضان":
        send_file(chat_id, "ramadan.pdf")

    elif text == "🧲 نوطة مغناطيسية":
        send_file(chat_id, "magnetic_note.pdf")

    # جدول خاص
    elif text == "📅 طلب جدول خاص":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("✅ دفع جدول خاص")
        markup.add("🔙 رجوع")

        bot.send_message(
            chat_id,
            f"📅 طلب جدول خاص\n\n💰 السعر: {CUSTOM_TABLE_PRICE}\n\n{PAYMENT_INFO}",
            reply_markup=markup
        )

    elif text == "✅ دفع جدول خاص":
        waiting_for_receipt[chat_id] = "custom"
        bot.send_message(chat_id, "📸 أرسل صورة الإيصال لتأكيد طلب الجدول.")

    # VIP
    elif text == "💎 استشارة VIP":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("✅ دفع استشارة VIP")
        markup.add("🔙 رجوع")

        bot.send_message(
            chat_id,
            f"💎 استشارة VIP\n\n💰 السعر: {VIP_PRICE}\n\n{PAYMENT_INFO}",
            reply_markup=markup
        )

    elif text == "✅ دفع استشارة VIP":
        waiting_for_receipt[chat_id] = "vip"
        bot.send_message(chat_id, "📸 أرسل صورة الإيصال لتأكيد الاستشارة.")

    # رجوع
    elif text == "🔙 رجوع":
        main_menu(chat_id, message.from_user.first_name)


# =========================================
# ===== استقبال الإيصال =====
# =========================================
@bot.message_handler(content_types=["photo"])
def handle_receipt(message):
    chat_id = message.chat.id

    if chat_id in waiting_for_receipt:
        order_type = waiting_for_receipt[chat_id]

        bot.send_message(
            MY_ADMIN_ID,
            f"📢 طلب جديد\n\n👤 ID: {chat_id}\n📦 النوع: {order_type}"
        )

        bot.forward_message(MY_ADMIN_ID, chat_id, message.message_id)

        bot.send_message(chat_id, "✅ تم إرسال الإيصال للإدارة.")
        del waiting_for_receipt[chat_id]


# =========================================
# ===== تشغيل البوت =====
# =========================================
if __name__ == "__main__":
    print("🚀 البوت يعمل باحتراف يا غيث...")
    bot.infinity_polling(timeout=5, long_polling_timeout=2)