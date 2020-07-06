FROM alpine:3

RUN apk add --update cairo cairo-gobject pango gdk-pixbuf py3-pip py3-cffi py3-pillow py3-lxml msttcorefonts-installer fontconfig
RUN update-ms-fonts
RUN fc-cache -f
RUN pip3 --no-cache-dir install weasyprint gunicorn flask

WORKDIR /app
ADD ./server.py /app

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 server:app
