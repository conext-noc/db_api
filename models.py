from app import (
    db,
)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    email = db.Column(db.String)
    password = db.Column(db.String)
