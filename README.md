"Платформа для онлайн обучения "
Реализован бэкенд-сервер для SPA веб-приложения LMS-системы, который возвращает клиенту JSON-структуры.
Django-проект, CRUD уроков, курсов, пользователей, возможность оплаты с использованием STRIPE, реализована задача которая проверят пользователей по дате последнего входа, функционал по подписке на обновление уроков/курсов через асинхронную рассылку с помощью Celery и Celery Beat. .
Настроен вывод документации проекта, основной функционал покрыт тестами.


Для запуска проекта (используется Poetry):
скачать файлы из репозитория,
установить зависимости poetry install,,
заполнить данными файл .env.sample переименовав его в .env
фикстуры для БД: payments.json, users/fixtures/groups.json
команда создание суперюзера: python3 manage.py csu
команда загрузки списка платежей: python3 manage.py load_payments


Шаг 6. (текущий)
Задание 1
Настройте проект для работы с Celery. Также настройте приложение на работу с 
celery-beat для выполнения периодических задач.
Не забудьте вынести настройки Redis в переменные окружения.

Задание 2
Ранее вы реализовали функционал подписки на обновление курсов. 
Теперь добавьте асинхронную рассылку писем пользователям об обновлении материалов курса.

Подсказка
Чтобы реализовать асинхронную рассылку, вызывайте специальную задачу по отправке письма 
в коде контроллера. То есть вызов задачи на отправку сообщения должен происходить в контроллере
обновления курса: когда курс обновлен — тем, кто подписан на обновления именно этого курса, 
отправляется письмо на почту.

Дополнительное задание
Пользователь может обновлять каждый урок курса отдельно. Добавьте проверку на то, 
что уведомление отправляется только в том случае, если курс не обновлялся более четырех часов.

Задание 3
С помощью celery-beat реализуйте фоновую задачу, которая будет проверять пользователей по дате 
последнего входа по полю last_login и, если пользователь не заходил более месяца, 
блокировать его с помощью флага is_active.
Задачу сделайте периодической и запланируйте расписание в настройках celery-beat.
Обратите внимание на timezone вашего приложения и timezone в настройках celery: важно, 
чтобы они были одинаковыми, чтобы задачи запускались в корректное время. 
Дополнительное задание, помеченное звездочкой, желательно, но не обязательно выполнять.

Шаг 5. (выполнен)
Задание 1
Подключить и настроить вывод документации для проекта. Убедиться, что каждый из реализованных эндпоинтов описан в 
документации верно, при необходимости описать вручную.
Для работы с документацией проекта воспользуйтесь библиотекой drf-yasg или drf-spectacular.
Как вручную можно сформировать документацию в drf-yasg можно почитать тут, в drf-spectacular — тут или тут.

Задание 2
Подключить возможность оплаты курсов через https://stripe.com/docs/api.
Доступы можно получить напрямую из документации, а также пройти простую регистрацию 
по адресу https://dashboard.stripe.com/register.
Для работы с учебным проектом достаточно зарегистрировать аккаунт и не подтверждать его — аккаунт 
будет находиться в тестовом режиме.
Для работы с запросами вам понадобится реализовать обращение к эндпоинтам:
https://stripe.com/docs/api/products/create — создание продукта;
https://stripe.com/docs/api/prices/create — создание цены;
https://stripe.com/docs/api/checkout/sessions/create — создание сессии для получения ссылки на оплату.
При создании цены и сессии обратите внимание на поля, которые вы передаете в запросе. Внимательно изучите 
значение каждого поля и проанализируйте ошибки при их возникновении, чтобы создать корректную запись.
При создании сессии нужно передавать id цены, которая соответствует конкретному продукту.
Для тестирования можно использовать номера карт из документации:
https://stripe.com/docs/terminal/references/testing#standard-test-cards.
Примечание
Подключение оплаты лучше всего рассматривать как обычную задачу подключения к стороннему API.
Основной путь: запрос на покупку → оплата. Статус проверять не нужно.
Каждый эквайринг предоставляет тестовые карты для работы с виртуальными деньгами.
Подсказка
Необходимо связать данные от сервиса платежей со своим приложением. Все взаимодействия с платежным сервисом 
опишите в сервисных функциях. Сервисные функции взаимодействуют с платежным сервисом (Stripe) и отдают ответы 
в виде JSON. Далее результаты работы сервисных функций мы используем в соответствующих View: при создании платежа в 
нашей системе мы должны создать продукт, цену и сессию для платежа в Stripe, сохранить ссылку на оплату в созданном 
платеже в нашей системе и отдать пользователю в ответе на POST-запрос ссылку на оплату или данные о платеже (которые 
будут включать ссылку на оплату).
При необходимости проверки статуса платежа можно реализовать дополнительную View, которая будет обращаться на 
Session Retrieve (https://stripe.com/docs/api/checkout/sessions/retrieve) по id созданной в Stripe сессии и 
отдавать пользователю данные о статусе платежа. Статус платежа также можно дополнительно хранить в модели платежей 
в нашей системе.
Перед созданием сессии необходимо создать продукт и цену. Все эти данные мы можем получить из модели платежа (модель 
платежа связана с продуктом, в продукте есть название и цена).
Обратите внимание, что цены при передаче в Strip указываются в копейках (то есть текущую цену продукта 
нужно умножить на 100).

Дополнительное задание
Реализуйте проверку статуса с помощью эндпоинта https://stripe.com/docs/api/checkout/sessions/retrieve — получение 
данных о сессии по идентификатору.
Дополнительное задание, помеченное звездочкой, желательно, но не обязательно выполнять.

Шаг 4. (выполнен)
Задание 1
Для сохранения уроков и курсов реализуйте дополнительную проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.
То есть ссылки на видео можно прикреплять в материалы, а ссылки на сторонние образовательные платформы или личные сайты — нельзя.
Создайте отдельный файл validators.py, реализуйте валидатор, проверяющий ссылку, 
которую пользователь хочет записать в поле урока с помощью класса или функции.
Интегрируйте валидатор в сериализатор.

Задание 2
Добавьте модель подписки на обновления курса для пользователя.
Вам необходимо реализовать эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.
При этом при выборке данных по курсу пользователю необходимо присылать признак подписки текущего пользователя на курс. 
То есть давать информацию, подписан пользователь на обновления курса или нет.

Задание 3
Реализуйте пагинацию для вывода всех уроков и курсов.

Пагинацию реализуйте в отдельном файле 
paginators.py. Можно реализовать один или несколько классов пагинатора. 
Укажите параметры page_size, page_size_query_param, max_page_size для класса PageNumberPagination. 
Количество элементов на странице выберите самостоятельно. 
Интегрируйте пагинатор в контроллеры, используя параметр pagination_class.

Задание 4
Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.

В тестах используйте метод setUp для заполнения базы данных тестовыми данными. 
Обработайте возможные варианты взаимодействия с контроллерами пользователей с разными правами доступа. 
Для аутентификации пользователей используйте self.client.force_authenticate().
Сохраните результат проверки покрытия тестами.

Шаг 3. (выполнен)
Задание 1
Реализуйте CRUD для пользователей, в том числе регистрацию пользователей, настройте в проекте использование JWT-авторизации и закройте каждый эндпоинт авторизацией.
    Эндпоинты для авторизации и регистрации должны остаться доступны для неавторизованных пользователей.

Задание 2
Заведите группу модераторов и опишите для нее права работы с любыми уроками и курсами, но без возможности их удалять и создавать новые. Заложите функционал такой проверки в контроллеры.

Задание 3
Опишите права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть, редактировать и удалять только свои курсы и уроки.
    Примечание
    Заводить группы лучше через админку и не реализовывать для этого дополнительных эндпоинтов.

Дополнительное задание
    Для профиля пользователя введите ограничения, чтобы авторизованный пользователь мог просматривать любой профиль, но редактировать только свой. При этом для просмотра чужого профиля должна быть доступна только общая информация, в которую не входят: пароль, фамилия, история платежей.
Примечание: дополнительные задания, помеченные звездочкой, желательны, но не обязательны к выполнению.

Шаг 2. (выполнен)

Задание 1
Для модели курса добавьте в сериализатор поле вывода количества уроков. Поле реализуйте с помощью
SerializerMethodField()

Задание 2
Добавьте новую модель в приложение users:
Платежи
    пользователь,
    дата оплаты,
    оплаченный курс или урок,
    сумма оплаты,
    способ оплаты: наличные или перевод на счет.
    Поля:
    пользователь,
    оплаченный курс
    и
    отдельно оплаченный урок
    должны быть ссылками на соответствующие модели.
Запишите в таблицу, соответствующую этой модели данные через инструмент фикстур или кастомную команду.
    Если вы забыли как работать с фикстурами или кастомной командой - можете вернуться к уроку 20.1 Работа с ORM в Django чтобы вспомнить материал.

Задание 3
Для сериализатора для модели курса реализуйте поле вывода уроков. Вывод реализуйте с помощью сериализатора для связанной модели.
    Один сериализатор должен выдавать и количество уроков курса и информацию по всем урокам курса одновременно.

Задание 4
Настроить фильтрацию для эндпоинта вывода списка платежей с возможностями:
    менять порядок сортировки по дате оплаты,
    фильтровать по курсу или уроку,
    фильтровать по способу оплаты.

Дополнительное задание
    Для профиля пользователя сделайте вывод истории платежей, расширив сериализатор для вывода списка платежей


Шаг 1. (выполнен)

Задание 1
Создайте новый Django-проект, подключите DRF в настройках проекта.

Задание 2
Создайте следующие модели:
    Пользователь:
        все поля от обычного пользователя, но авторизацию заменить на email;
        телефон;
        город;
        аватарка.
    Модель пользователя разместите в приложении users
    Курс:
        название,
        превью (картинка),
        описание.
    Урок:
        название,
        описание,
        превью (картинка),
        ссылка на видео.
    Урок и курс - это связанные между собой сущности. Уроки складываются в курс, в одном курсе может быть много уроков. Реализуйте связь между ними.
Модель курса и урока разместите в отдельном приложении. Название для приложения выбирайте такое, чтобы оно описывало то, с какими сущностями приложение работает. Например, lms или materials - отличные варианты.

Задание 3
Опишите CRUD для моделей курса и урока. Для реализации CRUD для курса используйте Viewsets, а для урока - Generic-классы.
Для работы контроллеров опишите простейшие сериализаторы.
    При реализации CRUD для уроков реализуйте все необходимые операции (получение списка, получение одной сущности, создание, изменение и удаление).
Для работы контроллеров опишите простейшие сериализаторы.
    Работу каждого эндпоинта необходимо проверять с помощью Postman.
    Также на данном этапе работы мы не заботимся о безопасности и не закрываем от редактирования объекты и модели даже самой простой авторизацией.

