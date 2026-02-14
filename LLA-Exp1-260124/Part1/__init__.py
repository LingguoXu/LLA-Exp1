from otree.api import *
import random
import csv

author = 'Lingguo Xu'
doc = """
Part 1: Attention pledge, PLS, overview, instructions for game and task. Same for all treatments
"""

class Constants(BaseConstants):
    name_in_url = 'Part1'
    players_per_group = None
    num_rounds = 1
    # participation_fee = 250
    # goldvalue_low = 680
    # goldvalue_high = 865
    # Add this line for the instruction text:
    max_bonus = 100  # Replace 100 with your actual max bonus amount

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.IntegerField(label="",
        choices=[[1, 'I agree']],
        widget=widgets.RadioSelect
    )

    # Q1: Gender
    gender = models.StringField(
        label="1. Please select your gender:",
        choices=["Female", "Male", "Prefer not to say"],
        widget=widgets.RadioSelect
    )

    # Q2: Age
    age = models.IntegerField(
        label="2. Please enter your age:",
        min=18, max=100
    )

    # Q3: Education
    education = models.StringField(
        label="3. Please select your highest level of education:",
        choices=[
            "Less than High School",
            "High School / GED",
            "Some College",
            "Bachelor's Degree",
            "Master's Degree",
            "Doctoral Degree"
        ],
        widget=widgets.RadioSelect
    )

    # Q4: Mother Tongue (Screening Question 1)
    is_native_english = models.BooleanField(
        label="4. Is your mother tongue English?",
        choices=[
            [True, "Yes"],
            [False, "No"]
        ],
        widget=widgets.RadioSelectHorizontal
    )

    # Q5: Other Languages (Screening Question 2)
    # 0 = Pass, 1-5 = Fail
    second_language_level = models.IntegerField(
        label="5. Please list any languages other than your mother tongue (English) you have been exposed to, and rate your proficiency:",
        choices=[
            [0,
             "Level 0: I only know a few words. I cannot communicate at the sentence level at all, or I do not understand it at all."],
            [1, "Level 1: I can ask for directions and answer simple questions."],
            [2, "Level 2: I can have basic conversations on familiar topics."],
            [3,
             "Level 3: I can communicate effectively in most situations (e.g. telling a story or filling out forms), but not fluently."],
            [4, "Level 4: Fluent but occasionally make mistakes; clearly sound like a foreigner."],
            [5, "Level 5: Very fluent; I can use the language like a native speaker."],
        ],
        widget=widgets.RadioSelect
    )

    # Internal field to store if they passed (calculated in pages.py)
    screened_out = models.BooleanField()

    # Task 1: FTR elicitation
    task1_answers_eng = models.LongStringField()
    task1_answers_fra = models.LongStringField()
    task1_answers_ger = models.LongStringField()

# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.treatment  = player.session.config['treatment']

# PAGES
class Attention_pledge(Page):
    pass

class PLS_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finalpayoff_ECU = Constants.participation_fee


class ScreeningQuestions(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'education', 'is_native_english', 'second_language_level']

    def before_next_page(player, timeout_happened):
        # LOGIC:
        # Pass if: Mother tongue is English (True) AND Second language level is 0.
        # Fail otherwise.
        if player.is_native_english == True and player.second_language_level == 0:
            player.screened_out = False
        else:
            player.screened_out = True


class ScreeningResult(Page):
    # No form fields here. Just a message.
    def vars_for_template(player):
        return {
            'passed': not player.screened_out
        }


class Task1_FTR_Eng(Page):
    form_model = 'player'
    form_fields = ['task1_answers_eng']

    def vars_for_template(player):
        # Define the options for each of the 10 gaps
        options = [
            ["notices", "believes", "doubts", "ignores"],  # 1
            ["snows", "will snow", "is going to snow", "snowed"],  # 2
            ["is making", "makes", "made", "has made"],  # 3
            ["won't be", "wouldn't be", "aren't", "were't"],  # 4
            ["don't have", "am not having", "didn't have", "haven't had"],  # 5
            ["watches", "checks", "stares", "looks"],  # 6
            ["left", "is leaving", "leaves", "has left"],  # 7
            ["go", "went", "will go", "am going"],  # 8
            ["will buy", "buy", "am buying", "bought"],  # 9
            ["prepare", "am preparing", "prepared", "will prepare"]  # 10
        ]

        # We zip the index (1-10) with the options so the template is easier to write
        return {
            'questions': zip(range(1, 11), options)
        }

class Task1_FTR_Fra(Page):
    form_model = 'player'
    form_fields = ['task1_answers_fra']

    def vars_for_template(player):
        options = [
            ["remarque", "croit", "doute", "ignore"],                   # 1
            ["neige", "va neiger", "neigera", "a neigé"],               # 2
            ["fait", "est en train de faire", "a fait", "faisait"],     # 3
            ["n'es pas", "ne pourras pas", "ne serais pas", "n'étais pas"], # 4
            ["n'ai pas", "n'avais pas", "ne vais pas avoir", "n'aie pas"], # 5
            ["regarde", "vérifie", "fixe", "voit"],                     # 6
            ["part", "est parti", "partait", "serait parti"],           # 7
            ["vais", "vais aller", "irai", "suis allé"],                # 8
            ["achète", "vais acheter", "achèterai", "ai acheté"],       # 9
            ["prépare", "vais préparer", "préparerai", "préparais"]     # 10
        ]
        return {'questions': zip(range(1, 11), options)}

class Task1_FTR_Ger(Page):
    form_model = 'player'
    form_fields = ['task1_answers_ger']

    def vars_for_template(player):
        options = [
            ["bemerkt", "glaubt", "bezweifelt", "ignoriert"],           # 1
            ["schneit", "wird schneien", "würde schneien", "schneite"], # 2
            ["macht", "macht gerade", "machte", "hat gemacht"],         # 3
            ["bist", "wirst sein", "wärst", "warst"],                   # 4
            ["habe keine", "hatte keine", "werde keine haben", "hätte keine"], # 5
            ["schaut", "prüft", "starrt", "sieht"],                     # 6
            ["fährt ab", "fuhr ab", "ist abgefahren", "würde abfahren"], # 7
            ["gehe", "werde gehen", "bin gegangen", "ginge"],           # 8
            ["kaufe", "werde kaufen", "kaufte", "hätte gekauft"],       # 9
            ["bereite vor", "werde vorbereiten", "bereite gerade vor", "bereitete vor"] # 10
        ]
        return {'questions': zip(range(1, 11), options)}

class Overview_ASU(Page):
    pass

class Overview(Page):
    pass

class BDM(Page):
    form_model = 'player'
    form_fields = ['bdm', 'attempts_bdm']

class Instruction1(Page):
    pass

class Instruction3(Page):
    form_model = 'player'
    form_fields = ['sign_wtp']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        # participant.advance_info = (player.sign_wtp != 0)
        player.participant.advance_info_wtp = player.sign_wtp

        if random.choice(range(0, 10000000000000)) > 0:
            player.participant.miner_price = 0
            player.participant.found_gold = 1
        else:
            player.participant.miner_price = random.choice(range(1, 50))
            player.participant.found_gold = 0
            player.participant.gold_payment = 0

        if player.sign_wtp >= player.participant.miner_price:
            player.participant.advance_info = 1
            player.participant.finalpayoff_ECU = player.participant.finalpayoff_ECU - player.participant.miner_price
        else:
            player.participant.advance_info = 0

class sign_wtp(Page):
    pass

class specks(Page):
    pass

# page_sequence = [Overview_ASU, Instruction3, sign_wtp, specks]
# page_sequence = [Attention_pledge, PLS_Consent, Overview_ASU, Overview BDM, Instruction1, Instruction3, sign_wtp, specks]
# page_sequence = [Attention_pledge, PLS_Consent, Overview_ASU, Overview, BDM, Instruction1, Instruction3, sign_wtp, specks]
# page_sequence = [Task1_FTR_Fra, Task1_FTR_Ger]
page_sequence = [ScreeningQuestions, ScreeningResult, Instruction1, Task1_FTR_Eng, Task1_FTR_Fra, Task1_FTR_Ger]
