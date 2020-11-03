# FactBook Explorers: 

> Backend REST API

## Local development

To get started download the repo using SSH ([guide on SSH](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent))

```bash
$ git clone git@github.com:mannuelf/nuc-studio-1-project-backend.git

$ cd nuc-studio-1-project-backend/

```

If all required dependecies are installed, to work on the project you must run it in a python environment using pipenv.

### 1. Start pipenv shell

Run this command to start a python environment, immediatly afterwards run python app.py.

```bash
$ pipenv shell
>> python app.py
```

### 2. Contributing code

We will use peer review in the form of Pull Requests. You must make a feature branch before starting to code. The `main` branch must always be clean and deployable at all times, do not work on `main` branch.

Lessons on branches and merging can be seen here: [:tv: Watch](https://github.com/Noroff-Fagskole/campus-advisor-training-mannuelf/tree/master/Module%201)


### Endpoints

| Method | Endpoint | Description |
| ------ | :------- | :---------- |
| GET | /hello-world | Gets all test messages |
| GET | /hello-world/{id} | Get one message |
| POST | /hello-world/ | Post a message to API |


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

### 2. Start pipenv shell


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

#### 4.1 Create a db, inside pipenv (only need to do this once one a fresh app.)

```bash
$ python app.py
>> from app import db
>> db.create_all()
>> exit()
```
