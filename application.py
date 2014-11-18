#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from lib import gaso
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('form.html')


@app.route('/traducir', methods=['POST'])
def traducir():
    return render_template(
        'result.html',
        texto_traducido=gaso.traducir_texto(request.form['texto']),
        texto_original=request.form['texto'],
    )


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000,
    )
