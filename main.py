# main.py

from flask import Flask
from app.routes.routes import routes_bp
from app.models.models import Base
from app.db.db_config import connect_with_connector

app = Flask(__name__)

app.register_blueprint(routes_bp)

# Initialize the database
db = connect_with_connector()
Base.metadata.create_all(db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)