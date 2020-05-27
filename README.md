# docker-weasyprint-service

This is a very simple Dockerfile based on [Alpine Linux](https://www.alpinelinux.org). It creates a very small (105MB+) [weasyprint](https://github.com/Kozea/WeasyPrint) service.  It uses a wsgi server by [aquavitae](https://github.com/aquavitae/docker-weasyprint) to provide WeasyPrint as a web service.

Building:

    docker build -t weasyprint-service .

Running locally:

    docker run --rm -p 8000:80 --name weasyprint-01 weasyprint-service

To use, `POST` some HTML to `localhost:8000/pdf`.  The response will be a rendered pdf file.

## Endpoints

- GET `/version`; the WeasyPrint version.
- GET `/health`; service health status.
- POST to `/pdf?filename=myfile.pdf`. The body should contain HTML. `filename` is the suggested filename for the file being returned.
- POST to `/multiple?filename=myfile.pdf`. The body should contain a JSON array of HTML strings. They will each be rendered and combined into a single PDF. `filename` is the suggested filename for the file being returned.

## Fonts

In order to make fonts available to WeasyPrint, copy them into `./fonts` and build the image.
