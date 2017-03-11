productname="dumpit"

unit-tests:
	@ ~/.virtualenvs/dumpit/bin/nosetests tests/unit.py

clean:
	@ rm -rf dist/

build:
	@ rm -rf dist/
	@ mkdir dist/
	@ ( cd src/ && zip -r ../dist/$(productname).pyx * )
	@ chmod +x dist/$(productname).pyx
