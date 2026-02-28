from otree.api import *
import json

doc = """
Task 2: FTR Elicitation (Production) & Subjective Probability (Perception).
Design based on Robertson et al. (2023).
Languages: English (en), French (fr), German (de), Japanese (ja).

Task 2.1 Design (SCENARIOS):
  - 27 Prediction items: 3 items × 3 modality (uncertain/neutral/certain) × 3 temporal distance
                         (tomorrow / six months / two years)
  - 3  Scheduling controls: 1 item × 3 temporal distances (neutral modality only)
  - 3  Intention controls:  1 item × 3 temporal distances (neutral modality only)
  Total: 33 items, each presented as an individual page.

  Modality conditions follow Robertson (2023):
    uncertain = ~40–60 % (low certainty, epistemic hedging expected)
    neutral   = no certainty cue (participant's default FTR encoding)
    certain   = 100 % (high certainty, strong assertion expected)

  Item sources:
    - Robertson (2023) Table A.5 FTR-elicitation questionnaire
    - Uploaded pilot item bank (Lin / Lumi)
    - New items adapted from both sources with temporal distance adjusted

Key linguistic note for German:
  Target sentences are structured so the verb blank falls at the END of the clause,
  accommodating both Präsens (finite verb) and Futur I (werden + Infinitiv at clause-end)
  without triggering separable-verb word-order problems.

Task 2.2 Design (SLIDER_ITEMS):
  Subjective certainty ratings on a 0–100 % slider.
  - English / Japanese: 13 items (Robertson et al. construction inventory)
  - French:             14 items (futur simple, futur proche, conditionnel,
                                  subjonctif triggers, modal adverbs, présent futurate)
  - German:             14 items (werden+Inf, Präsens futurisch, modal verbs,
                                  Konjunktiv II, modal particles/adverbs)
  All items use identical propositional content ("rain next week") to isolate
  the effect of grammatical construction on perceived certainty.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# ═══════════════════════════════════════════════════════════
# UI STRINGS
# ═══════════════════════════════════════════════════════════
UI = dict(
    btn_next    = dict(en='Next',    fr='Suivant', de='Weiter', ja='次へ'),
    btn_submit  = dict(en='Submit',  fr='Soumettre', de='Absenden', ja='送信'),
    required_msg = dict(
        en='Please answer all items.',
        fr='Veuillez répondre à toutes les questions.',
        de='Bitte beantworten Sie alle Fragen.',
        ja='すべての項目に回答してください。',
    ),
    # ── Task 2 Intro ──
    intro_title = dict(en='Part 2', fr='Partie 2', de='Teil 2', ja='パート2'),
    intro_text  = dict(
        en='You are now moving on to the second part of the study. Please click the button below to continue.',
        fr="Vous passez maintenant à la deuxième partie de l'étude. Veuillez cliquer sur le bouton ci-dessous pour continuer.",
        de='Sie fahren nun mit dem zweiten Teil der Studie fort. Bitte klicken Sie auf die Schaltfläche unten, um fortzufahren.',
        ja='調査の第2パートに移ります。下のボタンをクリックして進んでください。',
    ),
    # ── Task 2.1 Instructions ──
    # Wording follows Robertson et al. (2023, p.14–15):
    #   "There are no correct answers."
    #   Respond "as though you were speaking to a close friend."
    #   The certainty badge means: "This indicates how certain you are about
    #   what you are saying — please imagine you are this certain and write
    #   down what you would say."
    t2_instructions = dict(
        en=(
            "There are no correct answers. "
            "Please complete the sentence as though you were speaking to a close friend. "
            "Use the verb shown in italics as a guide, and write whatever feels most natural to you. "
            "Where a certainty percentage is shown, imagine you are exactly that certain "
            "and write what you would say."
        ),
        fr=(
            "Il n'y a pas de bonnes ou de mauvaises réponses. "
            "Complétez la phrase comme si vous parliez à un(e) ami(e) proche. "
            "Le verbe en italique est une indication — écrivez ce qui vous semble le plus naturel. "
            "Lorsqu'un pourcentage de certitude est indiqué, imaginez que vous êtes exactement "
            "aussi certain(e) et écrivez ce que vous diriez."
        ),
        de=(
            "Es gibt keine richtigen oder falschen Antworten. "
            "Vervollständigen Sie den Satz, als würden Sie mit einem guten Freund / einer guten Freundin sprechen. "
            "Das kursiv gedruckte Verb dient als Hinweis — schreiben Sie, was sich für Sie am natürlichsten anfühlt. "
            "Wenn ein Sicherheitsprozentsatz angegeben ist, stellen Sie sich vor, genau so sicher zu sein, "
            "und schreiben Sie, was Sie sagen würden."
        ),
        ja=(
            "正解・不正解はありません。"
            "親しい友人に話しかけるつもりで文を完成させてください。"
            "斜体の動詞はヒントです——最も自然に感じる表現を書いてください。"
            "確率（%）が表示されている場合は、自分がちょうどその確率で確信しているとイメージして、"
            "そのときに言うであろう表現を書いてください。"
        ),
    ),
    # ── Task 2.2 Slider ──
    # Wording follows Robertson et al. (2023, p.18):
    #   "You will be asked to indicate how much certainty each statement
    #    expresses in YOUR eyes."
    #   "Indicate how much certainty YOU would be expressing in the
    #    following statement."
    #   Scale: "uncertain" (0) → "certain" (100).
    slider_title = dict(
        en='Part 2: Certainty Ratings',
        fr='Partie 2 : Évaluation de la certitude',
        de='Teil 2: Bewertung der Gewissheit',
        ja='パート2：確信度の評価',
    ),
    slider_prompt = dict(
        en=(
            "You will be asked to indicate how much certainty each statement expresses in YOUR eyes. "
            "For each sentence, indicate how much certainty YOU would be expressing if you said it "
            "(0 = Uncertain, 100 = Certain)."
        ),
        fr=(
            "Vous allez indiquer à quel point chaque énoncé exprime de la certitude À VOS YEUX. "
            "Pour chaque phrase, indiquez quelle quantité de certitude VOUS exprimeriez en la disant "
            "(0 = Incertain(e), 100 = Certain(e))."
        ),
        de=(
            "Sie werden angeben, wie viel Gewissheit jede Aussage IN IHREN AUGEN ausdrückt. "
            "Geben Sie für jeden Satz an, wie viel Gewissheit SIE ausdrücken würden, wenn Sie ihn sagen würden "
            "(0 = Unsicher, 100 = Sicher)."
        ),
        ja=(
            "それぞれの文があなたの目にどれだけの確信を表しているかを示してください。"
            "各文について、「もし自分がこれを言ったとしたら、どれだけの確信を表していることになるか」を答えてください"
            "（0 = 不確か、100 = 確実）。"
        ),
    ),
    # Slider endpoint labels: "uncertain" → "certain" (following Robertson 2023)
    impossible = dict(en='Uncertain', fr='Incertain(e)', de='Unsicher', ja='不確か'),
    certain    = dict(en='Certain',   fr='Certain(e)',   de='Sicher',   ja='確実'),
)


def ui_dict(lang):
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ═══════════════════════════════════════════════════════════
# TASK 2.1 SCENARIOS  (Production / FTR elicitation)
#
# Structure: single master list; each scenario dict has multilingual
# sub-dicts for context_header, context_prob, and text.
# _get_scenario() extracts the language-specific version at runtime.
#
# Field glossary:
#   id            – unique slug (used as data key)
#   ftr_mode      – 'prediction' | 'scheduling' | 'intention'
#   temporal      – 'tomorrow' | 'six_months' | 'two_years'
#   modality      – 'uncertain' | 'neutral' | 'certain'
#   certainty     – numeric seed (40/50/60/100) or None for neutral
#   context_header – displayed title box (per language)
#   context_prob  – displayed badge (empty string for neutral)
#   text          – HTML snippet; {{N}} → input blank; verb hint in <em>
#
# German note: blank is placed at CLAUSE END so that both
#   Präsens (finite verb) and Futur I (werden + Infinitiv) are
#   grammatically natural without separable-verb word-order issues.
# ═══════════════════════════════════════════════════════════
SCENARIOS = [

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — TOMORROW
    # ══════════════════════════════════════════════════════

    # P-T1  Tomorrow / Uncertain ~50 %
    dict(
        id='p_tmr_unc_1',
        ftr_mode='prediction', temporal='tomorrow', modality='uncertain', certainty=50,
        context_header=dict(
            en="Exam Tomorrow",
            fr="Examen demain",
            de="Prüfung morgen",
            ja="明日の試験",
        ),
        context_prob=dict(
            en="~50 % Likely",
            fr="~50 % probable",
            de="~50 % wahrscheinlich",
            ja="約50 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Do you think the exam tomorrow will be hard? We've studied so much...</p>
<p><strong>B:</strong> Maybe, but I never know with Professor Johnson...</p>
<p class='target'>...so I think we {{1}} <em>(pass)</em>.</p>
""",
            fr="""
<p><strong>A :</strong> Tu penses que l'examen demain va être difficile ? On a beaucoup révisé...</p>
<p><strong>B :</strong> Peut-être, mais avec le professeur Martin, on ne sait jamais...</p>
<p class='target'>...alors je pense qu'on {{1}} <em>(réussir)</em>.</p>
""",
            de="""
<p><strong>A:</strong> Glaubst du, die Prüfung morgen wird schwer? Wir haben so viel gelernt...</p>
<p><strong>B:</strong> Vielleicht, aber bei Professor Müller weiß man nie...</p>
<p class='target'>...Ich denke, wir werden morgen {{1}} <em>(bestehen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>明日の試験は難しいと思う？すごく勉強したんだけど…</p>
<p><strong>B：</strong>どうかな。ジョンソン先生のことだから何とも言えないけど…</p>
<p class='target'>…だから、私たちは{{1}}と思う。<em>（合格する）</em></p>
""",
        ),
    ),

    # P-T2  Tomorrow / Uncertain ~40 %
    dict(
        id='p_tmr_unc_2',
        ftr_mode='prediction', temporal='tomorrow', modality='uncertain', certainty=40,
        context_header=dict(
            en="Today's Weather",
            fr="La météo aujourd'hui",
            de="Wetter heute",
            ja="今日の天気",
        ),
        context_prob=dict(
            en="~40 % Likely",
            fr="~40 % probable",
            de="~40 % wahrscheinlich",
            ja="約40 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Should I bring an extra warm jacket for later? The sky looks odd.</p>
<p><strong>B:</strong> It's hard to say — the forecast is unclear today...</p>
<p class='target'>...it {{1}} <em>(snow)</em> this afternoon.</p>
""",
            fr="""
<p><strong>A :</strong> Est-ce que je devrais prendre un manteau chaud pour plus tard ? Le ciel a l'air bizarre.</p>
<p><strong>B :</strong> C'est difficile à dire — la météo n'est pas très claire aujourd'hui...</p>
<p class='target'>...il {{1}} <em>(neiger)</em> cet après-midi.</p>
""",
            de="""
<p><strong>A:</strong> Soll ich für später eine wärmere Jacke mitnehmen? Der Himmel sieht seltsam aus.</p>
<p><strong>B:</strong> Schwer zu sagen — die Vorhersage ist heute nicht klar...</p>
<p class='target'>...heute Nachmittag könnte es {{1}} <em>(schneien)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>後で厚手のジャケットを持っていった方がいい？空が変な感じ。</p>
<p><strong>B：</strong>なんとも言えないね。今日の天気予報がはっきりしないから…</p>
<p class='target'>…今日の午後{{1}}かもしれないよ。<em>（雪が降る）</em></p>
""",
        ),
    ),

    # P-T3  Tomorrow / Neutral
    dict(
        id='p_tmr_neu_1',
        ftr_mode='prediction', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Market Investment",
            fr="Investissement en bourse",
            de="Marktinvestition",
            ja="市場への投資",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> I was thinking about putting money into derivatives.</p>
<p><strong>B:</strong> Don't — the market is completely fraudulent...</p>
<p class='target'>...it {{1}} <em>(crash)</em> tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> Je pensais investir dans des produits dérivés.</p>
<p><strong>B :</strong> Non — le marché est complètement frauduleux...</p>
<p class='target'>...ça {{1}} <em>(s'effondrer)</em> demain.</p>
""",
            de="""
<p><strong>A:</strong> Ich dachte daran, Geld in Derivate zu stecken.</p>
<p><strong>B:</strong> Auf keinen Fall — der Markt ist völlig betrügerisch...</p>
<p class='target'>...morgen wird er {{1}} <em>(kollabieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>デリバティブに投資しようと思っているんだけど。</p>
<p><strong>B：</strong>やめて——あの市場は完全に詐欺だから…</p>
<p class='target'>…明日{{1}}よ。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # P-T4  Tomorrow / Neutral
    dict(
        id='p_tmr_neu_2',
        ftr_mode='prediction', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Tonight's Dinner Party",
            fr="Dîner ce soir",
            de="Abendessen heute Abend",
            ja="今夜のディナーパーティー",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> You should come to the dinner tonight — your friend fancies John.</p>
<p><strong>B:</strong> Really? Is he actually going to be there?</p>
<p class='target'><strong>A:</strong> Yes! John {{1}} <em>(be)</em> there tonight.</p>
""",
            fr="""
<p><strong>A :</strong> Tu devrais venir au dîner ce soir — tu sais que ton amie s'intéresse à Jean.</p>
<p><strong>B :</strong> Vraiment ? Il va vraiment être là ?</p>
<p class='target'><strong>A :</strong> Oui ! Jean {{1}} <em>(être)</em> là ce soir.</p>
""",
            de="""
<p><strong>A:</strong> Du solltest heute Abend zum Essen kommen — deine Freundin steht auf Jan.</p>
<p><strong>B:</strong> Wirklich? Wird er wirklich da sein?</p>
<p class='target'><strong>A:</strong> Ja! Heute Abend wird Jan {{1}} <em>(da sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今夜のディナーに来てよ——あなたの友達がジョンに気があるの知ってるでしょ。</p>
<p><strong>B：</strong>本当に？彼も来るの？</p>
<p class='target'><strong>A：</strong>うん！ジョンも今夜{{1}}から。<em>（いる）</em></p>
""",
        ),
    ),

    # P-T5  Tomorrow / Certain 100 %
    dict(
        id='p_tmr_cer_1',
        ftr_mode='prediction', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Weather Forecast",
            fr="Prévisions météo",
            de="Wettervorhersage",
            ja="天気予報",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Should I pack my bathing suit for tomorrow?</p>
<p><strong>B:</strong> Absolutely. I just checked the official weather service...</p>
<p class='target'>...the temperature {{1}} <em>(hit)</em> 40 degrees tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> Est-ce que je devrais prendre mon maillot de bain pour demain ?</p>
<p><strong>B :</strong> Absolument. Je viens de consulter la météo officielle...</p>
<p class='target'>...la température {{1}} <em>(atteindre)</em> 40 degrés demain.</p>
""",
            de="""
<p><strong>A:</strong> Soll ich meinen Badeanzug für morgen einpacken?</p>
<p><strong>B:</strong> Unbedingt. Ich habe gerade den offiziellen Wetterdienst gecheckt...</p>
<p class='target'>...morgen wird die Temperatur 40 Grad {{1}} <em>(erreichen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>明日のために水着を持っていった方がいい？</p>
<p><strong>B：</strong>絶対に。公式の気象サービスを確認したところ…</p>
<p class='target'>…明日の気温は40度に{{1}}よ。<em>（達する）</em></p>
""",
        ),
    ),

    # P-T6  Tomorrow / Certain 100 %
    dict(
        id='p_tmr_cer_2',
        ftr_mode='prediction', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Financial Markets",
            fr="Marchés financiers",
            de="Finanzmärkte",
            ja="金融市場",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Look at these indicators. Every single sign is pointing the same way.</p>
<p><strong>B:</strong> So you're saying...</p>
<p class='target'><strong>A:</strong> The market {{1}} <em>(crash)</em> tomorrow. It's unavoidable.</p>
""",
            fr="""
<p><strong>A :</strong> Regarde ces indicateurs. Tous les signaux pointent dans le même sens.</p>
<p><strong>B :</strong> Donc tu dis que...</p>
<p class='target'><strong>A :</strong> Le marché {{1}} <em>(s'effondrer)</em> demain. C'est inévitable.</p>
""",
            de="""
<p><strong>A:</strong> Schau dir diese Indikatoren an. Alle Zeichen zeigen in dieselbe Richtung.</p>
<p><strong>B:</strong> Du sagst also...</p>
<p class='target'><strong>A:</strong> Morgen wird der Markt {{1}} <em>(kollabieren)</em>. Das ist unvermeidlich.</p>
""",
            ja="""
<p><strong>A：</strong>これらの指標を見て。全ての兆候が同じ方向を指している。</p>
<p><strong>B：</strong>つまり…</p>
<p class='target'><strong>A：</strong>市場は明日{{1}}。<em>（崩壊する）</em>避けられない。</p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — SIX MONTHS
    # ══════════════════════════════════════════════════════

    # P-6M1  Six months / Uncertain ~40 %
    dict(
        id='p_6mo_unc_1',
        ftr_mode='prediction', temporal='six_months', modality='uncertain', certainty=40,
        context_header=dict(
            en="Election Outcome",
            fr="Résultat des élections",
            de="Wahlergebnis",
            ja="選挙結果",
        ),
        context_prob=dict(
            en="~40 % Likely",
            fr="~40 % probable",
            de="~40 % wahrscheinlich",
            ja="約40 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> It's January. What do you think will happen to the Conservative Party this year?</p>
<p><strong>B:</strong> I really can't say for sure. Looking at the polls right now...</p>
<p class='target'>...I think they {{1}} <em>(lose)</em> this summer.</p>
""",
            fr="""
<p><strong>A :</strong> On est en janvier. Que pensez-vous qu'il arrivera au Parti conservateur cette année ?</p>
<p><strong>B :</strong> Je ne peux vraiment pas dire avec certitude. En regardant les sondages maintenant...</p>
<p class='target'>...je pense qu'ils {{1}} <em>(perdre)</em> cet été.</p>
""",
            de="""
<p><strong>A:</strong> Es ist Januar. Was glauben Sie, was dieses Jahr mit der Konservativen Partei passiert?</p>
<p><strong>B:</strong> Das kann ich wirklich nicht mit Sicherheit sagen. Wenn man die Umfragen ansieht...</p>
<p class='target'>...ich glaube, diesen Sommer werden sie {{1}} <em>(verlieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今は1月。今年の保守党はどうなると思いますか？</p>
<p><strong>B：</strong>確かなことは言えないけど、今の世論調査を見ると…</p>
<p class='target'>…今年の夏には彼らは{{1}}と思います。<em>（負ける）</em></p>
""",
        ),
    ),

    # P-6M2  Six months / Uncertain ~60 %
    dict(
        id='p_6mo_unc_2',
        ftr_mode='prediction', temporal='six_months', modality='uncertain', certainty=60,
        context_header=dict(
            en="Summer Weather Outlook",
            fr="Prévisions météo d'été",
            de="Sommerliche Wetteraussichten",
            ja="夏の天気予報",
        ),
        context_prob=dict(
            en="~60 % Likely",
            fr="~60 % probable",
            de="~60 % wahrscheinlich",
            ja="約60 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> [In spring] The broad weather outlook for the next few months is fairly unstable. What's your take?</p>
<p><strong>B:</strong> Well, I wouldn't count on it...</p>
<p class='target'>...but we {{1}} <em>(see)</em> some sunny weather this summer.</p>
""",
            fr="""
<p><strong>A :</strong> [Au printemps] Les perspectives météo pour les prochains mois sont assez instables. Qu'en pensez-vous ?</p>
<p><strong>B :</strong> Eh bien, je n'y compterais pas trop...</p>
<p class='target'>...mais on {{1}} <em>(voir)</em> du beau temps cet été.</p>
""",
            de="""
<p><strong>A:</strong> [Im Frühling] Die allgemeinen Wetteraussichten für die nächsten Monate sind recht unbeständig. Was meinen Sie?</p>
<p><strong>B:</strong> Nun, ich würde nicht fest damit rechnen...</p>
<p class='target'>...aber diesen Sommer werden wir wohl etwas Sonnenschein {{1}} <em>(sehen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>[春の話]これからの数ヶ月の天気の見通しはかなり不安定。どう思いますか？</p>
<p><strong>B：</strong>そうですね、あまり期待しない方がいいかもしれないけど…</p>
<p class='target'>…今年の夏には晴れた天気が{{1}}でしょう。<em>（見られる）</em></p>
""",
        ),
    ),

    # P-6M3  Six months / Neutral
    dict(
        id='p_6mo_neu_1',
        ftr_mode='prediction', temporal='six_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Tech Industry Investment",
            fr="Investissement dans la tech",
            de="Tech-Investition",
            ja="テクノロジー業界への投資",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> I'm thinking about putting money into the tech industry right now.</p>
<p><strong>B:</strong> Don't bother with that...</p>
<p class='target'>...Silicon Valley {{1}} <em>(crash)</em> within six months.</p>
""",
            fr="""
<p><strong>A :</strong> Je pense à investir dans le secteur technologique en ce moment.</p>
<p><strong>B :</strong> Ne te donne pas cette peine...</p>
<p class='target'>...la Silicon Valley {{1}} <em>(s'effondrer)</em> dans six mois.</p>
""",
            de="""
<p><strong>A:</strong> Ich denke daran, jetzt Geld in die Technologiebranche zu stecken.</p>
<p><strong>B:</strong> Das lohnt sich nicht...</p>
<p class='target'>...in sechs Monaten wird das Silicon Valley {{1}} <em>(kollabieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今テクノロジー業界に投資しようと思っているんだ。</p>
<p><strong>B：</strong>やめた方がいいよ…</p>
<p class='target'>…シリコンバレーは6ヶ月以内に{{1}}よ。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # P-6M4  Six months / Neutral
    dict(
        id='p_6mo_neu_2',
        ftr_mode='prediction', temporal='six_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Election Strategy",
            fr="Stratégie électorale",
            de="Wahlstrategie",
            ja="選挙戦略",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> It's July. Which party do you recommend?</p>
<p><strong>B:</strong> Don't waste your vote on the Liberal Party...</p>
<p class='target'>...they {{1}} <em>(lose)</em> in January.</p>
""",
            fr="""
<p><strong>A :</strong> On est en juillet. Quel parti recommandez-vous ?</p>
<p><strong>B :</strong> Ne gâchez pas votre vote sur le Parti libéral...</p>
<p class='target'>...ils {{1}} <em>(perdre)</em> en janvier.</p>
""",
            de="""
<p><strong>A:</strong> Es ist Juli. Welche Partei empfehlen Sie?</p>
<p><strong>B:</strong> Verschwenden Sie Ihre Stimme nicht an die Liberalen...</p>
<p class='target'>...im Januar werden sie {{1}} <em>(verlieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>7月の話。どの政党に投票するのがよいですか？</p>
<p><strong>B：</strong>自由党に票を無駄にしないで…</p>
<p class='target'>…彼らは1月に{{1}}から。<em>（負ける）</em></p>
""",
        ),
    ),

    # P-6M5  Six months / Certain 100 %
    dict(
        id='p_6mo_cer_1',
        ftr_mode='prediction', temporal='six_months', modality='certain', certainty=100,
        context_header=dict(
            en="Economic Bubble",
            fr="Bulle économique",
            de="Wirtschaftsblase",
            ja="経済バブル",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> I'm thinking about investing in the Chinese market.</p>
<p><strong>B:</strong> Absolutely not. There is clearly a bubble — all the indicators show it...</p>
<p class='target'>...it {{1}} <em>(crash)</em> within six months.</p>
""",
            fr="""
<p><strong>A :</strong> Je pense à investir dans le marché chinois.</p>
<p><strong>B :</strong> Hors de question. Il y a clairement une bulle — tous les indicateurs le montrent...</p>
<p class='target'>...ça {{1}} <em>(s'effondrer)</em> dans les six mois.</p>
""",
            de="""
<p><strong>A:</strong> Ich denke daran, in den chinesischen Markt zu investieren.</p>
<p><strong>B:</strong> Auf keinen Fall. Da gibt es eindeutig eine Blase — alle Indikatoren zeigen es...</p>
<p class='target'>...innerhalb von sechs Monaten wird es {{1}} <em>(kollabieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>中国市場に投資しようと思っているんだけど。</p>
<p><strong>B：</strong>絶対ダメ。明らかにバブルがある——全ての指標がそれを示してる…</p>
<p class='target'>…6ヶ月以内に{{1}}よ。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # P-6M6  Six months / Certain 100 %
    dict(
        id='p_6mo_cer_2',
        ftr_mode='prediction', temporal='six_months', modality='certain', certainty=100,
        context_header=dict(
            en="Medical Recovery",
            fr="Récupération médicale",
            de="Medizinische Genesung",
            ja="医療回復",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>Doctor:</strong> This is just stress — I see it all the time. Follow my advice carefully.</p>
<p><strong>Patient:</strong> Will I get better?</p>
<p class='target'><strong>Doctor:</strong> In a few months you {{1}} <em>(feel)</em> much better. I am absolutely certain of it.</p>
""",
            fr="""
<p><strong>Médecin :</strong> C'est juste du stress — je le vois tout le temps. Suivez bien mes conseils.</p>
<p><strong>Patient :</strong> Est-ce que je vais aller mieux ?</p>
<p class='target'><strong>Médecin :</strong> Dans quelques mois vous {{1}} <em>(se sentir)</em> beaucoup mieux. J'en suis absolument certain.</p>
""",
            de="""
<p><strong>Arzt:</strong> Das ist nur Stress — das sehe ich ständig. Folgen Sie meinem Rat sorgfältig.</p>
<p><strong>Patient:</strong> Werde ich gesund werden?</p>
<p class='target'><strong>Arzt:</strong> In ein paar Monaten werden Sie sich viel besser {{1}} <em>(fühlen)</em>. Da bin ich absolut sicher.</p>
""",
            ja="""
<p><strong>医師：</strong>これはただのストレスです——よく見るケースです。アドバイスをきちんと守ってください。</p>
<p><strong>患者：</strong>良くなりますか？</p>
<p class='target'><strong>医師：</strong>数ヶ月後には、ずっと{{1}}でしょう。<em>（気分が良くなる）</em>絶対に確信しています。</p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — TWO YEARS
    # ══════════════════════════════════════════════════════

    # P-2Y1  Two years / Uncertain ~40 %
    dict(
        id='p_2yr_unc_1',
        ftr_mode='prediction', temporal='two_years', modality='uncertain', certainty=40,
        context_header=dict(
            en="Old Car Purchase",
            fr="Achat d'une vieille voiture",
            de="Kauf eines alten Autos",
            ja="古い車の購入",
        ),
        context_prob=dict(
            en="~40 % Likely",
            fr="~40 % probable",
            de="~40 % wahrscheinlich",
            ja="約40 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> I'm thinking about buying that old Ford.</p>
<p><strong>B:</strong> Be careful — it's been used quite hard...</p>
<p class='target'>...the engine {{1}} <em>(wear out)</em> in a couple of years.</p>
""",
            fr="""
<p><strong>A :</strong> Je pense à acheter cette vieille Ford.</p>
<p><strong>B :</strong> Fais attention — elle a beaucoup servi...</p>
<p class='target'>...le moteur {{1}} <em>(tomber en panne)</em> dans quelques années.</p>
""",
            de="""
<p><strong>A:</strong> Ich denke daran, diesen alten Ford zu kaufen.</p>
<p><strong>B:</strong> Sei vorsichtig — er wurde ziemlich stark benutzt...</p>
<p class='target'>...in ein paar Jahren wird der Motor {{1}} <em>(versagen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>あの古いフォードを買おうと思ってるんだ。</p>
<p><strong>B：</strong>気をつけて——かなり酷使されてきたから…</p>
<p class='target'>…エンジンが数年で{{1}}かもしれないよ。<em>（壊れる）</em></p>
""",
        ),
    ),

    # P-2Y2  Two years / Uncertain ~60 %
    dict(
        id='p_2yr_unc_2',
        ftr_mode='prediction', temporal='two_years', modality='uncertain', certainty=60,
        context_header=dict(
            en="Cryptocurrency Investment",
            fr="Investissement en cryptomonnaie",
            de="Krypto-Investition",
            ja="暗号通貨への投資",
        ),
        context_prob=dict(
            en="~60 % Likely",
            fr="~60 % probable",
            de="~60 % wahrscheinlich",
            ja="約60 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Should I put my savings into cryptocurrency?</p>
<p><strong>B:</strong> Be cautious. In the next couple of years...</p>
<p class='target'>...the market {{1}} <em>(crash)</em>.</p>
""",
            fr="""
<p><strong>A :</strong> Est-ce que je devrais placer mes économies dans les cryptomonnaies ?</p>
<p><strong>B :</strong> Sois prudent(e). Dans les prochaines années...</p>
<p class='target'>...le marché {{1}} <em>(s'effondrer)</em>.</p>
""",
            de="""
<p><strong>A:</strong> Soll ich meine Ersparnisse in Kryptowährungen stecken?</p>
<p><strong>B:</strong> Sei vorsichtig. In den nächsten paar Jahren...</p>
<p class='target'>...könnte der Markt {{1}} <em>(kollabieren)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>貯金を暗号通貨に入れるべきかな？</p>
<p><strong>B：</strong>慎重にね。この数年で…</p>
<p class='target'>…市場は{{1}}かもしれない。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # P-2Y3  Two years / Neutral
    dict(
        id='p_2yr_neu_1',
        ftr_mode='prediction', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="Energy Stocks",
            fr="Actions énergétiques",
            de="Energieaktien",
            ja="エネルギー株",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> I'm considering buying a lot of oil stocks right now.</p>
<p><strong>B:</strong> Be careful about that...</p>
<p class='target'>...renewable energy {{1}} <em>(be)</em> cheaper in a couple of years.</p>
""",
            fr="""
<p><strong>A :</strong> J'envisage d'acheter beaucoup d'actions pétrolières en ce moment.</p>
<p><strong>B :</strong> Méfie-toi d'en acheter maintenant...</p>
<p class='target'>...les énergies renouvelables {{1}} <em>(être)</em> moins chères dans quelques années.</p>
""",
            de="""
<p><strong>A:</strong> Ich überlege, jetzt viele Ölaktien zu kaufen.</p>
<p><strong>B:</strong> Sei vorsichtig dabei...</p>
<p class='target'>...in ein paar Jahren wird erneuerbare Energie günstiger {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今、石油株をたくさん買おうと思っているんだ。</p>
<p><strong>B：</strong>今買うのは気をつけた方がいいよ…</p>
<p class='target'>…数年後には再生可能エネルギーの方が{{1}}よ。<em>（安くなる）</em></p>
""",
        ),
    ),

    # P-2Y4  Two years / Neutral
    dict(
        id='p_2yr_neu_2',
        ftr_mode='prediction', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="Housing Market",
            fr="Marché immobilier",
            de="Immobilienmarkt",
            ja="住宅市場",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> Are you selling your house?</p>
<p><strong>B:</strong> We're not sure. The market is shaky right now, but in two years...</p>
<p class='target'>...it {{1}} <em>(be)</em> more valuable.</p>
""",
            fr="""
<p><strong>A :</strong> Tu vends ta maison ?</p>
<p><strong>B :</strong> On n'est pas sûr. Le marché est instable en ce moment, mais dans deux ans...</p>
<p class='target'>...elle {{1}} <em>(valoir)</em> plus.</p>
""",
            de="""
<p><strong>A:</strong> Verkaufst du dein Haus?</p>
<p><strong>B:</strong> Wir sind uns nicht sicher. Der Markt ist gerade instabil, aber in zwei Jahren...</p>
<p class='target'>...wird es mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>家を売るの？</p>
<p><strong>B：</strong>わからない。今は市場が不安定だけど、2年後には…</p>
<p class='target'>…{{1}}でしょう。<em>（価値が上がる）</em></p>
""",
        ),
    ),

    # P-2Y5  Two years / Certain 100 %
    dict(
        id='p_2yr_cer_1',
        ftr_mode='prediction', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Sea Level Rise",
            fr="Montée du niveau de la mer",
            de="Meeresspiegelanstieg",
            ja="海面上昇",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> What do you expect to happen to sea levels over the next two years?</p>
<p><strong>B:</strong> Look at the data. The science is absolutely conclusive...</p>
<p class='target'>...they {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>A :</strong> À quoi vous attendez-vous pour les niveaux de la mer au cours des deux prochaines années ?</p>
<p><strong>B :</strong> Regardez les données. La science est absolument concluante...</p>
<p class='target'>...ils {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>A:</strong> Was erwarten Sie von den Meeresspiegeln in den nächsten zwei Jahren?</p>
<p><strong>B:</strong> Schauen Sie sich die Daten an. Die Wissenschaft ist absolut schlüssig...</p>
<p class='target'>...in zwei Jahren werden sie {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今後2年間で海面水位はどうなると思いますか？</p>
<p><strong>B：</strong>データを見てください。科学的には完全に結論が出ています…</p>
<p class='target'>…{{1}}でしょう。<em>（上昇する）</em></p>
""",
        ),
    ),

    # P-2Y6  Two years / Certain 100 %
    dict(
        id='p_2yr_cer_2',
        ftr_mode='prediction', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Retirement Savings",
            fr="Épargne retraite",
            de="Altersvorsorge",
            ja="老後の貯蓄",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> I'm not sure it's worth investing in a retirement savings plan right now.</p>
<p><strong>B:</strong> There's no excuse not to. The returns are guaranteed. In two years...</p>
<p class='target'>...your money {{1}} <em>(be)</em> worth significantly more.</p>
""",
            fr="""
<p><strong>A :</strong> Je ne suis pas sûr(e) que ce soit utile d'investir dans un plan d'épargne-retraite maintenant.</p>
<p><strong>B :</strong> Il n'y a aucune excuse. Les rendements sont garantis. Dans deux ans...</p>
<p class='target'>...votre argent {{1}} <em>(valoir)</em> bien plus.</p>
""",
            de="""
<p><strong>A:</strong> Ich bin nicht sicher, ob es sich lohnt, jetzt in einen Rentensparbeplan zu investieren.</p>
<p><strong>B:</strong> Es gibt keine Entschuldigung. Die Renditen sind garantiert. In zwei Jahren...</p>
<p class='target'>...wird Ihr Geld deutlich mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今、老後の貯蓄プランに投資する価値があるかどうかわからない。</p>
<p><strong>B：</strong>しない理由はない。利益は保証されている。2年後には…</p>
<p class='target'>…あなたのお金は大幅に{{1}}でしょう。<em>（価値が増える）</em></p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — TOMORROW  (third item per modality)
    # ══════════════════════════════════════════════════════

    # P-T7  Tomorrow / Uncertain ~50 %
    # Source: adapted from uploaded bank: ginger tea / stomach ache
    dict(
        id='p_tmr_unc_3',
        ftr_mode='prediction', temporal='tomorrow', modality='uncertain', certainty=50,
        context_header=dict(
            en="Home Remedy Advice",
            fr="Remède maison",
            de="Hausmittel-Ratschlag",
            ja="家庭の治療法のアドバイス",
        ),
        context_prob=dict(
            en="~50 % Likely",
            fr="~50 % probable",
            de="~50 % wahrscheinlich",
            ja="約50 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> I have a stomach ache. Nothing is working.</p>
<p><strong>B:</strong> Have you tried ginger tea? I have been drinking it lately...</p>
<p class='target'>...it {{1}} <em>(help)</em> by tomorrow morning, I reckon.</p>
""",
            fr="""
<p><strong>A :</strong> J'ai mal à l'estomac. Rien ne marche.</p>
<p><strong>B :</strong> Tu as essayé le thé au gingembre ? J'en bois depuis peu...</p>
<p class='target'>...d'ici demain matin, je pense que ça {{1}} <em>(aider)</em>.</p>
""",
            de="""
<p><strong>A:</strong> Ich habe Magenschmerzen. Nichts hilft.</p>
<p><strong>B:</strong> Hast du Ingwertee versucht? Ich trinke ihn seit kurzem...</p>
<p class='target'>...bis morgen früh wird es vermutlich {{1}} <em>(helfen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>お腹が痛くて、何をやっても効かない。</p>
<p><strong>B：</strong>ジンジャーティーを試してみた？最近飲んでいるんだけど…</p>
<p class='target'>…明日の朝までには{{1}}と思うよ。<em>（効く）</em></p>
""",
        ),
    ),

    # P-T8  Tomorrow / Neutral
    # Source: adapted from uploaded bank: "study extra material → question on it"
    dict(
        id='p_tmr_neu_3',
        ftr_mode='prediction', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Exam Preparation",
            fr="Préparation à l'examen",
            de="Prüfungsvorbereitung",
            ja="試験の準備",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> Do you think we even need to study the extra material for tomorrow?</p>
<p><strong>B:</strong> Absolutely. Knowing Professor Lee...</p>
<p class='target'>...there {{1}} <em>(be)</em> a question on it tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> Tu crois qu'on a vraiment besoin d'étudier le matériel supplémentaire pour demain ?</p>
<p><strong>B :</strong> Absolument. Connaissant le professeur Leroy...</p>
<p class='target'>...il {{1}} <em>(avoir)</em> une question là-dessus demain.</p>
""",
            de="""
<p><strong>A:</strong> Glaubst du, wir müssen das zusätzliche Material für morgen wirklich lernen?</p>
<p><strong>B:</strong> Auf jeden Fall. Professor Lehmann ist so...</p>
<p class='target'>...morgen wird es dazu eine Frage {{1}} <em>(geben)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>明日のために追加資料まで勉強する必要があると思う？</p>
<p><strong>B：</strong>絶対。李先生のことを考えると…</p>
<p class='target'>…明日の試験にそこから{{1}}でしょうね。<em>（問題が出る）</em></p>
""",
        ),
    ),

    # P-T9  Tomorrow / Certain 100 %
    # Source: adapted from uploaded bank: "anti-inflammatories → help wrist"
    dict(
        id='p_tmr_cer_3',
        ftr_mode='prediction', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Medical Advice",
            fr="Conseil médical",
            de="Medizinischer Rat",
            ja="医療アドバイス",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> My wrist has been in pain for days. Should I take anti-inflammatories?</p>
<p><strong>B:</strong> Yes — I'm a pharmacist, trust me on this. Take them now...</p>
<p class='target'>...they {{1}} <em>(help)</em> it heal faster. You'll feel a difference by tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> Mon poignet est douloureux depuis plusieurs jours. Je devrais prendre des anti-inflammatoires ?</p>
<p><strong>B :</strong> Oui — je suis pharmacien(ne), faites-moi confiance. Prenez-en maintenant...</p>
<p class='target'>...ils {{1}} <em>(aider)</em> à guérir plus vite. Vous sentirez la différence d'ici demain.</p>
""",
            de="""
<p><strong>A:</strong> Mein Handgelenk schmerzt seit Tagen. Soll ich Entzündungshemmer nehmen?</p>
<p><strong>B:</strong> Ja — ich bin Apotheker(in), vertrauen Sie mir. Nehmen Sie sie jetzt...</p>
<p class='target'>...sie werden der Heilung {{1}} <em>(helfen)</em>. Morgen werden Sie den Unterschied spüren.</p>
""",
            ja="""
<p><strong>A：</strong>何日も手首が痛くて。抗炎症薬を飲んだ方がいい？</p>
<p><strong>B：</strong>はい——私は薬剤師です、信じてください。今すぐ飲んでください…</p>
<p class='target'>…それが早く治るのに{{1}}でしょう。<em>（役立つ）</em>明日には違いを感じるはずです。</p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — SIX MONTHS  (third item per modality)
    # ══════════════════════════════════════════════════════

    # P-6M7  Six months / Uncertain ~50 %
    # Source: Robertson Table A.5 item 1144: gold market / skittish
    dict(
        id='p_6mo_unc_3',
        ftr_mode='prediction', temporal='six_months', modality='uncertain', certainty=50,
        context_header=dict(
            en="Gold Investment",
            fr="Investissement en or",
            de="Goldinvestition",
            ja="金への投資",
        ),
        context_prob=dict(
            en="~50 % Likely",
            fr="~50 % probable",
            de="~50 % wahrscheinlich",
            ja="約50 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> The markets are really skittish right now. Should we invest in gold?</p>
<p><strong>B:</strong> Gold usually goes up when markets are nervous. Don't worry...</p>
<p class='target'>...we {{1}} <em>(start)</em> to make money in a few months.</p>
""",
            fr="""
<p><strong>A :</strong> Les marchés sont vraiment nerveux en ce moment. On devrait investir dans l'or ?</p>
<p><strong>B :</strong> L'or monte généralement quand les marchés sont agités. Ne t'inquiète pas...</p>
<p class='target'>...on {{1}} <em>(commencer)</em> à gagner de l'argent dans quelques mois.</p>
""",
            de="""
<p><strong>A:</strong> Die Märkte sind gerade wirklich nervös. Sollten wir in Gold investieren?</p>
<p><strong>B:</strong> Gold steigt normalerweise, wenn die Märkte nervös sind. Keine Sorge...</p>
<p class='target'>...in ein paar Monaten werden wir {{1}} <em>(anfangen)</em>, Geld zu verdienen.</p>
""",
            ja="""
<p><strong>A：</strong>今、市場が本当に神経質な状態です。金に投資すべきかな？</p>
<p><strong>B：</strong>市場が不安定な時は金が上がることが多い。心配しないで…</p>
<p class='target'>…数ヶ月後には稼ぎ{{1}}でしょう。<em>（始める）</em></p>
""",
        ),
    ),

    # P-6M8  Six months / Neutral
    # Source: Robertson Table A.5 item 1024/1140: teacher → student improving
    dict(
        id='p_6mo_neu_3',
        ftr_mode='prediction', temporal='six_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Child at New School",
            fr="Enfant dans une nouvelle école",
            de="Kind in neuer Schule",
            ja="新しい学校の子供",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>Teacher:</strong> Ellie worries me a little, but I think she just needs time to adjust.</p>
<p><strong>Parent:</strong> Will she be OK?</p>
<p class='target'><strong>Teacher:</strong> In a couple of months she {{1}} <em>(improve)</em>. I see it every year.</p>
""",
            fr="""
<p><strong>Professeur :</strong> Ellie m'inquiète un peu, mais je pense qu'elle a juste besoin de temps pour s'adapter.</p>
<p><strong>Parent :</strong> Elle va s'en sortir ?</p>
<p class='target'><strong>Professeur :</strong> Dans quelques mois elle {{1}} <em>(progresser)</em>. Je le vois chaque année.</p>
""",
            de="""
<p><strong>Lehrerin:</strong> Ellie macht mir ein bisschen Sorgen, aber ich glaube, sie braucht nur Zeit zum Eingewöhnen.</p>
<p><strong>Elternteil:</strong> Wird sie sich erholen?</p>
<p class='target'><strong>Lehrerin:</strong> In ein paar Monaten wird sie {{1}} <em>(Fortschritte machen)</em>. Das sehe ich jedes Jahr.</p>
""",
            ja="""
<p><strong>先生：</strong>エリーのことが少し心配ですが、ただ慣れるまでの時間が必要なだけだと思います。</p>
<p><strong>保護者：</strong>大丈夫でしょうか？</p>
<p class='target'><strong>先生：</strong>数ヶ月で{{1}}でしょう。<em>（上達する）</em>毎年見てきています。</p>
""",
        ),
    ),

    # P-6M9  Six months / Certain 100 %
    # Source: adapted from uploaded bank: Africa investment → crash
    dict(
        id='p_6mo_cer_3',
        ftr_mode='prediction', temporal='six_months', modality='certain', certainty=100,
        context_header=dict(
            en="Emerging Market Warning",
            fr="Avertissement sur les marchés émergents",
            de="Warnung vor Schwellenländern",
            ja="新興市場への警告",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> I was thinking of putting my savings into African emerging markets.</p>
<p><strong>B:</strong> Are you sure? The next six months look very unstable — every analyst agrees...</p>
<p class='target'>...it {{1}} <em>(crash)</em>. Don't do it.</p>
""",
            fr="""
<p><strong>A :</strong> Je pensais placer mes économies dans les marchés émergents africains.</p>
<p><strong>B :</strong> Tu es sûr(e) ? Les six prochains mois s'annoncent très instables — tous les analystes sont d'accord...</p>
<p class='target'>...ça {{1}} <em>(s'effondrer)</em>. Ne le fais pas.</p>
""",
            de="""
<p><strong>A:</strong> Ich dachte daran, meine Ersparnisse in afrikanische Schwellenmärkte zu stecken.</p>
<p><strong>B:</strong> Bist du sicher? Die nächsten sechs Monate sehen sehr instabil aus — alle Analysten sind sich einig...</p>
<p class='target'>...in sechs Monaten wird es {{1}} <em>(kollabieren)</em>. Tu es nicht.</p>
""",
            ja="""
<p><strong>A：</strong>貯金をアフリカの新興市場に投資しようと思っているんだ。</p>
<p><strong>B：</strong>本当に？これから6ヶ月はとても不安定になる——全てのアナリストが同意している…</p>
<p class='target'>…{{1}}よ。<em>（崩壊する）</em>やめた方がいい。</p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # PREDICTIONS — TWO YEARS  (third item per modality)
    # ══════════════════════════════════════════════════════

    # P-2Y7  Two years / Uncertain ~60 %
    # Source: adapted from uploaded bank: sea levels (unclear science)
    dict(
        id='p_2yr_unc_3',
        ftr_mode='prediction', temporal='two_years', modality='uncertain', certainty=60,
        context_header=dict(
            en="Climate Policy Debate",
            fr="Débat sur la politique climatique",
            de="Klimapolitische Debatte",
            ja="気候政策の議論",
        ),
        context_prob=dict(
            en="~60 % Likely",
            fr="~60 % probable",
            de="~60 % wahrscheinlich",
            ja="約60 %の確率",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> What do you think will happen to sea levels in the next two years?</p>
<p><strong>B:</strong> The science is still debated, but the trend is fairly clear...</p>
<p class='target'>...I think they {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>A :</strong> Que pensez-vous qu'il arrivera aux niveaux de la mer dans les deux prochaines années ?</p>
<p><strong>B :</strong> La science fait encore débat, mais la tendance est assez claire...</p>
<p class='target'>...je pense qu'ils {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>A:</strong> Was denken Sie, was in den nächsten zwei Jahren mit den Meeresspiegeln passiert?</p>
<p><strong>B:</strong> Die Wissenschaft ist noch umstritten, aber der Trend ist ziemlich klar...</p>
<p class='target'>...ich glaube, in zwei Jahren werden sie {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今後2年間で海面水位はどうなると思いますか？</p>
<p><strong>B：</strong>科学的にはまだ議論がありますが、傾向はかなり明確で…</p>
<p class='target'>…{{1}}と思います。<em>（上昇する）</em></p>
""",
        ),
    ),

    # P-2Y8  Two years / Neutral
    # Source: Robertson Table A.5 item 1164: retirement savings / shaky rates
    dict(
        id='p_2yr_neu_3',
        ftr_mode='prediction', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="Retirement Planning",
            fr="Planification de la retraite",
            de="Altersplanung",
            ja="退職後の計画",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> Is it really worth putting money into a retirement savings plan right now? Interest rates are so shaky.</p>
<p><strong>B:</strong> Trust the long term. In two years...</p>
<p class='target'>...it {{1}} <em>(be)</em> worth quite a bit more.</p>
""",
            fr="""
<p><strong>A :</strong> Est-ce que ça vaut vraiment la peine de mettre de l'argent dans un plan d'épargne-retraite maintenant ? Les taux d'intérêt sont si instables.</p>
<p><strong>B :</strong> Faites confiance au long terme. Dans deux ans...</p>
<p class='target'>...ça {{1}} <em>(valoir)</em> bien plus.</p>
""",
            de="""
<p><strong>A:</strong> Lohnt es sich wirklich, jetzt Geld in einen Rentensparbeplan zu stecken? Die Zinsen sind so unbeständig.</p>
<p><strong>B:</strong> Vertrauen Sie dem langen Atem. In zwei Jahren...</p>
<p class='target'>...wird es deutlich mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今、老後の積立プランにお金を入れる価値は本当にありますか？金利が不安定で。</p>
<p><strong>B：</strong>長期的に信じてください。2年後には…</p>
<p class='target'>…かなり{{1}}でしょう。<em>（価値が増える）</em></p>
""",
        ),
    ),

    # P-2Y9  Two years / Certain 100 %
    # Source: adapted from uploaded bank: "saving £100 every paycheque → worth £30,000"
    dict(
        id='p_2yr_cer_3',
        ftr_mode='prediction', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Savings Growth",
            fr="Croissance de l'épargne",
            de="Ersparniszuwachs",
            ja="貯蓄の成長",
        ),
        context_prob=dict(
            en="100 % Certain",
            fr="100 % certain",
            de="100 % sicher",
            ja="100 % 確実",
        ),
        text=dict(
            en="""
<p><strong>A:</strong> Are you saving every month?</p>
<p><strong>B:</strong> Yes — I put away £200 every paycheque into a compound interest account. The math is simple...</p>
<p class='target'>...in two years it {{1}} <em>(be)</em> worth over £5,000. Guaranteed.</p>
""",
            fr="""
<p><strong>A :</strong> Tu épargnes tous les mois ?</p>
<p><strong>B :</strong> Oui — je mets 200 € de côté à chaque salaire sur un compte à intérêts composés. Le calcul est simple...</p>
<p class='target'>...dans deux ans ça {{1}} <em>(valoir)</em> plus de 5 000 €. Garanti.</p>
""",
            de="""
<p><strong>A:</strong> Sparst du jeden Monat?</p>
<p><strong>B:</strong> Ja — ich lege 200 € von jedem Gehalt auf ein Zinseszins-Konto. Die Rechnung ist einfach...</p>
<p class='target'>...in zwei Jahren wird es über 5.000 € wert {{1}} <em>(sein)</em>. Garantiert.</p>
""",
            ja="""
<p><strong>A：</strong>毎月貯金しているの？</p>
<p><strong>B：</strong>うん——毎月の給料から2万円を複利口座に積み立てている。計算は簡単で…</p>
<p class='target'>…2年後には50万円以上の価値に{{1}}でしょう。<em>（なる）</em>保証付きです。</p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # SCHEDULING CONTROLS  (Neutral modality only)
    # ══════════════════════════════════════════════════════

    # S-T  Tomorrow / Neutral
    dict(
        id='s_tmr',
        ftr_mode='scheduling', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Travel Schedule",
            fr="Programme de voyage",
            de="Reiseplan",
            ja="旅行スケジュール",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> What time is your flight tomorrow?</p>
<p><strong>B:</strong> I just checked the ticket...</p>
<p class='target'>...my flight {{1}} <em>(leave)</em> at 8 AM tomorrow morning.</p>
""",
            fr="""
<p><strong>A :</strong> À quelle heure est ton vol demain ?</p>
<p><strong>B :</strong> Je viens de vérifier le billet...</p>
<p class='target'>...mon vol {{1}} <em>(partir)</em> demain matin à 8 h.</p>
""",
            de="""
<p><strong>A:</strong> Wann geht dein Flug morgen?</p>
<p><strong>B:</strong> Ich habe gerade das Ticket überprüft...</p>
<p class='target'>...morgen früh um 8 Uhr wird mein Flug {{1}} <em>(starten)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>明日のフライトは何時？</p>
<p><strong>B：</strong>今チケットを確認したんだけど…</p>
<p class='target'>…明日の朝8時に便が{{1}}。<em>（出発する）</em></p>
""",
        ),
    ),

    # S-6M  Six months / Neutral
    dict(
        id='s_6mo',
        ftr_mode='scheduling', temporal='six_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Moving House",
            fr="Déménagement",
            de="Umzug",
            ja="引っ越し",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> When are you planning to move house?</p>
<p><strong>B:</strong> I need to check the documents, but...</p>
<p class='target'>...our lease {{1}} <em>(expire)</em> in six months.</p>
""",
            fr="""
<p><strong>A :</strong> Quand est-ce que tu comptes déménager ?</p>
<p><strong>B :</strong> Je dois vérifier les documents, mais...</p>
<p class='target'>...notre bail {{1}} <em>(expirer)</em> dans six mois.</p>
""",
            de="""
<p><strong>A:</strong> Wann planst du umzuziehen?</p>
<p><strong>B:</strong> Ich muss die Dokumente prüfen, aber...</p>
<p class='target'>...in sechs Monaten wird unser Mietvertrag {{1}} <em>(enden)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>いつ引っ越す予定なの？</p>
<p><strong>B：</strong>書類を確認しないといけないんだけど…</p>
<p class='target'>…私たちの賃貸契約が6ヶ月で{{1}}予定です。<em>（切れる）</em></p>
""",
        ),
    ),

    # S-2Y  Two years / Neutral
    dict(
        id='s_2yr',
        ftr_mode='scheduling', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="University Degree",
            fr="Diplôme universitaire",
            de="Hochschulabschluss",
            ja="大学の学位",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> How much longer do you have on your degree?</p>
<p><strong>B:</strong> I need to check how many credits I still have, but...</p>
<p class='target'>...I {{1}} <em>(graduate)</em> in two years.</p>
""",
            fr="""
<p><strong>A :</strong> Combien de temps te reste-t-il avant d'obtenir ton diplôme ?</p>
<p><strong>B :</strong> Je dois vérifier mes crédits, mais...</p>
<p class='target'>...j'{{1}} <em>(obtenir mon diplôme)</em> dans deux ans.</p>
""",
            de="""
<p><strong>A:</strong> Wie lange hast du noch bis zu deinem Abschluss?</p>
<p><strong>B:</strong> Ich muss meine Kreditpunkte prüfen, aber...</p>
<p class='target'>...in zwei Jahren werde ich meinen Abschluss {{1}} <em>(machen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>学位取得までどれくらいかかりますか？</p>
<p><strong>B：</strong>まだ取得しなければならない単位数を確認する必要がありますが…</p>
<p class='target'>…2年後に{{1}}予定です。<em>（卒業する）</em></p>
""",
        ),
    ),

    # ══════════════════════════════════════════════════════
    # INTENTION CONTROLS  (Neutral modality only)
    # ══════════════════════════════════════════════════════

    # I-T  Tomorrow / Neutral
    dict(
        id='i_tmr',
        ftr_mode='intention', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Plans for Tonight",
            fr="Plans pour ce soir",
            de="Pläne für heute Abend",
            ja="今夜の予定",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> Do you want to come see a film tonight?</p>
<p><strong>B:</strong> Sorry, I can't...</p>
<p class='target'>...I {{1}} <em>(dine out)</em> with Sarah tonight.</p>
""",
            fr="""
<p><strong>A :</strong> Tu veux venir voir un film ce soir ?</p>
<p><strong>B :</strong> Désolé(e), je ne peux pas...</p>
<p class='target'>...je {{1}} <em>(dîner)</em> au restaurant avec Sophie ce soir.</p>
""",
            de="""
<p><strong>A:</strong> Willst du heute Abend einen Film sehen?</p>
<p><strong>B:</strong> Leider nicht...</p>
<p class='target'>...heute Abend werde ich mit Laura {{1}} <em>(speisen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今夜映画を見に行きませんか？</p>
<p><strong>B：</strong>ごめんなさい、無理なんです…</p>
<p class='target'>…今夜サラと{{1}}んです。<em>（外食する）</em></p>
""",
        ),
    ),

    # I-6M  Six months / Neutral
    dict(
        id='i_6mo',
        ftr_mode='intention', temporal='six_months', modality='neutral', certainty=None,
        context_header=dict(
            en="A Friend's Plans",
            fr="Les projets d'un ami",
            de="Pläne eines Freundes",
            ja="友人の計画",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> [In October] What's Thomas up to lately? He seems unhappy living here.</p>
<p><strong>B:</strong> I don't think he's happy here. In the spring...</p>
<p class='target'>...he {{1}} <em>(travel)</em> in Mexico.</p>
""",
            fr="""
<p><strong>A :</strong> [En octobre] Qu'est-ce que Thomas fait ces temps-ci ? Il a l'air malheureux ici.</p>
<p><strong>B :</strong> Je ne pense pas qu'il soit heureux ici. Au printemps...</p>
<p class='target'>...il {{1}} <em>(voyager)</em> au Mexique.</p>
""",
            de="""
<p><strong>A:</strong> [Im Oktober] Was macht Thomas gerade? Er wirkt unglücklich hier.</p>
<p><strong>B:</strong> Ich glaube nicht, dass er hier glücklich ist. Im Frühjahr...</p>
<p class='target'>...wird er in Mexiko {{1}} <em>(reisen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>[10月の話]トーマスは最近どうしてる？ここでの生活が嫌みたいだけど。</p>
<p><strong>B：</strong>彼はここでの生活が幸せじゃないと思う。春には…</p>
<p class='target'>…メキシコを{{1}}つもりみたい。<em>（旅行する）</em></p>
""",
        ),
    ),

    # I-2Y  Two years / Neutral
    dict(
        id='i_2yr',
        ftr_mode='intention', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="Long-term Plans",
            fr="Plans à long terme",
            de="Langzeitpläne",
            ja="長期計画",
        ),
        context_prob=dict(en='', fr='', de='', ja=''),
        text=dict(
            en="""
<p><strong>A:</strong> Are you planning to stay in the UK long term?</p>
<p><strong>B:</strong> I really love it here. In two years...</p>
<p class='target'>...I {{1}} <em>(apply)</em> for permanent residency.</p>
""",
            fr="""
<p><strong>A :</strong> Est-ce que tu comptes rester au Royaume-Uni à long terme ?</p>
<p><strong>B :</strong> J'adore vraiment être ici. Dans deux ans...</p>
<p class='target'>...je {{1}} <em>(faire une demande)</em> de résidence permanente.</p>
""",
            de="""
<p><strong>A:</strong> Planst du, langfristig in Großbritannien zu bleiben?</p>
<p><strong>B:</strong> Ich liebe es wirklich hier. In zwei Jahren...</p>
<p class='target'>...werde ich die dauerhafte Aufenthaltserlaubnis {{1}} <em>(beantragen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>長期的にイギリスに滞在するつもりですか？</p>
<p><strong>B：</strong>本当にここが大好きです。2年後には…</p>
<p class='target'>…永住権を{{1}}つもりです。<em>（申請する）</em></p>
""",
        ),
    ),

]  # end SCENARIOS


def _get_scenario(lang, idx):
    """Return a language-specific, flat scenario dict for the template."""
    s = SCENARIOS[idx]
    return dict(
        id=s['id'],
        ftr_mode=s['ftr_mode'],
        temporal=s['temporal'],
        modality=s['modality'],
        certainty=s.get('certainty'),
        context_header=s['context_header'].get(lang, s['context_header']['en']),
        context_prob=s['context_prob'].get(lang, s['context_prob']['en']),
        text=s['text'].get(lang, s['text']['en']),
    )


# ═══════════════════════════════════════════════════════════
# TASK 2.2 SENTENCES  (Perception / Subjective Probability)
# ═══════════════════════════════════════════════════════════
SLIDER_ITEMS = dict(
    # ── English: 13 items (Robertson et al., 2023) ──
    en=[
        "It is going to rain next week.",            #  1. be going to
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

    # ── French: 14 items ──
    fr=[
        "Il va pleuvoir la semaine prochaine.",                #  1. Futur proche
        "Il pleuvra la semaine prochaine.",                    #  2. Futur simple
        "Je pense qu'il va pleuvoir la semaine prochaine.",    #  3. Je pense + futur proche
        "Je pense qu'il pleuvra la semaine prochaine.",        #  4. Je pense + futur simple
        "Il pleuvra certainement la semaine prochaine.",       #  5. Futur simple + certainement
        "Il pleuvra sans doute la semaine prochaine.",         #  6. Futur simple + sans doute
        "Il pourrait pleuvoir la semaine prochaine.",          #  7. Conditionnel (pouvoir)
        "Il devrait pleuvoir la semaine prochaine.",           #  8. Conditionnel (devoir)
        "Il se peut qu'il pleuve la semaine prochaine.",       #  9. Il se peut que + subjonctif
        "Il est possible qu'il pleuve la semaine prochaine.",  # 10. Il est possible que + subjonctif
        "Peut-être qu'il pleuvra la semaine prochaine.",       # 11. Peut-être + futur simple
        "Il pleuvrait la semaine prochaine.",                  # 12. Conditionnel (reportatif)
        "Il va sûrement pleuvoir la semaine prochaine.",       # 13. Futur proche + sûrement
        "Il pleut la semaine prochaine.",                      # 14. Présent à valeur de futur
    ],

    # ── German: 14 items ──
    de=[
        "Es wird nächste Woche regnen.",                       #  1. werden + Inf (standard Futur I)
        "Es regnet nächste Woche.",                            #  2. Präsens futurisch
        "Ich denke, es wird nächste Woche regnen.",            #  3. Ich denke + werden
        "Es wird bestimmt nächste Woche regnen.",              #  4. werden + bestimmt
        "Es wird sicherlich nächste Woche regnen.",            #  5. werden + sicherlich
        "Es könnte nächste Woche regnen.",                     #  6. Konjunktiv II (können)
        "Es kann nächste Woche regnen.",                       #  7. können (Indikativ)
        "Es dürfte nächste Woche regnen.",                     #  8. dürfen (Konj. II)
        "Es mag nächste Woche regnen.",                        #  9. mögen (Indikativ)
        "Es soll nächste Woche regnen.",                       # 10. sollen (reportativ)
        "Vielleicht regnet es nächste Woche.",                 # 11. vielleicht + Präsens
        "Es wird wohl nächste Woche regnen.",                  # 12. werden + wohl (Modalpartikel)
        "Es wird wahrscheinlich nächste Woche regnen.",        # 13. werden + wahrscheinlich
        "Ich glaube, es regnet nächste Woche.",                # 14. Ich glaube + Präsens
    ],

    # ── Japanese: 13 items ──
    ja=[
        "来週、雨が降るだろう。",                     #  1. ～だろう (conjecture)
        "来週、雨が降ります。",                       #  2. ～ます (polite declarative)
        "来週、雨が降ると思います。",                  #  3. ～と思います
        "来週、間違いなく雨が降ります。",              #  4. 間違いなく (without doubt)
        "来週、雨が降るかもしれない。",                #  5. ～かもしれない (possibility)
        "来週、雨が降りうる。",                       #  6. ～うる (potential)
        "来週、雨が降るかもしれません。",              #  7. ～かもしれません (polite poss.)
        "来週、必ず雨が降ります。",                   #  8. 必ず (certainly)
        "来週、雨が降るんじゃないかと思います。",       #  9. ～んじゃないかと思う (hedged)
        "来週、ひょっとしたら雨が降るかもしれない。",   # 10. ひょっとしたら (remote poss.)
        "来週、雨が降るはずです。",                   # 11. ～はずです (expectation)
        "来週、おそらく雨が降るでしょう。",            # 12. おそらく～でしょう (probably)
        "来週、雨が降る。",                          # 13. Dictionary form (casual declarative)
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

    # Task 2.1 responses: {"p_tmr_unc_1": {"1": "will pass"}, ...}
    t2_production_data = models.LongStringField(initial='{}', blank=True)

    # Task 2.2 responses: {"It will rain...": 80, ...}
    t2_perception_data = models.LongStringField(initial='{}', blank=True)


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
def _ctx(player, progress):
    lang = player.language
    return dict(lang=lang, ui=ui_dict(lang), progress=progress)


# ═══════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════
class Task2Intro(Page):
    @staticmethod
    def vars_for_template(player):
        lang = player.session.config.get('language', 'en')
        player.language = lang
        return _ctx(player, 50)


ITEMS_PER_PAGE = 7   # ← change this to 6 or 8 if desired


class Task2Item(Page):
    """Base class; subclasses are generated dynamically (one per page-chunk)."""
    template_name = 'Task2/Task2Item.html'
    form_model = 'player'
    form_fields = ['t2_production_data']

    @staticmethod
    def _vars(player, indices, progress):
        lang = player.language
        scenarios = [_get_scenario(lang, i) for i in indices]
        return dict(
            scenarios=scenarios,
            existing=player.t2_production_data or '{}',
            **_ctx(player, progress),
        )


def _make_item_page(indices):
    """Factory: generate one Task2Item page for a chunk of scenario indices."""
    n_pages = -(-len(SCENARIOS) // ITEMS_PER_PAGE)   # ceiling division
    page_num = indices[0] // ITEMS_PER_PAGE           # 0-based page number
    # Progress sweeps from 55 % (first page) to 93 % (last page)
    progress = 55 + round(38 * page_num / max(1, n_pages - 1))
    label = f'{indices[0] + 1}_{indices[-1] + 1}'

    class _ItemPage(Task2Item):
        @staticmethod
        def vars_for_template(player):
            return Task2Item._vars(player, indices, progress)

    _ItemPage.__name__     = f'Task2ItemPage_{label}'
    _ItemPage.__qualname__ = f'Task2ItemPage_{label}'
    return _ItemPage


# Build all item pages — one per chunk of ITEMS_PER_PAGE scenarios
# 33 scenarios at 7/page → 5 pages  (4 × 7 + 1 × 5)
_all_indices = list(range(len(SCENARIOS)))
_chunks      = [_all_indices[i:i + ITEMS_PER_PAGE]
                for i in range(0, len(_all_indices), ITEMS_PER_PAGE)]
_ITEM_PAGES  = [_make_item_page(chunk) for chunk in _chunks]


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
            **_ctx(player, 98),
        )


# ═══════════════════════════════════════════════════════════
# PAGE SEQUENCE
# ═══════════════════════════════════════════════════════════
page_sequence = [Task2Intro] + _ITEM_PAGES + [Task2Slider]