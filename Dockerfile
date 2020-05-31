FROM alpine:latest
RUN apk update
RUN apk add \
git \
python3 \
py3-pip \
python3-dev
RUN rm -rf /var/cache/apk/*
WORKDIR /root
RUN git clone https://github.com/thewhiteh4t/pwnedOrNot.git
WORKDIR /root/pwnedOrNot/
RUN pip3 install --upgrade pip
RUN pip3 install requests
ENTRYPOINT ["python3", "pwnedornot.py"]