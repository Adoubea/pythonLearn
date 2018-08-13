#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,abort
import json,os
from flask_sqlalchemy import SQLAlchemy

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'

db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category',backref=db.backref('File'))

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %s>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %s>' % self.name

@app.route('/')
def index():
    #jfile = Jsonfile()
    return render_template('index.html',filelist=File.query.all())

@app.route('/files/<file_id>')
def file(file_id):
     files = File.query.filter(File.id==file_id).first()
     if files is None:
         abort(404)
     else:
         for files in File.query.filter(File.id==file_id).all():
             return render_template('file.html',filedict=files) 

'''
@app.route('/files/<filename>')
def file(filename):
    filename += '.json'
    jfile = Jsonfile()
    result = jfile.parserfile(filename)
    if result == 0:
        abort(404)
    else:
        return render_template('file.html',filedict=result)
'''


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


if __name__ == '__main__':
    app.run()
