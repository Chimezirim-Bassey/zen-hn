# ZenHN

Django Fullstack Project with ZenBlog Bootstrap Template.

## Commands

Run the following commands to populate the database with data from hackernews api using the `async-queue-manager`

### Populate

Populate the database by scraping the top stories 

```bash
python manage.py populate --timeout 600
```

### Latest

Get the latest by walking back from the latest item

```bash
python manage.py latest --timeout 600 --amount 6000
```

### Updates

Get the latest updates

```bash
python manage.py update --timeout 600
```

## Usage

Run with docker compose

```bash
docker compose up
```
