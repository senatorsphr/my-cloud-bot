import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ---------------------------------------------------------------------
# بخش ویرایش و افزودن کلمات (اینجا را در آینده ویرایش کنید)
# ---------------------------------------------------------------------
RESPONSES = {
    "هخامنشیان": {
        "question": "آیا اطلاعات بیشتری درباره «هخامنشیان» می‌خواهید؟",
        "answer": """
**شاهنشاهی هخامنشی: فراز و فرود نخستین امپراتوری جهانی**

شاهنشاهی هخامنشی، که به عنوان نخستین امپراتوری واقعی جهان شناخته می‌شود، در میانه قرن ششم پیش از میلاد توسط کوروش بزرگ پایه‌گذاری شد. این امپراتوری پهناور برای بیش از دو قرن، از مرزهای هند تا شمال آفریقا و جنوب شرقی اروپا را تحت سیطره خود داشت و میراثی ماندگار در تاریخ مدیریت، فرهنگ و حقوق بشر از خود به جای گذاشت.

**تأسیس و پایه‌گذاری توسط کوروش بزرگ:**

کوروش، که از دودمان هخامنشی در پارس برخاسته بود، با متحد کردن اقوام ایرانی، ابتدا پادشاهی ماد را شکست داد و سپس به سرعت لیدیه (در ترکیه امروزی) و بابل (در عراق امروزی) را فتح کرد. اوج کار او، صدور "منشور کوروش" پس از فتح بابل بود که در آن بر آزادی دین، لغو بردگی و احترام به سنت‌های اقوام تابعه تأکید شده بود. این رویکرد خردمندانه، سنگ بنای یک امپراتوری چندملیتی و پایدار را گذاشت.

**سازماندهی و اوج قدرت در زمان داریوش بزرگ:**

پس از کوروش و دوره کوتاه سلطنت پسرش کمبوجیه (که مصر را فتح کرد)، داریوش بزرگ به قدرت رسید. او یک مدیر و سازمان‌دهنده بی‌نظیر بود. داریوش برای اداره بهتر امپراتوری، آن را به واحدهای اداری به نام "ساتراپی" تقسیم کرد که هرکدام توسط یک شهربان (ساتراپ) اداره می‌شد. او با ایجاد "راه شاهی"، یک جاده طولانی و مجهز، ارتباط سریع میان پایتخت (شوش) و دورترین نقاط کشور را ممکن ساخت. ضرب سکه یکسان به نام "دریک" و ایجاد یک نظام مالیاتی منظم، اقتصاد امپراتوری را شکوفا کرد. ساخت بنای باشکوه تخت جمشید (پرسپولیس) به عنوان پایتخت تشریفاتی و نماد قدرت هخامنشیان نیز در دوران او آغاز شد.

**چالش‌ها و جنگ با یونان:**

در دوران داریوش و پسرش خشایارشا، امپراتوری هخامنشی با دولت‌شهرهای یونانی وارد مجموعه‌ای از درگیری‌ها شد که به "جنگ‌های ایران و یونان" معروف است. اگرچه ارتش پارس در نبردهایی مانند ماراتن و سالامیس شکست خورد، اما این جنگ‌ها قدرت و وسعت ارتش هخامنشی را به نمایش گذاشت و تأثیرات عمیقی بر روابط دو تمدن داشت.

**فرهنگ، دین و جامعه:**

جامعه هخامنشی به شکل شگفت‌انگیزی چندفرهنگی بود. اقوام مختلف با زبان‌ها، ادیان و سنت‌های گوناگون در کنار یکدیگر زندگی می‌کردند. دین رسمی دربار، آئین زرتشت بود که بر پایه پندار نیک، گفتار نیک و کردار نیک استوار بود، اما سایر ادیان نیز آزادانه پرستش می‌شدند. هنر هخامنشی، به ویژه در معماری و حجاری‌های تخت جمشید، ترکیبی از هنر اقوام مختلف مانند مصری، آشوری و یونانی است که در قالبی ایرانی ارائه شده است.

**افول و سقوط:**

پس از دوران خشایارشا، امپراتوری به تدریج دچار ضعف شد. درگیری‌های داخلی بر سر جانشینی، شورش در ساتراپی‌ها (به ویژه مصر) و افزایش فشار بر منابع مالی، قدرت مرکزی را تحلیل برد. این ضعف داخلی، راه را برای ظهور یک دشمن قدرتمند هموار کرد. در سال ۳۳۴ پیش از میلاد، اسکندر مقدونی با ارتشی منظم به قلمرو هخامنشی حمله کرد و پس از چندین نبرد، سرانجام در نبرد "گوگمل" داریوش سوم را شکست داد و به حیات این امپراتوری بزرگ پایان بخشید.

**میراث هخامنشیان:**

با وجود سقوط، میراث هخامنشیان هرگز از بین نرفت. ایده یک حکومت مرکزی مقتدر که به حقوق و فرهنگ‌های محلی احترام می‌گذارد، الگویی برای امپراتوری‌های بعدی شد. ساختار اداری، سیستم راه‌ها و نظام پستی آن‌ها تا قرن‌ها مورد استفاده قرار گرفت و نام ایران و پارس را در تاریخ جهان جاودانه کرد.
"""
    },
}

# ---------------------------------------------------------------------
# بخش اصلی ربات (از اینجا به بعد کد برای Webhook تغییر کرده است)
# ---------------------------------------------------------------------

# توکن و نام ربات را از متغیرهای محیطی می‌خوانیم
TOKEN = os.environ.get("8395270552:AAGoGJUXh9zxIEcn1pKzN1VeXBtqiXPZXqo")
APP_NAME = os.environ.get("KOYEB_APP_NAME")

# ساخت اپلیکیشن Flask برای ایجاد وب سرور
server = Flask(__name__)

# ساخت اپلیکیشن ربات تلگرام
application = Application.builder().token(TOKEN).build()

# تابع برای چک کردن پیام‌های گروه (بدون تغییر)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    for trigger_word, data in RESPONSES.items():
        if trigger_word in message_text:
            keyboard = [
                [
                    InlineKeyboardButton("آره، بگو", callback_data=f"show:{trigger_word}"),
                    InlineKeyboardButton("نه، ممنون", callback_data=f"delete:{trigger_word}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(data["question"], reply_markup=reply_markup)
            break

# تابع برای مدیریت دکمه‌ها (بدون تغییر)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action, trigger_word = query.data.split(":", 1)
    if action == "show":
        response_text = RESPONSES[trigger_word]["answer"]
        await query.message.reply_text(response_text, parse_mode='Markdown')
        await query.message.delete()
    elif action == "delete":
        await query.message.delete()

# یک مسیر برای سرور تعریف می‌کنیم که تلگرام به آن پیام‌ها را بفرستد
@server.route(f"/{TOKEN}", methods=["POST"])
async def webhook_handler():
    update_data = request.get_json()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return "ok"

# یک مسیر ساده برای اینکه ببینیم سرور آنلاین است
@server.route("/")
def index():
    return "Hello, I am the bot server!"

async def main():
    # ثبت کردن کنترل‌کننده‌ها
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(CallbackQueryHandler(button_handler))

    # تنظیم Webhook
    # Koyeb آدرس عمومی را در این متغیر قرار می‌دهد
    webhook_url = f"https://{APP_NAME}.koyeb.app/{TOKEN}"
    await application.bot.set_webhook(url=webhook_url)
    print(f"Webhook با موفقیت روی آدرس {webhook_url} تنظیم شد.")

    # اجرای وب سرور Flask
    # Koyeb پورت را در این متغیر قرار می‌دهد
    port = int(os.environ.get('PORT', 8000))
    print("وب سرور در حال اجراست...")
    server.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
