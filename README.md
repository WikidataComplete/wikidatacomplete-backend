# WikidataComplete-Backend

## Local Setup

- Git clone (`git clone https://github.com/WikidataComplete/wikidatacomplete-backend.git`)
- `cd wikidatacomplete-backend`
- Setup virtual environment (`python3 -m venv env .`)
- Install requirements (`pip install -r requirements.txt`)
- Create env file `touch .env`
- Add these variables inside env file:

```
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DEBUG=True/False
SECRET_KEY=""
```

- Run migrations (`python manage.py makemigrations`, `python manage.py migrate`)
- Run server (`python manage.py runserver`)
- See it running on http://localhost:8000/api/v1/facts/

## API Docs

- http://localhost:8000/swagger/
