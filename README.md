# WikidataComplete-Backend

## Local Setup (using python 3.7)

- Git clone (`git clone https://github.com/WikidataComplete/wikidatacomplete-backend.git`)
- `cd wikidatacomplete-backend`
- Setup virtual environment (`python3 -m venv env .`)
- Activate virtual environment (`source env/bin/activate`)
- Install requirements (`pip install -r requirements.txt`)
- Create env file `touch .env`
- Add these variables inside env file:

```
DEBUG=True/False (have 1 value either True or False)
SECRET_KEY=""    (use django project secret key here, can be generated via https://djecrety.ir/)
```

- Run migrations (`python manage.py makemigrations`, `python manage.py migrate`)
- Run server (`python manage.py runserver`)
- Run custom management command to populate data (`python manage.py transfer_old_facts`)
- See it running on http://localhost:8000/api/v1/facts/

## API Docs

- https://datacompletewiki.toolforge.org/ (on live)
- http://localhost:8000/ (on local)
