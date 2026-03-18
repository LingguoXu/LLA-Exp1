from os import environ

SESSION_CONFIGS = [
    dict(
        name='study_ja',
        display_name="FTR Study — Japanese",
        app_sequence=['Task1','Task2','Task3'],
        # app_sequence=['Task3'],
        num_demo_participants=3,
        language='ja',
    ),
    dict(
        name='study_en',
        display_name="FTR Study — English (reference)",
        app_sequence=['Task1','Task2','Task3'],
        # app_sequence=['Task1'],
        num_demo_participants=3,
        language='en',
        completion_code='CFZCG8H4',
    ),
    dict(
        name='study_fr',
        display_name="FTR Study — French",
        app_sequence=['Task1','Task2','Task3'],
        num_demo_participants=3,
        language='fr',
    ),
    dict(
        name='study_de',
        display_name="FTR Study — German",
        app_sequence=['Task1','Task2','Task3'],
        num_demo_participants=3,
        language='de',
    ),
    dict(
        name='study_zh',
        display_name="FTR Study — Chinese",
        app_sequence=['Task1','Task2','Task3'],
        num_demo_participants=3,
        language='zh',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

PARTICIPANT_FIELDS = ['language', 'prolific_id']
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='en',
        display_name='English Session',
    ),
    dict(
        name='fr',
        display_name='French Session',
    ),
    dict(
        name='de',
        display_name='German Session',
    ),
    dict(
        name='ja',
        display_name='Japanese Session',
    ),
    dict(
        name='zh',
        display_name='Chinese Session',
    ),
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')
DEMO_PAGE_INTRO_HTML = ""
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'change-me-in-production')
DEBUG = environ.get('OTREE_DEBUG', 'True') == 'True'

# ============================================================
# PUSHING TO GITHUB AND HEROKU SERVER
# ============================================================
# Run these commands from the ROOT folder (LLA-Exp1/), NOT the subfolder.
#
# 1. Stage and commit all changes:
#       git add .
#       git commit -m "your message here"
#
# 2. Push to GitHub:
#       git push origin main
#
# 3. Push to Heroku (app lives in subfolder LLA-Exp1-260214/):
#       git subtree push --prefix LLA-Exp1-260214 heroku main
#
#    If rejected due to non-fast-forward error, force push with:
#       git push heroku `git subtree split --prefix LLA-Exp1-260214 main`:main --force
#
# 4. Reset the Heroku database (clears all participant data):
#       heroku run otree resetdb --app lla-exp1
#
#    Or if you are inside the subfolder (LLA-Exp1-260214/):
#       otree resetdb
#
# WARNING: resetdb permanently deletes all collected data.
#          Always export your data before resetting.
#
# NOTE: Always commit before pushing to Heroku. Heroku deploys
#       from Git, so uncommitted changes will NOT be reflected.
# ============================================================
