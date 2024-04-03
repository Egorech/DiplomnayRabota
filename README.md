<h1>Backend приложение по парсингу данных с маркетплейсов на основе DjangoRestFramework</h1>

Возможности приложения:
1) возможность авторизации и аутентификация в системе;
2) возможность парсить цены товаров с маркетплейсов
3) возможность парсить характеристики товаров с маркетплейсов
3) возможность получения данных о том, сколько раз были собраны данные с тех или иных сайтов
4) возможность менять статус задачи, в зависимости от того, на каком этапе находится задача парсинга
5) возможность парсить данные асинхронно, чтобы пользователь не ждал в реальном времени окончания решения задачи

Используемые технологии:
1) DjangoRestFramework
2) RabbitMQ
3) Celery
4) PostgreSQL
5) Docker Compose

Схема БД:
![image](https://github.com/Egorech/DiplomnayRabota/assets/90097022/ed0e906b-af22-452f-9faf-6299d1b9cbfd)

1) Таблица CustomUser хранит информацию о имени пользователя, пароле, почте и имени с фамилией.
2) Таблица OfferTask хранит информацию о статусе задачи и использует связь один ко многому с CustomUser, так один пользователь может иметь много задач.
3) Таблица OfferTaskRequst хранит информацию о запросе пользователя, и также использует связь один к одному c OfferTask, так как каждая задача имеет только один статус выполнения и пользователя.
4) Таблица ProductOffer хранит информацию о регионе, домене, ссылке, имеет свой статус выполнения и хранит в себе данные о исходной задаче, также использует связь один ко многому с OfferTask, так как каждая задача может иметь множество продуктов.
5) Таблица Offer хранит информацию о ценах продуктов и имеет связь один ко многому с ProductOffer, так как у продукта могут быть разные цены (обычная цена, цена по скидке и т.д.).
6) Таблица SpecTask хранит информацию о статусе задачи и использует связь один ко многому, так один пользователь может иметь много задач.
7) Таблица SpecTaskRequst хранит информацию о запросе пользователя, и также использует связь один к одному с SpecTask, так как каждая задача имеет только один статус выполнения и пользователя.
8) Таблица ProductSpec хранит информацию о домене, статусе, данных о исходной задаче и имеет связь один ко многому с SpecTask, так как у одной задачи может быть множество характеристик.

Для запуска проекта нужно будет сделать следующие действия:
1) git clone https://github.com/Egorech/DiplomnayRabota.git
2) docker compose build
3) docker compose up
5) http://localhost:8000/

<strong>(Важно отметить, что для корректной работы с Docker нужен запщуенный docker engine, в качестве решения можете скачать Docker Desktop по ссылке: https://www.docker.com/products/docker-desktop/)</strong>