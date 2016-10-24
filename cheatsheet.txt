source env/bin/activate -> activar el entorno. Se hace solo con el .env
deactivate -> salir del entorno

git push origin <branch_name> -> pushear en github
git push stage master -> pushear en heroku staging
git push prod master -> pushear en heroku production

python manage.py db migrate -> generar migrations
python manage.py db upgrade -> run migrations

heroku run python manage.py db upgrade --app <heroku_app_name> -> run migrations on heroku

psql -> base de datos
pip freeze > requirements.txt -> despues de un pip install, para guardar los paquetes requeridos

python manage.py runserver
python app.py