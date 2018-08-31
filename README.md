How to build and run a docker environnement
=====

Installation
-----

This assumes you already have a minimal developper enrionnemt installed.
You need:
- Docker
- Python 2 or Python 3 (you might need to run ```pip install python-dotenv```)

Steps:
1. Build the necessary notebook images:
    > open a terminal in this folder and run:
    ```bash
    bash
    sh build_all.sh
    ```
    This will build the images (**it will take a while !!!)**:
    -  *'ewsconsulting/ubuntu_python'*
    -  *'ewsconsulting/nb_py2'*
    -  *'ewsconsulting/nb_py3'*
    -  *'ubuntu'* (could be removed)

2. Create the volumes used to store the Postgresql and MongoDB data
    > open a terminal in this folder and run:
    ```cmd
    docker volume create --driver local --name=pgvolume
    docker volume create --driver local --name=pga4volume
    docker volume create --driver local --name=mongovolume
    docker volume ls
    ```
    This will create the named volumes:
    -  *'mongovolume'*
    -  *'pga4volume'*
    -  *'pgvolume*
3. Create a ```.env``` file:
    > open a terminal in this folder and run:
    ```cmd
    bash
    touch .env
    ```
    > This will create and empty .env file.<br>
    > Open it and add the followwing entries (add the necessary passwords and email):
    ```text
    # POSTGRESQL DATABASE
    POSTGRES_HOST=postgres_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<a password here!!!>
    POSTGRES_DB=ewsdb
    POSTGRES_PORT=5432

    # MongoDB
    MONGO_INITDB_ROOT_USERNAME=mongo
    MONGO_INITDB_ROOT_PASSWORD=<a password here!!!>

    # PG ADMIN
    PGADMIN_SETUP_EMAIL=<your_email here!!!>
    PGADMIN_SETUP_PASSWORD=<a password here!!!>
    SERVER_PORT=5050

    # General
    EWS_DRIVES_PATH=/home/ewsuser/ews_drives/
    EWS_DRIVES_PATH_SEPARATOR=_
    ```

4. Build the docker-compose.yaml file and pull the necessary images:
    > open a terminal in this folder and run:
    ```bash
    python write_docker-compose.py --no-py2 --no-py3 --postgres --pgadmin --mongo --mongoexp --no-mount
    docker-compose pull
    ```
    This will pull the images (**it can take a while !!!**):
    -  *'crunchydata/crunchy-pgadmin4:centos7-10.5-2.1.0'*
    -  *'timescale/timescaledb-postgis:0.11.0-pg10'*
    -  *'mongo:4.0.1'*
    -  *'mongo-express:0.49.0'*
    -  *'debian:jessie-slim'* (could be removed)

5. You can start the service py running:    ```start_docker-compose.bat```
    > By default, the options are:<br>
        - ```--py2``` *(this will enable a service for Jupyter/Python2 on port 8888)*<br>
        - ```--py3``` *(this will enable a service for Jupyter/Python3 on port 8889)*<br>
        - ```--postgres``` *(this will enable a service for PostgreSQL)*<br>
        - ```--pgadmin``` *(this will enable a service for PgAdmin4 on port 5050)*<br>
        - ```--mongo``` *(this will enable a service for MongoDB)*<br>
        - ```--mongoexp``` *(this will enable a service for Mongo-Express on port 8081)*<br>
        - ```--drives f,p,s,t``` *(this will mount the drives F:, P:, S: and T:)*<br>

6. To kill the service, use:    ```docker-compose rm -f -s -v```

7. Setup ***pgAdmin4***:
    > Go in [pgAdmin4 web interface](http://192.168.1.88:5050/browser)
    > Log-in using the login and password you defined for:
     - $PGADMIN_SETUP_EMAIL
     - $PGADMIN_SETUP_PASSWORD
    > Create a new server connection:
     - ```General/Name```: PG10 (or whatever)
     - ```Connection/Host name```: $POSTGRES_HOST
     - ```Port```: 5432
     - ```Username```: $POSTGRES_USER
     - ```Password```: $POSTGRES_PASSWORD
    > You should be sweet!



Remove commands
====
```bash
docker image rm ewsconsulting/ubuntu_python
docker image rm ewsconsulting/nb_py2
docker image rm ewsconsulting/nb_py3
docker image rm mongo:4.0.1
docker image rm mongo-express:0.49.0
docker image rm crunchydata/crunchy-pgadmin4:centos7-10.5-2.1.0 docker image rm docker image rm timescale/timescaledb-postgis:0.11.0-pg10
docker image rm debian:jessie-slim
docker image rm ubuntu
```
