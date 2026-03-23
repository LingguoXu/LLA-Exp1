from otree.api import *
import random
import json
import math

doc = """
Task 3: Loss Aversion Elicitation (Gächter et al. MPL + Bisection method) & Post-Experiment Survey.
Languages: English (en), French (fr), German (de), Japanese (ja), Chinese (zh).
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # --- MPL (original method) ---
    LOTTERIES = [dict(id=i, gain=10, loss=i) for i in range(1, 13)]

    # --- BISECTION (new method) ---
    GAIN_BASE = 10  # base gain (×rate for currency)
    X_MIN = 1.0
    X_MAX = 20.0
    BISECTION_STEPS = 5

    # ── LA Incentive ──────────────────────
    LA_ENDOWMENT_BASE = 20  # base endowment (×rate for currency)
    COMP_EXAMPLE_LOSS_BASE = 6  # example loss for comprehension check (×rate)

    # ── Currency per language ────────────
    CURRENCY = dict(
        en=dict(rate=0.50, symbol='£', code='GBP', decimals=2),
        fr=dict(rate=0.50, symbol='€', code='EUR', decimals=2),
        de=dict(rate=0.50, symbol='€', code='EUR', decimals=2),
        ja=dict(rate=75.0, symbol='¥', code='JPY', decimals=0),
        zh=dict(rate=3.50, symbol='¥', code='CNY', decimals=0),
    )

    LIKERT_RANGE = list(range(11))

    # ── Temporal Discounting MPL ──────────────────────────────────────────
    TD_SOONER_BASE = 100  # base sooner amount (×rate for currency)

    TD_HORIZONS = [
        dict(
            id='1mo',
            delay_days=30,
            rows=[
                dict(row=1, sooner=100, later=100),  # k=0
                dict(row=2, sooner=100, later=108),  # k=1
                dict(row=3, sooner=100, later=117),  # k=2
                dict(row=4, sooner=100, later=125),  # k=3
                dict(row=5, sooner=100, later=133),  # k=4
                dict(row=6, sooner=100, later=150),  # k=6
                dict(row=7, sooner=100, later=200),  # k=12
            ],
            k_values=[0, 1, 2, 3, 4, 6, 12],
            label=dict(en='1-Month Gap', fr='Écart de 1 mois', de='1 Monat Abstand', ja='1ヶ月の差', zh='间隔1个月'),
            sooner_label=dict(en='in 2 weeks', fr='dans 2 sem.', de='in 2 Wo.', ja='2週間後', zh='2周后'),
            later_label=dict(en='in 6 weeks', fr='dans 6 sem.', de='in 6 Wo.', ja='6週間後', zh='6周后'),
        ),
        dict(
            id='6mo',
            delay_days=180,
            rows=[
                dict(row=1, sooner=100, later=100),  # k=0
                dict(row=2, sooner=100, later=125),  # k=0.5
                dict(row=3, sooner=100, later=150),  # k=1
                dict(row=4, sooner=100, later=175),  # k=1.5
                dict(row=5, sooner=100, later=200),  # k=2
                dict(row=6, sooner=100, later=250),  # k=3
                dict(row=7, sooner=100, later=300),  # k=4
            ],
            k_values=[0, 0.5, 1, 1.5, 2, 3, 4],
            label=dict(en='6-Month Gap', fr='Écart de 6 mois', de='6 Monate Abstand', ja='6ヶ月の差', zh='间隔6个月'),
            sooner_label=dict(en='in 2 weeks', fr='dans 2 sem.', de='in 2 Wo.', ja='2週間後', zh='2周后'),
            later_label=dict(en='in 6.5 months', fr='dans 6,5 mo.', de='in 6,5 Mon.', ja='約6.5ヶ月後', zh='约6.5个月后'),
        ),
        dict(
            id='2yr',
            delay_days=730,
            rows=[
                dict(row=1, sooner=100, later=100),  # k=0
                dict(row=2, sooner=100, later=150),  # k=0.25
                dict(row=3, sooner=100, later=200),  # k=0.5
                dict(row=4, sooner=100, later=250),  # k=0.75
                dict(row=5, sooner=100, later=300),  # k=1.0
                dict(row=6, sooner=100, later=400),  # k=1.5
                dict(row=7, sooner=100, later=500),  # k=2.0
            ],
            k_values=[0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
            label=dict(en='2-Year Gap', fr='Écart de 2 ans', de='2 Jahre Abstand', ja='2年の差', zh='间隔2年'),
            sooner_label=dict(en='in 2 weeks', fr='dans 2 sem.', de='in 2 Wo.', ja='2週間後', zh='2周后'),
            later_label=dict(en='in 2 years', fr='dans 2 ans', de='in 2 Jahren', ja='約2年後', zh='约2年后'),
        ),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    language = models.StringField(initial='en')

    # --- MPL FIELDS ---
    la_switching_point = models.IntegerField(min=1, max=13)
    la_selected_row = models.IntegerField()
    la_choice = models.StringField()
    la_coin_flip = models.StringField()
    la_payoff = models.CurrencyField()

    # --- BISECTION FIELDS ---
    la2_indifference_x = models.FloatField(blank=True)
    la2_bisection_data = models.LongStringField(blank=True)
    la2_endowment = models.FloatField(blank=True)
    la2_selected_step = models.IntegerField(blank=True)
    la2_selected_x = models.FloatField(blank=True)
    la2_selected_choice = models.StringField(blank=True)
    la2_coin_flip = models.StringField(blank=True)
    la2_bonus = models.FloatField(blank=True)
    la2_lambda = models.FloatField(blank=True)

    # --- ANTICIPATION (pre-outcome) ---
    la2_anticipation_worry = models.IntegerField(min=1, max=9, blank=True)
    la2_anticipation_prob = models.IntegerField(min=0, max=100, blank=True)

    # --- BONUS CONTACT ---
    bonus_contact_email = models.StringField(blank=True)

    # --- COMPREHENSION CHECK ---
    comp_q1_attempts = models.IntegerField(initial=0, blank=True)
    comp_q2_attempts = models.IntegerField(initial=0, blank=True)
    comp_q3_attempts = models.IntegerField(initial=0, blank=True)

    # --- TEMPORAL DISCOUNTING FIELDS ---
    td_switching_1mo = models.IntegerField(min=1, max=8, blank=True)
    td_switching_6mo = models.IntegerField(min=1, max=8, blank=True)
    td_switching_2yr = models.IntegerField(min=1, max=8, blank=True)
    td_data = models.LongStringField(blank=True)
    td_selected_horizon = models.StringField(blank=True)
    td_selected_row = models.IntegerField(blank=True)
    td_k_1mo = models.FloatField(blank=True)
    td_k_6mo = models.FloatField(blank=True)
    td_k_2yr = models.FloatField(blank=True)
    td_k_geo_mean = models.FloatField(blank=True)
    td_choice = models.StringField(blank=True)

    # --- SURVEY FIELDS ---
    gender = models.StringField()
    home_country = models.StringField()
    years_in_country = models.IntegerField(min=0)
    employment_industry = models.StringField()
    income_level = models.StringField()
    risk_general = models.IntegerField(min=0, max=10)
    patience_general = models.IntegerField(min=0, max=10)
    study_feedback = models.LongStringField(blank=True)


# ══════════════════════════════════════════════════════════════
# UI TRANSLATIONS
# ══════════════════════════════════════════════════════════════
UI = dict(
    btn_next=dict(en='Next', fr='Suivant', de='Weiter', ja='次へ', zh='下一步'),
    btn_submit=dict(en='Submit Decisions', fr='Soumettre', de='Entscheidungen absenden', ja='決定を送信', zh='提交决定'),
    intro_title=dict(en='Part 3: Decision Making', fr='Partie 3: Prise de décision', de='Teil 3: Entscheidungsfindung',
                     ja='パート3: 意思決定', zh='第三部分：决策'),
    intro_text=dict(
        en=(
            'In this final part, you will choose between lotteries and safe options.'
            '<br><br>'
            'You start with a bonus balance of <strong>{symbol}{endowment}</strong>. '
            'In each round you pick either a <strong>lottery</strong> (a coin flip that can increase or decrease your balance) or a <strong>safe option</strong> (keep your balance unchanged). '
            'At the end, <strong>one round is selected at random and played out for real</strong>.'
            '<br><br>'
            'Please decide as if every choice is real.'
        ),
        fr=(
            'Dans cette dernière partie, vous choisirez entre des loteries et des options sûres impliquant des gains et des pertes potentiels.'
            '<br><br>'
            'Vous commencez avec un solde bonus de <strong>{symbol}{endowment}</strong>. '
            'À chaque tour, vous choisissez soit une <strong>loterie</strong> (un tirage au sort qui peut augmenter ou diminuer votre solde), soit une <strong>option sûre</strong> (conserver votre solde inchangé). '
            'À la fin, <strong>un tour est sélectionné au hasard et joué pour de vrai</strong>.'
            '<br><br>'
            '1 participant sur 10 sera sélectionné au hasard pour recevoir son bonus <strong>via Prolific</strong>. '
            'Veuillez décider comme si chaque choix était réel.'
        ),
        de=(
            'In diesem letzten Teil wählen Sie zwischen Lotterien und sicheren Optionen mit möglichen Gewinnen und Verlusten.'
            '<br><br>'
            'Sie starten mit einem Bonusguthaben von <strong>{symbol}{endowment}</strong>. '
            'In jeder Runde wählen Sie entweder eine <strong>Lotterie</strong> (ein Münzwurf, der Ihr Guthaben erhöhen oder verringern kann) oder eine <strong>sichere Option</strong> (Guthaben unverändert behalten). '
            'Am Ende wird <strong>eine Runde zufällig ausgewählt und tatsächlich ausgespielt</strong>.'
            '<br><br>'
            '1 von 10 Teilnehmenden wird zufällig ausgewählt, um den Bonus <strong>über Prolific</strong> zu erhalten. '
            'Bitte entscheiden Sie so, als ob jede Wahl real wäre.'
        ),
        ja=(
            'この最終パートでは、利益と損失を含むくじと安全な選択肢のどちらかを選びます。'
            '<br><br>'
            'まず、ボーナス残高として<strong>{symbol}{endowment}</strong>が支給されます。'
            '各ラウンドで<strong>くじ</strong>（コイン投げで残高が増減する）か<strong>安全な選択肢</strong>（残高をそのまま維持する）を選びます。'
            '最後に、<strong>1つのラウンドがランダムに選ばれ、実際に実行されます</strong>。'
            '<br><br>'
            '参加者の10人に1人がランダムに選ばれ、<strong>Prolificを通じて</strong>ボーナスが支払われます。'
            'すべての選択が実際のものであるかのようにお答えください。'
        ),
        zh=(
            '在最后这部分中，您将在涉及潜在收益和损失的抽奖与稳妥选项之间做出选择。'
            '<br><br>'
            '您的初始奖金余额为<strong>{symbol}{endowment}</strong>。'
            '每轮您可以选择<strong>抽奖</strong>（掷硬币决定余额增减）或<strong>稳妥选项</strong>（余额不变）。'
            '最后，<strong>系统将随机抽取一轮进行真实结算</strong>。'
            '<br><br>'
            '每10名参与者中将随机选出1名，<strong>通过Prolific</strong>发放奖金。'
            '请将每个选择都当作真实决定来对待。'
        ),
    ),
    la_alert_head=dict(en='How it works:', fr='Comment ça marche :', de='So funktioniert es:', ja='仕組み:', zh='规则说明：'),
    la_alert_text=dict(
        en=(
            '<strong>Option A</strong> is a lottery: a 50% chance to <strong>win {symbol}{gain}</strong> and a 50% chance to <strong>lose {symbol}X</strong>, where X increases with each row. '
            '<strong>Option B</strong> is to receive <strong>{symbol}0 for certain</strong> (you reject the lottery). '
            'Most people start by preferring Option A when the potential loss is small, then switch to Option B as the loss grows. '
            'You should switch <em>at most once</em>. Click any row to set your switch point — the table updates automatically.'
        ),
        fr=(
            '<strong>L\'option A</strong> est un tirage au sort : 50 % de chances de <strong>gagner {symbol}{gain}</strong> et 50 % de chances de <strong>perdre {symbol}X</strong>, X augmentant à chaque ligne. '
            '<strong>L\'option B</strong> consiste à recevoir <strong>{symbol}0 de façon certaine</strong> (vous refusez le tirage au sort). '
            'La plupart des gens préfèrent d\'abord l\'option A quand la perte est faible, puis basculent vers l\'option B quand elle augmente. '
            'Vous ne devez basculer <em>qu\'une seule fois au maximum</em>. Cliquez sur n\'importe quelle ligne pour définir votre point de bascule — le tableau se met à jour automatiquement.'
        ),
        de=(
            '<strong>Option A</strong> ist eine Lotterie: 50 % Chance, <strong>{symbol}{gain} zu gewinnen</strong>, und 50 % Chance, <strong>{symbol}X zu verlieren</strong>, wobei X mit jeder Zeile steigt. '
            '<strong>Option B</strong> bedeutet, <strong>sicher {symbol}0</strong> zu erhalten (Sie lehnen die Lotterie ab). '
            'Die meisten Menschen bevorzugen zunächst Option A, wenn der mögliche Verlust gering ist, und wechseln zu Option B, wenn er größer wird. '
            'Sie sollten <em>höchstens einmal wechseln</em>. Klicken Sie auf eine beliebige Zeile — die Tabelle aktualisiert sich automatisch.'
        ),
        ja=(
            '<strong>選択肢A</strong>はくじです：50%の確率で<strong>{symbol}{gain}を獲得</strong>し、50%の確率で<strong>{symbol}Xを失います</strong>（Xは行ごとに増加）。'
            '<strong>選択肢B</strong>は<strong>確実に{symbol}0</strong>を受け取ること（くじを断る）です。'
            'ほとんどの方は、損失が小さいうちは選択肢Aを好み、損失が大きくなるにつれて選択肢Bに切り替えます。'
            '切り替えは<em>最大1回</em>だけです。どの行をクリックしても切り替えポイントを設定でき、表は自動更新されます。'
        ),
        zh=(
            '<strong>选项A</strong>是抽奖：50%的概率<strong>赢得{symbol}{gain}</strong>，50%的概率<strong>损失{symbol}X</strong>（X逐行递增）。'
            '<strong>选项B</strong>是<strong>确定获得{symbol}0</strong>（即放弃抽奖）。'
            '大多数人在潜在损失较小时倾向于选A，随着损失增大转而选B。'
            '您最多只能切换<em>一次</em>。点击任意一行即可设置切换点，表格会自动更新。'
        ),
    ),
    la_inst=dict(
        en='Each row presents the same choice with a different potential loss. Click once to set your switch point — the rest fills in automatically.',
        fr='Chaque ligne présente le même choix avec une perte potentielle différente. Cliquez une fois pour définir votre point de bascule — le reste se remplit automatiquement.',
        de='Jede Zeile zeigt dieselbe Entscheidung mit einem anderen möglichen Verlust. Klicken Sie einmal, um Ihren Wechselpunkt festzulegen — der Rest wird automatisch ausgefüllt.',
        ja='各行は損失額だけが異なる同じ選択を示しています。一度クリックすれば切り替えポイントが設定され、残りは自動的に入力されます。',
        zh='每行是同一选择，但潜在损失金额不同。点击一次即可设置切换点，其余自动填充。',
    ),
    opt_a=dict(en='Option A: Lottery', ja='選択肢A: くじ', zh='选项A：抽奖'),
    opt_b=dict(en='Option B: Sure Amount', ja='選択肢B: 確実な金額', zh='选项B：确定金额'),
    win=dict(en='Win', ja='獲得', zh='赢得'),
    lose=dict(en='Lose', ja='損失', zh='损失'),
    reject=dict(en='Get {symbol}0 for sure', ja='確実に {symbol}0 を得る', zh='确定获得 {symbol}0'),
    error_sel=dict(en='Please make a selection before submitting.', ja='送信する前に選択してください。', zh='请先做出选择再提交。'),

    la2_title=dict(
        en='Part 3: Lottery Decisions',
        fr='Partie 3 : Décisions de loterie',
        de='Teil 3: Lotterie-Entscheidungen',
        ja='パート3: くじの決定',
        zh='第三部分：抽奖决策'
    ),
    la2_intro=dict(
        en='You will now make a series of choices between a <strong>lottery</strong> and a <strong>safe option</strong> (keeping your bonus as-is). The lottery always gives you a 50% chance to <strong>win {symbol}{gain}</strong>. The potential loss changes with each choice. Your task is to find the loss amount where the lottery and the safe option feel <em>equally appealing</em> to you. <strong>Remember, the outcome of this task will be revealed to you immediately after you submit your decision.</strong>',
        fr='Vous allez maintenant faire une série de choix entre une <strong>loterie</strong> et une <strong>option sûre</strong> (garder votre bonus tel quel). La loterie vous donne toujours 50% de chance de <strong>gagner {symbol}{gain}</strong>. Le montant de la perte change à chaque choix. Votre tâche est de trouver le montant de perte où la loterie et l\'option sûre vous semblent <em>aussi attractives l\'une que l\'autre</em>. <strong>N\'oubliez pas que le résultat de cette tâche vous sera révélé immédiatement après avoir soumis votre décision.</strong>',
        de='Sie treffen nun eine Reihe von Entscheidungen zwischen einer <strong>Lotterie</strong> und einer <strong>sicheren Option</strong> (Ihr Bonus bleibt unverändert). Die Lotterie bietet immer eine 50%-Chance, <strong>{symbol}{gain} zu gewinnen</strong>. Der mögliche Verlust ändert sich bei jeder Entscheidung. Ihre Aufgabe ist es, den Verlustbetrag zu finden, bei dem Lotterie und sichere Option für Sie <em>gleich attraktiv</em> sind. <strong>Denken Sie daran, dass Ihnen das Ergebnis dieser Aufgabe sofort nach dem Absenden Ihrer Entscheidung mitgeteilt wird.</strong>',
        ja='これから、<strong>くじ</strong>と<strong>安全な選択肢</strong>（ボーナスをそのまま保持）の間で一連の選択を行います。くじは常に50%の確率で<strong>{symbol}{gain}を獲得</strong>できます。損失額は選択ごとに変わります。あなたの課題は、くじと安全な選択肢が<em>同じくらい魅力的に感じる</em>損失額を見つけることです。<strong>この課題の結果は、決定を送信した後すぐに発表されますのでご注意ください。</strong>',
        zh='接下来，您将在<strong>抽奖</strong>与<strong>稳妥选项</strong>（保持奖金不变）之间做出一系列选择。抽奖始终有50%的概率<strong>赢得{symbol}{gain}</strong>，但潜在损失金额每次不同。您的任务是找到一个损失金额，使抽奖和稳妥选项对您来说<em>同样有吸引力</em>。<strong>请注意，提交决定后将立即揭晓本任务的结果。</strong>'
    ),
    la2_step_label=dict(
        en='Comparison {current} of {total}',
        fr='Comparaison {current} sur {total}',
        de='Vergleich {current} von {total}',
        ja='比較 {current} / {total}',
        zh='第 {current} 次比较（共 {total} 次）'
    ),
    la2_bonus_note=dict(
        en='Your task bonus starts at <strong>{symbol}{endowment}</strong>. The amounts shown below reflect potential changes to this bonus.',
        fr='Votre bonus de tâche commence à <strong>{symbol}{endowment}</strong>. Les montants ci-dessous reflètent les changements potentiels de ce bonus.',
        de='Ihr Aufgabenbonus beginnt bei <strong>{symbol}{endowment}</strong>. Die unten angezeigten Beträge spiegeln mögliche Änderungen dieses Bonus wider.',
        ja='課題のボーナスは<strong>{symbol}{endowment}</strong>から始まります。以下の金額は、このボーナスに対する変動を示しています。',
        zh='您的任务奖金从<strong>{symbol}{endowment}</strong>开始。以下金额反映了奖金可能的变动。',
    ),
    la2_question=dict(
        en='Which would you prefer?',
        fr='Que préféreriez-vous ?',
        de='Was würden Sie bevorzugen?',
        ja='どちらを選びますか？',
        zh='您更倾向于哪个？'
    ),
    la2_opt_lottery=dict(en='Take the Lottery', fr='Prendre la loterie', de='Lotterie nehmen', ja='くじを選ぶ', zh='选择抽奖'),
    la2_opt_sure=dict(en='Take the Safe Option', fr='Prendre l\'option sûre', de='Sichere Option nehmen',
                      ja='安全な選択肢を選ぶ', zh='选择稳妥选项'),
    la2_lottery_label=dict(en='Lottery', fr='Loterie', de='Lotterie', ja='くじ', zh='抽奖'),
    la2_sure_label=dict(en='Safe Option', fr='Option sûre', de='Sichere Option', ja='安全な選択肢', zh='稳妥选项'),
    la2_win_line=dict(
        en='<strong>Win {symbol}{gain}</strong>',
        fr='<strong>Gagner {symbol}{gain}</strong>',
        de='<strong>{symbol}{gain} gewinnen</strong>',
        ja='<strong>{symbol}{gain} 獲得</strong>',
        zh='<strong>赢得 {symbol}{gain}</strong>'
    ),
    la2_lose_line=dict(
        en='<strong>Lose {symbol}{x}</strong>',
        fr='<strong>Perdre {symbol}{x}</strong>',
        de='<strong>{symbol}{x} verlieren</strong>',
        ja='<strong>{symbol}{x} 損失</strong>',
        zh='<strong>损失 {symbol}{x}</strong>'
    ),
    la2_sure_line=dict(
        en='<strong>Keep your {symbol}{endowment}</strong> (no change)',
        fr='<strong>Garder vos {symbol}{endowment}</strong> (aucun changement)',
        de='<strong>Ihre {symbol}{endowment} behalten</strong> (keine Änderung)',
        ja='<strong>{symbol}{endowment}をそのまま保持</strong>（変更なし）',
        zh='<strong>保留您的 {symbol}{endowment}</strong>（不变）'
    ),
    la2_slider_title=dict(
        en='Almost done — adjust the exact amount',
        fr='Presque fini — ajustez le montant exact',
        de='Fast fertig — passen Sie den genauen Betrag an',
        ja='もう少しです — 正確な金額を調整してください',
        zh='即将完成 — 请调整精确金额'
    ),
    la2_slider_intro=dict(
        en='Based on your choices, we\'ve narrowed it down to a small range. Use the slider to set the <strong>exact loss amount</strong> where the lottery and the safe option feel equally appealing to you.',
        fr='Sur la base de vos choix, nous avons réduit la plage. Utilisez le curseur pour définir le <strong>montant de perte exact</strong> où la loterie et l\'option sûre vous semblent aussi attractives l\'une que l\'autre.',
        de='Basierend auf Ihren Entscheidungen haben wir den Bereich eingegrenzt. Verwenden Sie den Schieberegler, um den <strong>genauen Verlustbetrag</strong> einzustellen, bei dem Lotterie und sichere Option für Sie gleich attraktiv erscheinen.',
        ja='あなたの選択に基づいて、範囲を狭めました。スライダーを使って、くじと安全な選択肢が同じくらい魅力的に感じる<strong>正確な損失額</strong>を設定してください。',
        zh='根据您的选择，我们已缩小范围。请使用滑动条设置一个<strong>精确的损失金额</strong>，使抽奖和稳妥选项对您来说同样有吸引力。'
    ),
    la2_slider_label_lose=dict(en='Lose', fr='Perdre', de='Verlieren', ja='損失', zh='损失'),
    la2_slider_label_cur=dict(en='', fr='', de='', ja='', zh=''),
    la2_confirm=dict(
        en='When both options feel <strong>equally acceptable</strong>, click Confirm.',
        fr='Lorsque les deux options vous semblent <strong>également acceptables</strong>, cliquez sur Confirmer.',
        de='Wenn beide Optionen <strong>gleich akzeptabel</strong> erscheinen, klicken Sie auf Bestätigen.',
        ja='両方の選択肢が<strong>同等に受け入れられる</strong>と感じたら、確認をクリックしてください。',
        zh='当两个选项对您来说<strong>同样可以接受</strong>时，请点击确认。'
    ),
    la2_btn_confirm=dict(en='Confirm', fr='Confirmer', de='Bestätigen', ja='確認', zh='确认'),
    la2_error=dict(
        en='Please complete all choices before submitting.',
        fr='Veuillez compléter tous les choix avant de soumettre.',
        de='Bitte treffen Sie alle Entscheidungen, bevor Sie absenden.',
        ja='送信前にすべての選択を完了してください。',
        zh='提交前请完成所有选择。'
    ),

    # --- Survey labels ---
    surv_title=dict(en='Final Survey', fr='Enquête finale', de='Abschlussumfrage', ja='最終アンケート', zh='最终问卷'),

    q_gender=dict(
        en='What is your gender?',
        fr='Quel est votre genre ?',
        de='Was ist Ihr Geschlecht?',
        ja='あなたの性別は？',
        zh='您的性别是？',
    ),
    gen_1=dict(en='Male', fr='Homme', de='Männlich', ja='男性', zh='男'),
    gen_2=dict(en='Female', fr='Femme', de='Weiblich', ja='女性', zh='女'),
    gen_3=dict(en='Non-binary / Third gender', fr='Non-binaire / Troisième genre', de='Nicht-binär / Drittes Geschlecht', ja='ノンバイナリー / 第三の性', zh='非二元性别 / 其他'),
    gen_4=dict(en='Prefer not to say', fr='Je préfère ne pas répondre', de='Keine Angabe', ja='回答したくない', zh='不愿透露'),

    q_home_country=dict(
        en='What is your home country?',
        fr='Quel est votre pays d\'origine ?',
        de='Was ist Ihr Heimatland?',
        ja='あなたの出身国はどこですか？',
        zh='您的祖国是哪里？',
    ),
    country_uk=dict(en='United Kingdom', fr='Royaume-Uni', de='Vereinigtes Königreich', ja='イギリス', zh='英国'),
    country_us=dict(en='United States', fr='États-Unis', de='Vereinigte Staaten', ja='アメリカ', zh='美国'),
    country_fr=dict(en='France', fr='France', de='Frankreich', ja='フランス', zh='法国'),
    country_de=dict(en='Germany', fr='Allemagne', de='Deutschland', ja='ドイツ', zh='德国'),
    country_jp=dict(en='Japan', fr='Japon', de='Japan', ja='日本', zh='日本'),
    country_cn=dict(en='China', fr='Chine', de='China', ja='中国', zh='中国'),
    country_in=dict(en='India', fr='Inde', de='Indien', ja='インド', zh='印度'),
    country_au=dict(en='Australia', fr='Australie', de='Australien', ja='オーストラリア', zh='澳大利亚'),
    country_ca=dict(en='Canada', fr='Canada', de='Kanada', ja='カナダ', zh='加拿大'),
    country_other=dict(en='Other', fr='Autre', de='Andere', ja='その他', zh='其他'),

    q_years_in_country=dict(
        en='How many years have you lived in the United Kingdom? Enter 0 if you do not currently reside there.',
        fr='Depuis combien d\'années vivez-vous en France ? Entrez 0 si vous n\'y résidez pas actuellement.',
        de='Wie viele Jahre leben Sie in Deutschland? Geben Sie 0 ein, wenn Sie derzeit nicht dort wohnen.',
        ja='日本に何年間住んでいますか？現在日本に住んでいない場合は0と入力してください。',
        zh='您在中国居住了多少年？如果目前不在中国居住，请输入0。',
    ),

    q_feedback=dict(
        en='Please feel free to leave any thoughts or comments about this study.',
        fr='N\'hésitez pas à laisser vos remarques ou commentaires sur cette étude.',
        de='Bitte hinterlassen Sie gerne Ihre Anmerkungen oder Kommentare zu dieser Studie.',
        ja='この調査についてのご意見やコメントがあれば、ぜひお聞かせください。',
        zh='如果您对本研究有任何想法或意见，请随时留言。',
    ),

    q_industry=dict(
        en='What industry do you currently work in?',
        fr='Dans quel secteur travaillez-vous actuellement ?',
        de='In welcher Branche arbeiten Sie derzeit?',
        ja='現在どの業界で働いていますか？',
        zh='您目前从事什么行业？'
    ),
    ind_1=dict(en='Agriculture / Mining', fr='Agriculture / Mines', de='Landwirtschaft / Bergbau', ja='農業・鉱業', zh='农业 / 矿业'),
    ind_2=dict(en='Manufacturing / Construction', fr='Fabrication / Construction', de='Fertigung / Bauwesen',
               ja='製造業・建設業', zh='制造业 / 建筑业'),
    ind_3=dict(en='IT / Technology', fr='Informatique / Technologie', de='IT / Technologie', ja='IT・テクノロジー', zh='IT / 科技'),
    ind_4=dict(en='Finance / Insurance', fr='Finance / Assurance', de='Finanzen / Versicherungen', ja='金融・保険', zh='金融 / 保险'),
    ind_5=dict(en='Healthcare / Medical', fr='Santé / Médical', de='Gesundheitswesen / Medizin', ja='医療・健康', zh='医疗 / 健康'),
    ind_6=dict(en='Education / Research', fr='Éducation / Recherche', de='Bildung / Forschung', ja='教育・研究', zh='教育 / 科研'),
    ind_7=dict(en='Retail / Hospitality', fr='Commerce / Hôtellerie', de='Einzelhandel / Gastgewerbe', ja='小売・サービス業', zh='零售 / 服务业'),
    ind_8=dict(en='Other / Unemployed / Student', fr='Autre / Sans emploi / Étudiant',
               de='Sonstiges / Arbeitslos / Student', ja='その他・無職・学生', zh='其他 / 待业 / 学生'),

    q_income=dict(
        en='What is your approximate annual income?',
        fr='Quel est votre revenu annuel approximatif ?',
        de='Was ist Ihr ungefähres Jahreseinkommen?',
        ja='おおよその年収はいくらですか？',
        zh='您的大致年收入是多少？'
    ),
    inc_1=dict(en='Less than £25,000', fr='Moins de 30 000 €', de='Weniger als 30.000 €', ja='450万円未満', zh='10万元以下'),
    inc_2=dict(en='£25,000 to £49,999', fr='30 000 € à 59 999 €', de='30.000 € bis 59.999 €', ja='450万円 ～ 899万円', zh='10万 ～ 20万元'),
    inc_3=dict(en='£50,000 to £74,999', fr='60 000 € à 89 999 €', de='60.000 € bis 89.999 €', ja='900万円 ～ 1,349万円', zh='20万 ～ 30万元'),
    inc_4=dict(en='£75,000 to £99,999', fr='90 000 € à 119 999 €', de='90.000 € bis 119.999 €',
               ja='1,350万円 ～ 1,799万円', zh='30万 ～ 50万元'),
    inc_5=dict(en='£100,000 or more', fr='120 000 € ou plus', de='120.000 € oder mehr', ja='1,800万円以上', zh='50万元以上'),
    inc_6=dict(en='Prefer not to say', fr='Je préfère ne pas répondre', de='Keine Angabe', ja='回答したくない', zh='不愿透露'),

    q_risk=dict(
        en='How do you see yourself: are you generally a person who is fully prepared to take risks or do you try to avoid taking risks?',
        fr='Comment vous voyez-vous : êtes-vous généralement une personne prête à prendre des risques ou essayez-vous d\'éviter de prendre des risques ?',
        de='Wie sehen Sie sich selbst: Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        ja='ご自身をどのように評価しますか：あなたは一般的にリスクを冒す準備ができている人ですか、それともリスクを避けようとする人ですか？',
        zh='您如何评价自己：您通常是一个愿意冒险的人，还是尽量规避风险的人？'
    ),
    risk_0=dict(en='Avoid risks', fr='Éviter les risques', de='Risiken vermeiden', ja='リスクを避ける', zh='回避风险'),
    risk_10=dict(en='Prepared to take risks', fr='Prêt à prendre des risques', de='Risikobereit', ja='リスクを冒す', zh='愿意冒险'),
    q_pat=dict(
        en='How do you see yourself: are you generally an impatient person, or someone who always shows great patience?',
        fr='Comment vous voyez-vous : êtes-vous généralement une personne impatiente ou quelqu\'un qui fait toujours preuve d\'une grande patience ?',
        de='Wie sehen Sie sich selbst: Sind Sie im Allgemeinen ein ungeduldiger Mensch oder jemand, der immer große Geduld zeigt?',
        ja='ご自身をどのように評価しますか：あなたは一般的にせっかちな人ですか、それとも常に忍耐強い人ですか？',
        zh='您如何评价自己：您通常是一个缺乏耐心的人，还是总是很有耐心的人？'
    ),
    pat_0=dict(en='Very impatient', fr='Très impatient', de='Sehr ungeduldig', ja='非常にせっかち', zh='非常没耐心'),
    pat_10=dict(en='Very patient', fr='Très patient', de='Sehr geduldig', ja='非常に忍耐強い', zh='非常有耐心'),

    payment_box_head=dict(
        en='Payment',
        fr='Paiement',
        de='Auszahlung',
        ja='支払い',
        zh='报酬',
    ),
    payment_box_note=dict(
        en='You start with {symbol}{endowment}. One round will be played out for real. 1 in 10 participants will receive their bonus through Prolific.',
        fr='Vous commencez avec {symbol}{endowment}. Un tour sera joué pour de vrai. 1 participant sur 10 recevra son bonus via Prolific.',
        de='Sie starten mit {symbol}{endowment}. Eine Runde wird tatsächlich ausgespielt. 1 von 10 Teilnehmenden erhält den Bonus über Prolific.',
        ja='{symbol}{endowment}からスタートします。1つのラウンドが実際に実行されます。10人に1人がProlificを通じてボーナスを受け取ります。',
        zh='您的起始金额为{symbol}{endowment}。系统将随机抽取一轮进行真实结算。每10名参与者中有1名可通过Prolific获得奖金。',
    ),

    td_title=dict(
        en='Part 3: Time Preferences',
        fr='Partie 3 : Préférences temporelles',
        de='Teil 3: Zeitpräferenzen',
        ja='パート3：時間的選好',
        zh='第三部分：时间偏好',
    ),
    td_intro=dict(
        en=(
            'You will now make a series of hypothetical choices between two payment options. '
            'One option pays a <strong>smaller amount sooner</strong>; '
            'the other pays a <strong>larger amount later</strong>. '
            'There are no right or wrong answers — we simply want to know your genuine preference.'
        ),
        fr=(
            'Vous allez maintenant faire une série de choix hypothétiques entre deux options de paiement. '
            'Une option verse un <strong>montant plus faible plus tôt</strong> ; '
            "l'autre verse un <strong>montant plus élevé plus tard</strong>. "
            "Il n'y a pas de bonnes ou de mauvaises réponses — nous voulons simplement connaître vos préférences réelles."
        ),
        de=(
            'Sie treffen nun eine Reihe von hypothetischen Entscheidungen zwischen zwei Zahlungsoptionen. '
            'Eine Option zahlt einen <strong>kleineren Betrag früher</strong>; '
            'die andere zahlt einen <strong>größeren Betrag später</strong>. '
            'Es gibt keine richtigen oder falschen Antworten — wir möchten nur Ihre ehrliche Präferenz kennen.'
        ),
        ja=(
            'これから、2つの支払いオプションの間で一連の仮想的な選択を行います。'
            '一方は<strong>少額を早く</strong>受け取るオプション、'
            'もう一方は<strong>多額を後で</strong>受け取るオプションです。'
            '正解・不正解はありません。あなたの正直な好みを教えてください。'
        ),
        zh=(
            '接下来，您将在两个假设的支付方案之间做出一系列选择。'
            '一个方案是<strong>较早获得较少金额</strong>；'
            '另一个方案是<strong>较晚获得较多金额</strong>。'
            '没有对错之分，我们只是想了解您的真实偏好。'
        ),
    ),
    td_alert=dict(
        en=(
            '<strong>How it works:</strong> Each row offers the same sooner amount but a higher later amount. '
            'Once you prefer the sooner option on a row, you will prefer it on all rows above too — '
            '<strong>click once to set your switch point</strong> and the table updates automatically.'
        ),
        fr=(
            '<strong>Comment ça marche :</strong> Chaque ligne propose le même montant précoce mais un montant tardif plus élevé. '
            "Une fois que vous préférez l'option précoce sur une ligne, vous la préférerez aussi sur toutes les lignes supérieures — "
            '<strong>cliquez une fois pour définir votre point de bascule</strong>, le tableau se met à jour automatiquement.'
        ),
        de=(
            '<strong>So funktioniert es:</strong> Jede Zeile bietet denselben früheren Betrag, aber einen höheren späteren Betrag. '
            'Wenn Sie in einer Zeile die frühere Option bevorzugen, tun Sie dies auch in allen darüber liegenden — '
            '<strong>klicken Sie einmal, um Ihren Wechselpunkt festzulegen</strong>, die Tabelle aktualisiert sich automatisch.'
        ),
        ja=(
            '<strong>仕組み：</strong>各行は同じ早期金額ですが、後期金額が高くなっています。'
            'ある行で早期オプションを選ぶなら、それより上の全ての行でも早期を選ぶはずです。'
            '<strong>一度クリックして切り替えポイントを設定すると</strong>、テーブルが自動更新されます。'
        ),
        zh=(
            '<strong>规则说明：</strong>每行的较早金额相同，但较晚金额逐行增加。'
            '如果您在某行更倾向较早选项，那么该行以上的所有行也应如此。'
            '<strong>点击一次即可设置切换点</strong>，表格会自动更新。'
        ),
    ),
    td_tracker_header=dict(
        en='Waiting time between options:',
        fr='Temps d\'attente entre les options :',
        de='Wartezeit zwischen den Optionen:',
        ja='選択肢間の待ち時間：',
        zh='选项之间的等待时间：',
    ),
    td_col_sooner=dict(en='Option A — Sooner', fr='Option A — Plus tôt', de='Option A — Früher', ja='選択肢A — 早く', zh='选项A — 较早'),
    td_col_later=dict(en='Option B — Later', fr='Option B — Plus tard', de='Option B — Später', ja='選択肢B — 後で', zh='选项B — 较晚'),
    td_btn_next_horizon=dict(
        en='Continue to next horizon →',
        fr="Continuer vers l'horizon suivant →",
        de='Weiter zum nächsten Horizont →',
        ja='次のホライズンへ →',
        zh='继续下一个时间段 →',
    ),
    td_btn_submit=dict(
        en='Submit Decisions →',
        fr='Soumettre les décisions →',
        de='Entscheidungen absenden →',
        ja='決定を送信 →',
        zh='提交决定 →',
    ),
    td_error=dict(
        en='Please make a choice in each row before continuing.',
        fr='Veuillez faire un choix dans chaque ligne avant de continuer.',
        de='Bitte treffen Sie in jeder Zeile eine Auswahl, bevor Sie fortfahren.',
        ja='続ける前に各行で選択してください。',
        zh='请在每行做出选择后再继续。',
    ),
    end_title=dict(en='Experiment Completed!', fr='Expérience terminée !', de='Experiment abgeschlossen!', ja='実験完了！', zh='实验完成！'),
    end_msg=dict(
        en='Thank you for participating! Your responses have been recorded.',
        fr='Merci de votre participation ! Vos réponses ont été enregistrées.',
        de='Vielen Dank für Ihre Teilnahme! Ihre Antworten wurden gespeichert.',
        ja='ご参加ありがとうございました！回答が記録されました。',
        zh='感谢您的参与！您的回答已被记录。',
    ),
    end_redirect=dict(
        en='You will be redirected to Prolific shortly. If not, click the button below.',
        fr='Vous serez redirigé(e) vers Prolific sous peu. Sinon, cliquez sur le bouton ci-dessous.',
        de='Sie werden in Kürze zu Prolific weitergeleitet. Falls nicht, klicken Sie auf die Schaltfläche unten.',
        ja='まもなくProlificにリダイレクトされます。されない場合は、下のボタンをクリックしてください。',
        zh='您将很快被重定向到Prolific。如果没有，请点击下面的按钮。',
    ),
    end_btn_prolific=dict(en='Return to Prolific', fr='Retourner à Prolific', de='Zurück zu Prolific', ja='Prolificに戻る', zh='返回Prolific'),
    end_code_label=dict(en='Completion code', fr='Code de complétion', de='Abschlusscode', ja='完了コード', zh='完成码'),
    # --- Anticipation page (pre-outcome) ---
    antic_title=dict(
        en='Before the result is revealed…',
        fr='Avant que le résultat ne soit révélé…',
        de='Bevor das Ergebnis enthüllt wird…',
        ja='結果が発表される前に…',
        zh='在结果揭晓之前…',
    ),
    antic_worry_q=dict(
        en='How worried are you <em>right now</em> about <em>losing</em> some of your {symbol}{endowment} bonus?',
        fr='À quel point êtes-vous inquiet(e) <em>en ce moment</em> de <em>perdre</em> une partie de votre bonus de {symbol}{endowment} ?',
        de='Wie besorgt sind Sie <em>gerade</em>, <em>einen Teil</em> Ihres {symbol}{endowment}-Bonus zu verlieren?',
        ja='<em>今</em>、{symbol}{endowment}のボーナスの一部を<em>失う</em>ことについてどのくらい心配していますか？',
        zh='您<em>现在</em>对可能<em>损失</em>{symbol}{endowment}奖金的一部分有多担心？',
    ),
    antic_worry_lo=dict(en='Not at all worried', fr='Pas du tout inquiet(e)', de='Überhaupt nicht besorgt', ja='まったく心配していない', zh='完全不担心'),
    antic_worry_hi=dict(en='Extremely worried', fr='Extrêmement inquiet(e)', de='Extrem besorgt', ja='非常に心配している', zh='非常担心'),
    antic_prob_q=dict(
        en='How likely do you think you are about to <em>lose</em> some of your {symbol}{endowment} bonus?',
        fr='Quelle est selon vous la probabilité que vous <em>perdiez</em> une partie de votre bonus de {symbol}{endowment} ?',
        de='Wie wahrscheinlich ist es Ihrer Meinung nach, dass Sie einen Teil Ihres {symbol}{endowment}-Bonus <em>verlieren</em>?',
        ja='{symbol}{endowment}のボーナスの一部を<em>失う</em>可能性はどのくらいだと思いますか？',
        zh='您觉得<em>损失</em>{symbol}{endowment}奖金的一部分的可能性有多大？',
    ),
    antic_prob_lo=dict(en='Impossible', fr='Impossible', de='Unmöglich', ja='ありえない', zh='不可能'),
    antic_prob_hi=dict(en='Certain', fr='Certain', de='Sicher', ja='確実', zh='一定会'),
    antic_required=dict(
        en='Please answer both questions before continuing.',
        fr='Veuillez répondre aux deux questions avant de continuer.',
        de='Bitte beantworten Sie beide Fragen, bevor Sie fortfahren.',
        ja='続ける前に両方の質問にお答えください。',
        zh='请先回答两个问题，再继续。',
    ),

    res_title=dict(en='Task Result', fr='Résultat de la tâche', de='Aufgabenergebnis', ja='課題の結果', zh='任务结果'),
    res_selected=dict(
        en='The computer randomly selected <strong>Comparison {step}</strong> for payment.',
        fr='L\'ordinateur a sélectionné au hasard la <strong>Comparaison {step}</strong> pour le paiement.',
        de='Der Computer hat zufällig <strong>Vergleich {step}</strong> für die Auszahlung ausgewählt.',
        ja='コンピュータは支払いのために<strong>比較 {step}</strong>をランダムに選択しました。',
        zh='系统随机选取了<strong>第 {step} 次比较</strong>作为支付依据。'
    ),
    res_choice_a=dict(
        en='In this comparison, you chose the <strong>Safe Option</strong> — keeping your bonus unchanged.',
        fr='Dans cette comparaison, vous avez choisi l\'<strong>Option Sûre</strong> — votre bonus reste inchangé.',
        de='In diesem Vergleich haben Sie die <strong>Sichere Option</strong> gewählt — Ihr Bonus bleibt unverändert.',
        ja='この比較では、あなたは<strong>安全な選択肢</strong>を選びました — ボーナスは変更なしです。',
        zh='在这次比较中，您选择了<strong>稳妥选项</strong>——奖金保持不变。'
    ),
    res_choice_b=dict(
        en='In this comparison, you chose the <strong>Lottery</strong>.',
        fr='Dans cette comparaison, vous avez choisi la <strong>Loterie</strong>.',
        de='In diesem Vergleich haben Sie die <strong>Lotterie</strong> gewählt.',
        ja='この比較では、あなたは<strong>くじ</strong>を選びました。',
        zh='在这次比较中，您选择了<strong>抽奖</strong>。'
    ),
    res_flip_win=dict(
        en='The coin flip resulted in a <strong>Win</strong>! You gained {symbol}{gain}.',
        fr='Le tirage au sort a donné une <strong>Victoire</strong> ! Vous avez gagné {symbol}{gain}.',
        de='Der Münzwurf ergab einen <strong>Gewinn</strong>! Sie haben {symbol}{gain} gewonnen.',
        ja='コイン投げの結果は<strong>勝ち</strong>でした！あなたは {symbol}{gain} を獲得しました。',
        zh='掷硬币结果为<strong>赢</strong>！您获得了 {symbol}{gain}。'
    ),
    res_flip_loss=dict(
        en='The coin flip resulted in a <strong>Loss</strong>. You lost {symbol}{loss}.',
        fr='Le tirage au sort a donné une <strong>Perte</strong>. Vous avez perdu {symbol}{loss}.',
        de='Der Münzwurf ergab einen <strong>Verlust</strong>. Sie haben {symbol}{loss} verloren.',
        ja='コイン投げの結果は<strong>負け</strong>でした。あなたは {symbol}{loss} を失いました。',
        zh='掷硬币结果为<strong>输</strong>。您损失了 {symbol}{loss}。'
    ),
    res_final=dict(
        en='Your final balance for this task is: <strong>{symbol}{endowment} {sign} {symbol}{outcome} = {symbol}{total}</strong>.',
        fr='Votre solde final pour cette tâche est : <strong>{symbol}{endowment} {sign} {symbol}{outcome} = {symbol}{total}</strong>.',
        de='Ihr Endstand für diese Aufgabe ist: <strong>{symbol}{endowment} {sign} {symbol}{outcome} = {symbol}{total}</strong>.',
        ja='この課題の最終残高は：<strong>{symbol}{endowment} {sign} {symbol}{outcome} = {symbol}{total}</strong>。',
        zh='本任务的最终余额为：<strong>{symbol}{endowment} {sign} {symbol}{outcome} = {symbol}{total}</strong>。'
    ),
    res_final_a=dict(
        en='Your final balance for this task is your endowment: <strong>{symbol}{total}</strong>.',
        fr='Votre solde final pour cette tâche est votre dotation : <strong>{symbol}{total}</strong>.',
        de='Ihr Endstand für diese Aufgabe ist Ihr Startguthaben: <strong>{symbol}{total}</strong>.',
        ja='この課題の最終残高は初期残高のままです：<strong>{symbol}{total}</strong>。',
        zh='本任务的最终余额为初始金额：<strong>{symbol}{total}</strong>。'
    ),
    res_email_label=dict(
        en='Please enter your contact email so we can reach you if you are selected for the bonus:',
        fr='Veuillez entrer votre adresse e-mail de contact afin que nous puissions vous joindre si vous êtes sélectionné(e) pour le bonus :',
        de='Bitte geben Sie Ihre Kontakt-E-Mail-Adresse an, damit wir Sie kontaktieren können, falls Sie für den Bonus ausgewählt werden:',
        ja='ボーナスに選ばれた場合に連絡できるよう、連絡先メールアドレスをご入力ください：',
        zh='如果您被选中获得奖金，请留下联系邮箱以便我们联系您：'
    ),
    res_email_placeholder=dict(
        en='your.email@example.com',
        fr='votre.email@example.com',
        de='ihre.email@example.com',
        ja='your.email@example.com',
        zh='your.email@example.com'
    ),

    # --- Comprehension Check ---
    comp_title=dict(
        en='Comprehension Check',
        fr='Vérification de compréhension',
        de='Verständnisprüfung',
        ja='理解度チェック',
        zh='理解测试'
    ),
    comp_intro=dict(
        en='Before we begin, let\'s make sure the task is clear. Below is an <strong>example</strong> of one of the five comparisons you will face. Imagine that <strong>this comparison is the one randomly selected</strong> to determine your bonus payment.',
        fr='Avant de commencer, vérifions que la tâche est bien comprise. Ci-dessous se trouve un <strong>exemple</strong> de l\'une des cinq comparaisons que vous rencontrerez. Imaginez que <strong>cette comparaison est celle sélectionnée au hasard</strong> pour déterminer votre paiement bonus.',
        de='Bevor wir beginnen, stellen wir sicher, dass die Aufgabe klar ist. Unten sehen Sie ein <strong>Beispiel</strong> eines der fünf Vergleiche, die Sie treffen werden. Stellen Sie sich vor, dass <strong>dieser Vergleich zufällig ausgewählt wird</strong>, um Ihre Bonuszahlung zu bestimmen.',
        ja='始める前に、課題が明確であることを確認しましょう。以下は、あなたが直面する5つの比較の1つの<strong>例</strong>です。<strong>この比較がランダムに選ばれて</strong>ボーナスの支払いを決定すると想像してください。',
        zh='在开始之前，让我们确认您理解了任务。以下是您将面对的5次比较中的一个<strong>示例</strong>。请想象<strong>这次比较被随机选中</strong>来决定您的奖金。'
    ),
    comp_example_label=dict(
        en='Example Comparison',
        fr='Comparaison exemple',
        de='Beispielvergleich',
        ja='比較の例',
        zh='示例比较'
    ),
    comp_q1=dict(
        en='<strong>Question 1:</strong> Suppose you chose <strong>Option A (Safe Option)</strong> for this comparison, and this comparison is the one randomly selected for payment. What would your bonus be?',
        fr='<strong>Question 1 :</strong> Supposons que vous ayez choisi <strong>l\'Option A (Option Sûre)</strong> pour cette comparaison, et que cette comparaison soit celle sélectionnée au hasard pour le paiement. Quel serait votre bonus ?',
        de='<strong>Frage 1:</strong> Angenommen, Sie haben <strong>Option A (Sichere Option)</strong> für diesen Vergleich gewählt, und dieser Vergleich wird zufällig für die Auszahlung ausgewählt. Wie hoch wäre Ihr Bonus?',
        ja='<strong>質問1：</strong>この比較で<strong>選択肢A（安全な選択肢）</strong>を選び、この比較が支払いのためにランダムに選ばれたとします。あなたのボーナスはいくらになりますか？',
        zh='<strong>问题1：</strong>假设您在这次比较中选择了<strong>选项A（稳妥选项）</strong>，且这次比较被随机选中用于支付。您的奖金是多少？'
    ),
    comp_q2=dict(
        en='<strong>Question 2:</strong> Suppose you chose <strong>Option B (Lottery)</strong> for this comparison, this comparison is randomly selected, and the coin flip results in a <strong>loss of {symbol}{example_loss}</strong>. What would your bonus be?',
        fr='<strong>Question 2 :</strong> Supposons que vous ayez choisi <strong>l\'Option B (Loterie)</strong> pour cette comparaison, que cette comparaison soit sélectionnée, et que le tirage au sort résulte en une <strong>perte de {symbol}{example_loss}</strong>. Quel serait votre bonus ?',
        de='<strong>Frage 2:</strong> Angenommen, Sie haben <strong>Option B (Lotterie)</strong> für diesen Vergleich gewählt, dieser Vergleich wird ausgewählt, und der Münzwurf ergibt einen <strong>Verlust von {symbol}{example_loss}</strong>. Wie hoch wäre Ihr Bonus?',
        ja='<strong>質問2：</strong>この比較で<strong>選択肢B（くじ）</strong>を選び、この比較が選ばれ、コイン投げの結果<strong>{symbol}{example_loss}の損失</strong>になったとします。あなたのボーナスはいくらになりますか？',
        zh='<strong>问题2：</strong>假设您在这次比较中选择了<strong>选项B（抽奖）</strong>，该比较被随机选中，掷硬币结果为<strong>损失{symbol}{example_loss}</strong>。您的奖金是多少？'
    ),
    comp_check_btn=dict(
        en='Check Answers',
        fr='Vérifier les réponses',
        de='Antworten prüfen',
        ja='答えを確認',
        zh='检查答案'
    ),
    comp_correct=dict(
        en='All answers are correct! You may now proceed.',
        fr='Toutes les réponses sont correctes ! Vous pouvez maintenant continuer.',
        de='Alle Antworten sind richtig! Sie können nun fortfahren.',
        ja='すべての回答が正解です！次に進むことができます。',
        zh='全部回答正确！您可以继续了。'
    ),
    comp_wrong_q1=dict(
        en='<strong>Question 1 is incorrect.</strong> When you choose the Safe Option, nothing changes — you simply keep your starting bonus. Please try again.',
        fr='<strong>La question 1 est incorrecte.</strong> Lorsque vous choisissez l\'Option Sûre, rien ne change — vous conservez simplement votre bonus de départ. Veuillez réessayer.',
        de='<strong>Frage 1 ist falsch.</strong> Wenn Sie die Sichere Option wählen, ändert sich nichts — Sie behalten einfach Ihren Startbonus. Bitte versuchen Sie es erneut.',
        ja='<strong>質問1は不正解です。</strong>安全な選択肢を選ぶと、何も変わりません — 開始ボーナスをそのまま受け取ります。もう一度お試しください。',
        zh='<strong>问题1回答错误。</strong>选择稳妥选项时，什么都不会改变——您只需保留初始奖金。请再试一次。'
    ),
    comp_wrong_q2=dict(
        en='<strong>Question 2 is incorrect.</strong> When you choose the Lottery and the coin flip results in a loss of {symbol}{example_loss}, that amount is subtracted from your starting bonus: {symbol}{endowment} &minus; {symbol}{example_loss} = <strong>{symbol}{loss_total}</strong>.',
        fr='<strong>La question 2 est incorrecte.</strong> Lorsque vous choisissez la Loterie et que le tirage donne une perte de {symbol}{example_loss}, ce montant est soustrait de votre bonus de départ : {symbol}{endowment} &minus; {symbol}{example_loss} = <strong>{symbol}{loss_total}</strong>.',
        de='<strong>Frage 2 ist falsch.</strong> Wenn Sie die Lotterie wählen und der Münzwurf einen Verlust von {symbol}{example_loss} ergibt, wird dieser Betrag von Ihrem Startbonus abgezogen: {symbol}{endowment} &minus; {symbol}{example_loss} = <strong>{symbol}{loss_total}</strong>.',
        ja='<strong>質問2は不正解です。</strong>くじを選んでコイン投げの結果{symbol}{example_loss}の損失になった場合、その金額が開始ボーナスから差し引かれます：{symbol}{endowment} &minus; {symbol}{example_loss} = <strong>{symbol}{loss_total}</strong>。',
        zh='<strong>问题2回答错误。</strong>选择抽奖且掷硬币结果为损失{symbol}{example_loss}时，该金额将从初始奖金中扣除：{symbol}{endowment} &minus; {symbol}{example_loss} = <strong>{symbol}{loss_total}</strong>。'
    ),
    comp_q3=dict(
        en='<strong>Question 3:</strong> Suppose you chose <strong>Option B (Lottery)</strong> for this comparison, this comparison is randomly selected, and the coin flip results in a <strong>win of {symbol}{gain}</strong>. What would your bonus be?',
        fr='<strong>Question 3 :</strong> Supposons que vous ayez choisi <strong>l\'Option B (Loterie)</strong> pour cette comparaison, que cette comparaison soit sélectionnée, et que le tirage au sort résulte en un <strong>gain de {symbol}{gain}</strong>. Quel serait votre bonus ?',
        de='<strong>Frage 3:</strong> Angenommen, Sie haben <strong>Option B (Lotterie)</strong> für diesen Vergleich gewählt, dieser Vergleich wird ausgewählt, und der Münzwurf ergibt einen <strong>Gewinn von {symbol}{gain}</strong>. Wie hoch wäre Ihr Bonus?',
        ja='<strong>質問3：</strong>この比較で<strong>選択肢B（くじ）</strong>を選び、この比較が選ばれ、コイン投げの結果<strong>{symbol}{gain}の獲得</strong>になったとします。あなたのボーナスはいくらになりますか？',
        zh='<strong>问题3：</strong>假设您在这次比较中选择了<strong>选项B（抽奖）</strong>，该比较被随机选中，掷硬币结果为<strong>赢得{symbol}{gain}</strong>。您的奖金是多少？'
    ),
    comp_wrong_q3=dict(
        en='<strong>Question 3 is incorrect.</strong> When you choose the Lottery and the coin flip results in a win of {symbol}{gain}, that amount is added to your starting bonus: {symbol}{endowment} + {symbol}{gain} = <strong>{symbol}{win_total}</strong>.',
        fr='<strong>La question 3 est incorrecte.</strong> Lorsque vous choisissez la Loterie et que le tirage donne un gain de {symbol}{gain}, ce montant est ajouté à votre bonus de départ : {symbol}{endowment} + {symbol}{gain} = <strong>{symbol}{win_total}</strong>.',
        de='<strong>Frage 3 ist falsch.</strong> Wenn Sie die Lotterie wählen und der Münzwurf einen Gewinn von {symbol}{gain} ergibt, wird dieser Betrag zu Ihrem Startbonus addiert: {symbol}{endowment} + {symbol}{gain} = <strong>{symbol}{win_total}</strong>.',
        ja='<strong>質問3は不正解です。</strong>くじを選んでコイン投げの結果{symbol}{gain}の獲得になった場合、その金額が開始ボーナスに加算されます：{symbol}{endowment} + {symbol}{gain} = <strong>{symbol}{win_total}</strong>。',
        zh='<strong>问题3回答错误。</strong>选择抽奖且掷硬币结果为赢得{symbol}{gain}时，该金额将加到初始奖金上：{symbol}{endowment} + {symbol}{gain} = <strong>{symbol}{win_total}</strong>。'
    ),
    comp_please_select=dict(
        en='Please answer all three questions before checking.',
        fr='Veuillez répondre aux trois questions avant de vérifier.',
        de='Bitte beantworten Sie alle drei Fragen, bevor Sie prüfen.',
        ja='確認する前に3つの質問すべてにお答えください。',
        zh='请回答全部三个问题后再检查。'
    ),
)


def ui_dict(lang):
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ══════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════

def _ctx(player, progress):
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
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        ui = ui_dict(lang)
        rate = cur['rate']
        symbol = cur['symbol']
        dec = cur['decimals']

        def fmt(v):
            return f'{v:.0f}' if dec == 0 else f'{v:.{dec}f}'

        endowment_str = fmt(C.LA_ENDOWMENT_BASE * rate)
        gain_str = fmt(C.GAIN_BASE * rate)

        ui['intro_text'] = ui['intro_text'].format(symbol=symbol, endowment=endowment_str)
        ui['la_alert_text'] = ui['la_alert_text'].format(symbol=symbol, gain=gain_str)
        ui['payment_box_note'] = ui['payment_box_note'].format(symbol=symbol, endowment=endowment_str)

        return dict(
            symbol=symbol,
            lang=lang,
            ui=ui,
            progress=75,
        )


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['comp_q1_attempts', 'comp_q2_attempts', 'comp_q3_attempts']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        rate = cur['rate']
        symbol = cur['symbol']
        dec = cur['decimals']
        ui = ui_dict(lang)

        def fmt(v):
            return f'{v:.0f}' if dec == 0 else f'{v:.{dec}f}'

        endowment = C.LA_ENDOWMENT_BASE * rate
        gain = C.GAIN_BASE * rate
        example_loss = C.COMP_EXAMPLE_LOSS_BASE * rate
        win_total = endowment + gain
        loss_total = endowment - example_loss

        endowment_s = fmt(endowment)
        gain_s = fmt(gain)
        example_loss_s = fmt(example_loss)
        win_total_s = fmt(win_total)
        loss_total_s = fmt(loss_total)

        # Format Q2, Q3 and feedback strings with example amounts
        ui['comp_q2'] = ui['comp_q2'].format(symbol=symbol, example_loss=example_loss_s)
        ui['comp_q3'] = ui['comp_q3'].format(symbol=symbol, gain=gain_s)
        ui['comp_wrong_q1'] = ui['comp_wrong_q1'].format(symbol=symbol, endowment=endowment_s)
        ui['comp_wrong_q2'] = ui['comp_wrong_q2'].format(
            symbol=symbol, example_loss=example_loss_s,
            endowment=endowment_s, loss_total=loss_total_s
        )
        ui['comp_wrong_q3'] = ui['comp_wrong_q3'].format(
            symbol=symbol, gain=gain_s,
            endowment=endowment_s, win_total=win_total_s
        )

        # Build the win line for the example card
        win_line = ui['la2_win_line'].format(symbol=symbol, gain=gain_s)
        lose_line = ui['la2_lose_line'].format(symbol=symbol, x=example_loss_s)
        sure_line = ui['la2_sure_line'].format(symbol=symbol, endowment=endowment_s)

        # Q1 options: $0, endowment (correct), win_total, loss_total
        q1_options = [
            dict(value='a', label=f'{symbol}0'),
            dict(value='b', label=f'{symbol}{endowment_s}'),
            dict(value='c', label=f'{symbol}{win_total_s}'),
            dict(value='d', label=f'{symbol}{loss_total_s}'),
        ]
        # Q2 options: win_total, $0, loss_total (correct), endowment
        q2_options = [
            dict(value='a', label=f'{symbol}{win_total_s}'),
            dict(value='b', label=f'{symbol}0'),
            dict(value='c', label=f'{symbol}{loss_total_s}'),
            dict(value='d', label=f'{symbol}{endowment_s}'),
        ]
        # Q3 options: loss_total, endowment, $0, win_total (correct)
        q3_options = [
            dict(value='a', label=f'{symbol}{loss_total_s}'),
            dict(value='b', label=f'{symbol}{endowment_s}'),
            dict(value='c', label=f'{symbol}0'),
            dict(value='d', label=f'{symbol}{win_total_s}'),
        ]

        return dict(
            lang=lang,
            ui=ui,
            progress=78,
            symbol=symbol,
            endowment=endowment_s,
            gain=gain_s,
            example_loss=example_loss_s,
            win_total=win_total_s,
            loss_total=loss_total_s,
            win_line=win_line,
            lose_line=lose_line,
            sure_line=sure_line,
            q1_options=q1_options,
            q2_options=q2_options,
            q3_options=q3_options,
        )


class LossAversionTask(Page):
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
    form_model = 'player'
    form_fields = ['la2_indifference_x', 'la2_bisection_data']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        rate = cur['rate']
        symbol = cur['symbol']
        dec = cur['decimals']

        def fmt(v):
            return f'{v:.0f}' if dec == 0 else f'{v:.{dec}f}'

        gain = C.GAIN_BASE * rate
        x_min = C.X_MIN * rate
        x_max = C.X_MAX * rate
        x_init = (x_min + x_max) / 2
        ui = ui_dict(lang)

        ui['la2_win_line_fmt'] = ui['la2_win_line'].format(symbol=symbol, gain=fmt(gain))
        ui['la2_lose_line_init'] = ui['la2_lose_line'].format(symbol=symbol, x=fmt(x_init))
        endowment_str = fmt(C.LA_ENDOWMENT_BASE * rate)
        ui['la2_sure_line'] = ui['la2_sure_line'].format(symbol=symbol, endowment=endowment_str)
        ui['la2_bonus_note'] = ui['la2_bonus_note'].format(symbol=symbol, endowment=endowment_str)

        return dict(
            lang=lang,
            ui=ui,
            progress=82,
            gain=gain,
            x_min=x_min,
            x_max=x_max,
            symbol=symbol,
            decimals=dec,
            endowment=C.LA_ENDOWMENT_BASE * rate,
            bisection_steps=C.BISECTION_STEPS,
            steps_range=list(range(1, C.BISECTION_STEPS + 1)),
            la2_intro_formatted=ui['la2_intro'].format(symbol=symbol, gain=fmt(gain)),
            step_label_1=ui['la2_step_label'].format(current=1, total=C.BISECTION_STEPS),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        lang = player.language
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        rate = cur['rate']
        endowment = C.LA_ENDOWMENT_BASE * rate
        gain = C.GAIN_BASE * rate
        player.la2_endowment = endowment

        steps = []
        try:
            steps = json.loads(player.field_maybe_none('la2_bisection_data') or '[]')
        except (json.JSONDecodeError, TypeError):
            steps = []

        if steps:
            selected = random.choice(steps)
            player.la2_selected_step = selected['step']
            player.la2_selected_x = round(selected['x_shown'], 2)
            player.la2_selected_choice = selected['choice']

            if selected['choice'] == 'A':
                player.la2_coin_flip = 'N/A'
                player.la2_bonus = round(endowment, 2)
            else:
                if random.random() < 0.5:
                    player.la2_coin_flip = 'Win'
                    player.la2_bonus = round(endowment + gain, 2)
                else:
                    player.la2_coin_flip = 'Loss'
                    player.la2_bonus = round(endowment - selected['x_shown'], 2)
        else:
            player.la2_selected_step = 0
            player.la2_selected_x = 0
            player.la2_selected_choice = ''
            player.la2_coin_flip = 'N/A'
            player.la2_bonus = round(endowment, 2)

        x_star = player.field_maybe_none('la2_indifference_x')
        if x_star is not None and x_star > 0:
            player.la2_lambda = round(gain / x_star, 4)
        elif x_star is not None and x_star == 0:
            player.la2_lambda = 999.0
        else:
            player.la2_lambda = None


class LossAversionAnticipation(Page):
    form_model = 'player'
    form_fields = ['la2_anticipation_worry', 'la2_anticipation_prob']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        symbol = cur['symbol']
        dec = cur['decimals']
        endowment = C.LA_ENDOWMENT_BASE * cur['rate']
        endowment_s = f'{endowment:.0f}' if dec == 0 else f'{endowment:.{dec}f}'

        ctx = _ctx(player, 85)
        fmt = dict(symbol=symbol, endowment=endowment_s)
        ctx['ui']['antic_worry_q'] = ctx['ui']['antic_worry_q'].format(**fmt)
        ctx['ui']['antic_prob_q'] = ctx['ui']['antic_prob_q'].format(**fmt)
        return dict(
            likert_range=list(range(1, 10)),
            **ctx,
        )


class LossAversionResult(Page):
    form_model = 'player'
    form_fields = ['bonus_contact_email']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        ui = ui_dict(lang)

        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        symbol = cur['symbol']
        dec = cur['decimals']

        def fmt(v):
            return f'{v:.0f}' if dec == 0 else f'{v:.{dec}f}'

        endowment = player.la2_endowment
        selected_step = player.la2_selected_step
        selected_x = player.la2_selected_x
        selected_choice = player.la2_selected_choice
        coin_flip = player.la2_coin_flip
        bonus = player.la2_bonus
        gain = C.GAIN_BASE * cur['rate']

        res_selected = ui['res_selected'].format(step=selected_step)

        if coin_flip == 'Win':
            outcome = gain
            sign = "+"
        else:
            outcome = selected_x
            sign = "-"

        res_flip_win = ui['res_flip_win'].format(symbol=symbol, gain=fmt(gain))
        res_flip_loss = ui['res_flip_loss'].format(symbol=symbol, loss=fmt(selected_x))
        res_final = ui['res_final'].format(symbol=symbol, endowment=fmt(endowment), sign=sign, outcome=fmt(outcome),
                                           total=fmt(bonus))
        res_final_a = ui['res_final_a'].format(symbol=symbol, total=fmt(bonus))

        return dict(
            lang=lang,
            ui=ui,
            progress=88,
            selected_choice=selected_choice,
            coin_flip=coin_flip,
            bonus=bonus,
            bonus_fmt=fmt(bonus),
            symbol=symbol,
            res_selected_formatted=res_selected,
            res_flip_win_formatted=res_flip_win,
            res_flip_loss_formatted=res_flip_loss,
            res_final_formatted=res_final,
            res_final_a_formatted=res_final_a,
        )


class TemporalDiscounting(Page):
    form_model = 'player'
    form_fields = ['td_switching_1mo', 'td_switching_6mo', 'td_switching_2yr', 'td_data']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        ui = ui_dict(lang)
        cur = C.CURRENCY.get(lang, C.CURRENCY['en'])
        rate = cur['rate']
        symbol = cur['symbol']
        dec = cur['decimals']

        def fmt(v):
            val = v * rate
            return f'{val:.0f}' if dec == 0 else f'{val:.{dec}f}'

        horizons_localised = []
        for h in C.TD_HORIZONS:
            converted_rows = []
            for row in h['rows']:
                converted_rows.append(dict(
                    row=row['row'],
                    sooner=fmt(row['sooner']),
                    later=fmt(row['later']),
                ))
            horizons_localised.append(dict(
                id=h['id'],
                rows=converted_rows,
                label=h['label'].get(lang, h['label']['en']),
                sooner_label=h['sooner_label'].get(lang, h['sooner_label']['en']),
                later_label=h['later_label'].get(lang, h['later_label']['en']),
            ))

        return dict(
            horizons=horizons_localised,
            n_horizons=len(C.TD_HORIZONS),
            symbol=symbol,
            **_ctx(player, 92),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        horizon = random.choice(C.TD_HORIZONS)
        row = random.choice(horizon['rows'])

        player.td_selected_horizon = horizon['id']
        player.td_selected_row = row['row']

        sp_map = {
            '1mo': player.field_maybe_none('td_switching_1mo') or 8,
            '6mo': player.field_maybe_none('td_switching_6mo') or 8,
            '2yr': player.field_maybe_none('td_switching_2yr') or 8,
        }
        sp = sp_map[horizon['id']]
        player.td_choice = 'later' if row['row'] >= sp else 'sooner'

        def implied_k(switch_point, k_values):
            # sp = first row where participant chooses 'later'
            # sp=1 → always later (most patient, k≈0)
            # sp>n → always sooner (most impatient, k=∞)
            n = len(k_values)
            if switch_point <= 1:
                return 0.0
            if switch_point > n:
                return 999.0
            k_low = k_values[switch_point - 2]
            k_high = k_values[switch_point - 1]
            return round((k_low + k_high) / 2, 4)

        horizon_map = {h['id']: h['k_values'] for h in C.TD_HORIZONS}

        player.td_k_1mo = implied_k(sp_map['1mo'], horizon_map['1mo'])
        player.td_k_6mo = implied_k(sp_map['6mo'], horizon_map['6mo'])
        player.td_k_2yr = implied_k(sp_map['2yr'], horizon_map['2yr'])

        finite_ks = [k for k in [player.td_k_1mo, player.td_k_6mo, player.td_k_2yr]
                     if k is not None and 0 < k < 999]
        if finite_ks:
            log_mean = sum(math.log(k) for k in finite_ks) / len(finite_ks)
            player.td_k_geo_mean = round(math.exp(log_mean), 4)
        else:
            player.td_k_geo_mean = None


class Survey(Page):
    form_model = 'player'
    form_fields = ['gender', 'home_country', 'years_in_country', 'employment_industry', 'income_level', 'risk_general', 'patience_general', 'study_feedback']

    @staticmethod
    def vars_for_template(player):
        return dict(
            likert_range=C.LIKERT_RANGE,
            **_ctx(player, 96)
        )


class FinalThankYou(Page):
    @staticmethod
    def vars_for_template(player):
        completion_code = player.session.config.get('completion_code', 'CFZCG8H4')
        prolific_url = f'https://app.prolific.com/submissions/complete?cc={completion_code}'
        ctx = _ctx(player, 100)
        ctx['completion_code'] = completion_code
        ctx['prolific_url'] = prolific_url
        return ctx


page_sequence = [
    Task3Intro,
    ComprehensionCheck,
    LossAversionBisection,
    LossAversionAnticipation,
    LossAversionResult,
    TemporalDiscounting,
    Survey,
    FinalThankYou,
]