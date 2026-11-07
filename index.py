from controller.app_controller import AppController
from model.database_model import DatabaseModel

database = DatabaseModel()
app_controller = AppController(database)
app_controller.run()