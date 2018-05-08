# scraptt
The most comprehensive PTT (踢踢踢) Crawler.  

---

## Requirements

+ python > 3.6.0

## Installation

    pip install -r requirements.txt

## Usage

    scrapy crawl ptt -a boards=movie
    scrapy crawl ptt -a boards=movie,Gossiping

---

# Docker

Create docker image

    docker build . -t scraptt

Create PostgresSQL container

    docker run -d --name scraptt-db -p 54321:5432 -e POSTGRES_PASSWORD=1234 -v /usr/local/var/scraptt/data:/var/lib/postgresql/data postgres:latest

Create container and mount docker volume

    docker run -td -v $(pwd)/db/:/usr/local/var --name scraptt --link scraptt-db:scraptt-link scraptt

Create database and tables

    docker exec -it scraptt /bin/sh -c 'python -c "from scraptt.postgres.db import init_db; init_db()"'

Crawl meta

    docker exec -it scraptt /bin/sh -c 'scrapy crawl meta'
    
Crawl

    docker exec -it scraptt /bin/sh -c 'scrapy crawl ptt -a boards=movie'
