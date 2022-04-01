Файл запуска main.py
====================
Для запуска бота достаточно отредактировать файл **src/main/main.py** под свои нужны и запустить скрипт:

.. code-block:: shell-session

    # cd vk_bot
    # python src/main/main.py

Пример 1
--------
Для запуска бота только для клиентов (в данном случае не будет возможности оформить заказ, потому что не будет списка админов-продавцов) используйте:

.. code-block:: python

    from src.main.bot.adrenaline_bot import Adrenaline_bot

    bot = Adrenaline_bot()
    bot.start_bot()

Пример 2
--------
Для добавления админов используйте:

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

После добавления админа он сохранится в списке,
который резервно копируется в локальный файл admins.pickle
автоматически, поэтому в случае **перезапуска** бота
**необходимо** использовать код из **Примера 1**.

Больше примеров использования бота можно найти тут_.

.. _тут: examples.html