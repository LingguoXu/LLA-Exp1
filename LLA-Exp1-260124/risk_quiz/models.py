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


author = 'Lunzheng Li'

doc = """
This app is based on the source code provided by Dr. Zhang Jingjing.
The source code seems originally developped by Chengbin Feng (UNSW)

1. We have three questions, let me firstly get one question;
(using my old method will need to define lots of variables
try to understand Feng's method, or define the var in var_in_templates)

2. Then create three questions in a fixed order;
    28/07 pushed the app to heroku, however, the pop out windows (modal) is not
    working try to figure out why.

3. Then follow here https://www.otreehub.com/projects/otree-snippets/ to
randomize the round/page/task order.

4. randomly choose one to pay (for each question choice one?)
"""
import random


class Constants(BaseConstants):
    name_in_url = 'risk_quiz'
    players_per_group = None

    sure = 2
    multiplier = 0.1

    tasks = ['gain', 'loss', 'ambiguity', ]

    num_rounds = len(tasks)

    # participation_fee = 5


class Subsession(BaseSubsession):
    def get_gain_objects(self):
        aversion_object_array = []
        for i in range(0, 21):
            num = i + 1
            left = '$0.00 with 50% chance, ' + \
                "${:,.2f}".format(Constants.sure) + ' with 50% chance'
            right = "${:,.2f}".format(i * Constants.multiplier) + ' for sure'

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
                player.paying_task = random.sample(Constants.tasks, 1)[0]
                player.paying_row = random.randint(1, 21)
                player.p_ambiguity = random.randint(0, 100)
                print(player.paying_task)
                print(player.paying_row)
                print(player.p_ambiguity)

    def get_quiz_data(self):
        return [
            dict(
                name='risk_quiz1',
                explanation='''Your answer is wrong. You have decided to switch 
                from preferring a lottery to preferring the corresponding sure amount of money at choice [7].
                Therefore, at choice [4], you payoff is the lottery.''',
            ),
            dict(
                name='risk_quiz2',
                explanation='''Your answer is wrong. You have decided to switch 
                from preferring a lottery to preferring the corresponding sure amount of money at choice [7].
                Therefore, at choice [11], you payoff is the sure amount.''',
            ),
            dict(
                name='risk_quiz3',
                explanation='''Your answer is wrong. You have decided to switch 
                from preferring a lottery to preferring the corresponding sure amount of money at choice [7].
                Therefore, at choice [6], you payoff is the lottery.''',
            ),
            dict(
                name='risk_quiz4',
                explanation='''Your answer is wrong. You have decided to switch 
                from preferring a lottery to preferring the corresponding sure amount of money at choice [7].
                Therefore, at choice [9], you payoff is the sure amount.''',
            ),

        ]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # pay_ID
    pay_ID = models.StringField(
        label='Please enter your PayID (your PayID is either your email or your phone number):')

    pay_ID_check = models.StringField(
        label='Please re-enter your PayID :')

    payoff_in_total = models.FloatField()
    payoff_in_total = models.CurrencyField()

    gain_switch_point = models.IntegerField()
    loss_switch_point = models.IntegerField()
    ambiguity_switch_point = models.IntegerField()

    # paying_decision and paying_row
    paying_task = models.StringField()
    paying_row = models.IntegerField()

    # p_ambiguity
    p_ambiguity = models.FloatField()

    # final payoff
    payoff_risk = models.FloatField()
    # payoff = models.FloatField()  # it seems that you don't need set the model here

    your_decision = models.StringField()

    # quiz
    risk_quiz1 = models.BooleanField(
        choices=[
            [True, 'a lottery that pays you $0.00 with 50% chance or $2.00 with 50% chance'],
            [False, '$0.30 for sure'],
        ],
        label='''Assume now that choice [4] is randomly selected for possible payoff (“payoff-relevant”).
                Your payoff relevant choice [4] then is:''',
    )
    risk_quiz2 = models.BooleanField(
        choices=[
                [False, 'a lottery that pays you $0.00 with 50% chance or $2.00 with 50% chance'],
                [True, '$1.00 for sure'],
        ],
        label='''Assume now that choice [11] is randomly selected for possible payoff (“payoff-relevant”).
                Your payoff relevant choice [11] then is:''',
    )

    risk_quiz3 = models.BooleanField(
        choices=[
                [True, '''a lottery that pays you $0.00 with p% chance or $2.00 with (100-p)% chance 
                where p is an unknown number between 0 and 100. (For example p might be 60, then the 
                lottery would pay you $0.00 with 60% chance or $2.00 with 40% chance).'''],
                [False, '$0.50 for sure'],
        ],
        label='''Assume now that choice [6] is randomly selected for possible payoff (“payoff-relevant”).
                Your payoff relevant choice [6] then is:''',
    )
    risk_quiz4 = models.BooleanField(
        choices=[
                [False, '''a lottery that pays you $0.00 with p % chance or $2.00 with (100 - p) % chance
                 where p is an unknown number between 0 and 100.(For example p might be 60, then the 
                 lottery would pay you $0.00 with 60% chance or $2.00 with 40% chance).'''],
                [True, '$0.80 for sure'],
        ],
        label='''Assume now that choice [9] is randomly selected for possible payoff (“payoff-relevant”).
                Your payoff relevant choice [9] then is:''',
    )

    def get_payoff(self):
        # get your choice in the chosen task and row
        if self.paying_task == 'gain':
            paying_switch_point = self.in_round(
                self.participant.vars['task_rounds']['gain']).gain_switch_point
            if paying_switch_point == 22:
                self.payoff_risk = random.choice([0, 2])
                self.your_decision = 'lottery'
            elif self.paying_row < paying_switch_point:
                self.payoff_risk = random.choice([0, 2])
                self.your_decision = 'lottery'
            else:
                self.payoff_risk = (self.paying_row - 1) * 0.1
                self.your_decision = 'sure payoff'

        elif self.paying_task == 'loss':
            paying_switch_point = self.in_round(
                self.participant.vars['task_rounds']['loss']).loss_switch_point
            if paying_switch_point == 22:
                self.payoff_risk = random.choice(
                    [-(self.paying_row - 1) * 0.1, 2])
                self.your_decision = 'lottery'
            elif self.paying_row < paying_switch_point:
                self.payoff_risk = random.choice(
                    [-(self.paying_row - 1) * 0.1, 2])
                self.your_decision = 'lottery'
            else:
                self.payoff_risk = 0
                self.your_decision = 'sure payoff'

        else:
            paying_switch_point = self.in_round(
                self.participant.vars['task_rounds']['ambiguity']).ambiguity_switch_point
            if paying_switch_point == 22:
                self.payoff_risk = random.choices([0, 2], weights=(
                    self.p_ambiguity, 100 - self.p_ambiguity), k=1)[0]
                self.your_decision = 'lottery'
            elif self.paying_row < paying_switch_point:
                self.payoff_risk = random.choices([0, 2], weights=(
                    self.p_ambiguity, 100 - self.p_ambiguity), k=1)[0]
                self.your_decision = 'lottery'
            else:
                self.payoff_risk = (self.paying_row - 1) * 0.1
                self.your_decision = 'sure payoff'
        print(paying_switch_point)
        # print(self.session.config["participation_fee"])
        self.payoff_risk = float("{:.1f}".format(self.payoff_risk))
        self.payoff = self.payoff_risk

        if 'game_total_payoff' in self.participant.vars:
            self.payoff_in_total = self.participant.vars['game_total_payoff'] /\
                self.session.config.get('point_to_dollar_factor') +\
                self.payoff_risk + self.session.config["participation_fee"]

            # self.payoff_in_total = c(self.participant.vars['game_total_payoff']/\
            # self.session.config.get('point_to_dollar_factor')) +\
            # c(self.payoff_risk) + self.session.config["participation_fee"]

            # self.payoff_in_total = float(
            #     "{:.1f}".format(self.payoff_in_total))
