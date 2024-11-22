from dotenv import load_dotenv
import json
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Файл для хранения списка подписчиков
USERS_FILE = "subscribed_users.json"

# Глобальный список пользователей
subscribed_users = []


# Загрузка списка подписчиков из файла
def load_users():
    global subscribed_users
    try:
        with open(USERS_FILE, "r") as f:
            subscribed_users = json.load(f)
        logging.info(f"Загружено {len(subscribed_users)} подписчиков.")
    except FileNotFoundError:
        subscribed_users = []
        logging.info("Файл с подписчиками не найден. Список пуст.")
    except Exception as e:
        logging.error(f"Ошибка при загрузке подписчиков: {e}")
        subscribed_users = []


# Сохранение списка подписчиков в файл
def save_users():
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(subscribed_users, f)
        logging.info(f"Список подписчиков ({len(subscribed_users)}) сохранен.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении подписчиков: {e}")


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id not in subscribed_users:
        subscribed_users.append(user.id)
        save_users()
        await update.message.reply_text("Вы подписаны на рассылку!")
        logging.info(f"Пользователь {user.id} подписан.")
    else:
        await update.message.reply_text("Вы уже подписаны.")


# Обработчик команды /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_id = int(os.getenv("ADMIN_ID", 0))
    if update.effective_user.id != admin_id:
        await update.message.reply_text("У вас нет прав для этой команды.")
        logging.warning(f"Пользователь {update.effective_user.id} попытался использовать /broadcast.")
        return

    message = ' '.join(context.args)
    if not message:
        await update.message.reply_text(
            "Введите сообщение, например: /broadcast Привет!"
        )
        return

    success_count = 0
    for user_id in subscribed_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            success_count += 1
        except Exception as e:
            logging.error(f"Ошибка отправки пользователю {user_id}: {e}")

    await update.message.reply_text(
        f"Сообщение отправлено {success_count} пользователям."
    )
    logging.info(f"Сообщение отправлено {success_count} подписчикам.")


# Основная функция запуска бота
def main():
    load_users()

    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError(
            "Токен бота не указан в переменной окружения BOT_TOKEN."
        )

    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Запуск бота
    logging.info("Бот запущен. Ожидание сообщений...")
    try:
        application.run_polling()
    except KeyboardInterrupt:
        logging.info("Остановка бота...")
    finally:
        save_users()
        logging.info("Список подписчиков сохранен при завершении работы.")


if __name__ == "__main__":
    main()
