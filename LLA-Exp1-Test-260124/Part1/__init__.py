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
    participation_fee = 250
    goldvalue_low = 680
    goldvalue_high = 865

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.IntegerField(label="",
        choices=[[1, 'I agree']],
        widget=widgets.RadioSelect
    )

    # Comprehension question for BDM
    bdm = models.IntegerField(min=0, max=100, label="Please fill in a number between 0 and 100")
    attempts_bdm = models.IntegerField(initial=0, blank = True)

    # WTP for advance information
    sign_wtp = models.IntegerField(min=0, max=50, label="Please fill in a number between 0 and 50")

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
page_sequence = [Attention_pledge, PLS_Consent, Overview_ASU, Overview, BDM, Instruction1, Instruction3, sign_wtp, specks]
# page_sequence = [PLS_Consent, Overview]
