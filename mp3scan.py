# -*- encoding: utf-8 -*-
import io
import os
import wmi
import datetime
import fnmatch
import yandexwebdav
import socket, uuid
import codecs, json

def generate_settings():
	patterns = list()
	patterns.append({'path':'c:/','names':'*.mp3'})
	patterns.append({'path':'c:/','names':'*.avi'})
	settings = {'about': True, 'applications': False, 'disk': {'user': 'username','password':'password'},'files': patterns}

	settings_file = open('settings.json','tw')
	settings_file.write(json.dumps(settings))
	settings_file.close()


def load_settings():
	setting_file = open('settings.json','tr')
	settings = json.loads(setting_file.read())
	setting_file.close()
	return settings


# если нет настроек, то генерим файл и открываем
if not os.path.exists('settings.json'):
	generate_settings()

settings = load_settings()


# делаем словарь для собираемых данных
report = {'hostname': None, 'ip4': None, 'mac_int': None, 'applications': None,'files':list()}

report['hostname'] = socket.gethostname()
#берем ip адрес
report['ip4'] = socket.gethostbyname(socket.gethostname())
report['mac_int'] = uuid.getnode()

# собираем список установленного софта
if settings['applications'] == True:
	apps = list()
	w = wmi.WMI()

	for app in w.Win32_Product():
		apps.append({'Caption':app.Caption,'Version':app.Version,'Vendor':app.Vendor})

	report['applications'] = apps
	# print(report['applications'])


# ищем все файлы в нужных местах с заданной маской
for pattern in settings['files']:
	for root, subdirs, files in os.walk(pattern['path']):
		for file_name in fnmatch.filter(files,pattern['names']):
			report['files'].append(file_name)

# print(report['files'])

# делаем отчет и вылаживаем его на яндекс диск в нужную директорию
if not os.path.exists('./report'):
	os.mkdir('./report')

now = str(datetime.datetime.now())
now = now.replace(':','-')
now = now.replace('.', '-')
now = now.replace(' ', '-')

report_file_name = str(report['mac_int'])+' '+now+'.txt'
report_file_path = './report/'+report_file_name	
report_file = open(report_file_path,'w')
report_file.write(json.dumps(report))
report_file.close()

conf = yandexwebdav.Config({'user':settings['disk']['user'],'password':settings['disk']['password']})
conf.upload(report_file_path,'/reports/'+report_file_name)

# если произошла ошибка делаем лог с описанием