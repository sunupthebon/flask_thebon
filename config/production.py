from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'thebon.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'z,y\x12\xc9\xd91\x8f\xfb\xd3c\xf5\x8aQ\xccJ'
