from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/toba.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Catalog(db.Model):
   __tablename__ = 'catalog'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nama = db.Column(db.String(200))
   deskripsi = db.Column(db.String(200))
   harga = db.Column(db.Float)

   def __init__(self, nama, deskripsi, harga):
       self.nama = nama
       self.deskripsi = deskripsi
       self.harga = harga

class History(db.Model):
   __tablename__ = 'history'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   id_catalog = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable = False)
   jumlah = db.Column(db.Integer)

   def __init__(self, id_catalog, jumlah):
       self.id_catalog =  id_catalog
       self.jumlah = jumlah

class CatalogSchema(ma.Schema):
    class Meta:
            fields = ('id', 'nama', 'deskripsi', 'harga')

    # init schema
catalog_schema = CatalogSchema(strict=True)
catalogs_schema = CatalogSchema(many=True, strict=True)

class HistorySchema(ma.Schema):
    class Meta:
            fields = ('id', 'id_catalog', 'jumlah')


class Recomendation(db.Model):
   __tablename__ = 'recomendation'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   id_history = db.Column(db.Integer, db.ForeignKey('history.id'), nullable = False)


   def __init__(self, id_history):
       self.id_history = id_history

class RecomendationSchema(ma.Schema):
    class Meta:
            fields = ('id', 'id_history')

reco_schema = RecomendationSchema(strict=True)
recos_schema = RecomendationSchema(many=True, strict=True)

@app.route('/favorit')
def favorit():
    con = sqlite3.connect("data/toba.sqlite")
    cur = con.cursor()
    cur.execute("SELECT catalog.nama FROM catalog inner join history on catalog.id = history.id_catalog GROUP BY nama ORDER BY id_catalog")
    data = cur.fetchall()

    return render_template('testFavorit.html', value=data)

if __name__ == '__main__':
    app.run(debug=True)
