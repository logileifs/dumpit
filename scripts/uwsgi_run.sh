#!/usr/bin/env bash
uwsgi --http-socket :9090 -p 4 --import bootstrap.py --module dumpit:app