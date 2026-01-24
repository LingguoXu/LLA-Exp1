from otree.api import *
import random

author = 'Lingguo XU'
doc = """
Part 3: Revelation for T1 and delay announcement for T2
"""

class Constants(BaseConstants):
    name_in_url = 'Part3'
    players_per_group = None
    num_rounds = 1
    ECUpercorrect = 2
    goldvalue_low = 680
    goldvalue_high = 865

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Absolute belief and confidence on belief
    wta_t1  = models.IntegerField(min=680, max=865, label="Please enter a number between 680 and 865.")

    # wta_t1  = models.IntegerField(choices = [680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870],
    #     label="Please put in a number between 680 and 870.")

    #Payoff for Part 3
    payoff_part3 = models.IntegerField()

# FUNCTIONS

def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.gold_value = random.choice(range(680, 865))
        print('set player.participant.gold_value', player.participant.gold_value)

# PAGE
class T1_wta (Page):
    form_model = 'player'
    form_fields = ['wta_t1']

    def is_displayed(player):
        return player.participant.treatment == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        participant.wta_t1 = player.wta_t1

        participant.buyer_price = random.choice(range(680, 865))

        if participant.buyer_price < participant.wta_t1:
            participant.get_gold = 1
            participant.gold_payment = participant.gold_value
            participant.finalpayoff_ECU = participant.finalpayoff_ECU + participant.gold_payment
        else:
            participant.get_gold = 0
            participant.gold_payment = participant.wta_t1
            participant.finalpayoff_ECU = participant.finalpayoff_ECU + participant.gold_payment

class T1_reveal(Page):
    form_model = 'player'

    def is_displayed(player):
        return player.participant.treatment == 1 and player.participant.found_gold == 1

class T2_delay(Page):
    form_model = 'player'

    def is_displayed(player):
        return player.participant.treatment == 2


page_sequence = [T1_wta, T1_reveal, T2_delay]
# page_sequence = [EndPage_ASU]


