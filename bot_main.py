import telebot
from telebot import types
import os
import random

# استيراد قائمة النصوص من الملف الخارجي
try:
    from data import CREATIVE_LIST
except ImportError:
    # في حال نسيان إنشاء ملف data.py، نضع قائمة احتياطية لتجنب توقف البوت
    CREATIVE_LIST = ["جاري تجهيز محتوى الإبداع.. انتظرونا! ✨"]

# ------------------ الإعدادات الأساسية ------------------
# جلب التوكن من متغيرات البيئة (مناسب لـ Railway)
TOKEN = os.getenv("TOKEN") 
MY_ADMIN_ID = 5825392632

bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ دالة إرسال الملفات المطورة ------------------
def send_file(chat_id, file_name, file_type="document"):
    path = os.path.join(BASE_DIR, file_name)
    
    if not os.path.exists(path):
        bot.send_message(chat_id, f"⚠️ عذراً زميلي، لم يتم العثور على الملف: `{file_name}`")
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

# القائمة الرئيسية (الأزرار الأربعة)
def main_menu(chat_id, name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn_novel = types.KeyboardButton("📖 الروايات")
    btn_creative = types.KeyboardButton("✨ عالم الإبداع")
    btn_bac = types.KeyboardButton("🎓 البكالوريا والملفات")
    btn_uni = types.KeyboardButton("🏛️ الجامعة")
    
    # توزيع الأزرار بشكل متناسق
    markup.add(btn_novel, btn_creative, btn_bac, btn_uni)
    markup.add(types.KeyboardButton("🔄 إعادة تشغيل"))
    
    greeting = f"أهلاً بك زميلي {name} في بوتك المطور 👋"
    bot.send_message(chat_id, greeting, reply_markup=markup)

# قائمة البكالوريا الفرعية
def bac_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 جدول 14 يوم", "📅 جدول 20 يوم", "📅 جدول رمضان", "🧲 نوطة مغناطيسية", "🔙 رجوع")
    bot.send_message(chat_id, "📂 قسم البكالوريا - اختر الملف المطلوب:", reply_markup=markup)

# ------------------ معالجة الرسائل ------------------

@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    # 1. زر الروايات
    if text == "📖 الروايات":
        bot.send_message(chat_id, "📖 يتم الآن إرسال رواية (قيامة الروح).. قراءة ممتعة!")
        send_file(chat_id, "2242.pdf")

    # 2. زر عالم الإبداع (اختيار عشوائي من الـ 100 نص)
    elif text == "✨ عالم الإبداع":
        random_text = random.choice(CREATIVE_LIST)
        bot.send_message(chat_id, random_text)

    # 3. زر البكالوريا
    elif text == "🎓 البكالوريا والملفات":
        bac_menu(chat_id)
    
    # معالجة ملفات البكالوريا
    elif text == "📅 جدول 14 يوم":
        send_file(chat_id, "schedule.pdf")
    elif text == "📅 جدول 20 يوم":
        send_file(chat_id, "schedule20.pdf")
    elif text == "📅 جدول رمضان":
        send_file(chat_id, "ramadan.pdf")
    elif text == "🧲 نوطة مغناطيسية":
        send_file(chat_id, "magnetic_note.pdf")

    # 4. زر الجامعة
    elif text == "🏛️ الجامعة":
        bot.send_message(chat_id, "🏛️ هذا القسم مخصص لطلاب الجامعات.. سيتم إضافة المحتوى قريباً جداً، انتظرونا!")

    # خيارات العودة والتشغيل
    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, user_name)

# ------------------ تشغيل البوت ------------------
if __name__ == "__main__":
    print("🚀 البوت انطلق بنجاح يا غيث.. شهد جاهزة للعمل!")
    bot.infinity_polling()
    
