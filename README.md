# Smart India Hackathon-2023 Client Dashboard - Centralized Monitoring System for Street Light Fault Detection and Location Tracking (alpha)

A client dashboard built with Flask to manage street lights, linesman and create automations. This project is currently in its alpha build stage.

- **Author:** Sakthi Santhosh
- **Created on:** 26/10/2023

## Pre-requisites

- `nginx`
- `python3` and `pip`
- `virtualenv`

## Getting Started

- Run the following in your shell to set-up a virtual environment in the project directory and install the required packages. Ensure `virtualenv` package is installed with `apt` or `pip` beforehand.

```sh
virtualenv -q ./venv/ && source ./venv/bin/activate
pip3 install -q -r ./requirements.txt
```

- Invoke the Flask shell by running this command.

```sh
flask --app "app:create_app('development')" shell
```

- Execute the following commands in the Flask shell interpreter to create a SQLite3 database file.

```python
>>> from app import db_handle
>>>
>>> db_handle.create_all()
>>> exit()
```

- Create a secrets file named `./.env` with the following command and add your secrets to it.

```sh
cat ./env.example > ./.env
nano ./.env
```

- Run the development server by running either of the following commands. Running the first command additionally exposes the app to the local network.

```sh
python3 ./run.py
```

```sh
flask --app "app:create_app('development')" run
```

## Deployment

- To run the app in a deployment environment, run the Flask app with Gunicorn and proxy it with Nginx with the following commands. If Nginx isn't installed in your system, you can install it with `apt`.

```sh
chmod +x ./shell/nginx_init.sh
sudo ./shell/nginx_init.sh deployment
sudo nginx -t
```

- Alternatively, you can display a website-under-maintenance page by running the same command with different argument. This HTML page is available for modifications at `./nginx/maintenance/index.html`.

```sh
sudo ./shell/nginx_init.sh maintenance
```

- Now that Nginx is ready to proxy the Flask app, start the Flask app with Gunicorn with the following command.

```sh
gunicorn --workers 4 "app:create_app('development')"
```
