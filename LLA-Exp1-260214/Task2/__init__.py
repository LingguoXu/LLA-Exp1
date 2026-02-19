from otree.api import *
import json

doc = """
Task 2: FTR Elicitation (Production) & Subjective Probability (Perception).
Design based on Robertson et al. (2023).
Languages: English (en), French (fr), German (de), Japanese (ja).
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# ═══════════════════════════════════════════════════════════
# UI STRINGS
# ═══════════════════════════════════════════════════════════
UI = dict(
    btn_next = dict(en='Next', fr='Suivant', de='Weiter', ja='次へ'),
    btn_submit = dict(en='Submit', fr='Soumettre', de='Absenden', ja='送信'),
    required_msg = dict(
        en='Please answer all items.',
        fr='Veuillez répondre à toutes les questions.',
        de='Bitte beantworten Sie alle Fragen.',
        ja='すべての項目に回答してください。',
    ),
    # ── Task 2 Intro Strings ──
    intro_title = dict(
        en='Part 2',
        fr='Partie 2',
        de='Teil 2',
        ja='パート2'
    ),
    intro_text = dict(
        en='You are now moving on to the second part of the study. Please click the button below to continue.',
        fr="Vous passez maintenant à la deuxième partie de l'étude. Veuillez cliquer sur le bouton ci-dessous pour continuer.",
        de='Sie fahren nun mit dem zweiten Teil der Studie fort. Bitte klicken Sie auf die Schaltfläche unten, um fortzufahren.',
        ja='調査の第2パートに移ります。下のボタンをクリックして進んでください。'
    ),
    # ── Task 2.1 Instructions ──
    t2_instructions = dict(
        en="Please complete the conversation. Use the verb in parentheses as a guide, but change it to fit the sentence naturally (e.g., 'go' → 'will go', 'is going', 'might go', etc.).",
        fr="Veuillez compléter la conversation. Utilisez le verbe entre parenthèses comme guide, mais conjuguez-le (ex: 'aller' → 'ira', 'va aller', 'pourrait aller').",
        de="Bitte vervollständigen Sie das Gespräch. Verwenden Sie das Verb in Klammern als Orientierung (z. B. 'gehen' → 'wird gehen', 'könnte gehen').",
        ja="会話を完成させてください。括弧内の動詞を参考に、文脈に合わせて自然な形に変えてください（例：「行く」→「行きます」、「行くでしょう」、「行くかもしれません」など）。",
    ),
    # ── Task 2.2 Slider Task ──
    slider_title = dict(
        en="Part 2: Certainty Ratings",
        fr="Partie 2: Évaluation de la certitude",
        de="Teil 2: Bewertung der Sicherheit",
        ja="パート2: 確信度の評価",
    ),
    slider_prompt = dict(
        en="Please read each sentence and indicate how CERTAIN the speaker sounds to you (0% = Impossible, 100% = Certain).",
        fr="Veuillez lire chaque phrase et indiquer à quel point l'orateur vous semble CERTAIN (0% = Impossible, 100% = Certain).",
        de="Bitte geben Sie für jeden Satz an, wie SICHER der Sprecher klingt (0% = Unmöglich, 100% = Sicher).",
        ja="各文を読み、話し手がどの程度「確信」を持っていると感じるかを示してください（0% = ありえない、100% = 確実）。",
    ),
    # ── Slider Label Translations ──
    impossible = dict(
        en="Impossible",
        fr="Impossible",
        de="Unmöglich",
        ja="ありえない"
    ),
    certain = dict(
        en="Certain",
        fr="Certain",
        de="Sicher",
        ja="確実"
    ),
)


def ui_dict(lang):
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ═══════════════════════════════════════════════════════════
# TASK 2.1 SCENARIOS (Production)
# 4 Conversations: (Prediction) x (Tmr/3Months) x (Low/Med/High Prob)
# ═══════════════════════════════════════════════════════════
SCENARIOS = dict(
    en=[
        # 1. Tomorrow / 60%
        dict(
            id='s1',
            context_header="Situation: Exam Tomorrow (Unsure)",
            context_prob="60% Likely",
            text="""
            <p><strong>A:</strong> Do you think the exam tomorrow is going to be difficult?</p>
            <p><strong>B:</strong> Well, Professor Green is usually pretty easy on us...</p>
            <p class='target'>...so I think we {{1}} <em>(pass)</em>.</p>
            """
        ),
        # 2. Tomorrow / 100%
        dict(
            id='s2',
            context_header="Situation: Meeting Schedule",
            context_prob="100% Certain",
            text="""
            <p><strong>A:</strong> When is the committee meeting tonight?</p>
            <p><strong>B:</strong> I just checked the official schedule...</p>
            <p class='target'>...it {{1}} <em>(be)</em> at 7:00 PM.</p>
            """
        ),
        # 3. 3 Months / 40%
        dict(
            id='s3',
            context_header="Situation: Project Deadline (3 Months)",
            context_prob="40% Likely",
            text="""
            <p><strong>A:</strong> How is the new software project going?</p>
            <p><strong>B:</strong> Honestly, the team is very far behind and we have no budget left.</p>
            <p class='target'>...I'm worried the project {{1}} <em>(fail)</em>.</p>
            """
        ),
        # 4. 3 Months / 100%
        dict(
            id='s4',
            context_header="Situation: School Calendar",
            context_prob="100% Certain",
            text="""
            <p><strong>A:</strong> Do we have classes in the summer?</p>
            <p><strong>B:</strong> No, looking at the university calendar...</p>
            <p class='target'>...the semester {{1}} <em>(end)</em> in June.</p>
            """
        )
    ],
    ja=[
        # 1. Tomorrow / 60%
        dict(
            id='s1',
            context_header="状況: 明日の試験（不確実）",
            context_prob="60% の確率",
            text="""
            <p><strong>A:</strong> 明日の試験は難しいと思いますか？</p>
            <p><strong>B:</strong> まあ、グリーン先生は普段優しいから…</p>
            <p class='target'>…たぶん私たちは{{1}}と思います。 <em>(合格する)</em></p>
            """
        ),
        # 2. Tomorrow / 100%
        dict(
            id='s2',
            context_header="状況: 会議のスケジュール",
            context_prob="100% 確実",
            text="""
            <p><strong>A:</strong> 今夜の委員会は何時からですか？</p>
            <p><strong>B:</strong> 公式スケジュールを確認したところ…</p>
            <p class='target'>…{{1}}7時です。 <em>(ある/行われる)</em></p>
            """
        ),
        # 3. 3 Months / 40%
        dict(
            id='s3',
            context_header="状況: プロジェクトの締め切り（3ヶ月後）",
            context_prob="40% の確率",
            text="""
            <p><strong>A:</strong> 新しいソフトのプロジェクトはどう？</p>
            <p><strong>B:</strong> 正直、チームは大幅に遅れてるし、予算もないんだ。</p>
            <p class='target'>…プロジェクトが{{1}}んじゃないかと心配だよ。 <em>(失敗する)</em></p>
            """
        ),
        # 4. 3 Months / 100%
        dict(
            id='s4',
            context_header="状況: 学校のカレンダー",
            context_prob="100% 確実",
            text="""
            <p><strong>A:</strong> 夏に授業はあるの？</p>
            <p><strong>B:</strong> いや、大学のカレンダーを見ると…</p>
            <p class='target'>…学期は6月に{{1}}。 <em>(終わる)</em></p>
            """
        )
    ]
)


# ═══════════════════════════════════════════════════════════
# TASK 2.2 SENTENCES (Perception / Subjective Probability)
# Based on Robertson et al. (2023) — 13 items for English.
#
# DESIGN RATIONALE:
# - English & Japanese: 13 items (direct mapping of Robertson items).
# - French: 14 items testing French-specific FTR constructions
#   (futur simple, futur proche, conditionnel, subjunctive triggers,
#    modal adverbs, devoir épistémique, présent futur).
# - German: 14 items testing German-specific FTR constructions
#   (werden+Inf, Präsens futur, modal verbs können/dürfte/soll/mag,
#    Konjunktiv II, modal particles wohl/bestimmt/vielleicht/
#    wahrscheinlich/sicherlich).
#
# All items use the same propositional content ("rain next week")
# to isolate the effect of grammatical construction on perceived
# certainty.
# ═══════════════════════════════════════════════════════════
SLIDER_ITEMS = dict(
    # ── English: 13 items (Robertson et al., 2023) ──
    en=[
        "It is going to rain next week.",           #  1. be going to
        "It will rain next week.",                   #  2. will (bare)
        "I think it will rain next week.",           #  3. I think + will
        "It will definitely rain next week.",        #  4. will + definitely
        "It may rain next week.",                    #  5. may
        "It could rain next week.",                  #  6. could
        "It might rain next week.",                  #  7. might
        "It will certainly rain next week.",         #  8. will + certainly
        "I think it is going to rain next week.",    #  9. I think + be going to
        "It possibly will rain next week.",          # 10. possibly + will
        "It should rain next week.",                 # 11. should
        "It probably will rain next week.",          # 12. probably + will
        "It is raining next week.",                  # 13. present progressive (futurate)
    ],

    # ── Japanese: 13 items (translation of English constructions) ──
    # Maps each English FTR construction to its closest Japanese
    # equivalent, covering the spectrum from low to high certainty.
    ja=[
        "来週、雨が降るだろう。",                     #  1. ～だろう (conjecture, neutral) ≈ be going to
        "来週、雨が降ります。",                       #  2. ～ます (polite, declarative) ≈ will
        "来週、雨が降ると思います。",                  #  3. ～と思います (I think) ≈ I think + will
        "来週、間違いなく雨が降ります。",              #  4. 間違いなく (without doubt) ≈ will definitely
        "来週、雨が降るかもしれない。",                #  5. ～かもしれない (possibility) ≈ may
        "来週、雨が降りうる。",                       #  6. ～うる (potential/capable of) ≈ could
        "来週、雨が降るかもしれません。",              #  7. ～かもしれません (polite possibility) ≈ might
        "来週、必ず雨が降ります。",                   #  8. 必ず (certainly) ≈ will certainly
        "来週、雨が降るんじゃないかと思います。",       #  9. ～んじゃないかと思う (hedged opinion) ≈ I think + going to
        "来週、ひょっとしたら雨が降るかもしれない。",    # 10. ひょっとしたら～かもしれない (remote poss.) ≈ possibly will
        "来週、雨が降るはずです。",                   # 11. ～はずです (expectation) ≈ should
        "来週、おそらく雨が降るでしょう。",            # 12. おそらく～でしょう (probably) ≈ probably will
        "来週、雨が降る。",                          # 13. dictionary form (casual declarative) ≈ present progressive futurate
    ],

    # ── French: 14 items (French-specific FTR constructions) ──
    # Tests the full range of French future-time reference forms,
    # including futur simple vs. futur proche, modal constructions,
    # conditional, and subjunctive-triggering expressions.
    fr=[
        "Il va pleuvoir la semaine prochaine.",                #  1. Futur proche (aller + inf) — near/planned future
        "Il pleuvra la semaine prochaine.",                    #  2. Futur simple — general future prediction
        "Je pense qu'il va pleuvoir la semaine prochaine.",    #  3. Je pense que + futur proche — hedged opinion (near)
        "Je pense qu'il pleuvra la semaine prochaine.",        #  4. Je pense que + futur simple — hedged opinion (general)
        "Il pleuvra certainement la semaine prochaine.",       #  5. Futur simple + certainement — high certainty
        "Il pleuvra sans doute la semaine prochaine.",         #  6. Futur simple + sans doute — probable (≈ probably)
        "Il pourrait pleuvoir la semaine prochaine.",          #  7. Conditionnel (pouvoir) — possibility
        "Il devrait pleuvoir la semaine prochaine.",           #  8. Conditionnel (devoir) — expectation/should
        "Il se peut qu'il pleuve la semaine prochaine.",       #  9. Il se peut que + subjonctif — impersonal possibility
        "Il est possible qu'il pleuve la semaine prochaine.",  # 10. Il est possible que + subjonctif — possible
        "Peut-être qu'il pleuvra la semaine prochaine.",       # 11. Peut-être que + futur simple — perhaps
        "Il pleuvrait la semaine prochaine.",                  # 12. Conditionnel (reportatif/hearsay) — rumour/reported
        "Il va sûrement pleuvoir la semaine prochaine.",       # 13. Futur proche + sûrement — surely (near future)
        "Il pleut la semaine prochaine.",                      # 14. Présent à valeur de futur — present-as-future
    ],

    # ── German: 14 items (German-specific FTR constructions) ──
    # Tests werden+Infinitiv, Präsens with future meaning,
    # modal verbs (können, dürfen, sollen, mögen), Konjunktiv II,
    # and the rich system of German modal particles/adverbs.
    de=[
        "Es wird nächste Woche regnen.",                       #  1. werden + Inf — standard future
        "Es regnet nächste Woche.",                            #  2. Präsens (futurisch) — present-as-future
        "Ich denke, es wird nächste Woche regnen.",            #  3. Ich denke + werden — hedged opinion
        "Es wird bestimmt nächste Woche regnen.",              #  4. werden + bestimmt — definite certainty
        "Es wird sicherlich nächste Woche regnen.",            #  5. werden + sicherlich — certainly
        "Es könnte nächste Woche regnen.",                     #  6. Konjunktiv II (können) — could/possibility
        "Es kann nächste Woche regnen.",                       #  7. können (Indikativ) — can/may
        "Es dürfte nächste Woche regnen.",                     #  8. dürfen (Konj. II) — ought to/likely
        "Es mag nächste Woche regnen.",                        #  9. mögen (Indikativ) — may (literary/formal)
        "Es soll nächste Woche regnen.",                       # 10. sollen — is said to / reported
        "Vielleicht regnet es nächste Woche.",                 # 11. vielleicht + Präsens — perhaps
        "Es wird wohl nächste Woche regnen.",                  # 12. werden + wohl — probably (modal particle)
        "Es wird wahrscheinlich nächste Woche regnen.",        # 13. werden + wahrscheinlich — probably (adverb)
        "Ich glaube, es regnet nächste Woche.",                # 14. Ich glaube + Präsens — I believe (colloquial)
    ],
)


# ═══════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    language = models.StringField(initial='en')

    # Store responses for Task 2.1 (Conversation Fill-in)
    # Format: {"s1": {"1": "will pass"}, "s2": ...}
    t2_production_data = models.LongStringField(initial='{}', blank=True)

    # Store responses for Task 2.2 (Sliders)
    # Format: {"It will rain...": 80, "It might...": 30}
    t2_perception_data = models.LongStringField(initial='{}', blank=True)


# ═══════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════

# Updated _ctx to accept 'progress'
def _ctx(player, progress):
    """Helper for template context"""
    lang = player.language
    return dict(lang=lang, ui=ui_dict(lang), progress=progress)


class Task2Intro(Page):
    @staticmethod
    def vars_for_template(player):
        lang = player.session.config.get('language', 'en')
        player.language = lang
        # Continue from Task 1: 50%
        return _ctx(player, 50)


class Task2Item(Page):
    template_name = 'Task2/Task2Item.html'
    form_model = 'player'
    form_fields = ['t2_production_data']

    # Updated to accept 'progress' argument
    @staticmethod
    def vars_for_template(player, scenario_index, progress):
        lang = player.language
        scenarios = SCENARIOS.get(lang, SCENARIOS['en'])

        if scenario_index >= len(scenarios):
            scenario = scenarios[0]
        else:
            scenario = scenarios[scenario_index]

        return dict(
            scenario=scenario,
            existing=player.t2_production_data or '{}',
            **_ctx(player, progress)
        )


class Task2Item1(Task2Item):
    @staticmethod
    def vars_for_template(player):
        # Progress: 60%
        return Task2Item.vars_for_template(player, 0, 60)


class Task2Item2(Task2Item):
    @staticmethod
    def vars_for_template(player):
        # Progress: 70%
        return Task2Item.vars_for_template(player, 1, 70)


class Task2Item3(Task2Item):
    @staticmethod
    def vars_for_template(player):
        # Progress: 80%
        return Task2Item.vars_for_template(player, 2, 80)


class Task2Item4(Task2Item):
    @staticmethod
    def vars_for_template(player):
        # Progress: 90%
        return Task2Item.vars_for_template(player, 3, 90)


class Task2Slider(Page):
    form_model = 'player'
    form_fields = ['t2_perception_data']

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        items = SLIDER_ITEMS.get(lang, SLIDER_ITEMS['en'])
        return dict(
            items=items,
            existing=player.t2_perception_data or '{}',
            # Progress: 98%
            **_ctx(player, 98)
        )


page_sequence = [
    Task2Intro,
    Task2Item1,
    Task2Item2,
    Task2Item3,
    Task2Item4,
    Task2Slider,
]