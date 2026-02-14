from otree.api import *
import random
import csv

author = 'Lingguo XU'
doc = """
Part 4: Task for T1, waiting and task for T2
"""

class Constants(BaseConstants):
    name_in_url = 'Part4'
    players_per_group = None
    ECUpercorrect = 2
    goldvalue_low = 680
    goldvalue_high = 865

    # with open('Part4/Part4_asnwerkey.csv') as questions_file:
    #     questions = list(csv.DictReader(questions_file))

    # num_rounds = len(questions)
    num_rounds = 12

class Subsession(BaseSubsession):
    pass
    # def creating_session(subsession):
    #     if player.round_number == 1:
    #         player.session.vars['questions'] = Constants.questions.copy()
    #
    #     for player in subsession.get_players():
    #         question_data = current_question(player)
    #         player.solution = question_data['solution']
    #         player.round_number = player.round_number

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    wta_t2 = models.IntegerField(min=680, max=865, label="Please enter a number between 680 and 865.")

    # solution = models.StringField()
    # # task_answers = models.StringField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    # #         label="Please select a number.", initial="")
    # task_answers = models.StringField(label="Your answer", initial="")
    # is_correct   = models.BooleanField(initial=0)
    # attempts_R2  = models.IntegerField()
    # success_R2   = models.IntegerField()
    # task2payoff  = models.IntegerField()

    def current_question(player):
        return player.session.vars['questions'][player.round_number - 1]

    num_checks  = models.IntegerField(initial=0, blank = True)
    total_checks_R2  = models.IntegerField(initial=0, blank = True)
    check_timing = models.FloatField(initial=0, blank = True)
    check_timing_teaser = models.FloatField(initial=0, blank = True)
    timeonimage = models.FloatField(initial=0, blank = True)
    total_timeonimage_R2 = models.FloatField(initial=0, blank = True)
    # timeleft    = models.FloatField(initial=0, blank = True)

# FUNCTIONS
# def get_timeout_seconds(player):
#     import time
#     return player.participant.expiry - time.time()
#
# def creating_session(subsession):
#     for player in subsession.get_players():
#         if player.round_number == 1:
#             player.session.vars['questions'] = Constants.questions.copy()
#
#         question_data = player.current_question()
#         player.solution = question_data['solution']
#         player.round_number = player.round_number

# PAGES
class ReadyTask_ASU(Page):
    def is_displayed(player):
        return player.round_number == 1

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     participant = player.participant
    #
    #     import time
    #     # user has 10 minutes to complete as many pages as possible
    #     participant.vars['expiry'] = time.time() + player.session.config['task_round_timeout_seconds_2']

class Task(Page):
    form_model = 'player'
    form_fields = ['num_checks', 'timeonimage', 'check_timing', 'check_timing_teaser']
    timer_text = 'Next round in:'
    timeout_seconds = 40

    # get_timeout_seconds = get_timeout_seconds
    #
    # @staticmethod
    # def is_displayed(player):
    #     import time
    #     return player.participant.expiry - time.time() > 1 and player.round_number != Constants.num_rounds
    #
    # @staticmethod
    # def vars_for_template(player):
    #     return dict(
    #         image_path_1='Part4/ImagQuestions/{}.png'.format(player.round_number),
    #         round_number = player.round_number
    #     )
    #
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     import time
    #
    #     if player.task_answers:
    #         player.is_correct = (player.task_answers.lower() == player.solution.lower())
    #         player.participant.finalpayoff_ECU = player.participant.finalpayoff_ECU + player.is_correct * Constants.ECUpercorrect
    #
    @staticmethod
    def js_vars(player):
        import time
        return dict(
            roundnum = player.round_number,
            # timeleft = player.participant.expiry - time.time(),
        )

class mining_complete(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 2

class Results_t1(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 1

    # @staticmethod
    # def vars_for_template(player):
    #     player_in_all_rounds = player.in_all_rounds()
    #     Need to filter out the none types where the player didn't get a chance to answer the questions
    #
    #     filtered1 = [p.task_answers for p in player_in_all_rounds if p.task_answers != ""]
    #     filtered2 = [p.is_correct for p in player_in_all_rounds]
    #
    #     player.attempts_R2 = len(filtered1)
    #     player.success_R2 = sum(filtered2)
    #
    #     Compute player payoff in Part 1
    #     player.task2payoff = Constants.ECUpercorrect * player.success_R2
    #
    #     Earnings from second task round, Treatment 1
    #     player.participant.task2payoff = player.task2payoff

class Results_t2(Page):
    form_model = 'player'
    form_fields = ['wta_t2']

    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 2

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.wta_t2 = player.wta_t2
        participant.buyer_price = random.choice(range(680, 865))

        if participant.buyer_price < participant.wta_t2:
            participant.get_gold = 1
            participant.gold_payment = participant.gold_value
            participant.finalpayoff_ECU = participant.finalpayoff_ECU + participant.gold_payment
        else:
            participant.get_gold = 0
            participant.gold_payment = participant.wta_t2
            participant.finalpayoff_ECU = participant.finalpayoff_ECU + participant.gold_payment

    @staticmethod
    def vars_for_template(player):
        player_in_all_rounds = player.in_all_rounds()
        # Need to filter out the none types where the player didn't get a chance to answer the questions

        # filtered1 = [p.task_answers for p in player_in_all_rounds if p.task_answers != ""]
        # filtered2 = [p.is_correct for p in player_in_all_rounds]
        filtered3 = [p.num_checks for p in player_in_all_rounds]
        filtered4 = [p.timeonimage for p in player_in_all_rounds]

        # player.attempts_R2 = len(filtered1)
        # player.success_R2 = sum(filtered2)
        player.total_checks_R2 = sum(filtered3)
        player.total_timeonimage_R2 = sum(filtered4)

        # # Compute player payoff in Part 1
        # player.task2payoff = Constants.ECUpercorrect * player.success_R2
        #
        # # Earnings from second task round, Treatment 2
        # player.participant.task2payoff = player.task2payoff

class T2_reveal(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 2 and player.participant.found_gold == 1

page_sequence = [ReadyTask_ASU, Task, Results_t1, mining_complete, Results_t2, T2_reveal]