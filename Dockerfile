FROM amigcamel/alpine-scrapy-psycopg2 
ENV PYTHONBUFFERED 1
RUN apk add --update tzdata git  # git is not needed when scraptt-pipeline is published on PyPI
ENV TZ=Asia/Taipei
ENV COCKROACHDB_HOST=scraptt-db
ENV COCKROACHDB_PORT=54321
ENV COCKROACHDB_USER=root
RUN mkdir /scraptt
ADD . /scraptt
RUN pip install -r /scraptt/requirements.txt
WORKDIR /scraptt
