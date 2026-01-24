from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json

class instruction(Page):
    def is_displayed(self):
        return self.player.round_number == 1


class Question_1(Page):
    form_model = 'player'
    form_fields = ['risk_quiz1', 'risk_quiz2']

    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        fields = self.subsession.get_quiz_data()[0:2]
        return dict(fields=fields, show_solutions=False)


class Result_1(Page):
    form_model = 'player'
    form_fields = ['risk_quiz1', 'risk_quiz2']

    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        fields = self.subsession.get_quiz_data()[0:2]
        answers = [self.player.risk_quiz1, self.player.risk_quiz2]
        i = 0
        for d in fields:
            d['is_correct'] = answers[i]
            i += 1
        return dict(fields=fields, show_solutions=True)


class Question_2(Page):
    form_model = 'player'
    form_fields = ['risk_quiz3', 'risk_quiz4']

    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        fields = self.subsession.get_quiz_data()[2:4]
        return dict(fields=fields, show_solutions=False)


class Result_2(Page):
    form_model = 'player'
    form_fields = ['risk_quiz3', 'risk_quiz4']

    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        fields = self.subsession.get_quiz_data()[2:4]
        answers = [self.player.risk_quiz3, self.player.risk_quiz4]
        i = 0
        for d in fields:
            d['is_correct'] = answers[i]
            i += 1
        return dict(fields=fields, show_solutions=True)


class gain(Page):
    form_model = 'player'
    form_fields = ['gain_switch_point']

    def is_displayed(self):
        participant = self.player.participant
        return self.player.round_number == participant.vars['task_rounds']['gain']

    def vars_for_template(self):
        return dict(
            aversion_data=self.subsession.get_gain_objects(),
        )

    def before_next_page(self):
        # print('before_next_page is running')
        if self.player.round_number == Constants.num_rounds:
            print('if condition is running')
            player = self.player
            player.get_payoff()


class loss(Page):
    form_model = 'player'
    form_fields = ['loss_switch_point']

    def is_displayed(self):
        participant = self.player.participant
        return self.player.round_number == participant.vars['task_rounds']['loss']

    def vars_for_template(self):
        return dict(
            aversion_data=self.subsession.get_loss_objects(),
        )

    def before_next_page(self):
        # print('before_next_page is running')
        if self.player.round_number == Constants.num_rounds:
            print('if condition is running')
            player = self.player
            player.get_payoff()


class ambiguity(Page):
    form_model = 'player'
    form_fields = ['ambiguity_switch_point']

    def is_displayed(self):
        participant = self.player.participant
        return self.player.round_number == participant.vars['task_rounds']['ambiguity']

    def vars_for_template(self):
        return dict(
            aversion_data=self.subsession.get_ambiguity_objects(),
        )

    def before_next_page(self):
        # print('before_next_page is running')
        if self.player.round_number == Constants.num_rounds:
            # print('if condition is running')
            player = self.player
            player.get_payoff()


class Summary(Page):
    form_model = 'player'
    form_fields = ['pay_ID', 'pay_ID_check']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        if 'game_total_payoff' in self.participant.vars:
            payoff_in_contest = self.player.participant.vars['game_total_payoff']
        else:
            payoff_in_contest = "no main experiment result"

        rounds_payoffs = json.loads(
            self.player.participant.vars["chosen_rounds"]
        )

        point_to_dollar_factor = self.session.config.get('point_to_dollar_factor')
        total_dollar_payoff_game = payoff_in_contest/point_to_dollar_factor

        return dict(
            payoff_in_contest=payoff_in_contest,
            chosen_rounds=", ".join(rounds_payoffs.keys()),
            rounds_payoffs=rounds_payoffs.items(),
            total_dollar_payoff_game=total_dollar_payoff_game,
            point_to_dollar_factor=point_to_dollar_factor,
            participation_fee=self.session.config["participation_fee"],
        )

    def error_message(self, values):
        if values['pay_ID'] != values['pay_ID_check']:
            return 'The second PayID must match the first!'


class Thankyou(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    instruction,
    Question_1,
    Result_1,
    Question_2,
    Result_2,
    gain,
    loss,
    ambiguity,
]
