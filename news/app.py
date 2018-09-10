#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,abort
import json,os
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

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
client = MongoClient('127.0.0.1', 27017)
mongodb = client.shiyanlou

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
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

    def add_tag(self,tag_name):
        file_item = mongodb.files.find_one({'file_id':self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongodb.files.update_one({'file_id':self.id},{'$set':{'tags':tags}})
        else:
            tags = [tag_name]
            mongodb.files.insert_one({'file_id':self.id,'tags':tags})
        return tags

    def remove_tag(self,tag_name):
        file_item = mongodb.files.find_one({'file_id':self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:
                return tags
            mongodb.filetags.update_one({'file_id':self.id},{'$set':{'tags':new_tags}})
            return new_tags
        return []

    @property
    def tags(self):
        file_item = mongodb.filetags.find_one({'file_id':self.id})
        if file_item:
            return file_item['tags']
        else:
            return []

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %s>' % self.name
        
    def insert_datas():
        java = Category('Java')
        python = Category('Python')
        file1 = File('Hello Java', datetime.utcnow(),
                 java, 'File Content - Java is cool!')
        file2 = File('Hello Python', datetime.utcnow(),
                 python, 'File Content - Python is cool!')
        db.session.add(java)
        db.session.add(python)
        db.session.add(file1)
        db.session.add(file2)
        db.session.commit()
        file1.add_tag('tech')
        file1.add_tag('java')
        file1.add_tag('linux')
        file2.add_tag('tech')
        file2.add_tag('python')

@app.route('/')
def index():
    #jfile = Jsonfile()
    return render_template('index.html',files=File.query.all())

@app.route('/files/<int:file_id>')
def file(file_id):
     file_item = File.query.get_or_404(file_id)
     return render_template('file.html',file_item=file_item) 

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
