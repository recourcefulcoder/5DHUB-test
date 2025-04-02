import logging
import sys

from database.engine import url_object

import src.settings as settings

if not settings.TESTING:
    logging.error("Application is not in testing mode! Aborting...")
    sys.exit(1)

if settings.POSTGRES_DB == url_object.database:
    logging.error("Tests run against production database! Aborting...")
    sys.exit(1)
