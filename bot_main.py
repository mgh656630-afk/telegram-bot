import telebot
from telebot import types
import os
import random

# الإعدادات الأساسية
TOKEN = "8377189184:AAGLhZ5mpVkeWwz1uL5NdhcqbHCDOWLSBzU"
MY_ADMIN_ID = 5825392632
bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ مكتبة العبارات ------------------
POETRY_LIST = [
    "يا أول نبع غنّت عليه طيور.. ويا جرة ذهب معزولة بالبيت.",
    "إنتَ الهوى وأنفاسي من دونك تضيق.. يا أغلى من الروح يا رفيقي وصديقي.",
    "كون العمر بستان وإنت الورد بيه.. كلما يمرني الضيق بضحكتك أعديه."
]

QUOTES_LIST = [
    "«القراءة تجعل من الشخص إنساناً كاملاً، والمشورة تجعله شخصاً مستعداً، والكتابة تجعله شخصاً دقيقاً».",
    "«ليس المهم ما يحدث لك، بل المهم كيف تتفاعل معه».",
    "«الجمال يكمن في بساطة الأشياء وعمق الأثر»."
]

MOTIVATION_LIST = [
    "تذكّر أن طريق الألف ميل يبدأ بخطوة، وخطوتك اليوم هي أساس نجاحك غداً 🚀.",
    "لا تتوقف عندما تتعب، توقف عندما تنتهي.. النجاح يليق بك جداً.",
    "كل سهر وتعب اليوم، سيتحول لقصة نجاح ترويها بكل فخر لاحقاً."
]

# ------------------ دالة إرسال الملفات المطورة ------------------
def send_file(chat_id, file_name, file_type="document"):
    path = os.path.join(BASE_DIR, file_name)
    
    if not os.path.exists(path):
        bot.send_message(chat_id, f"⚠️ عذراً، لم يتم العثور على الملف: {file_name}")
        return

    try:
        with open(path, "rb") as f:
            if file_type == "photo":
                bot.send_photo(chat_id, f)
            else:
                bot.send_document(chat_id, f)
    except Exception as e:
        bot.send_message(chat_id, "❌ حدث خطأ فني أثناء إرسال الملف.")
        print(f"Error: {e}")

# ------------------ القوائم (Keyboard Markup) ------------------
def main_menu(chat_id, name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🛒 متجر زاد", "📂 نماذج مجانية", "💎 استشارة VIP")
    markup.add("📜 الشعر", "💭 اقتباسات", "🔥 تحفيز")
    markup.add("📖 رواية قيامة الروح") # الزر الجديد هنا
    markup.add("🔄 إعادة تشغيل")
    greeting = f"أهلاً {name} 👋" if name else "أهلاً بك 👋"
    bot.send_message(chat_id, greeting, reply_markup=markup)

def store_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📝 دفتر الشهر", "📓 Notebook", "📞 تواصل معي", "🔙 رجوع")
    bot.send_message(chat_id, "🛒 منتجات متجر زاد:", reply_markup=markup)

def free_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 جدول 14 يوم", "📅 جدول 20 يوم", "📅 جدول رمضان", "🧲 نوطة مغناطيسية", "🔙 رجوع")
    bot.send_message(chat_id, "📂 اختر نموذج:", reply_markup=markup)

# ------------------ معالجة الرسائل ------------------
@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    if text == "🛒 متجر زاد":
        store_menu(chat_id)
    elif text == "📂 نماذج مجانية":
        free_menu(chat_id)
    elif text == "📅 جدول 14 يوم":
        send_file(chat_id, "schedule.pdf")
    elif text == "📅 جدول 20 يوم":
        send_file(chat_id, "schedule20.pdf")
    elif text == "📅 جدول رمضان":
        send_file(chat_id, "ramadan.pdf")
    elif text == "🧲 نوطة مغناطيسية":
        send_file(chat_id, "magnetic_note.pdf")
    elif text == "📝 دفتر الشهر":
        for img in ["shahr1.jpg", "shahr2.jpg", "zadk.jpg", "zadk2.jpg"]:
            send_file(chat_id, img, "photo")
    elif text == "📓 Notebook":
        send_file(chat_id, "molahathat.pdf")
        send_file(chat_id, "molahathat2.pdf")

    # معالجة زر الرواية الجديد
    elif text == "📖 رواية قيامة الروح":
        bot.send_message(chat_id, "📖 جاري تحميل رواية 'قيامة الروح'.. قراءة ممتعة!")
        send_file(chat_id, "2242.pdf")# المكتبة اللغوية
    elif text == "📜 الشعر":
        bot.send_message(chat_id, random.choice(POETRY_LIST))
    elif text == "💭 اقتباسات":
        bot.send_message(chat_id, random.choice(QUOTES_LIST))
    elif text == "🔥 تحفيز":
        bot.send_message(chat_id, random.choice(MOTIVATION_LIST))

    elif text == "💎 استشارة VIP":
        bot.send_message(chat_id, "يرجى تحويل 100 ليرة عبر سيرياتيل كاش (43236225) وإرسال صورة الإيصال.")
    elif text == "📞 تواصل معي":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📩 تلغرام", url="https://t.me/V_u_23"))
        bot.send_message(chat_id, "تواصل معي عبر الرابط:", reply_markup=markup)
    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, user_name)

# التشغيل
bot.infinity_polling()
