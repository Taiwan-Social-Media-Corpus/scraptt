FROM amigcamel/alpine-scrapy-psycopg2 
ENV PYTHONBUFFERED 1
RUN apk add --update tzdata
ENV TZ=Asia/Taipei
RUN mkdir /scraptt
ADD . /scraptt
RUN pip install -r /scraptt/requirements.txt
RUN pip install -r /scraptt/scraptt-pipeline/requirements.txt
WORKDIR /scraptt
