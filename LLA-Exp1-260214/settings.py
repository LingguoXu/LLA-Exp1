from os import environ

SESSION_CONFIGS = [
    dict(
        name='ait_life_year',
        display_name='AIT Life-Year Mixed Gambles',
        app_sequence=['study'],
        num_demo_participants=4,
        completion_code='AIT2026X',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)


# SESSION_CONFIGS = [
#      dict(
#         name = 'Treatment_1',
#         display_name = "Treatment_1",
#         num_demo_participants = 3,
#         app_sequence = ['Part1'],
#         # app_sequence=['Part2'],
#         # app_sequence=['Part0', 'Part2'],
#         treatment = 1,
#      ),
#     dict(
#         name='Treatment_2',
#         display_name="Treatment_2",
#         num_demo_participants = 3,
#         app_sequence = ['Part1'],
#         treatment = 2,
#     ),
# ]
# ROOMS = [
#     dict(
#         name='Treatment_1',
#         display_name='Treatment_1',
#         participant_label_file='_rooms/participants_labels.txt',
#         use_secure_urls=True
#     ),
#     dict(
#         name='Treatment_2',
#         display_name='Treatment_2',
#         participant_label_file='_rooms/participants_labels.txt',
#         use_secure_urls=True
#     ),
# ]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# Participant fields
PARTICIPANT_FIELDS = [];

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = True

OTREE_AUTH_LEVEL = 'study'
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD') # password is set at your_password_here
# To reset password: heroku config:set OTREE_ADMIN_PASSWORD=my_new_password
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8033565326101'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

"""
========================================================================
HEROKU DEPLOYMENT & PRODUCTION CHEATSHEET
========================================================================

APP NAME: lla-exp1
SUBFOLDER NAME: LLA-Exp1-Test-260124


------------------------------------------------------------------------
ROUTINE 2: PRODUCTION UPGRADE (Run 1-2 days before N=300 session)
------------------------------------------------------------------------
1. Upgrade Server Power (Prevent crashes):
   heroku dyno:resize web=standard-1x

2. Add High-Speed Cache (Crucial for 300 concurrent users):
   heroku addons:create heroku-redis:mini

3. Upgrade Database (Prevent connection limits):
   heroku addons:upgrade heroku-postgresql:standard-0
   heroku addons:wait

4. Add Logs (For debugging if things go wrong):
   heroku addons:create papertrail

5. Set Production Mode:
   heroku config:set OTREE_PRODUCTION=1 OTREE_AUTH_LEVEL=STUDY

------------------------------------------------------------------------
ROUTINE 3: SCALE DOWN (Run after data collection to save money)
------------------------------------------------------------------------
1. Downgrade Server:
   heroku dyno:resize web=eco

2. Remove Cache:
   heroku addons:destroy heroku-redis

3. Downgrade Database (Optional, if allowed):
   heroku addons:upgrade heroku-postgresql:essential-0
   
------------------------------------------------------------------------
ROUTINE 4: open heroku
heroku open

or use direct URL:  https://lla-exp1.herokuapp.com
------------------------------------------------------------------------
"""

