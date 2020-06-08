#!/bin/bash

python gen_secret_key.py
python init_torch.py

python manage.py mkaemigrations
until python manage.py migrate; do
  sleep 2
  echo "Retry migrate";
done

python manage.py makegmirations
python manage.py migrate
echo "Migration success";
python manage.py runserver 0:7777