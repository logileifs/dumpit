.PHONY: clean

productname="dumpit"
host="dumpit.pw"
user="dumpitadmin"

add-public-key:
	@ cat ~/.ssh/id_rsa.pub | ssh root@dumpit.pw "mkdir -p /home/dumpitadmin/.ssh && cat >> /home/dumpitadmin/.ssh/authorized_keys"

setup:
	@ fab setup:$(host),$(user),$(productname)

unit-tests:
	@ ~/.virtualenvs/dumpit/bin/nosetests tests/unit.py

clean:
	@ rm -rf dist/

build:
	@ rm -rf dist/
	@ mkdir dist/
	@ pip freeze > requirements.txt
	@ ( cd src/ && zip -r ../dist/$(productname).zip * )
	@ chmod +x dist/$(productname).zip
	@ echo '#!/usr/bin/env python' | cat - dist/dumpit.zip &> /dev/null
	@ cp requirements.txt dist/

deploy:
	@ fab deploy:$(host),$(user),$(productname)

restart:
	@ fab restart:$(host),$(user)
