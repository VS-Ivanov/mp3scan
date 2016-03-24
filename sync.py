import yandexwebdav
import os, io


def sync_disk(settings):
	# проводим синхронизацию с яндекс диском
	if not os.path.exists('./disk'):
		os.mkdir('./disk')

	ydisk = yandexwebdav.Config({'user':settings['disk']['user'],'password':settings['disk']['password']})
	for file_name in ydisk.list('/reports')[1]:
		print("Downloading file - "+file_name)
		ydisk.downloadTo(file_name, './disk/'+str(file_name).split('/')[2])
