# Introduction

This example contains the usage of following items:

- [Celery](https://docs.celeryproject.org/en/stable/index.html)
  - Broker: [AWS SQS](https://aws.amazon.com/sqs/)
  - Backend: [AWS RDS](https://aws.amazon.com/rds/) (Postgresql)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Flask in this example is just for showing results in the backend, which is optional for production use cases. If you just need a message queue to handle distributed messages, you don't need to deploy Flask into production.

## Diagram

![diagram.png](diagram/high-level-diagram.png)

## AWS setup in prototype

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

### Test RDS

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

### DDB setup (Optional)

If you plan to use DDB instead of RDS (which is much simpler than RDS), you can follow below spec:

1. Partition key (Hash key) can be anything, that's juse use `id`.
2. Sort key (Range key) is not needed.
3. RW both should be on-demand.


### AWS setup in Production

To prevent the complexity of learning this example, I have no plan to make this project contain code/config related to CDK/CloudFormation. If you want to proceed to production, you definitely should consider using them to setup the AWS environment. And you should always consider limiting to just enough permission for IAM role rather than Admin permission for IAM user.


## Docker setup

You need to install Docker Desktop in your host for development, follow [this guide](https://docs.docker.com/desktop/) to install it.

## Project setup

### Prerequisite

1. Make sure you finish AWS and Docker setup.
2. Make sure your RDS is accessible by **Debugger/db_conn.py**.

### Development

Start to run the application

```
docker-compose up --build
```

Access the flask app to test the functionality

```
http://127.0.0.1:8080
```

### Upload image to ECR

1. Create repository (One-off)

```
$ aws ecr create-repository --repository-name celery-test

{
    "repository": {
        "repositoryArn": "arn:aws:ecr:xx-yyyy-z:123456789:repository/celery-test",
        "registryId": "123456789",
        "repositoryName": "celery-test",
        "repositoryUri": "123456789.dkr.ecr.xx-yyyy-z.amazonaws.com/celery-test",
        "createdAt": 123456789.0,
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

2. Tag your image

```
$ docker images

REPOSITORY                                                 TAG                 IMAGE ID            CREATED             SIZE
celery-rds-sqs-flask-uwsgi-nginx_myapp-flask               latest              aaaaaabbbbbb        12 hours ago        1.03GB
celery-test_myapp-flask                                    latest              aaaaaacccccc        23 hours ago        1.03GB
celery-rds-sqs-flask-uwsgi-nginx_myapp-celery              latest              aaaaaadddddd        34 hours ago        1.02GB

$ docker tag aaaaaabbbbbb 123456789.dkr.ecr.xx-yyyy-z.amazonaws.com/celery-test:myapp-flask
$ docker tag aaaaaacccccc 123456789.dkr.ecr.xx-yyyy-z.amazonaws.com/celery-test:myapp-celery
$ docker tag aaaaaadddddd 123456789.dkr.ecr.xx-yyyy-z.amazonaws.com/celery-test:nginx
```

3 Login and push the image to ECR

```
$ $(aws ecr get-login --registry-ids 123456789 --no-include-email)
$ docker push 123456789.dkr.ecr.xx-yyyy-z.amazonaws.com/celery-test
```

#### Development without Docker

This project currently requires to develop by docker, local development requires some import path overrides. This is out of the scope of this project.


### Cleanup

Kill all docker processes

```
docker rm $(docker ps -a -q)
```


## TODO

- Provide CDK template
- Make the project locally develop-able


## Reference

- [Building a Flask app with Docker | Learning Flask Ep. 24](https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose)
- [https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e](https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e) 
