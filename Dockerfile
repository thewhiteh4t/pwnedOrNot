FROM ubuntu:18.04
LABEL \
      author="thewhiteh4t" \
      maintainer="Vincent Nadal <vincent.nadal@orange.fr>" 
RUN apt-get update && \
    apt-get -y install python3 python3-pip nodejs locales
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
RUN pip3 install requests
RUN pip3 install cfscrape
COPY * ./
RUN chmod +x docker-entrypoint.sh ; sync;
ENTRYPOINT ["/docker-entrypoint.sh"]
