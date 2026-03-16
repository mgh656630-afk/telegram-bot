import telebot
from telebot import types
import os
import random
import google.generativeai as genai

# ⚠️ الإعدادات الأساسية
TOKEN = "8377189184:AAGLhZ5mpVkeWwz1uL5NdhcqbHCDOWLSBzU"
MY_ADMIN_ID = 5825392632
genai.configure(api_key="AIzaSyDyqdXgJjjSNP2zhUFbeMSxrhk39PgnUOM")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ نظام الذكاء الاصطناعي ------------------
def ask_shaza(prompt_type):
    prompts = {
        "poetry": "اكتب بيت شعر واحد فقط باللهجة العراقية عن الطموح والنجاح، وبدي كل مرة يكون البيت مختلف.",
        "quote": "أعطني اقتباساً عالمياً ملهماً عن الإصرار مع ذكر اسم صاحب المقولة، غير اللي قلته قبل قليل.",
        "boost": "أنتِ شهد، طالبة صيدلة زميلة ومحبة. وجهي رسالة تحفيزية قصيرة جداً ولهجة سورية لطيفة لزميلك غيث اللي عم يدرس صيدلة وتعبان، كل مرة غيري العبارة."
    }
    
    try:
        # إضافة عنصر عشوائي بسيط للطلب عشان الـ AI ما يكرر نفسه
        random_suffix = f" (تحديث رقم: {random.randint(1, 1000)})"
        response = ai_model.generate_content(prompts[prompt_type] + random_suffix)
        return response.text
    except:
        return "خلي طموحك عالي، النجاح بيستاهل التعب! ✨" # هاد الرد الاحتياطي

# ------------------ حفظ المشتركين وإرسال الملفات ------------------
def save_user(chat_id):
    with open("users.txt", "a+") as f:
        f.seek(0)
        if str(chat_id) not in f.read().splitlines():
            f.write(str(chat_id) + "\n")

def send_file(chat_id, file_name, file_type="document"):
    try:
        path = os.path.join(BASE_DIR, file_name)
        with open(path, "rb") as f:
            if file_type == "photo": bot.send_photo(chat_id, f)
            else: bot.send_document(chat_id, f)
    except:
        bot.send_message(chat_id, "⚠️ الملف غير متوفر حالياً.")

# ------------------ القوائم ------------------
def main_menu(chat_id, name=""):
    save_user(chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🎓 بكلوريا", "🛒 متجر زاد")
    markup.add("💊 صيدلة", "✨ اقتباس وتحفيز")
    markup.add("🔄 إعادة تشغيل")
    bot.send_message(chat_id, f"أهلاً {name} 👋\nأنا شهد.. كيف بقدر ساعدك؟", reply_markup=markup)

# ------------------ معالجة الأوامر والرسائل ------------------
@bot.message_handler(commands=["start"])
def start(message):
    main_menu(message.chat.id, message.from_user.first_name)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    
    if call.data == "bac_files":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("📅 جدول 14 يوم", "📅 جدول 20 يوم", "📅 جدول رمضان", "🧲 نوطة مغناطيسية", "🔙 رجوع")
        bot.send_message(chat_id, "📂 إليك النماذج المتاحة:", reply_markup=markup)
    elif call.data == "bac_vip":
        bot.send_message(chat_id, "💎 طلب استشارة VIP\nيرجى تحويل 100 ليرة (سيرياتيل كاش: 43236225) وإرسال صورة الإيصال هنا.")
    elif call.data == "type_poetry":
        bot.send_message(chat_id, f"📜 من بحور الشعر:\n\n{ask_shaza('poetry')}")
    elif call.data == "type_quote":
        bot.send_message(chat_id, f"💡 اقتباس اليوم:\n\n{ask_shaza('quote')}")
    elif call.data == "type_boost":
        bot.send_message(chat_id, f"💪 رسالة من شهد إلك:\n\n{ask_shaza('boost')}")

@bot.message_handler(func=lambda m: True)
def handle(message):
    text, chat_id = message.text, message.chat.id
    if text == "🎓 بكلوريا":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("📂 نماذج مجانية", callback_data="bac_files"),
                   types.InlineKeyboardButton("💎 استشارة VIP", callback_data="bac_vip"))
        bot.send_message(chat_id, "🎓 قسم البكلوريا:", reply_markup=markup)
    elif text == "✨ اقتباس وتحفيز":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("📜 شعر", callback_data="type_poetry"),
        types.InlineKeyboardButton("💡 اقتباس", callback_data="type_quote"),
                   types.InlineKeyboardButton("💪 تحفيز", callback_data="type_boost"))
        bot.send_message(chat_id, "✨ اختر نوع التحفيز:", reply_markup=markup)
    elif text == "🛒 متجر زاد":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("📝 دفتر الشهر", "📓 notebook", "📞 تواصل معي", "🔙 رجوع")
        bot.send_message(chat_id, "🛒 منتجات متجر زاد:", reply_markup=markup)
    elif text == "💊 صيدلة":
        bot.send_message(chat_id, "💊 زميلي الصيدلي.. المحتوى قيد التجهيز حالياً!")
    elif text in ["🔙 رجوع", "🔄 إعادة تشغيل"]:
        main_menu(chat_id, message.from_user.first_name)
    elif text == "📅 جدول 14 يوم": send_file(chat_id, "schedule14.pdf")
    elif text == "📅 جدول 20 يوم": send_file(chat_id, "schedule20.pdf")
    elif text == "📅 جدول رمضان": send_file(chat_id, "ramadan.pdf")
    elif text == "🧲 نوطة مغناطيسية": send_file(chat_id, "magnetic_note.pdf")
    elif text == "📞 تواصل معي":
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("📩 راسلني", url="https://t.me/V_u_23"))
        bot.send_message(chat_id, "اضغط للتواصل 👇", reply_markup=m)

@bot.message_handler(content_types=['photo'])
def handle_payment(message):
    bot.forward_message(MY_ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "✅ وصل الإيصال! رح نتواصل معك بأقرب وقت.")

print("🚀 البوت المطور جاهز!")
bot.infinity_polling()
