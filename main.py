import asyncio
import os
from threading import Thread
from flask import Flask

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


async def send_with_typing(update, text, delay=1.5):
    """Отправляет сообщение с эффектом 'печатает...'"""
    await update.message.chat.send_action(action='typing')
    await asyncio.sleep(delay)
    await update.message.reply_text(text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Срабатывает при нажатии кнопки Start."""
    await send_with_typing(
        update,
        'Здравствуйте, мне сказали, что вы занимаетесь поиском человека, укравшего мой торт. Это так?',
        delay=4.0
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # ФИНАЛ, часть 2 — "А как же гости? Вы остались без торта?"
    if 'а как же гости' in text or 'остались без торта' in text:
        await send_with_typing(
            update,
            'Не переживайте, все были накормлены.Я купила другой торт, хоть и не совсем подходящий по стилю к моему празднику.'
            'Так что забирайте найденный торт себе и устраивайте чаепитие – вы это заслужили!🤗 '
            'Пусть этому негоднику всё вернется, и он получит по заслугам, а я с ним еще сама поговорю. '
            'Спасибо вам ещё раз!💕',
            delay=15.0
        )

    # ФИНАЛ, часть 1 — "нашли воришку, им оказался Арсений"
    elif 'нашли воришку' in text or 'им оказался арсений' in text or 'оказался арсений' in text:
        await send_with_typing(
            update,
            'Какой же Арсений негодяй, надо же было торт украсть! 🤦‍♀️'
            'Вы и ваши детективы просто огромные молодцы, спасибо вам огромное за проделанную работу. '
            'Но, увы, праздник уже закончился, все разошлись.',
            delay=10.5
        )

    elif 'мы на месте' in text or 'скоро будет найден' in text:
        await send_with_typing(update, 'Хоть бы, хоть бы.', delay=5.0)

    elif 'нашли улики' in text or 'скоро отправимся к детективам' in text:
        await send_with_typing(update, 'Поняла вас.', delay=4.0)

    elif 'будем сообщать' in text or 'сделаем все возможное' in text:
        await send_with_typing(update, 'Спасибо.', delay=3.5)

    elif 'собираем улики' in text or 'приступим к поиску' in text:
        await send_with_typing(
            update,
            'Найдите поскорее, пожалуйста. Праздник должен состояться.😣 '
            'Но даже если не успеете, главное – найти вора!',
            delay=7.0
        )

    else:
        await send_with_typing(update, 'Хм, я не совсем поняла...', delay=2.0)


def run_bot():
    """Запускает бота в отдельном потоке."""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('Бабушка Агафья на связи!')
    app.run_polling()


web_app = Flask(__name__)


@web_app.route('/')
@web_app.route('/health')
def health_check():
    return 'Bot is running', 200


def run_web():
    """Запускает Flask-сервер в отдельном потоке."""
    port = int(os.environ.get('PORT', 5000))
    web_app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    run_bot()

    # Бот — в главном потоке (так надо для Telegram)
    run_bot()
