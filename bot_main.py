import telebot
from telebot import types
import os
import random

# استيراد قائمة النصوص من الملف الخارجي
try:
    from data import CREATIVE_LIST
except ImportError:
    CREATIVE_LIST = ["جاري تجهيز محتوى الإبداع.. انتظرونا! ✨"]

# ------------------ الإعدادات الأساسية ------------------
TOKEN = os.getenv("TOKEN") 
MY_ADMIN_ID = 5825392632

bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ دالة إرسال الملفات ------------------
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
                bot.send_document(chat_id, f, caption=f"📄 ملف: {file_name}")
    except Exception as e:
        print(f"Error: {e}")

# ------------------ القوائم (Keyboards) ------------------

def main_menu(chat_id, name=""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📖 الروايات", "✨ عالم الإبداع")
    markup.add("🎓 البكالوريا والملفات", "🏛️ الجامعة")
    markup.add("💎 استشارة VIP", "🔄 إعادة تشغيل")
    bot.send_message(chat_id, f"أهلاً بك {name} 👋\nاختر من الأقسام المتاحة:", reply_markup=markup)

def bac_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 الجداول والنوط", "🛒 متجر زاد")
    markup.add("🔙 رجوع")
    bot.send_message(chat_id, "🎓 قسم البكالوريا:", reply_markup=markup)

def store_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📝 دفتر الشهر", "📓 Notebook", "📞 تواصل مع المتجر", "🔙 رجوع")
    bot.send_message(chat_id, "🛒 منتجات متجر زاد:", reply_markup=markup)

def free_files_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 جدول 14 يوم", "📅 جدول 20 يوم", "📅 جدول رمضان", "🧲 نوطة مغناطيسية", "🔙 رجوع")
    bot.send_message(chat_id, "📂 الملفات المجانية والجداول:", reply_markup=markup)

# ------------------ معالجة الرسائل ------------------

@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    # 1. الروايات والإبداع والجامعة
    if text == "📖 الروايات":
        send_file(chat_id, "2242.pdf")
    
    elif text == "✨ عالم الإبداع":
        bot.send_message(chat_id, random.choice(CREATIVE_LIST))

    elif text == "🏛️ الجامعة":
        # إرسال ملف الاختبار التفاعلي مباشرة من السيرفر
        send_file(chat_id, "Organic_Ch1_Quiz.html")
        bot.send_message(chat_id, "🧪 تفضل زميلي، هذا هو ملف الاختبار التفاعلي للمحاضرة الأولى.\n\nافتح الملف من جهازك ليظهر لك بشكل تفاعلي ومنظم.")

    # 2. قسم البكالوريا
    elif text == "🎓 البكالوريا والملفات":
        bac_menu(chat_id)
    elif text == "📅 الجداول والنوط":
        free_files_menu(chat_id)
    elif text == "🛒 متجر زاد":
        store_menu(chat_id)

    # 3. محتويات متجر زاد
    elif text == "📝 دفتر الشهر":
        for img in ["shahr1.jpg", "shahr2.jpg", "zadk.jpg", "zadk2.jpg"]:
            send_file(chat_id, img, "photo")
    elif text == "📓 Notebook":
        send_file(chat_id, "molahathat.pdf")
    elif text == "📞 تواصل مع المتجر":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📩 تلغرام", url="https://t.me/V_u_23"))
        bot.send_message(chat_id, "تواصل معي لطلب المنتجات:", reply_markup=markup)

    # 4. ملفات البكالوريا
    elif text == "📅 جدول 14 يوم": send_file(chat_id, "schedule.pdf")
    elif text == "📅 جدول 20 يوم": send_file(chat_id, "schedule20.pdf")
    elif text == "📅 جدول رمضان": send_file(chat_id, "ramadan.pdf")
    elif text == "🧲 نوطة مغناطيسية": send_file(chat_id, "magnetic_note.pdf")

    # 5. استشارة VIP
    elif text == "💎 استشارة VIP":
        markup = types.InlineKeyboardMarkup()
        btn_pharma = types.InlineKeyboardButton("💊 أنا طالب صيدلة", callback_data="consult_pharma")
        btn_bac = types.InlineKeyboardButton("🎓 أنا طالب بكالوريا", callback_data="consult_bac")
        markup.add(btn_pharma, btn_bac)
        bot.send_message(chat_id, "يرجى تحديد تخصصك لنتمكن من مساعدتك بشكل أفضل:", reply_markup=markup)

    # العودة
    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, user_name)

# معالجة ضغط أزرار الكول باك (Inline Buttons)
@bot.callback_query_handler(func=lambda call: call.data.startswith('consult_'))
def callback_consult(call):
    chat_id = call.message.chat.id
    if call.data == "consult_pharma":
        bot.send_message(chat_id, "أهلاً بك زميلي الصيدلاني 💊.\nيرجى تحويل 100 ليرة (سيرياتيل كاش 43236225) وإرسال الإيصال لبدء الاستشارة.")
    elif call.data == "consult_bac":
        bot.send_message(chat_id, "بالتوفيق بطل البكالوريا 🎓.\nيرجى تحويل 100 ليرة (سيرياتيل كاش 43236225) وإرسال الإيصال لبدء الاستشارة.")

if __name__ == "__main__":
    print("🚀 البوت انطلق بكامل التحديثات يا غيث!")
    bot.infinity_polling()
    
