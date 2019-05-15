FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get upgrade -y

#docker build -t maxime_barnier_1 .
#docker run -it maxime_barnier_1

RUN apt-get install -y python3.pip
RUN apt-get install -y python3.dev
RUN apt-get install -y git

RUN git clone https://github.com/Barnier-Maxime/machine_learning_project.git