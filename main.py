from flask import Flask
from app.routes.routes import routes_bp
from app.models.models import Base
from app.db.db_config import connect_with_connector

app = Flask(__name__)

app.register_blueprint(routes_bp)

# Initialize the database
engine, Session = connect_with_connector()
# Session = connect_with_connector()
# engine = create_engine("mysql+pymysql://", creator=Session.kw['bind'].creator)
Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)