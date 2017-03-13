import configparser

cfg = configparser.ConfigParser()

section = 'uwsgi'

cfg.add_section(section)
cfg[section]['module'] = 'dumpit:app'
cfg[section]['master'] = 'true'
cfg[section]['socket'] = '/tmp/dumpit.sock'
cfg[section]['chmod-socket'] = '660'
cfg[section]['vacuum'] = 'true'
cfg[section]['die-on-term'] = 'true'

with open('templates/uwsgi2.ini', 'w') as f:
	cfg.write(f)
