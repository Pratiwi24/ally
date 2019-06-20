from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir =os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'toba.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200))
    deskripsi = db.Column(db.String(200))
    harga = db.Column(db.Float)


    def __init__(self, nama, deskripsi, harga):
        self.nama = nama
        self.deskripsi = deskripsi
        self.harga = harga


class CatalogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama', 'deskripsi', 'harga')

#init schema
catalog_schema = CatalogSchema(strict=True)
catalogs_schema = CatalogSchema(many=True, strict=True)

#create catalog
@app.route('/catalog', methods=['POST'])
def add_catalog():
    nama = request.json['nama']
    deskripsi = request.json['deskripsi']
    harga = request.json['harga']


    new_catalog = Catalog(nama, deskripsi,harga)

    db.session.add(new_catalog)
    db.session.commit()

    return catalog_schema.jsonify(new_catalog)

#Get All Product
@app.route('/catalog', methods=['GET'])
def get_catalogs():
    all_catalogs = Catalog.query.all()
    result = catalogs_schema.dump(all_catalogs)
    return jsonify(result.data)

#Get SingleCatalog
@app.route('/catalog/<id>', methods=['GET'])
def get_catalog(id):
    catalog = Catalog.query.get(id)
    return catalog_schema.jsonify(catalog)

# Update a Catalog
@app.route('/catalog/<id>', methods=['PUT'])
def update_catalog(id):
    catalog = Catalog.query.get(id)

    nama = request.json['nama']
    deskripsi = request.json['deskripsi']
    harga = request.json['harga']


    catalog.nama = nama
    catalog.deskripsi = deskripsi
    catalog.harga = harga


    db.session.commit()

    return catalog_schema.jsonify(catalog)

#delete catalog
@app.route('/catalog/<id>', methods=['DELETE'])
def delete_catalog(id):
    catalog = Catalog.query.get(id)
    db.session.delete(catalog)
    db.session.commit()

    return catalog_schema.jsonify(catalog)

if __name__ == '__main__':
    app.run(debug=True)
