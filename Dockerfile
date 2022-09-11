FROM hwan001/pluto:latest
MAINTAINER hwan001 "woghks7209@gmail.com"

RUN apt-get update
RUN apt-get install -y vim net-tools
RUN apt-get install -y python3-dev build-essential python3 python3-pip python3-venv

RUN rm -rf /Pluto
COPY . /Pluto
WORKDIR /Pluto

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["run.py"]
