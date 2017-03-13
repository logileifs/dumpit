from fabric.api import *
from fabric.contrib.project import rsync_project


def setup(host, user, prod_name):
	env.host_string = host
	env.user = user
	sudo('apt-get update')
	sudo('apt-get install -y uwsgi nginx python-pip build-essential libssl-dev libffi-dev python-dev')
	sudo('pip install virtualenvwrapper')
	sudo("if [ -z ${WORKON_HOME+x} ]; then echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.profile; fi")
	sudo("if [ -z ${WORKON_HOME+x} ]; then echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.profile; fi")
	run('source .profile')
	run('mkvirtualenv ' + prod_name)
	put('templates/dumpit.conf', '/etc/init/', use_sudo=True)
	put('templates/uwsgi.ini', '/home/' + user + '/', use_sudo=False)
	sudo('chown root:root /etc/init/dumpit.conf')
	sudo('chmod 644 /etc/init/dumpit.conf')
	put('templates/dumpit', '/etc/nginx/sites-available/', use_sudo=True)
	sudo('chown root:root /etc/nginx/sites-available/dumpit')
	sudo('chmod 644 /etc/nginx/sites-available/dumpit')
	with settings(warn_only=True):
		sudo('ln -s /etc/nginx/sites-available/dumpit /etc/nginx/sites-enabled')
	put('templates/bootstrap.py', '/home/' + user + '/', use_sudo=False)


def deploy(host, user, prod_name):
	env.host_string = host
	env.user = user
	rsync_project(remote_dir='/home/' + user + '/', local_dir='dist/')
	run('workon ' + prod_name)
	sudo('/home/' + user + '/.virtualenvs/' + prod_name + '/bin/pip install -r requirements.txt')
	sudo('restart ' + prod_name)
	#sudo('unzip -j dumpit.zip start.py -d .')


def restart(host, user):
	env.host_string = host
	env.user = user
	sudo('shutdown -r now')


def clean():
	local('rm -rf dist/')


def build(prod_name):
	art_path = 'dist/' + prod_name
	zip_path = art_path + '.zip'
	clean()
	local('mkdir dist/')
	local('pip freeze > requirements.txt')
	local('( cd src/ && zip -r ../' + zip_path + ' * )')
	local("echo '#!/usr/bin/env python' | cat - " + zip_path + " > dist/dumpit")
	local('chmod +x ' + art_path)
	local('rm -f ' + zip_path)
	local('cp requirements.txt dist/')
