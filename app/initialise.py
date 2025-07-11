class Initialise():

    def db(self, app):

        app.config.from_object("config.Config")

        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(
            app.config["DB_USERNAME"],
            app.config["DB_PASSWORD"],
            app.config["DB_LOCATION"],
            app.config["DB_DATABASE"]
        )
        app.secret_key = app.config['SECRET_KEY']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app