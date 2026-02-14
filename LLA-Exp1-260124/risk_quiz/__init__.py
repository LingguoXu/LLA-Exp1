from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from otree.api import *

from otree.api import Currency as c, currency_range
import json

author = 'Lunzheng Li; Lingguo Xu'

doc = """ Survey 2: Risk, uncertainty and payment """
import random


class Constants(BaseConstants):
    name_in_url = 'risk_quiz'
    players_per_group = None
    participationfee = 250
    surveypayment = 130
    waitingpayment = 0
    num_rounds = 1
    sure = 2
    multiplier = 0.1
    ecuconversion = 50

class Subsession(BaseSubsession):
    def get_gain_objects(self):
        aversion_object_array = []
        for i in range(0, 21):
            num = i + 1
            left = '$0.00 with 50% chance, ' + \
                "${:,.2f}".format(Constants.sure) + ' with 50% chance'
            right = "${:,.2f}".format(i * Constants.multiplier)

            aversion_object_array.append(
                {'num': num, 'left': left, 'right': right})
        return aversion_object_array

    def get_loss_objects(self):
        aversion_object_array = []
        for i in range(0, 21):
            num = i + 1
            left = "-${:,.2f}".format(i * Constants.multiplier) + \
                ' with 50% chance, ' + "${:,.2f}".format(Constants.sure) + \
                ' with 50% chance'
            right = '$0.00 for sure'

            aversion_object_array.append(
                {'num': num, 'left': left, 'right': right})
        return aversion_object_array

    def get_ambiguity_objects(self):
        aversion_object_array = []
        for i in range(0, 21):
            num = i + 1
            left = '$0.00 with p% chance, ' + \
                "${:,.2f}".format(Constants.sure) + ' with (100-p)% chance'
            right = "${:,.2f}".format(i * Constants.multiplier) + ' for sure'

            aversion_object_array.append(
                {'num': num, 'left': left, 'right': right})
        return aversion_object_array

    def creating_session(self):
        for player in self.get_players():
            if self.round_number == Constants.num_rounds:
                round_numbers = list(range(1, Constants.num_rounds + 1))
                random.shuffle(round_numbers)
                print(round_numbers)
                player.participant.vars['task_rounds'] = dict(
                    zip(Constants.tasks, round_numbers))
                # get which task and which row to pay
                player.paying_task = random.randint(1, 3)
                player.paying_row = random.randint(1, 21)
                player.p_ambiguity = random.randint(0, 100)
                print(player.paying_task)
                print(player.paying_row)
                print(player.p_ambiguity)


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    gain_switch_point = models.IntegerField()
    loss_switch_point = models.IntegerField()
    ambiguity_switch_point = models.IntegerField()

    # paying_decision and paying_row
    paying_task = models.IntegerField()
    paying_row = models.IntegerField()

    # p_ambiguity
    p_ambiguity = models.FloatField()

    # final payoff
    payoff_risk = models.FloatField()
    # payoff = models.FloatField()  # it seems that you don't need set the model here

    # ProlificID = models.StringField(label="")
    PayID1 = models.StringField(label="")
    PayID2 = models.StringField(label="")
    Email  = models.StringField(label="")

    finalpayoff = models.FloatField()

class Instruction_risk(Page):
    def is_displayed(player):
        return player.round_number == 1

    def before_next_page(player, timeout_happened):
        player.paying_task = random.randint(1, 3)
        player.paying_row = random.randint(1, 21)
        player.p_ambiguity = random.randint(0, 100)
        print('You typed in', player.paying_task)
        print('You typed in', player.paying_row)

class gain(Page):
    form_model = 'player'
    form_fields = ['gain_switch_point']

    def vars_for_template(player):
        return dict(
            aversion_data=player.subsession.get_gain_objects(),
        )

    def before_next_page(player, timeout_happened):
        # print('before_next_page is running')
            if player.paying_task == 1:
                paying_switch_point = player.gain_switch_point
                if paying_switch_point == 22:
                    player.payoff_risk = random.choice([0, 2])
                elif player.paying_row < paying_switch_point:
                    player.payoff_risk = random.choice([0, 2])
                else:
                    player.payoff_risk = (player.paying_row - 1) * 0.1

                print(player.payoff_risk)

class loss(Page):
    form_model = 'player'
    form_fields = ['loss_switch_point']

    # def is_displayed(player):
    #     participant = player.participant
    #     return player.round_number == participant.vars['task_rounds']['loss']

    def vars_for_template(player):
        return dict(
            aversion_data=player.subsession.get_loss_objects(),
        )

    def before_next_page(player, timeout_happened):
        # print('before_next_page is running')
        if player.paying_task == 2:
            paying_switch_point = player.loss_switch_point
            if paying_switch_point == 22:
                player.payoff_risk = random.choice([-(player.paying_row - 1) * 0.1, 2])
            elif player.paying_row < paying_switch_point:
                player.payoff_risk = random.choice([-(player.paying_row - 1) * 0.1, 2])
            else:
                player.payoff_risk = 0

            print(player.payoff_risk)

class ambiguity(Page):
    form_model = 'player'
    form_fields = ['ambiguity_switch_point']

    # def is_displayed(player):
    #     participant = player.participant
    #     return player.round_number == participant.vars['task_rounds']['ambiguity']

    def vars_for_template(player):
        return dict(
            aversion_data=player.subsession.get_ambiguity_objects(),
        )

    def before_next_page(player, timeout_happened):
        # print('before_next_page is running')
        if player.paying_task == 3:
            paying_switch_point = player.loss_switch_point
            if paying_switch_point == 22:
                player.payoff_risk = random.choices([0, 2], weights=(player.p_ambiguity, 100 - player.p_ambiguity), k=1)[0]
            elif player.paying_row < paying_switch_point:
                player.payoff_risk = random.choices([0, 2], weights=(
                    player.p_ambiguity, 100 - player.p_ambiguity), k=1)[0]
            else:
                player.payoff_risk = (player.paying_row - 1) * 0.1

            print(player.payoff_risk)

class PayID(Page):
    form_model = 'player'
    form_fields = ['PayID1', 'PayID2', 'Email']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.payoff_risk = player.payoff_risk * Constants.ecuconversion

        player.participant.finalpayoff_ECU = Constants.participationfee + player.participant.miner_price +\
                                             player.participant.gold_payment + \
                                             player.participant.payoff_risk + Constants.surveypayment + Constants.waitingpayment

        player.finalpayoff = player.participant.finalpayoff_ECU / Constants.ecuconversion

    @staticmethod
    def error_message(player, values):
        if values['PayID1'] != values['PayID2']:
            return 'Please make sure you enter the same PayID.'

class Results(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            finalpayoff = player.finalpayoff,
        )

page_sequence = [
    Instruction_risk,
    gain,
    loss,
    ambiguity,
    PayID,
    Results
]