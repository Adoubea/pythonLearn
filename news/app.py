#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,abort
import json,os

class Jsonfile:
    def __init__(self):
        self._titles = []
        self._filedir = '/home/shiyanlou/files/'
        for root,dirs,self._files in os.walk(self._filedir):
            pass

    def parserfile(self, file_name):
        file_path = self._filedir+file_name
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return json.loads(file.read())
        else:
            return 0

    def gettitles(self):
        for file in self._files:
            jsondict = self.parserfile(file)
            self._titles.append(jsondict['title'])
        return self._titles





app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    jfile = Jsonfile()
    return render_template('index.html',filelist=jfile.gettitles())

@app.route('/files/<filename>')
def file(filename):
    filename += '.json'
    jfile = Jsonfile()
    result = jfile.parserfile(filename)
    if result == 0:
        abort(404)
    else:
        return render_template('file.html',filedict=result)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


if __name__ == '__main__':
    app.run()
