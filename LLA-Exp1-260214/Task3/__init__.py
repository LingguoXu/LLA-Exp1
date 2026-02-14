from otree.api import *
import random

doc = """
Task 3: Loss Aversion Elicitation (Gächter et al.) & Post-Experiment Survey.
Languages: English (en), French (fr), German (de), Japanese (ja).
"""


class C(BaseConstants):
    NAME_IN_URL = 'task3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # 12-row structure from source: Win 10, Lose 1-12
    LOTTERIES = [dict(id=i, gain=10, loss=i) for i in range(1, 13)]

    # Define the 0-10 range here for the template to loop over safely
    LIKERT_RANGE = list(range(11))

    # Range for Risk/Patience Likert scales (0-10)
    LIKERT_RANGE = list(range(11))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    language = models.StringField(initial='en')

    # --- REPLICATED FIELDS ---
    la_switching_point = models.IntegerField(min=1, max=13) # 13 means they always chose A
    la_selected_row = models.IntegerField()
    la_choice = models.StringField()
    la_coin_flip = models.StringField()
    la_payoff = models.CurrencyField()

    # --- SURVEY FIELDS ---
    age = models.IntegerField(min=18, max=100)
    gender = models.StringField()
    native_language = models.StringField()
    risk_general = models.IntegerField(min=0, max=10)
    patience_general = models.IntegerField(min=0, max=10)
    strategy_comment = models.LongStringField(blank=True)


# ═══════════════════════════════════════════════════════════
# UI TRANSLATIONS
# ═══════════════════════════════════════════════════════════
UI = dict(
    btn_next = dict(en='Next', fr='Suivant', de='Weiter', ja='次へ'),
    btn_submit = dict(en='Submit Decisions', fr='Soumettre', de='Entscheidungen absenden', ja='決定を送信'),
    intro_title = dict(en='Part 3: Decision Making', fr='Partie 3: Prise de décision', de='Teil 3: Entscheidungsfindung', ja='パート3: 意思決定'),
    intro_text = dict(
        en='In this final task, you will make a series of decisions involving potential gains and losses.',
        fr='Dans cette dernière tâche, vous prendrez une série de décisions impliquant des gains et des pertes.',
        de='In dieser letzten Aufgabe treffen Sie eine Reihe von Entscheidungen mit Gewinnen und Verlusten.',
        ja='この最後の課題では、潜在的な利益と損失を含む一連の意思決定を行います。'
    ),
    la_alert_head = dict(en='How it works:', fr='Comment ça marche :', de='So funktioniert es:', ja='仕組み:'),
    la_alert_text = dict(
        en='If you switch from Option A to Option B in one row, the computer will automatically select Option A for all rows above it and Option B for all rows below it. You only need to click once to set your "switching point."',
        fr='Si vous passez de l\'option A à l\'option B sur une ligne, l\'ordinateur sélectionnera automatiquement l\'option A pour toutes les lignes situées au-dessus et l\'option B pour toutes les lignes situées en dessous.',
        de='Wenn Sie in einer Zeile von Option A zu Option B wechseln, wählt der Computer automatisch Option A für alle darüber liegenden Zeilen und Option B für alle darunter liegenden Zeilen.',
        ja='ある行で選択肢Aから選択肢Bに切り替えると、それより上のすべての行で選択肢Aが、それより下のすべての行で選択肢Bが自動的に選択されます。「切り替えポイント」を設定するには、一度クリックするだけです。'
    ),
    la_inst = dict(en='Please make a choice for each of the 12 rows below.', ja='以下の12の行それぞれについて選択してください。'),
    opt_a = dict(en='Option A: Lottery', ja='選択肢A: くじ'),
    opt_b = dict(en='Option B: Sure Amount', ja='選択肢B: 確実な金額'),
    win = dict(en='Win', ja='獲得'),
    lose = dict(en='Lose', ja='損失'),
    reject = dict(en='Get 0 ECU for sure', ja='確実に 0 ECU を得る'),
    error_sel = dict(en='Please make a selection before submitting.', ja='送信する前に選択してください。'),
    surv_title=dict(en='Final Survey', fr='Enquête finale', de='Abschlussumfrage', ja='最終アンケート'),
    q_age=dict(en='What is your age?', fr='Quel est votre âge ?', de='Wie alt sind Sie?', ja='あなたの年齢は？'),
    q_gender=dict(en='What is your gender?', fr='Quel est votre genre ?', de='Was ist Ihr Geschlecht?', ja='あなたの性別は？'),
    g_male=dict(en='Male', fr='Homme', de='Männlich', ja='男性'),
    g_female=dict(en='Female', fr='Femme', de='Weiblich', ja='女性'),
    g_nb=dict(en='Non-binary', fr='Non-binaire', de='Nicht-binär', ja='ノンバイナリー'),
    g_no=dict(en='Prefer not to say', fr='Je préfère ne pas répondre', de='Keine Angabe', ja='回答したくない'),
    q_lang=dict(en='What is your native language?', fr='Quelle est votre langue maternelle ?',
                de='Was ist Ihre Muttersprache?', ja='あなたの母国語は？'),
    q_risk=dict(
        en='How do you see yourself: are you generally a person who is fully prepared to take risks or do you try to avoid taking risks?',
        fr='Comment vous voyez-vous : êtes-vous généralement une personne prête à prendre des risques ou essayez-vous d\'éviter de prendre des risques ?',
        de='Wie sehen Sie sich selbst: Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        ja='ご自身をどのように評価しますか：あなたは一般的にリスクを冒す準備ができている人ですか、それともリスクを避けようとする人ですか？'
    ),
    risk_0=dict(en='Avoid risks', fr='Éviter les risques', de='Risiken vermeiden', ja='リスクを避ける'),
    risk_10=dict(en='Prepared to take risks', fr='Prêt à prendre des risques', de='Risikobereit', ja='リスクを冒す'),
    q_pat=dict(
        en='How do you see yourself: are you generally an impatient person, or someone who always shows great patience?',
        fr='Comment vous voyez-vous : êtes-vous généralement une personne impatiente ou quelqu\'un qui fait toujours preuve d\'une grande patience ?',
        de='Wie sehen Sie sich selbst: Sind Sie im Allgemeinen ein ungeduldiger Mensch oder jemand, der immer große Geduld zeigt?',
        ja='ご自身をどのように評価しますか：あなたは一般的にせっかちな人ですか、それとも常に忍耐強い人ですか？'
    ),
    pat_0=dict(en='Very impatient', fr='Très impatient', de='Sehr ungeduldig', ja='非常にせっかち'),
    pat_10=dict(en='Very patient', fr='Très patient', de='Sehr geduldig', ja='非常に忍耐強い'),
    q_strat=dict(
        en='Briefly, how did you make your decisions in the lottery task?',
        fr='Brièvement, comment avez-vous pris vos décisions dans la tâche de loterie ?',
        de='Kurz gesagt, wie haben Sie Ihre Entscheidungen in der Lotterieaufgabe getroffen?',
        ja='くじの課題でどのように決定を下したか、簡単に説明してください。'
    ),
    end_title=dict(en='Experiment Completed', fr='Expérience terminée', de='Experiment beendet', ja='実験終了'),
    end_msg=dict(
        en='Thank you for participating! You may now close this window.',
        fr='Merci de votre participation ! Vous pouvez maintenant fermer cette fenêtre.',
        de='Vielen Dank für Ihre Teilnahme! Sie können dieses Fenster jetzt schließen.',
        ja='ご参加ありがとうございました！このウィンドウを閉じてください。'
    )
)


def ui_dict(lang):
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ═══════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════

def _ctx(player, progress):
    """Context helper providing mandatory 'lang' and 'progress' variables."""
    return dict(
        lang=player.language,
        ui=ui_dict(player.language),
        progress=progress
    )


class Task3Intro(Page):
    @staticmethod
    def vars_for_template(player):
        player.language = player.session.config.get('language', 'en')
        return _ctx(player, 99)  # Progress from Task 2 (98%)


class LossAversionTask(Page):
    form_model = 'player'
    form_fields = ['la_switching_point']

    @staticmethod
    def vars_for_template(player):
        return dict(rows=C.LOTTERIES, **_ctx(player, 99))

    @staticmethod
    def before_next_page(player, timeout_happened):
        # 1. Select random row to play out
        selected_row = random.randint(1, 12)
        player.la_selected_row = selected_row

        # 2. Determine Choice based on Switching Point
        if selected_row < player.la_switching_point:
            player.la_choice = "A"
        else:
            player.la_choice = "B"

        # 3. Calculate Payoff (Gain is fixed at 10)
        gain = 10
        loss = selected_row

        if player.la_choice == "B":
            player.la_payoff = 0
            player.la_coin_flip = "N/A"
        else:
            if random.random() < 0.5:
                player.la_payoff = gain
                player.la_coin_flip = "Win"
            else:
                player.la_payoff = -loss
                player.la_coin_flip = "Loss"
        player.payoff += player.la_payoff


class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'native_language', 'risk_general', 'patience_general', 'strategy_comment']

    @staticmethod
    def vars_for_template(player):
        # Pass the range to the template to avoid complex template logic
        return dict(
            likert_range=C.LIKERT_RANGE,
            **_ctx(player, 100)
        )


class FinalThankYou(Page):
    @staticmethod
    def vars_for_template(player):
        return _ctx(player, 100)


page_sequence = [
    Task3Intro,
    LossAversionTask,
    Survey,
    FinalThankYou
]