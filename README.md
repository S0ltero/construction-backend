# ConstructionCRM

**ENG:** Project implements a CRM system for a construction company with the following functionality:

- Create list of construction elements (e.g. nails or planks)
- Create list of constructions (e.g. house frame)
- Create list of projects (e.g. two-storey log house)
- Create list of templates (can be user on create project)
- Create list of clients
- Elements can be exported to excel table or imported
- Project can be exported to excel table with his nested structured (e.g. constructions and elements)
  - Can be exported for estimate, purchaser and foreman person

---

**RUS:** Проект реализует CRM систему для строительной компании со следующим функционалом:

- Создание списка строительных элементов (Например: гвоздей или планок)
- Создание списка конструкций (Например: каркаса дома)
- Создание списка проектов (Например: двухэтажного дома из бруса)
- Создание списка клиентов
- Экспорт элементов в excel таблицу, или импорт
- Экспорт проекта в excel таблицу со всеми его вложенными структурами (Например: конструкций и элементов)
  - Может быть экспортирован для клиента, закупщика и бригадира


# Prerequisites

- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [PostgreSQL](https://www.postgresql.org/)

# Environments

Create file `.env`

Provide in file this values:

```
DJANGO_SECRET_KEY=        # Can be generated here: https://djecrety.ir/
DJANGO_ALLOWED_HOSTS=     # hosts split by whitespace
DJANGO_DEBUG=             # 1 or 0

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_HOST=                  # For use local database, set `host.docker.internal` 
```

# Local Development

Start the dev server for local development:

```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Create migrations

```
docker-compose run --rm web python manage.py makemigrations
```

Apply migrations

```
docker-compose run --rm web python manage.py migrate
```

Create superuser

```bash
docker-compose run --rm web python manage.py createsuperuser
```
