import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'we_love_writing_programs_123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance/database.sqlite')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
