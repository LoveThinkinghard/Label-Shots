import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='IT_(GRDS*',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'label_shot.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from label_shot import db
    db.init_app(app)

    # apply the blueprints to the app
    from label_shot import auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # in another app, you might define a separate main label here with
    # app.route, while giving the main blueprint a url_prefix, but for
    # the tutorial the main will be the main label
    app.add_url_rule('/', endpoint='label')

    return app

app = create_app()
