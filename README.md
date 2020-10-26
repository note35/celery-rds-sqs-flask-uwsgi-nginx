# Introduction

This example contains the usage of following items:

- [Celery](https://docs.celeryproject.org/en/stable/index.html)
  - Broker: [AWS SQS](https://aws.amazon.com/sqs/)
  - Backend: [AWS RDS](https://aws.amazon.com/rds/) (Postgresql)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Flask in this example is just for showing results in the backend, which is optional for production use cases. If you just need a message queue to handle distributed messages, you don't need to deploy Flask into production.


# AWS setup in prototype

- IAM user and SQS
  - For prototype, it's okay to do things by a IAM user with admin permission
  - There's no setup for SQS if your IAM user has admin permission

- RDS
  - You can follow [this guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html#) to setup RDS.
  - After creating a database in AWS console, by default there's no database but only database name. So you will meet the following error: `while connecting to PostgreSQL FATAL:  database 'database_name' does not exist`. To solve this, you need to follow the below steps. [Reference](https://stackoverflow.com/questions/17633422/psql-fatal-database-user-does-not-exist).
    - You can follow [this guide](https://blog.timescale.com/tutorials/how-to-install-psql-on-mac-ubuntu-debian-windows/) to install psql command

Here's MacOS example:

```python
brew install libpq
createdb <database_name> -h <database_endpoint> -U <database_name>
```

## Test RDS

1. Copy **myapp/config.py.example** to **myapp/config.py** and fill the information
2. Setup python environment

```
python3 -m venv py3
./py3/bin/pip install -r myapp/requirements-dev.txt

# In MacOS, you may need to install with param
ARCHFLAGS="-arch x86_64" ./py3/bin/pip install -r myapp/requirements-dev.txt
```

3. Use **Debugger/db_conn.py** to test the connect-ability

```
./py3/bin/python Debugger/db_conn.py
```

## AWS setup in Production

To prevent the complexity of learning this example, I have no plan to make this project contain code/config related to CDK/CloudFormation. If you want to proceed to production, you definitely should consider using them to setup the AWS environment. And you should always consider limiting to just enough permission for IAM role rather than Admin permission for IAM user.


# Docker setup

You need to install Docker Desktop in your host for development, follow [this guide](https://docs.docker.com/desktop/) to install it.

# Project setup

## Prerequisite

1. Make sure you finish AWS and Docker setup.
2. Make sure your RDS is accessible by **Debugger/db_conn.py**.

## Development

Start to run the application

```
docker-compose up --build
```

Access the flask app to test the functionality

```
http://127.0.0.1:8080
```

### Development without Docker

This project currently requires to develop by docker, local development requires some import path overrides. This is out of the scope of this project.


## Cleanup

Kill all docker processes

```
docker rm $(docker ps -a -q)
```


# TODO

- Provide CDK template
- Make the project locally develop-able


# Reference

- [Building a Flask app with Docker | Learning Flask Ep. 24](https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose)
- [https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e](https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e) 
