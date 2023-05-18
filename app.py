from flask import (
    Flask,
)
from flask_sqlalchemy import (
    SQLAlchemy,
)


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://tg_conext:conext123@54.186.94.225:5432/conext"
db = SQLAlchemy(app)
