FROM alpine:latest
RUN apk update
RUN apk add \
python3 \
py3-pip \
python3-dev
RUN rm -rf /var/cache/apk/*
WORKDIR /root
COPY . /root/pwnedornot/
WORKDIR /root/pwnedornot/
RUN chmod +x install.sh
RUN ./install.sh