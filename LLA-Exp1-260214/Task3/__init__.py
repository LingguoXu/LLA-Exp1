from otree.api import *
import random
import json

doc = """
Task 3: Loss Aversion Elicitation (Gächter et al. MPL + Bisection method) & Post-Experiment Survey.
Languages: English (en), French (fr), German (de), Japanese (ja).
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # --- MPL (original method) ---
    # 12-row structure from source: Win 10, Lose 1-12
    LOTTERIES = [dict(id=i, gain=10, loss=i) for i in range(1, 13)]

    # --- BISECTION (new method) ---
    # Gamble: 50% win GAIN_ECU, 50% lose X ECU
    # Sure option: 0 ECU (reject gamble)
    # Bisection narrows X over BISECTION_STEPS, then slider pins exact indifference point
    GAIN_ECU = 10          # fixed gain side of the gamble
    X_MIN = 1.0            # minimum possible loss in gamble (ECU)
    X_MAX = 20.0           # maximum possible loss in gamble (ECU)
    BISECTION_STEPS = 5    # number of binary choices before slider

    # Range for Risk/Patience Likert scales (0-10)
    LIKERT_RANGE = list(range(11))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    language = models.StringField(initial='en')

    # --- MPL FIELDS (original method, kept intact) ---
    la_switching_point = models.IntegerField(min=1, max=13)  # 13 means always chose A
    la_selected_row = models.IntegerField()
    la_choice = models.StringField()
    la_coin_flip = models.StringField()
    la_payoff = models.CurrencyField()

    # --- BISECTION FIELDS (new method) ---
    la2_indifference_x = models.FloatField(
        doc="Indifference loss amount (ECU) elicited via bisection + slider",
        min=0, max=30, blank=True
    )
    la2_bisection_data = models.LongStringField(
        doc="JSON array recording each bisection step: step, x_shown, choice",
        blank=True
    )

    # --- SURVEY FIELDS ---
    age = models.IntegerField(min=18, max=100)
    gender = models.StringField()
    native_language = models.StringField()
    risk_general = models.IntegerField(min=0, max=10)
    patience_general = models.IntegerField(min=0, max=10)
    strategy_comment = models.LongStringField(blank=True)


# ══════════════════════════════════════════════════════════════
# UI TRANSLATIONS
# ══════════════════════════════════════════════════════════════
UI = dict(
    btn_next=dict(en='Next', fr='Suivant', de='Weiter', ja='次へ'),
    btn_submit=dict(en='Submit Decisions', fr='Soumettre', de='Entscheidungen absenden', ja='決定を送信'),
    intro_title=dict(en='Part 3: Decision Making', fr='Partie 3: Prise de décision', de='Teil 3: Entscheidungsfindung', ja='パート3: 意思決定'),
    intro_text=dict(
        en='In this final task, you will make a series of decisions involving potential gains and losses.',
        fr='Dans cette dernière tâche, vous prendrez une série de décisions impliquant des gains et des pertes.',
        de='In dieser letzten Aufgabe treffen Sie eine Reihe von Entscheidungen mit Gewinnen und Verlusten.',
        ja='この最後の課題では、潜在的な利益と損失を含む一連の意思決定を行います。'
    ),

    # --- MPL labels ---
    la_alert_head=dict(en='How it works:', fr='Comment ça marche :', de='So funktioniert es:', ja='仕組み:'),
    la_alert_text=dict(
        en='If you switch from Option A to Option B in one row, the computer will automatically select Option A for all rows above it and Option B for all rows below it. You only need to click once to set your "switching point."',
        fr='Si vous passez de l\'option A à l\'option B sur une ligne, l\'ordinateur sélectionnera automatiquement l\'option A pour toutes les lignes situées au-dessus et l\'option B pour toutes les lignes situées en dessous.',
        de='Wenn Sie in einer Zeile von Option A zu Option B wechseln, wählt der Computer automatisch Option A für alle darüber liegenden Zeilen und Option B für alle darunter liegenden Zeilen.',
        ja='ある行で選択肢Aから選択肢Bに切り替えると、それより上のすべての行で選択肢Aが、それより下のすべての行で選択肢Bが自動的に選択されます。「切り替えポイント」を設定するには、一度クリックするだけです。'
    ),
    la_inst=dict(en='Please make a choice for each of the 12 rows below.', ja='以下の12の行それぞれについて選択してください。'),
    opt_a=dict(en='Option A: Lottery', ja='選択肢A: くじ'),
    opt_b=dict(en='Option B: Sure Amount', ja='選択肢B: 確実な金額'),
    win=dict(en='Win', ja='獲得'),
    lose=dict(en='Lose', ja='損失'),
    reject=dict(en='Get 0 ECU for sure', ja='確実に 0 ECU を得る'),
    error_sel=dict(en='Please make a selection before submitting.', ja='送信する前に選択してください。'),

    # --- Bisection page labels ---
    la2_title=dict(
        en='Part 3B: Lottery Decisions (Alternative Method)',
        fr='Partie 3B: Décisions de loterie (méthode alternative)',
        de='Teil 3B: Lotterie-Entscheidungen (alternative Methode)',
        ja='パート3B: くじの決定（別の方法）'
    ),
    la2_intro=dict(
        en='You will now make a series of choices between a <strong>lottery</strong> and a <strong>sure amount of 0 ECU</strong>. The lottery always gives you a 50% chance to <strong>win {gain} ECU</strong>. The loss amount varies across choices. Your task is to find the loss amount that makes you indifferent between the two options.',
        fr='Vous allez maintenant faire une série de choix entre une <strong>loterie</strong> et un <strong>montant certain de 0 ECU</strong>. La loterie vous donne toujours 50% de chance de <strong>gagner {gain} ECU</strong>. Le montant de la perte varie selon les choix. Votre tâche est de trouver le montant de la perte qui vous rend indifférent entre les deux options.',
        de='Sie treffen nun eine Reihe von Entscheidungen zwischen einer <strong>Lotterie</strong> und einem <strong>sicheren Betrag von 0 ECU</strong>. Die Lotterie bietet immer eine 50%-Chance, <strong>{gain} ECU zu gewinnen</strong>. Der Verlustbetrag variiert. Ihre Aufgabe ist es, den Verlustbetrag zu finden, bei dem Sie zwischen beiden Optionen gleichgültig sind.',
        ja='これから、<strong>くじ</strong>と<strong>確実に0 ECU</strong>の間で一連の選択を行います。くじは常に50%の確率で<strong>{gain} ECUを獲得</strong>できます。損失額は選択肢によって異なります。あなたの課題は、両方の選択肢の間で無差別になる損失額を見つけることです。'
    ),
    la2_step_label=dict(
        en='Comparison {current} of {total}',
        fr='Comparaison {current} sur {total}',
        de='Vergleich {current} von {total}',
        ja='比較 {current} / {total}'
    ),
    la2_question=dict(
        en='Which would you prefer?',
        fr='Que préféreriez-vous ?',
        de='Was würden Sie bevorzugen?',
        ja='どちらを選びますか？'
    ),
    la2_opt_lottery=dict(en='Take the Lottery', fr='Prendre la loterie', de='Lotterie nehmen', ja='くじを選ぶ'),
    la2_opt_sure=dict(en='Get 0 ECU for sure', fr='Obtenir 0 ECU à coup sûr', de='Sicher 0 ECU erhalten', ja='確実に0 ECUを得る'),
    la2_lottery_label=dict(en='Lottery', fr='Loterie', de='Lotterie', ja='くじ'),
    la2_sure_label=dict(en='Sure Amount', fr='Montant certain', de='Sicherer Betrag', ja='確実な金額'),
    la2_win_line=dict(
        en='50% chance: <strong>win {gain} ECU</strong>',
        fr='50% de chance: <strong>gagner {gain} ECU</strong>',
        de='50% Chance: <strong>{gain} ECU gewinnen</strong>',
        ja='50%の確率で：<strong>{gain} ECU 獲得</strong>'
    ),
    la2_lose_line=dict(
        en='50% chance: <strong>lose {x} ECU</strong>',
        fr='50% de chance: <strong>perdre {x} ECU</strong>',
        de='50% Chance: <strong>{x} ECU verlieren</strong>',
        ja='50%の確率で：<strong>{x} ECU 損失</strong>'
    ),
    la2_sure_line=dict(
        en='<strong>0 ECU</strong> (certain)',
        fr='<strong>0 ECU</strong> (certain)',
        de='<strong>0 ECU</strong> (sicher)',
        ja='<strong>0 ECU</strong>（確実）'
    ),
    la2_slider_title=dict(
        en='Fine-tune your indifference point',
        fr='Affinez votre point d\'indifférence',
        de='Verfeinern Sie Ihren Indifferenzpunkt',
        ja='無差別点を微調整する'
    ),
    la2_slider_intro=dict(
        en='Based on your choices, we\'ve narrowed down the loss to a small range. Use the slider to set the <strong>exact loss amount</strong> at which the lottery and the sure option feel equally attractive to you.',
        fr='Sur la base de vos choix, nous avons réduit la perte à une petite plage. Utilisez le curseur pour définir le <strong>montant de perte exact</strong> auquel la loterie et l\'option certaine vous semblent également attractives.',
        de='Basierend auf Ihren Entscheidungen haben wir den Verlust auf einen kleinen Bereich eingegrenzt. Verwenden Sie den Schieberegler, um den <strong>genauen Verlustbetrag</strong> einzustellen, bei dem Lotterie und sichere Option gleich attraktiv erscheinen.',
        ja='あなたの選択に基づいて、損失を狭い範囲に絞り込みました。スライダーを使って、くじと確実な選択肢が同等に魅力的に感じる<strong>正確な損失額</strong>を設定してください。'
    ),
    la2_slider_label_lose=dict(en='Lose', fr='Perdre', de='Verlieren', ja='損失'),
    la2_slider_label_ecu=dict(en='ECU', fr='ECU', de='ECU', ja='ECU'),
    la2_confirm=dict(
        en='When both options feel <strong>equally acceptable</strong>, click Confirm.',
        fr='Lorsque les deux options vous semblent <strong>également acceptables</strong>, cliquez sur Confirmer.',
        de='Wenn beide Optionen <strong>gleich akzeptabel</strong> erscheinen, klicken Sie auf Bestätigen.',
        ja='両方の選択肢が<strong>同等に受け入れられる</strong>と感じたら、確認をクリックしてください。'
    ),
    la2_btn_confirm=dict(en='Confirm', fr='Confirmer', de='Bestätigen', ja='確認'),
    la2_error=dict(
        en='Please complete all choices before submitting.',
        fr='Veuillez compléter tous les choix avant de soumettre.',
        de='Bitte treffen Sie alle Entscheidungen, bevor Sie absenden.',
        ja='送信前にすべての選択を完了してください。'
    ),

    # --- Survey labels ---
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


# ══════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════

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
        return _ctx(player, 99)


class LossAversionTask(Page):
    """Original MPL elicitation (Gächter et al. 12-row design)."""
    form_model = 'player'
    form_fields = ['la_switching_point']

    @staticmethod
    def vars_for_template(player):
        return dict(rows=C.LOTTERIES, **_ctx(player, 99))

    @staticmethod
    def before_next_page(player, timeout_happened):
        selected_row = random.randint(1, 12)
        player.la_selected_row = selected_row

        if selected_row < player.la_switching_point:
            player.la_choice = "A"
        else:
            player.la_choice = "B"

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


class LossAversionBisection(Page):
    """
    Alternative LA elicitation using bisection + slider.
    Gamble: 50% win GAIN_ECU, 50% lose X ECU  vs.  Sure: 0 ECU.
    Binary choices narrow X over BISECTION_STEPS, then slider pins exact indifference point.
    Reference: Abdellaoui et al. (2007, Management Science).
    """
    form_model = 'player'
    form_fields = ['la2_indifference_x', 'la2_bisection_data']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        gain = C.GAIN_ECU
        x_init = (C.X_MIN + C.X_MAX) / 2

        ui = ui_dict(lang)

        # Pre-format strings that need Python variable substitution
        ui['la2_win_line_fmt']   = ui['la2_win_line'].format(gain=gain)
        ui['la2_lose_line_init'] = ui['la2_lose_line'].format(x=round(x_init, 1))

        return dict(
            lang=lang,
            ui=ui,
            progress=99,
            gain=gain,
            x_min=C.X_MIN,
            x_max=C.X_MAX,
            bisection_steps=C.BISECTION_STEPS,
            steps_range=list(range(1, C.BISECTION_STEPS + 1)),
            la2_intro_formatted=ui['la2_intro'].format(gain=gain),
            step_label_1=ui['la2_step_label'].format(current=1, total=C.BISECTION_STEPS),
        )


class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'native_language', 'risk_general', 'patience_general', 'strategy_comment']

    @staticmethod
    def vars_for_template(player):
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
    LossAversionTask,          # Original MPL method (kept intact)
    LossAversionBisection,     # New bisection + slider method
    Survey,
    FinalThankYou
]