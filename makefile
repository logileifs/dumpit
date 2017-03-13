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
	@ fab clean

build:
	@ fab build:$(productname)

deploy:
	@ fab deploy:$(host),$(user),$(productname)

restart:
	@ fab restart:$(host),$(user)
