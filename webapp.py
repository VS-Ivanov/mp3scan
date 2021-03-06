from flask import Flask
import yandexwebdav
import os, io
import json
import sync

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

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return 'WebApp is running...'

# синхронизация с яндекс диском
sync.sync_disk(settings)

app.run()
