FROM debian:latest
LABEL \
      author="thewhiteh4t" \
      maintainer="Vincent Nadal <vincent.nadal@orange.fr>" 
RUN apt-get update && \
    apt-get -y install python3 python3-pip nodejs
RUN pip3 install requests
RUN pip3 install cfscrape
COPY * ./
RUN chmod +x docker-entrypoint.sh ; sync;
ENTRYPOINT ["/docker-entrypoint.sh"]
