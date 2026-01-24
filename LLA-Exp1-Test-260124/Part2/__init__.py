from otree.api import *
import random
import csv

author = 'Lingguo XU'
doc = """
Part 2: Waiting for mining to complete & first task round
"""

class Constants(BaseConstants):
    name_in_url = 'Part2'
    players_per_group = None
    ECUpercorrect = 2
    ECUwaiting = 0
    waitingfee = 80
    time_eachround = 40
    # with open('Part2/asnwerkey.csv') as questions_file:
    #     questions = list(csv.DictReader(questions_file))

    # num_rounds = len(questions)
    num_rounds = 15

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
    # solution     = models.StringField()
    # task_answers = models.StringField(label="Your answer", initial="")
    # is_correct   = models.BooleanField(initial=0)
    # attempts_R1  = models.IntegerField()
    # success_R1   = models.IntegerField()
    # task1payoff  = models.IntegerField()

    # def current_question(player):
    #     return player.session.vars['questions'][player.round_number - 1]

    num_checks  = models.IntegerField(initial=0, blank = True)
    total_checks_R1  = models.IntegerField(initial=0, blank = True)
    check_timing = models.FloatField(initial=0, blank = True)
    check_timing_teaser = models.FloatField(initial=0, blank = True)
    timeonimage = models.FloatField(initial=0, blank = True)
    total_timeonimage_R1 = models.FloatField(initial=0, blank = True)
    # timeleft    = models.FloatField(initial=0, blank = True)

# FUNCTIONS
# def get_timeout_seconds(player):
#     import time
#     return player.participant.expiry - time.time()

# def creating_session(subsession):
#     for player in subsession.get_players():
#         if player.round_number == 1:
#             player.session.vars['questions'] = Constants.questions.copy()
#
#         question_data       = player.current_question()
#         player.solution     = question_data['solution']
#         player.round_number = player.round_number

# PAGES
class ReadyTask(Page):
    def is_displayed(player):
        return player.round_number == 1

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     participant = player.participant
    #
    #     import time
    #     # user has 10 minutes to complete as many pages as possible
    #     participant.vars['expiry'] = time.time() + player.session.config['task_round_timeout_seconds']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.finalpayoff_ECU = participant.finalpayoff_ECU + Constants.ECUwaiting

class Task(Page):
    form_model = 'player'
    form_fields = ['num_checks', 'timeonimage', 'check_timing', 'check_timing_teaser']
    timer_text = 'Next round in:'
    timeout_seconds = 40

    # get_timeout_seconds = get_timeout_seconds

    # @staticmethod
    # def is_displayed(player):
    #     import time
    #     return player.participant.expiry - time.time() > 1
    #
    # @staticmethod
    # def vars_for_template(player):
    #     return dict(
    #         image_path_1='Part1/ImagQuestions/{}.png'.format(player.round_number),
    #         image_path_2='Part1/ImagAnswers/{}.jpg'.format(player.round_number),
    #         round_number = player.round_number
    #     )

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     import time
    #     if player.task_answers:
    #         player.is_correct = (player.task_answers.lower() == player.solution.lower())
    #         player.participant.finalpayoff_ECU = player.participant.finalpayoff_ECU + player.is_correct * Constants.ECUpercorrect

        # if player.num_checks == None:
        #     player.num_checks = 0
        # if player.timeonimage == None:
        #     player.timeonimage = 0

    @staticmethod
    def js_vars(player):
        import time
        return dict(
            roundnum = player.round_number,
            # timeleft = player.participant.expiry - time.time(),
        )

class Results_ASU(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        player_in_all_rounds = player.in_all_rounds()
        # Need to filter out the none types where the player didn't get a chance to answer the questions

        # filtered1 = [p.task_answers for p in player_in_all_rounds if p.task_answers != ""]
        # filtered2 = [p.is_correct for p in player_in_all_rounds]
        filtered3 = [p.num_checks for p in player_in_all_rounds]
        filtered4 = [p.timeonimage for p in player_in_all_rounds]

        # player.attempts_R1 = len(filtered1)
        # player.success_R1 = sum(filtered2)
        player.total_checks_R1 = sum(filtered3)
        player.total_timeonimage_R1 = sum(filtered4)

        # Compute player payoff from first task
        # player.task1payoff = Constants.ECUpercorrect * player.success_R1
        # player.participant.task1payoff = player.task1payoff
        player.participant.checkprogress = player.total_checks_R1

page_sequence = [ReadyTask, Task, Results_ASU]