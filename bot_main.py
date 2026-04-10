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
RESERVE_ADMIN_ID = 6724250074  # ضع هنا ID حسابك الاحتياطي يا غيث
ADMINS = [MY_ADMIN_ID, RESERVE_ADMIN_ID]

CHANNELS = ["@mgh_math25", "@le_Ghaith0000"] # معرفات القنوات

bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ دالات التحقق والملفات ------------------

def check_sub(user_id):
    """التحقق من اشتراك المستخدم في القنوات الإجبارية"""
    if user_id in ADMINS:
        return True
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

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
    bot.send_message(chat_id, f"أهلاً بك {name} 👋 في بوت المستشار الدراسي\nاختر من الأقسام المتاحة:", reply_markup=markup)

def university_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("💊 صيدلة", "🔙 رجوع")
    bot.send_message(chat_id, "🏛️ قسم الجامعة - اختر كليتك:", reply_markup=markup)

def pharma_years_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("السنة الأولى", "السنة الثانية")
    markup.add("السنة الثالثة", "السنة الرابعة", "السنة الخامسة")
    markup.add("🔙 رجوع")
    bot.send_message(chat_id, "💊 كلية الصيدلة - اختر سنتك الدراسية:", reply_markup=markup)

def pharma_year1_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("اختبارات عضوية", "ملفات اخرى")
    markup.add("🔙 رجوع")
    bot.send_message(chat_id, "📚 صيدلة - سنة أولى:", reply_markup=markup)

def pharma_organic_tests_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("اختبار المحاضرة الأولى", "اختبار المحاضرة الثانية")
    markup.add("🔙 رجوع")
    bot.send_message(chat_id, "🧪 اختبارات الكيمياء العضوية التفاعلية:", reply_markup=markup)

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
    if not check_sub(message.chat.id):
        show_sub_message(message.chat.id)
        return
    main_menu(message.chat.id, message.from_user.first_name)

def show_sub_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("قناة الطب 🩺", url="https://t.me/mgh_math25")
    btn2 = types.InlineKeyboardButton("قناة الاقتباسات ✨", url="https://t.me/le_Ghaith0000")
    btn_done = types.InlineKeyboardButton("تم الاشتراك ✅", callback_data="check_subscription")
    markup.add(btn1, btn2)
    markup.add(btn_done)
    bot.send_message(chat_id, "⚠️ عفواً زميلي، يجب عليك الاشتراك في قنواتنا لتتمكن من استخدام البوت والحصول على الملفات:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text
    user_name = message.from_user.first_name

    # التحقق من الاشتراك أولاً
    if not check_sub(chat_id):
        show_sub_message(chat_id)
        return

    # 1. الأقسام الرئيسية والجامعة
    if text == "🏛️ الجامعة":
        university_menu(chat_id)
    
    elif text == "💊 صيدلة":
        pharma_years_menu(chat_id)

    elif text == "السنة الأولى":
        pharma_year1_menu(chat_id)

    elif text in ["السنة الثانية", "السنة الثالثة", "السنة الرابعة", "السنة الخامسة", "ملفات اخرى"]:
        bot.send_message(chat_id, "🚧 سيتم إضافة المحتوى قريباً.. نحن نعمل على ذلك!")

    elif text == "اختبارات عضوية":
        pharma_organic_tests_menu(chat_id)

    elif text == "اختبار المحاضرة الأولى":
        send_file(chat_id, "Organic_Ch1_Quiz.html")
        bot.send_message(chat_id, "🧪 تفضل زميلي، اختبار المحاضرة الأولى (تفاعلي).")

    elif text == "اختبار المحاضرة الثانية":
        send_file(chat_id, "Organic_Ch2_Quiz.html")
        bot.send_message(chat_id, "🧪 تفضل زميلي، اختبار المحاضرة الثانية (تفاعلي).")

    # 2. الروايات والإبداع
    elif text == "📖 الروايات":
        send_file(chat_id, "2242.pdf")
    
    elif text == "✨ عالم الإبداع":
        bot.send_message(chat_id, random.choice(CREATIVE_LIST))

    # 3. قسم البكالوريا والمتجر
    elif text == "🎓 البكالوريا والملفات":
        bac_menu(chat_id)
    elif text == "📅 الجداول والنوط":
        free_files_menu(chat_id)
    elif text == "🛒 متجر زاد":
        store_menu(chat_id)

    # 4. محتويات متجر زاد
    elif text == "📝 دفتر الشهر":
        for img in ["shahr1.jpg", "shahr2.jpg", "zadk.jpg", "zadk2.jpg"]:
            send_file(chat_id, img, "photo")
    elif text == "📓 Notebook":
        send_file(chat_id, "molahathat.pdf")
    elif text == "📞 تواصل مع المتجر":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📩 تلغرام", url="https://t.me/V_u_23"))
        bot.send_message(chat_id, "تواصل معي لطلب المنتجات:", reply_markup=markup)

    # 5. ملفات البكالوريا
    elif text == "📅 جدول 14 يوم": send_file(chat_id, "schedule.pdf")
    elif text == "📅 جدول 20 يوم": send_file(chat_id, "schedule20.pdf")
    elif text == "📅 جدول رمضان": send_file(chat_id, "ramadan.pdf")
    elif text == "🧲 نوطة مغناطيسية": send_file(chat_id, "magnetic_note.pdf")

    # 6. استشارة VIP
    elif text == "💎 استشارة VIP":
        markup = types.InlineKeyboardMarkup()
        btn_pharma = types.InlineKeyboardButton("💊 أنا طالب صيدلة", callback_data="consult_pharma")
        btn_bac = types.InlineKeyboardButton("🎓 أنا طالب بكالوريا", callback_data="consult_bac")
        markup.add(btn_pharma, btn_bac)
        bot.send_message(chat_id, "يرجى تحديد تخصصك لنتمكن من مساعدتك بشكل أفضل:", reply_markup=markup)

    # العودة
    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, user_name)

# معالجة ضغط أزرار الكول باك
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    
    if call.data == "check_subscription":
        if check_sub(chat_id):
            bot.answer_callback_query(call.id, "شكراً لاشتراكك! تم تفعيل البوت ✅")
            main_menu(chat_id, call.from_user.first_name)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد!", show_alert=True)
            
    elif call.data == "consult_pharma":
        bot.send_message(chat_id, "أهلاً بك زميلي الصيدلاني 💊.\nيرجى تحويل 100 ليرة (سيرياتيل كاش 43236225) وإرسال الإيصال لبدء الاستشارة.")
    elif call.data == "consult_bac":
        bot.send_message(chat_id, "بالتوفيق بطل البكالوريا 🎓.\nيرجى تحويل 100 ليرة (سيرياتيل كاش 43236225) وإرسال الإيصال لبدء الاستشارة.")

if __name__ == "__main__":
    print("🚀 البوت انطلق بتحديثات 'غيث' الجديدة.. بالتوفيق!")
    bot.infinity_polling()
    
