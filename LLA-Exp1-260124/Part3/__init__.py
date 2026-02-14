from otree.api import *
import random

author = 'Lingguo XU'
doc = """
Part 3: loss aversion
"""

class Constants(BaseConstants):
    name_in_url = 'Part3'
    players_per_group = None
    num_rounds = 1
    ECUpercorrect = 2

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # ... existing fields ...

    # --- NEW MPL LOSS AVERSION FIELDS ---

    # We store the "Switching Point".
    # Values 1-12 mean they switched to B at that row.
    # Value 13 means they never switched (chose A for all).
    switching_point = models.IntegerField()

    # Payoff calculation fields
    la_selected_row = models.IntegerField()
    la_choice = models.StringField()  # "A" or "B"
    la_coin_flip = models.StringField()  # "Heads" (Win) or "Tails" (Loss)
    la_payoff = models.CurrencyField()


class task_la(Page):
    form_model = 'player'
    form_fields = ['switching_point']

    def vars_for_template(player):
        # Define 12 rows.
        # Example: Gain is always 10. Loss increases from 1 to 12.
        # Structure: [Row Number, Gain, Loss]
        rows = []
        for i in range(1, 13):
            rows.append([i, 10, i])

        return {'rows': rows}

    def before_next_page(player, timeout_happened):
        import random

        # 1. Select a row at random (1 to 12) to play out
        selected_row = random.randint(1, 12)
        player.la_selected_row = selected_row

        # 2. Determine Choice based on Switching Point
        # If the selected row is BEFORE the switch, they chose A.
        # If the selected row is AT or AFTER the switch, they chose B.
        if selected_row < player.switching_point:
            player.la_choice = "A"
        else:
            player.la_choice = "B"

        # 3. Calculate Payoff
        gain = 10
        loss = selected_row  # In this example, Loss equals the Row Number (1-12)

        if player.la_choice == "B":
            # Option B: Sure 0
            player.la_payoff = 0
            player.la_coin_flip = "N/A"
        else:
            # Option A: 50/50 Lottery
            if random.random() < 0.5:
                # Win
                player.la_payoff = gain
                player.la_coin_flip = "Win"
            else:
                # Loss
                player.la_payoff = -loss
                player.la_coin_flip = "Loss"

        # 4. Add to total payoff (optional)
        player.payoff += player.la_payoff

page_sequence = [task_la]
# page_sequence = [EndPage_ASU]


