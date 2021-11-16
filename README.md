# Cuppy
YASP. "Smart" plant carer.


Document de analiza a cerintelor clientului

https://docs.google.com/document/d/1-p3hWnDAfIacA3iQ7mOvyylVqV1A6ozL/edit?usp=sharing&ouid=113184110368473894588&rtpof=true&sd=true

## Pentru development

Creeaza un virtual environment:
```python3 -m venv .``` (in folderul in care ai dat clone)
```source bin/activate```
```pip install -r requirements.txt```

Ca sa rulezi server-ul:
```python manage.py runserver```

Ca sa faci migratiile (daca schimbi/adaugi/stergi ceva in models.py):
```python manage.py makemigrations cuppy```
```python manage.py migrate```

Credentiale pentru superuser pentru development:
username: admin
user email: admin@example.com
pass: f!WY3GGJrNJ^oeDBmyL6B$