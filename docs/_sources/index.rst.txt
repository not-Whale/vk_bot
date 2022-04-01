.. vk_bot documentation master file, created by
   sphinx-quickstart on Thu Mar 31 15:18:45 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация vk_bot
===================
vk_bot - бот для продажи энергетиков в студенческом общежитии, подключаемый к сообществу


Установка и запуск
------------------
Для быстрой установки и запуска проекта:

1. Склонируйте репозиторий в папку на персональном компьютере:

   .. code-block:: shell-session

      # git clone https://github.com/not-Whale/vk_bot

2. Создайте в директории **src/main/bot** файл **open_keys.py**;

3. Задайте в созданном файле следующие обязательные строковые переменные:

   * SBERBANK_CARD_NUMBER - номер карты Сбербанк для оплаты;

   * TINKOFF_CARD_NUMBER - номер карты Тинькофф для оплаты;

   * TELEPHONE_FOR_PAYMENT - номер телефона для переводов;

   * PAY_URL - ссылка на перевод через платежную систему (мы использовали платежи Тинькофф);

   * VK_TOKEN - токен для авторизации в качестве сообщества;

   * VK_LOGIN - логин админа (если авторизация планируется не через токен)

   * VK_PASSWORD - пароль админа (если авторизация планируется не через токен);

4. Отредактируйте файл **src/main/main.py** под свои нужны. Например:

   .. code-block:: python

      from src.main.bot.adrenaline_bot import Adrenaline_bot
      from src.main.user.admin import Admin

      bot = Adrenaline_bot()
      bot.add_new_admin(
         Admin(
            'user_id',
            'room_number',
            'sberbank_card',
            'tinkoff_card',
            'telephone_number'
         )
      )
      bot.start_bot()

Примеры настройки бота можно посмотреть в разделе Примеры_ или на Github (ССЫЛКА).

.. _Примеры: examples.html

Навигация
---------

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   main
   bot
   users
   examples


.. Indices and tables
   ------------------
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
