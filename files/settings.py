from os import environ

SESSION_CONFIGS = [
    dict(
        name='study_en',
        display_name="FTR Study — English (reference)",
        app_sequence=['experiment'],
        num_demo_participants=3,
        language='en',
    ),
    dict(
        name='study_fr',
        display_name="FTR Study — French",
        app_sequence=['experiment'],
        num_demo_participants=3,
        language='fr',
    ),
    dict(
        name='study_de',
        display_name="FTR Study — German",
        app_sequence=['experiment'],
        num_demo_participants=3,
        language='de',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

PARTICIPANT_FIELDS = ['language']
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')
DEMO_PAGE_INTRO_HTML = ""
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'change-me-in-production')
DEBUG = environ.get('OTREE_DEBUG', 'True') == 'True'
