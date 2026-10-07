import telebot

TOKEN = '8845193601:AAHF8hf6xmMndP3LfTQOFhfpcTax-uT31U8'
GROUP_CHAT_ID = -1003875886407
TOPIC_ID = 207

bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "გამარჯობა! ეს არის სერვისების განაცხადების ბოტი. აღწერეთ რა სერვისი გჭირდებათ და დატოვეთ კონტაქტები.\n\n"
        "Hello! This is a service request bot. Please describe the service you need and leave your contacts.\n\n"
        "Здравствуйте! Это бот для приёма заявок на услуги. Опишите, какая услуга вам необходима, и оставьте контакты."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_request(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else f"{user.first_name} (без юзернейма)"
    
    lead_text = (
        "🔔 **Новая заявка из бота!**\n"
        f"👤 **Клиент:** {username} (ID: `{user.id}`)\n"
        f"📝 **Текст обращения:**\n{message.text}"
    )
    
    try:
        bot.send_message(
            GROUP_CHAT_ID, 
            lead_text, 
            message_thread_id=TOPIC_ID, 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка отправки в группу: {e}")
    
    reply_text = (
        "მადლობა! თქვენი განაცხადი დაფიქსირდა, დაელოდეთ დაკავშირებას.\n\n"
        "Thank you! Your request has been recorded, please expect contact.\n\n"
        "Спасибо, заявка зафиксирована, ожидайте связи!"
    )
    bot.reply_to(message, reply_text)

if __name__ == '__main__':
    print("Бот успешно запущен и ждет заявки...")
    bot.infinity_polling()