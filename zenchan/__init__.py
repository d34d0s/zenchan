import os
from flask import Flask

def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='murasakino02',  # TODO: generate random key here
            DATABASE=os.path.join(app.instance_path, 'zenchan.sqlite'),
    )

    if test_config == None:
        # load instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try: os.makedirs(app.instance_path)
    except (OSError) as err: pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint='index')

    return app

