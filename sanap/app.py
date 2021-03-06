import flask
import logging
import jinja2

from werkzeug import SharedDataMiddleware

from webassets.filter import get_filter

from flask.ext.assets import Environment, Bundle
from flask.ext.uploads import configure_uploads
from flask_mail import Mail

from raven.contrib.flask import Sentry
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

from sanap.models import db
from sanap.auth import login_manager
from sanap import auth, frameservice, survey, report
from sanap.forms.survey import files
from sanap.context_processor import model_data_context
from sanap.templatetags import pretty, is_not_empty
from sanap.emails import mail

from .assets import *


DEFAULT_CONFIG = {
    'MONGODB_SETTINGS': {
        'DB': 'sanap',
    },
    'ASSETS_DEBUG': False,
    'CSRF_ENABLED': False,
    'LDAP_ENCODING': 'utf-8',
    'LDAP_USER_DN': "uid=%s,ou=Users,o=EIONET,l=Europe",
    'LDAP_USER_SCHEMA': {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
        'phone_number': 'telephoneNumber',
        'organisation': 'o',
        'uid': 'uid',
    },
    'HOSTNAME': 'http://localhost:5000',
}

BLUEPRINTS = (
    auth,
    survey,
    report,
)

CONTEXT_PROCESSORS = (
    model_data_context,
)

sentry = Sentry()


def create_app(instance_path=None, config={}):
    app = flask.Flask(__name__, instance_path=instance_path,
                      instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app)
    configure_assets(app)
    configure_static(app)
    configure_authentication(app)
    configure_templating(app)
    configure_error_pages(app)
    configure_uploads(app, files)
    configure_context_processor(app)
    configure_email(app)
    if app.config.get('SENTRY_DSN'):
        configure_sentry(app)
    db.init_app(app)
    return app


def configure_app(app, config):
    app.config.update(DEFAULT_CONFIG)
    app.config.from_pyfile('settings.py', silent=True)
    app.config.update(config)


def configure_blueprints(app):
    for blueprint in BLUEPRINTS:
        blueprint.initialize_app(app)


def configure_context_processor(app):
    for context in CONTEXT_PROCESSORS:
        app.context_processor(context)


def configure_assets(app):
    assets = Environment(app)
    js = Bundle(*BUNDLE_JS, filters='jsmin', output='output/packed.js')
    css_rewrite = get_filter('cssrewrite', replace={'/static/':'../'})
    css = Bundle(*BUNDLE_CSS, filters=(css_rewrite, 'cssmin'),
                 output='output/packed.css')
    ie7_css = Bundle(*BUNDLE_IE7_CSS, filters='cssmin', output='output/packed_ie7.css')
    ie8_css = Bundle(*BUNDLE_IE8_CSS, filters='cssmin', output='output/packed_ie8.css')
    ie9_css = Bundle(*BUNDLE_IE9_CSS, filters='cssmin', output='output/packed_ie9.css')
    print_css = Bundle(*BUNDLE_PRINT_CSS, filters='cssmin', output='output/packed_print.css')

    assets.register('packed_js', js)
    assets.register('packed_css', css)
    assets.register('packed_ie7_css', ie7_css)
    assets.register('packed_ie8_css', ie8_css)
    assets.register('packed_ie9_css', ie9_css)
    assets.register('packed_print_css', print_css)


def configure_static(app):
    if app.config['DEBUG']:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            "/static/files": app.config['UPLOADED_FILES_DEST'],
        })


def configure_authentication(app):
    login_manager.setup_app(app)


def configure_error_pages(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template('404.html'), 404

    @app.errorhandler(500)
    def page_error(e):
        return flask.render_template('500.html'), 500

    @app.route('/crashme')
    def crashme():
        raise Exception


def configure_templating(app):
    original_loader = app.jinja_env.loader
    func_loader = jinja2.FunctionLoader(frameservice.load_template)
    app.jinja_env.loader = jinja2.ChoiceLoader([func_loader, original_loader])
    app.jinja_env.filters['pretty'] = pretty
    app.jinja_env.filters['is_not_empty'] = is_not_empty


def configure_email(app):
    mail.init_app(app)


def configure_sentry(app):
    sentry.init_app(app)
    sentry_handler = SentryHandler(sentry.client)
    sentry_handler.setLevel(logging.WARN)
    setup_logging(sentry_handler)
