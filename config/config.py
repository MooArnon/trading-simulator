##########
# Import #
##############################################################################

import os

##########
# Config #
##############################################################################

config = {}

config['DUCK_DB_BUCKET'] = os.getenv("DUCK_DB_BUCKET", "space-time-lake-house")
config['DUCK_DB_PREFIX'] = os.getenv("DUCK_DB_PREFIX", "duck_db")

config['DISCORD_REPORT_WEBHOOK'] = os.getenv("DISCORD_REPORT_WEBHOOK", "CHANGEME")

##############################################################################
