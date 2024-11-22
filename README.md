Телеграм бот для массовой рассылки.

1. После загрузки репозитория установите и активируйте виртуальное окружение

   python -m venv venv
   или
   python3 -m venv venv

   Активация:

   MacOS:      source venv/bin/activate
   Windows:    venvScriptsactivate

3. Установите зависимости

   pip install -r requirements.txt

4. Создайте файл .env и добавьте туда следующую информацию:
   
   BOT_TOKEN="токен_вашего_бота"
   ADMIN_ID="телеграм_id_администратора_бота"

5. Для запуска введите:

   python bot.py

6. Команды:

   Для отправки сообщения людям которые нажали "Start" в боте введите в телеграмме /broadcast Ваше сообщение
   
