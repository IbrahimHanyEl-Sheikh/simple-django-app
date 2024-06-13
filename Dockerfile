# Copyright © 2021-2024 Dell Inc. or its subsidiaries. All Rights Reserved.
FROM phm.artifactory.cec.lab.emc.com/mobile-phoenix-platform-docker/ubuntu:22.04 as framework_base

#Build docker container with docker build -t testrunner -f Dockerfile.Run .
#Run tests with docker run -v ${pwd}:/src testrunner (from product_test_5g directory)
WORKDIR /app
# Install Tshark and Pip
RUN apt-get update && apt-get install -f && apt-get install -y software-properties-common
RUN	add-apt-repository universe
RUN apt install -y tshark=3.6.2-2
RUN apt install -y python3-pip

COPY . .

# Install Python Packages
RUN python3 -m pip install -r requirements.txt

FROM framework_base
WORKDIR /app
ENV PYTHONUNBUFFERED=1
EXPOSE 8090
RUN python3 ./manage.py makemigrations
RUN python3 ./manage.py migrate
CMD python3 ./manage.py runserver 0.0.0.0:8090
