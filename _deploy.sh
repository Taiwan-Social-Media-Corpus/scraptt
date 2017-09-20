#!/usr/bin/env bash

rm db/*
docker rm -f scraptt
docker rm -f scraptt-db
docker build . -t scraptt --no-cache
rm -rf /tmp/pgdata/*
docker run -d --name scraptt-db -p 54321:5432 -e POSTGRES_PASSWORD=1234 -v /usr/local/var/scraptt:/var/lib/postgresql/data postgres:latest
docker run -td -v $(pwd)/db/:/usr/local/var --name scraptt --link scraptt-db:scraptt-link scraptt
sleep 15
docker exec -it scraptt /bin/sh -c 'python -c "from scraptt.postgres.db import init_db; init_db()"'
