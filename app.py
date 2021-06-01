from flask_migrate import Migrate
from flask_script import Manager

from apps import create_app
from exts import db

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)

if __name__ == "__main__":
    manager.run()
