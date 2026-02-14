from otree.api import *
import json

doc = """
Life-Year AIT: Mixed Gambles
Tests whether delay increases loss aversion for life-year outcomes,
and whether anticipatory emotions explain this effect.
"""

# ─── CONSTANTS ───────────────────────────────────────────────

class C(BaseConstants):
    NAME_IN_URL = 'study'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Scenario parameters
    DIAGNOSIS_AGE = 60
    MAX_LIFESPAN = 70       # max years with condition (Drug A guarantees this)
    GOOD_OUTCOME_AGE = 75   # age if Drug B works (gain of 5 years)
    GAIN_YEARS = 5          # years gained in good outcome

    # Bisection parameters
    BISECTION_STEPS = 5     # number of binary choices
    X_MIN = 0.5             # minimum years at risk (6 months)
    X_MAX = 10.0            # maximum years at risk


# ─── SUBSESSION ──────────────────────────────────────────────

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    import itertools
    # Balanced assignment: alternating delay / no_delay
    treatments = itertools.cycle(['delay', 'no_delay'])
    for player in subsession.get_players():
        player.treatment = next(treatments)


# ─── GROUP ───────────────────────────────────────────────────

class Group(BaseGroup):
    pass


# ─── PLAYER ──────────────────────────────────────────────────

class Player(BasePlayer):
    # Treatment assignment
    treatment = models.StringField(
        doc="Between-subjects: 'delay' or 'no_delay'"
    )

    # ── Primary elicitation (the "real" data) ──
    primary_x = models.FloatField(
        doc="Indifference X (years lost in bad outcome) for primary condition",
        min=0, max=10, blank=True
    )
    primary_bisection_data = models.LongStringField(
        doc="JSON: bisection choices for primary elicitation",
        blank=True
    )

    # ── Mock elicitation (exploratory data) ──
    mock_x = models.FloatField(
        doc="Indifference X for mock (opposite) condition",
        min=0, max=10, blank=True
    )
    mock_bisection_data = models.LongStringField(
        doc="JSON: bisection choices for mock elicitation",
        blank=True
    )

    # ── Anticipatory emotions (for the delay choice) ──
    dread = models.IntegerField(
        label="How anxious would you feel while waiting for the result?",
        choices=range(1, 10),
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    savouring = models.IntegerField(
        label="How excited would you feel while waiting for the result?",
        choices=range(1, 10),
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    attention = models.IntegerField(
        label="How often would you think about the outcome while waiting?",
        choices=range(1, 10),
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    vividness = models.IntegerField(
        label="How vividly could you imagine the outcome while waiting?",
        choices=range(1, 10),
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )

    # ── Demographics ──
    age = models.IntegerField(
        label="What is your age?",
        min=18, max=100, blank=True
    )
    gender = models.StringField(
        label="What is your gender?",
        choices=[
            ['male', 'Male'],
            ['female', 'Female'],
            ['non_binary', 'Non-binary / third gender'],
            ['prefer_not', 'Prefer not to say'],
        ],
        blank=True
    )
    uk_resident = models.BooleanField(
        label="Are you currently a resident of the United Kingdom?",
        blank=True
    )


# ─── HELPER: shared vars for drug pages ──────────────────────

def drug_page_vars(is_delay):
    """Variables passed to DrugIntro and ChoiceElicitation templates."""
    return dict(
        is_delay=is_delay,
        delay_label='6 months' if is_delay else 'immediately',
        timing_description=(
            'The results of Drug B will take <strong>6 months</strong> to become clear. '
            'During this waiting period, you will not know whether the outcome is good or bad.'
        ) if is_delay else (
            'The results of Drug B will be known <strong>immediately</strong> after you take it.'
        ),
        diagnosis_age=C.DIAGNOSIS_AGE,
        max_lifespan=C.MAX_LIFESPAN,
        good_outcome_age=C.GOOD_OUTCOME_AGE,
        gain_years=C.GAIN_YEARS,
        x_min=C.X_MIN,
        x_max=C.X_MAX,
        bisection_steps=C.BISECTION_STEPS,
    )


# ─── PAGES ───────────────────────────────────────────────────

class Introduction(Page):
    """Welcome page with progressive reveal."""
    pass


class Diagnosis(Page):
    """Beta-syndrome scenario reveal."""
    pass


class PrimaryDrugIntro(Page):
    """Explains Drug A & B for the primary condition."""
    template_name = 'study/DrugIntro.html'

    @staticmethod
    def vars_for_template(player: Player):
        is_delay = (player.treatment == 'delay')
        v = drug_page_vars(is_delay)
        v['is_primary'] = True
        v['choice_number'] = 1
        return v


class PrimaryChoice(Page):
    """Interactive bisection + slider for primary elicitation."""
    template_name = 'study/ChoiceElicitation.html'
    form_model = 'player'
    form_fields = ['primary_x', 'primary_bisection_data']

    @staticmethod
    def vars_for_template(player: Player):
        is_delay = (player.treatment == 'delay')
        v = drug_page_vars(is_delay)
        v['is_primary'] = True
        v['field_x'] = 'primary_x'
        v['field_bisection'] = 'primary_bisection_data'
        return v


class PrimaryAnticipationIntro(Page):
    """Transition to emotion questions (delay treatment only)."""
    template_name = 'study/AnticipationIntro.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'delay'


class PrimaryEmotionRatings(Page):
    """Emotion ratings for delay treatment's primary choice."""
    template_name = 'study/EmotionRatings.html'
    form_model = 'player'
    form_fields = ['dread', 'savouring', 'attention', 'vividness']

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'delay'


class MockTransition(Page):
    """Brief transition page introducing the second scenario."""
    pass


class MockDrugIntro(Page):
    """Explains Drug A & B for the mock (opposite) condition."""
    template_name = 'study/DrugIntro.html'

    @staticmethod
    def vars_for_template(player: Player):
        # Mock is opposite condition
        is_delay = (player.treatment != 'delay')
        v = drug_page_vars(is_delay)
        v['is_primary'] = False
        v['choice_number'] = 2
        return v


class MockChoice(Page):
    """Interactive bisection + slider for mock elicitation."""
    template_name = 'study/ChoiceElicitation.html'
    form_model = 'player'
    form_fields = ['mock_x', 'mock_bisection_data']

    @staticmethod
    def vars_for_template(player: Player):
        is_delay = (player.treatment != 'delay')
        v = drug_page_vars(is_delay)
        v['is_primary'] = False
        v['field_x'] = 'mock_x'
        v['field_bisection'] = 'mock_bisection_data'
        return v


class MockAnticipationIntro(Page):
    """Transition to emotion questions (no_delay treatment only)."""
    template_name = 'study/AnticipationIntro.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'no_delay'


class MockEmotionRatings(Page):
    """Emotion ratings for no_delay treatment's mock choice."""
    template_name = 'study/EmotionRatings.html'
    form_model = 'player'
    form_fields = ['dread', 'savouring', 'attention', 'vividness']

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'no_delay'


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'uk_resident']


class ThankYou(Page):
    pass


# ─── PAGE SEQUENCE ───────────────────────────────────────────
# Both treatments see all pages; is_displayed() controls which are skipped.
# Flow for delay treatment:    Intro → Diagnosis → DrugIntro(delay) → Choice(delay) → Anticipation → Emotions → Transition → DrugIntro(immediate) → Choice(immediate) → Demographics → End
# Flow for no_delay treatment: Intro → Diagnosis → DrugIntro(immediate) → Choice(immediate) → Transition → DrugIntro(delay) → Choice(delay) → Anticipation → Emotions → Demographics → End

page_sequence = [
    Introduction,
    Diagnosis,
    PrimaryDrugIntro,
    PrimaryChoice,
    PrimaryAnticipationIntro,   # only delay treatment
    PrimaryEmotionRatings,      # only delay treatment
    MockTransition,
    MockDrugIntro,
    MockChoice,
    MockAnticipationIntro,      # only no_delay treatment
    MockEmotionRatings,         # only no_delay treatment
    Demographics,
    ThankYou,
]