FROM ubuntu:focal

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git python3-pip 

RUN mkdir /setup
COPY requirements.txt /setup/
RUN pip install -r /setup/requirements.txt

# COPY safe_preprocessing.py /code/
# COPY test_safe_preprocessing.py /code/
