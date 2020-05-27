FROM alpine:3

RUN apk add --update cairo cairo-gobject pango gdk-pixbuf py3-cffi py3-pillow py3-lxml msttcorefonts-installer fontconfig \
    && update-ms-fonts \
    && fc-cache -f \
    && pip3 --no-cache-dir install weasyprint gunicorn flask

WORKDIR /app
ADD ./server.py /app

CMD gunicorn --bind 0.0.0.0:80 server:app
