from otree.api import *
import random
import json

doc = """
Task 2: Modality Elicitation (Cloze Test) - High/Low Certainty.
Task 3: Subjective Probability (Sliders) - 13 English Sentences.
"""


class Constants(BaseConstants):
    name_in_url = 'modality_task'
    players_per_group = None
    num_rounds = 1

    # --- TASK 2 DATA ---
    QUESTIONS_POOL = [
        {'id': 2, 'high': "[Q: Should I bring my sun hat? A: Yes...] ...it {BE} very hot.",
         'low': "[Q: Should I bring a jacket? A: Maybe...] ...it {SNOW} this afternoon."},
        {'id': 3, 'high': "[Friend to Friend: You should come tonight...] ...Annie {BE} there.",
         'low': "[Friend to Friend: You should come tonight...] ...John {BE} there."},
        {'id': 7, 'high': "[Q: Is the exam hard? A: Prof Green is easy...] ...we {PASS}.",
         'low': "[Q: Is the exam hard? A: Prof Johnson is random...] ...we {PASS}."},
        {'id': 10, 'high': "[Bring an umbrella...] ...it {RAIN} in Berlin.",
         'low': "[Bring a swimsuit...] ...the temperature {HIT} 45 degrees."},
        {'id': 14, 'high': "[Mother: Put allowance in savings. Next month...] ...it {BE} worth more.",
         'low': "[Father: Keep that toy. Next month...] ...it {BE} worth something."},
        {'id': 17, 'high': "[Doctor: Sleep well. In a few months...] ...you {FEEL} better.",
         'low': "[Doctor: Tests are concerning. In a few months...] ...you {FEEL} better."},
        {'id': 1, 'high': "[Q: Want to see a film? A: Can't...] ...I {DINE OUT} with Ellie.",
         'low': "[Q: What you doing? A: Hmm...] ...I {DINE OUT} with Christine."},
        {'id': 13, 'high': "[Uncle sends money...] ...she {BUY} new skis.",
         'low': "[Brother sends money...] ...he {SPEND} it at the bar."},
        {'id': 16, 'high': "[Girl: Party in 3 months?] Boy: I {BE} there.",
         'low': "[Boy: Party in 3 months?] Girl: ...I {COME}."},
        {'id': 4, 'high': "[Q: When is the exam?] ...it {BE} at 7pm.",
         'low': "[Q: When is the exam? I have to check...] ...it {BE} at 7pm."},
        {'id': 8, 'high': "[Q: Sun rise tomorrow?] ...It {RISE} at 6:17.",
         'low': "[Q: Moon rise tomorrow?] ...It {RISE} at 17:00."},
        {'id': 12, 'high': "[Brother leaves tomorrow...] ...flight {LEAVE} next week.",
         'low': "[Mary leaves in two weeks...] ...flight {LEAVE} next week."},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # --- TASK 2 FIELDS ---
    task_data_dump = models.LongStringField()
    q1_response = models.StringField(label="")
    q2_response = models.StringField(label="")
    q3_response = models.StringField(label="")
    q4_response = models.StringField(label="")
    q5_response = models.StringField(label="")
    q6_response = models.StringField(label="")
    q7_response = models.StringField(label="")
    q8_response = models.StringField(label="")
    q9_response = models.StringField(label="")
    q10_response = models.StringField(label="")
    q11_response = models.StringField(label="")
    q12_response = models.StringField(label="")

    # --- TASK 3 FIELDS (Sliders) ---
    # We name them specifically so data analysis is easy later
    cert_will = models.IntegerField(min=0, max=100, label="It will rain next week.")
    cert_going_to = models.IntegerField(min=0, max=100, label="It is going to rain next week.")
    cert_present = models.IntegerField(min=0, max=100, label="It is raining next week.")
    cert_definitely = models.IntegerField(min=0, max=100, label="It will definitely rain next week.")
    cert_certainly = models.IntegerField(min=0, max=100, label="It will certainly rain next week.")
    cert_probably = models.IntegerField(min=0, max=100, label="It probably will rain next week.")
    cert_possibly = models.IntegerField(min=0, max=100, label="It possibly will rain next week.")
    cert_could = models.IntegerField(min=0, max=100, label="It could rain next week.")
    cert_might = models.IntegerField(min=0, max=100, label="It might rain next week.")
    cert_may = models.IntegerField(min=0, max=100, label="It may rain next week.")
    cert_should = models.IntegerField(min=0, max=100, label="It should rain next week.")
    cert_think_will = models.IntegerField(min=0, max=100, label="I think it will rain next week.")
    cert_think_going_to = models.IntegerField(min=0, max=100, label="I think it is going to rain next week.")

    # To store the randomized order for Task 3
    task3_order_dump = models.LongStringField()


# FUNCTIONS
def creating_session(subsession):
    pass


# --- PAGES ---

class Introduction(Page):
    def before_next_page(player, timeout_happened):
        # -- TASK 2 SETUP --
        items = Constants.QUESTIONS_POOL.copy()
        random.shuffle(items)
        assigned_data = []
        for i, item in enumerate(items):
            is_high = random.choice([True, False])
            text_to_show = item['high'] if is_high else item['low']
            data_point = {
                'field_name': f'q{i + 1}_response',
                'q_id': item['id'],
                'condition': 'High' if is_high else 'Low',
                'display_text': text_to_show
            }
            assigned_data.append(data_point)
        player.task_data_dump = json.dumps(assigned_data)

        # -- TASK 3 SETUP (Randomize Order) --
        # We create a list of the field names
        slider_fields = [
            'cert_will', 'cert_going_to', 'cert_present', 'cert_definitely',
            'cert_certainly', 'cert_probably', 'cert_possibly', 'cert_could',
            'cert_might', 'cert_may', 'cert_should', 'cert_think_will',
            'cert_think_going_to'
        ]
        random.shuffle(slider_fields)
        # We save this list to the database so the Page knows which order to display
        player.task3_order_dump = json.dumps(slider_fields)


class Page1(Page):
    form_model = 'player'
    form_fields = ['q1_response', 'q2_response', 'q3_response', 'q4_response', 'q5_response', 'q6_response']

    def vars_for_template(player):
        if not player.task_data_dump: return {'questions': []}
        all_data = json.loads(player.task_data_dump)
        page_items = all_data[0:6]
        display_list = []
        for item in page_items:
            raw = item['display_text']
            if ']' in raw:
                parts = raw.split(']', 1)
                context = parts[0].replace('[', '').strip()
                target = parts[1].strip()
            else:
                context = "",
                target = raw
            display_list.append({'field_name': item['field_name'], 'context': context, 'target': target})
        return {'questions': display_list}


class Page2(Page):
    form_model = 'player'
    form_fields = ['q7_response', 'q8_response', 'q9_response', 'q10_response', 'q11_response', 'q12_response']

    def vars_for_template(player):
        if not player.task_data_dump: return {'questions': []}
        all_data = json.loads(player.task_data_dump)
        page_items = all_data[6:12]
        display_list = []
        for item in page_items:
            raw = item['display_text']
            if ']' in raw:
                parts = raw.split(']', 1)
                context = parts[0].replace('[', '').strip()
                target = parts[1].strip()
            else:
                context = "",
                target = raw
            display_list.append({'field_name': item['field_name'], 'context': context, 'target': target})
        return {'questions': display_list}


class Task3Intro(Page):
    pass


class Task3(Page):
    form_model = 'player'
    # We must list all fields here so oTree saves the data
    form_fields = [
        'cert_will', 'cert_going_to', 'cert_present', 'cert_definitely',
        'cert_certainly', 'cert_probably', 'cert_possibly', 'cert_could',
        'cert_might', 'cert_may', 'cert_should', 'cert_think_will',
        'cert_think_going_to'
    ]

    def vars_for_template(player):
        # 1. Define the labels manually to avoid _meta errors
        labels = {
            'cert_will': "It will rain next week.",
            'cert_going_to': "It is going to rain next week.",
            'cert_present': "It is raining next week.",
            'cert_definitely': "It will definitely rain next week.",
            'cert_certainly': "It will certainly rain next week.",
            'cert_probably': "It probably will rain next week.",
            'cert_possibly': "It possibly will rain next week.",
            'cert_could': "It could rain next week.",
            'cert_might': "It might rain next week.",
            'cert_may': "It may rain next week.",
            'cert_should': "It should rain next week.",
            'cert_think_will': "I think it will rain next week.",
            'cert_think_going_to': "I think it is going to rain next week."
        }

        # 2. Determine the order (randomized or default)
        if player.task3_order_dump:
            field_names = json.loads(player.task3_order_dump)
        else:
            # Fallback if something went wrong with shuffle
            field_names = list(labels.keys())

        # 3. Build the list for the template
        slider_items = []
        for name in field_names:
            slider_items.append({
                'name': name,
                'label': labels[name]  # Look up the label from our simple dict
            })

        return {'slider_items': slider_items}

# Update the sequence
page_sequence = [Introduction, Page1, Page2, Task3Intro, Task3]
# page_sequence = [Task3]