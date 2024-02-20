import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from routes.authentication import blp as AuthBlueprint
from routes.user import blp as UserBlueprint
from utils.jwt_config import initialise_jwt_config
from routes.event import blp as EventBlueprint
from routes.booked_events import blp as BookedEventsBlueprint

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

def create_app():
    app = Flask(__name__)
    
    app.config["API_TITLE"] = "BOOK MY EVENT API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['DEBUG'] = True
    
    api = Api(app)
    
    
    app.config["JWT_SECRET_KEY"] = "82149326908263419269080266928341264331"
    jwt = JWTManager(app)
    
    
        
    initialise_jwt_config(app)
    
    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(EventBlueprint)
    api.register_blueprint(BookedEventsBlueprint)
    
    
    return app

app = create_app()

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
    
    
    

# from views.menu import Menu
# from utils import logs

# def main():
#     instance = Menu()
#     logs.start_app()
#     instance.start_view()

# if __name__ == '__main__':
#     main()
