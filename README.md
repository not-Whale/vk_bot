### vk_bot - бот для продажи энергетиков в студенческом общежитии!
<img src="./src/resources/photos/main logo 250x250.png" alt="logo"/>

***
### Немного истории
*В конце февраля 2022 года* у двух моих хороших друзей родилась идея *продавать энергетики* в студенческом общежитии, чтобы сэкономить время других студентов на походе в магазин и дать возможность получить заряд кофеина даже ночью, когда все закрыто. 

В этот момент в моей голове возникла идея помочь им с продвижением и реализовать свою давнюю маленькую **мечту** - написать бота для *сообщества vk*, который будет работать как интерактивное меню и автоматизировать обработку заявок (представим, что поток клиентов достаточно большой для того, чтобы отвечать всем самостоятельно).

Так и появился *vk_bot*, актуальную версию которого вы можете видеть здесь!
***
### Описание
В репозитории представлен исходный код *бота для vkontakte*, который подключается к социальной сети путем авторизации как администратор (по логину и паролю) либо как сообщество (по ключу доступа). 

Есть **два** типа взаимодействия с ботом в зависимости от роли пользователя. Все роли пользователей *определяются при инициализации* экземпляра класса бота и *сохраняются локально* для каждой копии проекта. 

Интерфейс взаимодействия с ботом **для админов** представляет из себя одну главную клавиатуру, на которой пользователь может указать свой `on/offline` статус, изменить количество энерегтиков на руках в данный момент и отметить новую проведенную сделку. Также админу предоставляется возможность изучить свою *краткую статистику* по продажам с помощью той же основной клавиатуры. 

Интерфейс взаимодействия с ботом **для покупателей** имеет 5 уровней вложенности с *различными* вариантами движения по нему в зависимости от потребностей пользователя. С помощью бота покупатель может ознакомиться со своей статистикой покупок, сделать новый заказ (выбрать количество энерегетиков, способ оплаты, получить данные продавца), оставить отзыв или связаться с разработчиком.

Возможен случай, когда покупатель сделал заказ, но ни одного админа нет в сети, тогда каждому из находящихся в базе админов *отправляется оповещение* о том, что поступила новая заявка и её нужно обработать как можно скорее.
***
### Что будет дальше? 
В бущем мы планируем *развивать* наш продукт, добавляя больше интересных, удобных и просто приятных фишек. Посмотреть краткосрочные задачи или оставить свои пожелания по развитию вы всегда можете [во вкладке issues](https://github.com/not-Whale/vk_bot/issues). Кроме того, особого внимание заслуживают следующие изменения:
* Добавления стэка вызовов для ускорения движения по клавиатурам и оптимизации кода;
* Добавления простейших алгоритмов удержания клиента: 
    * Скидочные программы для оптовых покупателей, 
    * Скидочные программы для постоянных покупателей, 
    * Специальные предложения для заинтересованных, но не решившихся;
* Добавление ключей командной строки для запуска бота в различных режимах;
* Создание интерактивной оболочки отправки команд боту для взаимодействия с функционалом суперпользователя без перезапуска скрипта;
* Добавление к сообщениям бота милых **картинок с котиками и Дорой** для поднятия настроения покупателей и админов;
***
### Наша команда:
* Резепин Никита [[@not-Whale](https://github.com/not-Whale)]: разработчик бота, тестировщик, не кит
* Калита Никита [[@ontoshenka](https://github.com/ontoshenka)] : научный руководитель
* Поляков Данила [[@qqqq4u](https://github.com/qqqq4u)] : автор задумки, идейный вдохновитель
* Кравченко Данила [[@228Danila228](https://github.com/228Danila228)] : автор задумки, талисман команды
* Уксусов Егор [[@egkssv](https://vk.com/egkssv)] : дизайнер логотипа
***
### Инструкция по установке и запуску:
1. Склонируйте репозиторий в папку на персональном компьютере:  
```
git clone https://github.com/not-Whale/vk_bot
```
2. Создайте в директории `src/main/bot` файл `open_keys.py`;
3. Задайте в созданном файле следующие обязательные строковые переменные:
    * SBERBANK_CARD_NUMBER - номер карты Сбербанк для оплаты;
    * TINKOFF_CARD_NUMBER - номер карты Тинькофф для оплаты;
    * TELEPHONE_FOR_PAYMENT - номер телефона для переводов;
    * PAY_URL - ссылка на перевод через платежную систему (мы использовали платежи Тинькофф);
    * VK_TOKEN - токен для авторизации в качестве сообщества;
    * VK_LOGIN - логин админа (если авторизация планируется не через токен)
    * VK_PASSWORD - пароль админа (если авторизация планируется не через токен);
4. При необходимости в файл `src/main/main.py` добавьте строку:  
```
bot.add_new_admin(Admin(%user_id%, %room_number%, ...))
```
С полный списком параметров и описанием работы каждой функции бота можно ознакомиться, обратившись к [документации](https://not-whale.github.io/vk_bot/);  

5. Установите любую версию python 3.x.x c [официального сайта](https://www.python.org/downloads/), если она еще не установлена;
6. Запустите скрипт бота:  
```
python src/main/main.py
```
7. Переходите в личные сообщения сообщества Вконтакте;
8. Готово!
***
### Интересно прочитать
В процессе разработки я пользовался следующими *информационными* ресурсами:
* [Vk_api](https://github.com/python273/vk_api) для python и их [документацией](https://vk-api.readthedocs.io/en/latest/);
* [Документацией](https://vk.com/dev/methods) API от Вконтакте;
* [Мотивационной статьей](https://habr.com/ru/post/427691/) на Хабре;
* [Документацией](https://sphinx-ru.readthedocs.io/ru/latest/sphinx.html) Sphinx.

А также стандартами оформления кода и документации, поиск которых оставим в качестве домашнего задания!
***
### Связь с разработчиками
В случае, если у вас есть *интересные идеи* по дальнейшему развитию и применению проекта или вам хочется лично обсудить вопросы, связанные с этим или другими проектами, **напишите мне** на почту, указанную в профиле, либо свяжитесь со мной в социальных сетях: [вконтакте](https://vk.com/rezepinn) или [телеграмм](https://t.me/rezepinn).
