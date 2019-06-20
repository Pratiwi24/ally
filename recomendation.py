from flask import Flask, request, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir =os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'ally.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    # init schema
history_schema = HistorySchema(strict=True)
historis_schema = HistorySchema(many=True, strict=True)

class Toko(db.Model):
   __tablename__ = 'toko'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   namaToko =db.Column(db.String(200))
   lokasi = db.Column(db.Float)

   def __init__(self, namaToko, lokasi):
       self.namaToko = namaToko
       self.lokasi = lokasi

class TokoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'namaToko', 'lokasi')

toko_schema = TokoSchema(strict=True)
tokos_schema = TokoSchema(many=True, strict=True)

class Recomendation(db.Model):
    __tablename__ = 'recomendation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idHistory = db.Column(db.Integer, db.ForeignKey('history.id', nullable=False))

    def __init__(self, idHistory):
        self.idHistory = idHistory

class RecomendationSchema(ma.Schema):
            class Meta:
                fields = ('id', 'idHistory')

recomendation_schema = RecomendationSchema(strict = True)
recomendations_schema = RecomendationSchema(many=True, strict=True)

if __name__ == '__main__':
    app.run(debug=True)
