FROM python:3.6.2
ENV PYTHONBUFFERED 1
RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN mkdir /scraptt
ADD . /scraptt
RUN pip install -r /scraptt/requirements.txt
RUN pip install -r /scraptt/scraptt-pipeline/requirements.txt
WORKDIR /scraptt
