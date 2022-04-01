Файлы классов доступа
=====================

Admin (класс для продавцов)
---------------------------

.. py:class:: Admin

    Класс админа для бота.

    **Атрибуты:**

    .. py:attribute:: self.user_id(str)

        Индивидуальный идентификатор - id страницы пользователя Вконтакте.

    .. py:attribute:: self.room_number(str)

        Номер комнаты.

    .. py:attribute:: self.menu_mode(str)

        Текущее положение админа в меню (название клавиатуры).

    .. py:attribute:: self.sberbank_card(str)

        Номер карты Сбербанк для оплаты.

    .. py:attribute:: self.tinkoff_card(str)

        Номер карты Тинькофф для оплаты.

    .. py:attribute:: self.telephone_number(str)

        Номер телефона, привязанный к мобильному банку, для перевода.

    .. py:attribute:: self.energy_amount(int)

        Количество энергетиков в наличии.

    .. py:attribute:: self.is_online(boolean)

        Статус в сети.

    .. py:attribute:: self.deals([int, datetime][])

        Массив проведенных сделок в формате: [количество энерегетиков, время сделки].

    **Методы:**

    .. py:method:: self.get_user_id(self)

        Получение значения поля user_id.

        :return: Индивидуальный идентификатор - id страницы пользователя Вконтакте.

    .. py:method:: self.get_room_number(self)

        Получение значения поля room_number.

        :return: Номер комнаты.

    .. py:method:: self.get_online_status(self)

        Получение значения поля is_online.

        :return: Статус в сети.

    .. py:method:: self.get_deals_list(self)

        Получение значения поля deals.

        :return: Массив проведенных сделок в формате: [количество энерегетиков, время сделки].

    .. py:method:: self.get_menu_mode(self)

        Получение значения поля menu_mode.

        :return: Текущее положение админа в меню (название клавиатуры).

    .. py:method:: self.get_energy_amount(self)

        Получение значения поля energy_amount.

        :return: Количество энергетиков в наличии.

    .. py:method:: self.get_sberbank_card(self)

        Получение значения поля sberbank_card.

        :return: Номер карты Сбербанк для оплаты.

    .. py:method:: self.get_tinkoff_card(self)

        Получение значения поля tinkoff_card.

        :return: Номер карты Тинькофф для оплаты.

    .. py:method:: self.get_telephone_number(self)

        Получение значения поля telephone_number.

        :return: Номер телефона, привязанный к мобильному банку, для перевода.

    .. py:method:: self.set_online(self)

        Изменение статуса админа на online.
        Меняет значение поля *is_online*.

    .. py:method:: self.set_offline(self)

        Изменение статуса админа на offline.
        Меняет значение поля *is_online*.

    .. py:method:: self.set_menu_mode(self, menu_mode)

        Установка положения в меню.
        Меняет значение поля *menu_mode*.

        :param menu_mode: Новое положение админа в меню.
        :type menu_mode: str

    .. py:method:: self.set_energy_amount(self, amount)

        Установка количества энерегетиков.
        Меняет значение поля *energy_amount*.

        :param amount: Новое количество энерегетиков.
        :type amount: int

    .. py:method:: self.new_deal(self, deal)

        Добавление новой сделки.
        Меняет значение поля *deals*.

        :param deal: Новая сделка.
        :type deal: [int, datetime]


Client (класс для клиентов)
---------------------------

.. py:class:: Client

    Класс клиента для бота.

    **Атрибуты:**

    .. py:attribute:: self.user_id(str)

        Индивидуальный идентификатор - id страницы пользователя Вконтакте.

    .. py:attribute:: self.name(str)

        Имя пользователя.

    .. py:attribute:: self.menu_mode(str)

        Текущее положение клиента в меню (название клавиатуры).

    .. py:attribute:: self.deals(int)

        Количество совершенных сделок.

    .. py:attribute:: self.energy_amount(int)

        Количество купленных энерегетиков.

    .. py:attribute:: self.current_order(src.main.user.order.Order)

        Объект текущего заказа.

    **Методы:**

    .. py:method:: self.get_user_id(self)

        Получение значения поля user_id.

        :return: Индивидуальный идентификатор - id страницы пользователя Вконтакте.

    .. py:method:: self.get_menu_mode(self)

        Получение значения поля menu_mode.

        :return: Текущее положение клиента в меню (название клавиатуры).

    .. py:method:: self.get_number_of_deals(self)

        Получение значения поля deals.

        :return: Количество совершенных сделок.

    .. py:method:: self.get_user_name(self)

        Получение значения поля name.

        :return: Имя пользователя.

    .. py:method:: self.get_energy_amount(self)

        Получение значения поля energy_amount.

        :return: Количество купленных энерегетиков.

    .. py:method:: self.get_current_order(self)

        Получение значения поля current_order.

        :return: Объект текущего заказа.

    .. py:method:: self.set_menu_mode(self, menu_mode)

        Установка положения в меню.
        Меняет значение поля *menu_mode*.

        :param menu_mode: Новое положение клиента в меню.
        :type menu_mode: str

    .. py:method:: self.new_deal(self, energy_amount)

        Добавление новой сделки.
        Меняет значения полей *deals*, *energy_amount*.

        :param energy_amount: Количество купленных энергетиков.
        :type energy_amount: int


Order (класс заказа клиента)
----------------------------

.. py:class:: Order

    Класс заказа клиента.

    **Атрибуты:**

    .. py:attribute:: self.client_id(str)

        Индивидуальный идентификатор клиента - id страницы пользователя Вконтакте.

    .. py:attribute:: self.energy_amount(int)

        Количество энергетиков в заказе.

    .. py:attribute:: self.admin(src.main.user.admin.Admin)

        Объект админа, привязанного к заказу.

    **Методы:**

    .. py:method:: self.set_energy_amount(self, energy_amount)

        Установка количества заказанных энерегетиков.
        Меняет значение поля *energy_amount*.

        :param energy_amount: Количество энерегетиков в заказе.
        :type energy_amount: int

    .. py:method:: self.set_admin(self, admin)

        Установка привязанного к заказу админа.
        Меняет значение поле *admin*.

        :param admin: Объект админа, привязываемого к заказу.
        :type admin: src.main.user.admin.Admin

    .. py:method:: self.get_admin(self)

        Получение значения поля admin.

        :return: Объект админа, привязанного к заказу.

    .. py:method:: self.get_energy_amount(self)

        Получение значение поля energy_amount.

        :return: Количество энерегетиков в заказе.

    .. py:method:: self.clear_order(self)

        Удаление заказа.
        Меняет значение полей *energy_amount*, *admin*.
