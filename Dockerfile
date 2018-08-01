FROM amigcamel/alpine-scrapy-psycopg2 
ENV PYTHONBUFFERED 1
RUN apk add --update tzdata git  # git is not needed when scraptt-pipeline is published on PyPI
ENV TZ=Asia/Taipei
ENV COCKROACHDB_HOST=scraptt-db
ENV COCKROACHDB_PORT=26257
ENV COCKROACHDB_USER=root
ENV ELASTICSEARCH_HOST=ptt-engine
ENV ELASTICSEARCH_PORT=19200
RUN mkdir /scraptt
ADD . /scraptt
RUN pip install -r /scraptt/requirements.txt
WORKDIR /scraptt
