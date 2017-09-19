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

Create container and mount docker volume

    docker run -td -v $(pwd)/db/:/usr/local/var --name scraptt scraptt

Create PostgresSQL container

docker run -p 54321:5432 -e POSTGRES_PASSWORD=1234 -v $(pwd)/db:/var/lib/postgresql/data postgres:latest -d postgres


Crawl

    docker exec -it scraptt /bin/sh -c 'scrapy crawl ptt -a boards=movie'
