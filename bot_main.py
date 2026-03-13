import telebot from telebot import types import os

# ⚠️ استبدل التوكن بتوكن جديد فوراً
TOKEN = "8377189184:AAGLhZ5mpVkeWwz1uL5NdhcqbHCDOWLSBzU"
MY_ADMIN_ID = 5825392632

bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ دالة إرسال الملفات ------------------

def send_file(chat_id, file_name, file_type="document"):
    try:
        path = os.path.join(BASE_DIR, file_name)
        with open(path, "rb") as f:
            if file_type == "photo":
                bot.send_photo(chat_id, f)
            else:
                bot.send_document(chat_id, f)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ عذراً، لم يتم العثور على الملف: {file_name}")
        print(f"Error: {e}")

# ------------------ القوائم (Keyboard Markup) ------------------

def main_menu(chat_id, name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🛒 متجر زاد", "📂 نماذج مجانية", "💎 استشارة VIP", "🔄 إعادة تشغيل")
    greeting = f"أهلاً {name} 👋" if name else "أهلاً بك 👋"
    bot.send_message(chat_id, greeting, reply_markup=markup)

def store_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📝 دفتر الشهر", "📓 notebook", "📞 تواصل معي", "🔙 رجوع")
    bot.send_message(chat_id, "🛒 منتجات متجر زاد:", reply_markup=markup)

def free_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 جدول 14 يوم", "📅 جدول 20 يوم", "📅 جدول رمضان", "🧲 نوطة مغناطيسية", "🔙 رجوع")
    bot.send_message(chat_id, "📂 اختر نموذج:", reply_markup=markup)

def post_payment_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🎓 استشارة في البكالوريا", "💊 استشارة في الصيدلة", "📝 طلب جدول دراسي خاص", "🔙 رجوع")
    bot.send_message(chat_id, "✅ تم استلام صورة الإيصال!\nاختر الآن نوع الاستشارة التي ترغب بها:", reply_markup=markup)

# ------------------ الأوامر ومعالجة الرسائل ------------------

@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

# معالجة الصور (إيصالات الدفع)
@bot.message_handler(content_types=['photo'])
def handle_payment_photo(message):
    # تحويل الإيصال للأدمن
    bot.forward_message(MY_ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(MY_ADMIN_ID, f"🔔 إيصال جديد من: @{message.from_user.username} (ID: {message.chat.id})")
    # فتح خيارات الاستشارة للمستخدم
    post_payment_menu(message.chat.id)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    if text == "🛒 متجر زاد":
        store_menu(chat_id)

    elif text == "📂 نماذج مجانية":
        free_menu(chat_id)

    elif text == "💎 استشارة VIP":
        payment_msg = (
            "💎 **طلب استشارة VIP**\n\n"
            "للحصول على الخدمة، يرجى تحويل مبلغ **100 ليرة سورية جديدة** عبر الرموز التالية:\n\n"
            "🇸🇾 **سيرياتيل كاش:**\n`43236225`\n\n"
            "💳 **شام كاش:**\n`dcef38efff3d8959a85147a200cfbda2`\n\n"
            "⚠️ (اضغط على الرمز لنسخه)\n\n"
            "📸 **بعد التحويل، يرجى إرسال صورة إيصال الدفع هنا مباشرة لفتح الميزات.**"
        )
        bot.send_message(chat_id, payment_msg, parse_mode="Markdown")

    elif text == "📅 جدول 14 يوم":
        send_file(chat_id, "schedule.pdf")

    elif text == "📅 جدول 20 يوم":
        send_file(chat_id, "schedule20.pdf")

    elif text == "📅 جدول رمضان":
        send_file(chat_id, "ramadan.pdf")

    elif text == "🧲 نوطة مغناطيسية":
        send_file(chat_id, "magnetic_note.pdf")

    elif text == "📝 دفتر الشهر":
        bot.send_message(chat_id, "📷 جاري إرسال الصور...")
        for img in ["shahr1.jpg", "shahr2.jpg", "zadk.jpg", "zadk2.jpg"]:
            send_file(chat_id, img, "photo")

    elif text == "📓 notebook":
        bot.send_message(chat_id, "📄 جاري إرسال الملفات...")
        send_file(chat_id, "molahathat.pdf")
        send_file(chat_id, "molahathat2.pdf")

    elif text == "📞 تواصل معي":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📩 راسلني على التلغرام", url="https://t.me/V_u_23"))
        bot.send_message(chat_id, "اضغط للتواصل 👇", reply_markup=markup)

    # أزرار الاستشارة بعد الدفع
    elif text == "🎓 استشارة في البكالوريا":
        bot.send_message(chat_id, "ممتاز! سأقوم بمتابعة وضعك في البكالوريا بأقرب وقت.")
    
    elif text == "💊 استشارة في الصيدلة":
        bot.send_message(chat_id, "أهلاً بك زميلي.. سأجيب على استفساراتك الصيدلانية قريباً.")
        
    elif text == "📝 طلب جدول دراسي خاص":
        bot.send_message(chat_id, "يرجى كتابة عدد المواد المتبقية وساعات دراستك اليومية لتجهيز الجدول.")

    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, user_name)

# ------------------ التشغيل ------------------

print("🚀 البوت اشتغل بنجاح!")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
        


