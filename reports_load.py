import sqlite3
import io, os, json
import yandexwebdav

def generate_settings():
	settings = {'disk': {'user': 'username','password':'password'}}

	settings_file = open('load_settings.json','tw')
	settings_file.write(json.dumps(settings))
	settings_file.close()


def load_settings():
	setting_file = open('load_settings.json','tr')
	settings = json.loads(setting_file.read())
	setting_file.close()
	return settings


# если нет настроек, то генерим файл и открываем
if not os.path.exists('load_settings.json'):
	generate_settings()

settings = load_settings()

# проверяем нашу базу данных
db = sqlite3.connect('reports.db')

c = db.cursor()

#проверяем наши таблицы
c.execute('SHOW DATABASES;')
print(c.fetchone())

db.commit()
db.close()