from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    characteristics = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'