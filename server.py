#!/usr/bin/env python

import json
import logging

from flask import Flask, Response, request, make_response
import weasyprint
from weasyprint import HTML

app = Flask('pdf')

@app.route('/health')
def index():\
    return Response('{"status": "pass"}', mimetype='application/health+json')

@app.route('/version')
def version_index():
    return weasyprint.__version__


@app.before_first_request
def setup_logging():
    logging.addLevelName(logging.DEBUG, "\033[1;36m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>PDF generator service</title>
    <style>
        html {
            background-color: #005367;
            font-family: sans-serif;
            line-height: 1.5;
        }
        body {
            background-color: #fff;
            padding: 0 2rem 2rem;
        }
        h1 { 
            background-color: #5b7883;
            color: #fff;
            margin: 0 -2rem;
            padding: .5rem 2rem;
         }
    </style>
</head>
<body>
    <h1>PDF generator service</h1>
    <p>This is a wrapper service around <a href="https://weasyprint.org/">WeasyPrint</a>.</p>
    <p>Available endpoints:</p>
    <ul>
        <li>
            GET <a href="./version"><code>/version</code></a>; the WeasyPrint version.
        </li>
        <li>
            GET <a href="./health"><code>/health</code></a>; service health status.
        </li>
        <li>
            POST to <code>/pdf?filename=myfile.pdf</code>.<br />
            The body should contain HTML.<br />
            <code>filename</code> is the suggested filename for the file being returned.
        </li>
        <li>
            POST to <code>/multiple?filename=myfile.pdf</code>.<br />
            The body should contain a JSON array of HTML strings. They will each be
            rendered and combined into a single PDF.<br />
            <code>filename</code> is the suggested filename for the file being returned.
        </li>
    </ul>
'''


@app.route('/pdf', methods=['POST'])
def generate():
    name = request.args.get('filename', 'unnamed.pdf')
    app.logger.info('POST  /pdf?filename=%s' % name)
    html = HTML(string=request.data)
    pdf = html.write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=%s' % name
    app.logger.info(' ==> POST  /pdf?filename=%s  ok' % name)
    return response


@app.route('/multiple', methods=['POST'])
def multiple():
    name = request.args.get('filename', 'unnamed.pdf')
    app.logger.info('POST  /multiple?filename=%s' % name)
    htmls = json.loads(request.data.decode('utf-8'))
    documents = [HTML(string=html).render() for html in htmls]
    pdf = documents[0].copy([page for doc in documents for page in doc.pages]).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=%s' % name
    app.logger.info(' ==> POST  /multiple?filename=%s  ok' % name)
    return response


if __name__ == '__main__':
    app.run()
