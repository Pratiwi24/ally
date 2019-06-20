from my_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Float(asdecimal=True))
    image = db.Column(db.Column(db.LargeBinary))

    def __init__(self, name, description, price, image):
        self.name = name
        self.description = description
        self.price = price
        self.image = image

    def __repr__(self):
        return '<Product %d>' % self.id
