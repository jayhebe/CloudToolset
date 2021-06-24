from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.user.models.model_user import User
from apps.azure.models.model_location import Location
from apps.azure.models.model_environment import Environment
from apps.azure.models.model_subscription import Subscription
from apps.azure.models.model_keyvault import Keyvault
from apps.azure.models.model_keyvault_secret import KeyvaultSecret
from apps import create_app
from exts import db

app = create_app()
manager = Manager(app=app)
manager.add_command("db", MigrateCommand)

migrate = Migrate(app=app, db=db)

if __name__ == "__main__":
    manager.run()
