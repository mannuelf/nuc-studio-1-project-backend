# FactBook Explorers: 

> Backend REST API

## System dependencies

You should use pyenv to install latest version of python

[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv), use the automatic installer: [https://github.com/pyenv/pyenv-installer](https://github.com/pyenv/pyenv-installer)

## Development dependencies

- [flask](https://flask.palletsprojects.com/)
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)

### 1. Install pyenv

```bash
$ pip3 install pyenv
```

### 2. Start pipenv shel

```bash
$ pipenv shell
```

### 3. Install Project dependencies

```bash
$ pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
```

You are good to go, start building, now you can run the app inside of pipenv.

### 4. Run inside pipenv
```bash
$ python app.py
```

