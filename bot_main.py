import telebot
from telebot import types
import os

TOKEN = "8377189184:AAGLhZ5mpVkeWwz1uL5NdhcqbHCDOWLSBzU"
MY_ADMIN_ID = 5825392632

bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ ارسال ملفات ------------------

def send_file(chat_id, file_name, file_type="document"):
    try:
        path = os.path.join(BASE_DIR, file_name)
        with open(path, "rb") as f:
            if file_type == "photo":
                bot.send_photo(chat_id, f)
            else:
                bot.send_document(chat_id, f)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ خطأ بالملف: {file_name}")
        print(e)

# ------------------ القائمة الرئيسية ------------------

def main_menu(chat_id, name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "🛒 متجر زاد",
        "📂 نماذج مجانية",
        "💎 استشارة VIP",
        "🔄 إعادة تشغيل"
    )
    bot.send_message(chat_id, f"أهلاً {name} 👋", reply_markup=markup)

# ------------------ متجر زاد ------------------

def store_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "📝 دفتر الشهر",
        "📓 دفتر ملاحظات",
        "📞 تواصل معي",
        "🔙 رجوع"
    )
    bot.send_message(chat_id, "🛒 منتجات متجر زاد:", reply_markup=markup)

# ------------------ نماذج مجانية ------------------

def free_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "📅 جدول 20 يوم",
        "📅 جدول رمضان",
        "🧲 نوطة مغناطيسية",
        "🔙 رجوع"
    )
    bot.send_message(chat_id, "📂 اختر نموذج:", reply_markup=markup)

# ------------------ START ------------------

@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

# ------------------ الأزرار ------------------

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text
    chat_id = message.chat.id

    if text == "🛒 متجر زاد":
        store_menu(chat_id)

    elif text == "📂 نماذج مجانية":
        free_menu(chat_id)

    elif text == "📝 دفتر الشهر":
        bot.send_message(chat_id, "📷 جاري إرسال الصور...")
        send_file(chat_id, "shahr1.jpg", "photo")
        send_file(chat_id, "shahr2.jpg", "photo")
        send_file(chat_id, "zadk.jpg", "photo")
        send_file(chat_id, "zadk2.jpg", "photo")

    elif text == "📓 دفتر ملاحظات":
        bot.send_message(chat_id, "📄 جاري إرسال الملفات...")
        send_file(chat_id, "molahathat.pdf")
        send_file(chat_id, "molahathat2.pdf")

    elif text == "📞 تواصل معي":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "📩 راسلني على التلغرام",
            url="https://t.me/V_u_23"
        ))
        bot.send_message(chat_id, "اضغط للتواصل 👇", reply_markup=markup)

    elif text == "📅 جدول 20 يوم":
        send_file(chat_id, "schedule20.pdf")

    elif text == "📅 جدول رمضان":
        send_file(chat_id, "ramadan.pdf")

    elif text == "🧲 نوطة مغناطيسية":
        send_file(chat_id, "magnetic_note.pdf")

    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, message.from_user.first_name)

# ------------------ تشغيل ------------------

print("🚀 البوت اشتغل يا غيث")
bot.infinity_polling()
    bot.infinity_polling(timeout=5, long_polling_timeout=2)
