from cx_Freeze import setup, Executable

setup (
	name = 'mp3scan',
	version = '0.1',
	description = 'mp3scan',
	executables = [Executable("mp3scan.py")]
	)