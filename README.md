# Scraptt
Distributed PTT (踢踢踢) Crawler

---

## Requirements

+ python > 3.6.0

## Installation

    pip install -r requirements.txt
    pip install -r scraptt-pipeline/requirements.txt

## Usage

Retrieve all board names (obligatory)
    scrapy crawl meta

Retrieve data from certain boards:
    scrapy crawl ptt -a boards=movie
    scrapy crawl ptt -a boards=movie,Gossiping

---

# Docker

Create docker image

    docker build . -t scraptt

Create a stack

    docker stack deploy -c docker-stack.yml scraptt

CockroachDB monitor page:

http://localhost:18080

Scrapyd monitor page:

http://localhost:16800

Remove stack:

    docker stack rm scraptt
    docker network rm scraptt-network
    docker volume rm scraptt-db
    docker volume rm scraptt
