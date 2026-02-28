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

    # ── ECU exchange rate (per language / recruitment locale) ────────────
    # Calibrated so 500 ECU (TD task maximum) ≈ local €1.50 equivalent.
    # French = EUR (France/Belgium). Update to CAD if recruiting Quebec francophones.
    ECU_RATES = dict(
        en=dict(rate=0.003, currency='USD', symbol='$',  example='100 ECU = $0.30'),
        fr=dict(rate=0.003, currency='EUR', symbol='€',  example='100 ECU = €0.30'),
        de=dict(rate=0.003, currency='EUR', symbol='€',  example='100 ECU = €0.30'),
        ja=dict(rate=0.45,  currency='JPY', symbol='¥',  example='100 ECU = ¥45'),
    )

    # Range for Risk/Patience Likert scales (0-10)
    LIKERT_RANGE = list(range(11))

    # ── Temporal Discounting MPL ──────────────────────────────────────────
    # Three-horizon MPL with single-switching enforcement.
    # Horizons deliberately match the FTR temporal distances: 1 month, 6 months, 2 years.
    # Front-end delay: sooner option is always "in 2 weeks" (not "today") to control
    # for immediacy/present bias and payment-trust confounds (Coller & Williams 1999).
    # Amounts calibrated using hyperbolic model V = A/(1+kT), SS = 100 ECU:
    #   1-month  horizon: k = 0 … 12  (annual)
    #   6-month  horizon: k = 0 … 4
    #   2-year   horizon: k = 0 … 2
    TD_SOONER_ECU = 100   # fixed sooner-option amount

    TD_HORIZONS = [
        dict(
            id='1mo',
            delay_days=30,
            rows=[
                dict(row=1, sooner=100, later=100),   # k=0
                dict(row=2, sooner=100, later=108),   # k=1
                dict(row=3, sooner=100, later=117),   # k=2
                dict(row=4, sooner=100, later=125),   # k=3
                dict(row=5, sooner=100, later=133),   # k=4
                dict(row=6, sooner=100, later=150),   # k=6
                dict(row=7, sooner=100, later=200),   # k=12
            ],
            label       =dict(en='1 Month',   fr='1 mois',      de='1 Monat',    ja='1ヶ月'),
            sooner_label=dict(en='in 2 weeks', fr='dans 2 sem.', de='in 2 Wo.',   ja='2週間後'),
            later_label =dict(en='in 6 weeks', fr='dans 6 sem.', de='in 6 Wo.',   ja='6週間後'),
        ),
        dict(
            id='6mo',
            delay_days=180,
            rows=[
                dict(row=1, sooner=100, later=100),   # k=0
                dict(row=2, sooner=100, later=125),   # k=0.5
                dict(row=3, sooner=100, later=150),   # k=1
                dict(row=4, sooner=100, later=175),   # k=1.5
                dict(row=5, sooner=100, later=200),   # k=2
                dict(row=6, sooner=100, later=250),   # k=3
                dict(row=7, sooner=100, later=300),   # k=4
            ],
            label       =dict(en='6 Months',       fr='6 mois',       de='6 Monate',       ja='6ヶ月'),
            sooner_label=dict(en='in 2 weeks',     fr='dans 2 sem.',   de='in 2 Wo.',       ja='2週間後'),
            later_label =dict(en='in ~6.5 months', fr='dans ~6,5 mo.', de='in ~6,5 Mon.',   ja='約6.5ヶ月後'),
        ),
        dict(
            id='2yr',
            delay_days=730,
            rows=[
                dict(row=1, sooner=100, later=100),   # k=0
                dict(row=2, sooner=100, later=150),   # k=0.25
                dict(row=3, sooner=100, later=200),   # k=0.5
                dict(row=4, sooner=100, later=250),   # k=0.75
                dict(row=5, sooner=100, later=300),   # k=1.0
                dict(row=6, sooner=100, later=400),   # k=1.5
                dict(row=7, sooner=100, later=500),   # k=2.0
            ],
            label       =dict(en='2 Years',     fr='2 ans',        de='2 Jahre',       ja='2年'),
            sooner_label=dict(en='in 2 weeks',  fr='dans 2 sem.',   de='in 2 Wo.',      ja='2週間後'),
            later_label =dict(en='in ~2 years', fr='dans ~2 ans',   de='in ~2 Jahren',  ja='約2年後'),
        ),
    ]


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

    # --- TEMPORAL DISCOUNTING FIELDS ---
    td_switching_1mo = models.IntegerField(min=1, max=8, blank=True)
    td_switching_6mo = models.IntegerField(min=1, max=8, blank=True)
    td_switching_2yr = models.IntegerField(min=1, max=8, blank=True)
    td_data             = models.LongStringField(blank=True)
    td_selected_horizon = models.StringField(blank=True)
    td_selected_row     = models.IntegerField(blank=True)
    td_choice           = models.StringField(blank=True)

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
        en=(
            'In this final part, you will make a series of decisions involving potential gains and losses. '
            'Amounts are expressed in <strong>ECU (Experimental Currency Units)</strong>, the in-study currency. '
            'At the end of the study, <strong>one of your decisions will be selected at random</strong> '
            'and paid out to you at the exchange rate shown below, in addition to your participation fee.'
        ),
        fr=(
            'Dans cette dernière partie, vous prendrez une série de décisions impliquant des gains et des pertes potentiels. '
            'Les montants sont exprimés en <strong>ECU (Experimental Currency Units)</strong>, la monnaie de cette étude. '
            'À la fin de l\'étude, <strong>une de vos décisions sera sélectionnée au hasard</strong> '
            'et vous sera payée au taux de change indiqué ci-dessous, en plus de votre indemnité de participation.'
        ),
        de=(
            'In diesem letzten Teil treffen Sie eine Reihe von Entscheidungen mit potenziellen Gewinnen und Verlusten. '
            'Beträge werden in <strong>ECU (Experimental Currency Units)</strong> angegeben, der Währung dieser Studie. '
            'Am Ende der Studie wird <strong>eine Ihrer Entscheidungen zufällig ausgewählt</strong> '
            'und Ihnen zum unten angegebenen Kurs ausgezahlt, zusätzlich zu Ihrer Teilnahmevergütung.'
        ),
        ja=(
            'この最終パートでは、潜在的な利益と損失を含む一連の意思決定を行います。'
            '金額は本研究で使用する通貨<strong>ECU（Experimental Currency Units）</strong>で表示されます。'
            '研究終了後、<strong>あなたの意思決定の中から1つがランダムに選ばれ</strong>、'
            '以下に示す交換レートで実際に支払われます（参加報酬に加算）。'
        ),
    ),


    # --- MPL labels ---
    la_alert_head=dict(en='How it works:', fr='Comment ça marche :', de='So funktioniert es:', ja='仕組み:'),
    la_alert_text=dict(
        en=(
            '<strong>Option A</strong> is a lottery: a 50% chance to <strong>win 10 ECU</strong> and a 50% chance to <strong>lose X ECU</strong>, where X increases with each row. '
            '<strong>Option B</strong> is to receive <strong>0 ECU for certain</strong> (you reject the lottery). '
            'Most people start by preferring Option A when the potential loss is small, then switch to Option B as the loss grows. '
            'You should switch <em>at most once</em>. Click any row to set your switch point — the table updates automatically.'
        ),
        fr=(
            '<strong>L\'option A</strong> est un tirage au sort : 50 % de chances de <strong>gagner 10 ECU</strong> et 50 % de chances de <strong>perdre X ECU</strong>, X augmentant à chaque ligne. '
            '<strong>L\'option B</strong> consiste à recevoir <strong>0 ECU de façon certaine</strong> (vous refusez le tirage au sort). '
            'La plupart des gens préfèrent d\'abord l\'option A quand la perte est faible, puis basculent vers l\'option B quand elle augmente. '
            'Vous ne devez basculer <em>qu\'une seule fois au maximum</em>. Cliquez sur n\'importe quelle ligne pour définir votre point de bascule — le tableau se met à jour automatiquement.'
        ),
        de=(
            '<strong>Option A</strong> ist eine Lotterie: 50 % Chance, <strong>10 ECU zu gewinnen</strong>, und 50 % Chance, <strong>X ECU zu verlieren</strong>, wobei X mit jeder Zeile steigt. '
            '<strong>Option B</strong> bedeutet, <strong>sicher 0 ECU</strong> zu erhalten (Sie lehnen die Lotterie ab). '
            'Die meisten Menschen bevorzugen zunächst Option A, wenn der mögliche Verlust gering ist, und wechseln zu Option B, wenn er größer wird. '
            'Sie sollten <em>höchstens einmal wechseln</em>. Klicken Sie auf eine beliebige Zeile — die Tabelle aktualisiert sich automatisch.'
        ),
        ja=(
            '<strong>選択肢A</strong>はくじです：50%の確率で<strong>10 ECUを獲得</strong>し、50%の確率で<strong>X ECUを失います</strong>（Xは行ごとに増加）。'
            '<strong>選択肢B</strong>は<strong>確実に0 ECU</strong>を受け取ること（くじを断る）です。'
            'ほとんどの方は、損失が小さいうちは選択肢Aを好み、損失が大きくなるにつれて選択肢Bに切り替えます。'
            '切り替えは<em>最大1回</em>だけです。どの行をクリックしても切り替えポイントを設定でき、表は自動更新されます。'
        ),
    ),
    la_inst=dict(
        en='Each row presents the same choice with a different potential loss. Click once to set your switch point — the rest fills in automatically.',
        fr='Chaque ligne présente le même choix avec une perte potentielle différente. Cliquez une fois pour définir votre point de bascule — le reste se remplit automatiquement.',
        de='Jede Zeile zeigt dieselbe Entscheidung mit einem anderen möglichen Verlust. Klicken Sie einmal, um Ihren Wechselpunkt festzulegen — der Rest wird automatisch ausgefüllt.',
        ja='各行は損失額だけが異なる同じ選択を示しています。一度クリックすれば切り替えポイントが設定され、残りは自動的に入力されます。',
    ),
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
    ecu_box_head=dict(
        en='Payment Currency',
        fr='Monnaie de paiement',
        de='Zahlungswährung',
        ja='支払い通貨',
    ),
    ecu_box_note=dict(
        en='One decision will be selected at random and paid out at this rate, on top of your participation fee.',
        fr='Une décision sera sélectionnée au hasard et payée à ce taux, en plus de votre indemnité de participation.',
        de='Eine Entscheidung wird zufällig ausgewählt und zu diesem Kurs ausgezahlt, zusätzlich zu Ihrer Teilnahmevergütung.',
        ja='1つの意思決定がランダムに選ばれ、このレートで支払われます（参加報酬に加算）。',
    ),

    # --- Temporal Discounting labels ---
    td_title=dict(
        en='Part 3C: Time Preferences',
        fr='Partie 3C : Préférences temporelles',
        de='Teil 3C: Zeitpräferenzen',
        ja='パート3C：時間的選好',
    ),
    td_intro=dict(
        en=(
            'You will now make a series of choices between two payment options. '
            'One option pays a <strong>smaller amount sooner</strong>; '
            'the other pays a <strong>larger amount later</strong>. '
            'There are no right or wrong answers — we simply want to know your genuine preference. '
            '<strong>One of your choices will be selected at random and paid out.</strong>'
        ),
        fr=(
            'Vous allez maintenant faire une série de choix entre deux options de paiement. '
            'Une option verse un <strong>montant plus faible plus tôt</strong> ; '
            "l'autre verse un <strong>montant plus élevé plus tard</strong>. "
            "Il n'y a pas de bonnes ou de mauvaises réponses — nous voulons simplement connaître vos préférences réelles. "
            '<strong>Un de vos choix sera sélectionné au hasard et payé.</strong>'
        ),
        de=(
            'Sie treffen nun eine Reihe von Entscheidungen zwischen zwei Zahlungsoptionen. '
            'Eine Option zahlt einen <strong>kleineren Betrag früher</strong>; '
            'die andere zahlt einen <strong>größeren Betrag später</strong>. '
            'Es gibt keine richtigen oder falschen Antworten — wir möchten nur Ihre ehrliche Präferenz kennen. '
            '<strong>Eine Ihrer Entscheidungen wird zufällig ausgewählt und ausgezahlt.</strong>'
        ),
        ja=(
            'これから、2つの支払いオプションの間で一連の選択を行います。'
            '一方は<strong>少額を早く</strong>受け取るオプション、'
            'もう一方は<strong>多額を後で</strong>受け取るオプションです。'
            '正解・不正解はありません。あなたの正直な好みを教えてください。'
            '<strong>あなたの選択のうち1つがランダムに選ばれ、実際に支払われます。</strong>'
        ),
    ),
    td_alert=dict(
        en=(
            '<strong>How it works:</strong> Each row offers the same sooner amount but a higher later amount. '
            'Once you prefer the sooner option on a row, you will prefer it on all rows above too — '
            'click once to set your switch point and the table updates automatically.'
        ),
        fr=(
            '<strong>Comment ça marche :</strong> Chaque ligne propose le même montant précoce mais un montant tardif plus élevé. '
            "Une fois que vous préférez l'option précoce sur une ligne, vous la préférerez aussi sur toutes les lignes supérieures — "
            'cliquez une fois pour définir votre point de bascule, le tableau se met à jour automatiquement.'
        ),
        de=(
            '<strong>So funktioniert es:</strong> Jede Zeile bietet denselben früheren Betrag, aber einen höheren späteren Betrag. '
            'Wenn Sie in einer Zeile die frühere Option bevorzugen, tun Sie dies auch in allen darüber liegenden — '
            'klicken Sie einmal, um Ihren Wechselpunkt festzulegen, die Tabelle aktualisiert sich automatisch.'
        ),
        ja=(
            '<strong>仕組み：</strong>各行は同じ早期金額ですが、後期金額が高くなっています。'
            'ある行で早期オプションを選ぶなら、それより上の全ての行でも早期を選ぶはずです。'
            '一度クリックして切り替えポイントを設定すると、テーブルが自動更新されます。'
        ),
    ),
    td_col_sooner=dict(
        en='Option A — Sooner', fr='Option A — Plus tôt',
        de='Option A — Früher', ja='選択肢A — 早く',
    ),
    td_col_later=dict(
        en='Option B — Later',  fr='Option B — Plus tard',
        de='Option B — Später', ja='選択肢B — 後で',
    ),
    td_btn_next_horizon=dict(
        en='Continue to next horizon →',
        fr="Continuer vers l'horizon suivant →",
        de='Weiter zum nächsten Horizont →',
        ja='次のホライズンへ →',
    ),
    td_btn_submit=dict(
        en='Submit Decisions →',
        fr='Soumettre les décisions →',
        de='Entscheidungen absenden →',
        ja='決定を送信 →',
    ),
    td_error=dict(
        en='Please make a choice in each row before continuing.',
        fr='Veuillez faire un choix dans chaque ligne avant de continuer.',
        de='Bitte treffen Sie in jeder Zeile eine Auswahl, bevor Sie fortfahren.',
        ja='続ける前に各行で選択してください。',
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
        lang = player.language
        ecu = C.ECU_RATES.get(lang, C.ECU_RATES['en'])
        return dict(
            ecu_rate    = ecu['rate'],
            ecu_symbol  = ecu['symbol'],
            ecu_currency= ecu['currency'],
            ecu_example = ecu['example'],
            **_ctx(player, 99),
        )


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


class TemporalDiscounting(Page):
    """
    Intertemporal choice MPL — 3 horizons (1 month / 6 months / 2 years).
    Horizons match the FTR temporal distances used in Tasks 1 & 2, enabling
    direct correlation between habitual FTR encoding and discount rates.
    Front-end delay: sooner option = 'in 2 weeks' throughout, to control for
    immediacy bias and payment-trust confounds (Coller & Williams 1999).
    Single-switching enforced: one click sets the entire column pattern.
    Incentive compatible: one randomly selected row is paid out.
    """
    form_model  = 'player'
    form_fields = ['td_switching_1mo', 'td_switching_6mo', 'td_switching_2yr', 'td_data']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        ui   = ui_dict(lang)

        horizons_localised = []
        for h in C.TD_HORIZONS:
            horizons_localised.append(dict(
                id           = h['id'],
                rows         = h['rows'],
                label        = h['label'].get(lang, h['label']['en']),
                sooner_label = h['sooner_label'].get(lang, h['sooner_label']['en']),
                later_label  = h['later_label'].get(lang,  h['later_label']['en']),
            ))

        return dict(
            horizons   = horizons_localised,
            n_horizons = len(C.TD_HORIZONS),
            sooner_ecu = C.TD_SOONER_ECU,
            **_ctx(player, 99),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        """Randomly select one row for incentive-compatible payment."""
        horizon = random.choice(C.TD_HORIZONS)
        row     = random.choice(horizon['rows'])

        player.td_selected_horizon = horizon['id']
        player.td_selected_row     = row['row']

        sp_map = {
            '1mo': player.td_switching_1mo or 8,
            '6mo': player.td_switching_6mo or 8,
            '2yr': player.td_switching_2yr or 8,
        }
        sp = sp_map[horizon['id']]
        player.td_choice = 'sooner' if row['row'] >= sp else 'later'


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
    LossAversionBisection,     # Bisection + slider (Abdellaoui et al. 2007)
    TemporalDiscounting,       # 3-horizon intertemporal choice MPL (Coller & Williams 1999)
    Survey,
    FinalThankYou,
]