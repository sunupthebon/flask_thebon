from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy import MetaData


#import config

db = SQLAlchemy()
migrate = Migrate()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
#    app.config.from_object(config)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from . import models

    # 블루프린트
    from .views import main_views, crawling_views, auth_views
        # , myfunction, google_search, sunup_function2
    app.register_blueprint(main_views.bp)
    app.register_blueprint(crawling_views.bp)
    app.register_blueprint(auth_views.bp)
    # app.register_blueprint(myfunction.bp)
    # app.register_blueprint(google_search.bp)
    # app.register_blueprint(sunup_function2.bp)

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app