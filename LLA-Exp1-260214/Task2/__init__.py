from otree.api import *
import json

doc = """
Task 2: FTR Elicitation (Production) & Subjective Probability (Perception).
Design based on Robertson et al. (2023).
Languages: English (en), French (fr), German (de), Japanese (ja).

Task 2.1 Design (SCENARIOS):
  PRIMARY (25 items, 3 pages of ~8–9):
    15 Predictions: full 3×5 factorial
       3 temporal distances  (tomorrow / 3 months / 2 years)
     × 5 certainty levels    (neutral / 40 % / 50 % / 60 % / 100 %)
     5 Intentions: one per certainty, time randomly assigned
     5 Scheduling:  one per certainty, time randomly assigned

  BACKUP (15 items, 1 page):
    15 additional Predictions: same 3×5 factorial (alternate items)

  Total: 40 items + 2 attention checks across 4 pages.

  Attention checks (2):
    Disguised as normal scenarios but instruct participant to type a
    specific word.  Buried mid-page in Pages 1 and 3.
    Used for data-quality screening.

  All items sourced from Robertson (2023) Table A.5, adapted for:
    - temporal distances (tomorrow / 3 months / 2 years)
    - cross-linguistic validity (culturally specific references generalised)
    - no {BE} or {DO} cloze verbs in questioner/context

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
        en='You are now moving on to the second part of the study.',
        fr="Vous passez maintenant à la deuxième partie de l'étude.",
        de='Sie fahren nun mit dem zweiten Teil der Studie fort.',
        ja='調査の第2パートに移ります。',
    ),
    t2_how_title=dict(
        en='How it works',
        fr='Comment ça marche',
        de='So funktioniert es',
        ja='やり方',
    ),
    t2_how_step1=dict(
        en='You will see short dialogue scenarios. Each one has a gap where a word or phrase is missing. The missing word appears as a blue hint.',
        fr='Vous verrez de courts scénarios de dialogue. Chacun comporte un espace où un mot ou une expression manque. Le mot manquant apparaît sous forme d\u2019indice en bleu.',
        de='Sie sehen kurze Dialogszenarien. Jedes hat eine Lücke, in der ein Wort oder eine Phrase fehlt. Das fehlende Wort erscheint als blauer Hinweis.',
        ja='短い会話のシナリオが表示されます。それぞれに単語やフレーズが欠けている空欄があります。欠けている単語は青いヒントとして表示されます。',
    ),
    t2_how_step2=dict(
        en='Click the blue hint to open the gap, then type what feels most natural to you. Use the hint verb as a guide.',
        fr='Cliquez sur l\u2019indice bleu pour ouvrir l\u2019espace, puis tapez ce qui vous semble le plus naturel. Utilisez le verbe indiqué comme guide.',
        de='Klicken Sie auf den blauen Hinweis, um die Lücke zu öffnen, und geben Sie ein, was sich für Sie am natürlichsten anfühlt. Verwenden Sie das Hinweiswort als Orientierung.',
        ja='青いヒントをクリックして空欄を開き、最も自然だと感じる表現を入力してください。ヒントの動詞を参考にしてください。',
    ),
    t2_how_step3=dict(
        en='Where a certainty percentage is shown, imagine you are exactly that certain and write what you would naturally say.',
        fr='Lorsqu\u2019un pourcentage de certitude est indiqué, imaginez que vous êtes exactement aussi certain(e) et écrivez ce que vous diriez naturellement.',
        de='Wenn ein Sicherheitsprozentsatz angegeben ist, stellen Sie sich vor, genau so sicher zu sein, und schreiben Sie, was Sie natürlich sagen würden.',
        ja='確率（％）が表示されている場合は、その確率で確信していると想像し、自然に言うであろう表現を書いてください。',
    ),
    t2_practice_label=dict(
        en='\u270f\ufe0f Try it yourself',
        fr='\u270f\ufe0f Essayez vous-m\u00eame',
        de='\u270f\ufe0f Probieren Sie es aus',
        ja='\u270f\ufe0f 練習してみましょう',
    ),
    t2_guidelines_title=dict(
        en='Tips',
        fr='Conseils',
        de='Tipps',
        ja='ヒント',
    ),
    t2_guideline_1=dict(
        en='\u2714\ufe0f There are no right or wrong answers. Write whatever feels most natural.',
        fr='\u2714\ufe0f Il n\u2019y a pas de bonne ou de mauvaise r\u00e9ponse. \u00c9crivez ce qui vous semble le plus naturel.',
        de='\u2714\ufe0f Es gibt keine richtigen oder falschen Antworten. Schreiben Sie, was Ihnen am nat\u00fcrlichsten vorkommt.',
        ja='\u2714\ufe0f 正解や不正解はありません。最も自然だと感じるものを書いてください。',
    ),
    t2_guideline_2=dict(
        en='\u2714\ufe0f Imagine you are talking to a close friend.',
        fr='\u2714\ufe0f Imaginez que vous parlez \u00e0 un ami proche.',
        de='\u2714\ufe0f Stellen Sie sich vor, Sie sprechen mit einem guten Freund.',
        ja='\u2714\ufe0f 親しい友人に話しているつもりで書いてください。',
    ),
    t2_guideline_3=dict(
        en='\u2714\ufe0f One word or a short phrase is enough.',
        fr='\u2714\ufe0f Un mot ou une courte expression suffit.',
        de='\u2714\ufe0f Ein Wort oder eine kurze Phrase reicht aus.',
        ja='\u2714\ufe0f 一語または短いフレーズで十分です。',
    ),
    # ── Task 2.1 Instructions ──
    t2_instructions = dict(
        en=(
            # "There are no correct answers. "
            "Please complete the sentence as though you were speaking to a close friend. "
            "Use the verb shown in italics as a guide, and write whatever feels most natural to you. "
            "Where a certainty percentage is shown, imagine you are exactly that certain "
            "and write what you would say."
        ),
        fr=(
            # "Il n'y a pas de bonnes ou de mauvaises réponses. "
            "Complétez la phrase comme si vous parliez à un(e) ami(e) proche. "
            "Le verbe en italique est une indication — écrivez ce qui vous semble le plus naturel. "
            "Lorsqu'un pourcentage de certitude est indiqué, imaginez que vous êtes exactement "
            "aussi certain(e) et écrivez ce que vous diriez."
        ),
        de=(
            # "Es gibt keine richtigen oder falschen Antworten. "
            "Vervollständigen Sie den Satz, als würden Sie mit einem guten Freund / einer guten Freundin sprechen. "
            "Das kursiv gedruckte Verb dient als Hinweis — schreiben Sie, was sich für Sie am natürlichsten anfühlt. "
            "Wenn ein Sicherheitsprozentsatz angegeben ist, stellen Sie sich vor, genau so sicher zu sein, "
            "und schreiben Sie, was Sie sagen würden."
        ),
        ja=(
            # "正解・不正解はありません。"
            "親しい友人に話しかけるつもりで文を完成させてください。"
            "斜体の動詞はヒントです——最も自然に感じる表現を書いてください。"
            "確率（%）が表示されている場合は、自分がちょうどその確率で確信しているとイメージして、"
            "そのときに言うであろう表現を書いてください。"
        ),
    ),
    # ── Task 2.2 Slider ──
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
    impossible = dict(en='Uncertain', fr='Incertain(e)', de='Unsicher', ja='不確か'),
    certain    = dict(en='Certain',   fr='Certain(e)',   de='Sicher',   ja='確実'),
)


def ui_dict(lang):
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ═══════════════════════════════════════════════════════════
# TASK 2.1 SCENARIOS  (Production / FTR elicitation)
#
# All items sourced from Robertson (2023) Table A.5.
# Adapted for temporal distances and cross-linguistic use.
#
# Field glossary:
#   id            – unique slug (used as data key)
#   ftr_mode      – 'prediction' | 'scheduling' | 'intention'
#   temporal      – 'tomorrow' | 'three_months' | 'two_years'
#   modality      – 'low_40' | 'low_50' | 'low_60' | 'neutral' | 'certain'
#   certainty     – numeric seed (40/50/60/100) or None for neutral
#   robertson_src – Robertson Table A.5 item number
#   context_header – displayed title box (per language)
#   context_prob  – displayed badge (empty string for neutral)
#   text          – HTML snippet; {{N}} → input blank; verb hint in <em>
#
# German note: blank is placed at CLAUSE END so that both
#   Präsens (finite verb) and Futur I (werden + Infinitiv) are
#   grammatically natural without separable-verb word-order issues.
# ═══════════════════════════════════════════════════════════

# ── Probability badge templates ──
_PROB = {
    40:   dict(en="40% Likely", fr="40% probable", de="40% wahrscheinlich", ja="40%の確率"),
    50:   dict(en="50% Likely", fr="50% probable", de="50% wahrscheinlich", ja="50%の確率"),
    60:   dict(en="60% Likely", fr="60% probable", de="60% wahrscheinlich", ja="60%の確率"),
    100:  dict(en="100% Certain", fr="100% certain", de="100% sicher", ja="100% 確実"),
    None: dict(en='', fr='', de='', ja=''),
}

SCENARIOS = [

    # ══════════════════════════════════════════════════════════
    #  PRIMARY ITEMS  (25)
    # ══════════════════════════════════════════════════════════

    # ─────────────────────────────────────────────────────────
    #  PREDICTIONS — TOMORROW  (5 items: neutral, 40, 50, 60, 100)
    # ─────────────────────────────────────────────────────────

    # Item 1 — Prediction / Tomorrow / Neutral  (Robertson 1022)
    dict(
        id='p_tmr_neu', robertson_src=1022,
        ftr_mode='prediction', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Retail Prices",
            fr="Prix en magasin",
            de="Ladenpreise",
            ja="小売価格",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>Salesman to customer:</strong> I'd come back tomorrow. New stock is arriving soon...</p>
<p class='target'>...the price on these {{1}} <em>(drop)</em>.</p>
""",
            fr="""
<p><strong>Vendeur au client :</strong> Je reviendrais demain si j'étais vous. De nouveaux stocks arrivent bientôt...</p>
<p class='target'>...le prix de ces articles {{1}} <em>(baisser)</em>.</p>
""",
            de="""
<p><strong>Verkäufer zum Kunden:</strong> Ich würde morgen wiederkommen. Neue Ware trifft bald ein...</p>
<p class='target'>...der Preis dafür wird {{1}} <em>(sinken)</em>.</p>
""",
            ja="""
<p><strong>店員から客へ：</strong>明日また来ていただいた方がいいですよ。新しい在庫がまもなく届きますので…</p>
<p class='target'>…こちらの値段は{{1}}でしょう。<em>（下がる）</em></p>
""",
        ),
    ),

    # Item 2 — Prediction / Tomorrow / 40 %  (Robertson 1135)
    dict(
        id='p_tmr_40', robertson_src=1135,
        ftr_mode='prediction', temporal='tomorrow', modality='low_40', certainty=40,
        context_header=dict(
            en="Stock Markets",
            fr="Marchés boursiers",
            de="Aktienmärkte",
            ja="株式市場",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> How do you expect the stock markets to perform tomorrow?</p>
<p><strong>A:</strong> It is unclear...</p>
<p class='target'>...they {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Comment pensez-vous que les marchés boursiers vont se comporter demain ?</p>
<p><strong>R :</strong> C'est difficile à dire...</p>
<p class='target'>...ils {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Wie werden sich die Aktienmärkte morgen Ihrer Meinung nach entwickeln?</p>
<p><strong>A:</strong> Das ist unklar...</p>
<p class='target'>...sie werden {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>明日の株式市場はどうなると思いますか？</p>
<p><strong>回答：</strong>はっきりしないけど…</p>
<p class='target'>…{{1}}と思う。<em>（上がる）</em></p>
""",
        ),
    ),

    # Item 3 — Prediction / Tomorrow / 50 %  (Robertson 1133)
    dict(
        id='p_tmr_50', robertson_src=1133,
        ftr_mode='prediction', temporal='tomorrow', modality='low_50', certainty=50,
        context_header=dict(
            en="Financial Markets",
            fr="Marchés financiers",
            de="Finanzmärkte",
            ja="金融市場",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>A:</strong> I wouldn't invest right now. Conditions are unstable...</p>
<p class='target'>...the market {{1}} <em>(crash)</em> tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> Je n'investirais pas maintenant. Les conditions sont instables...</p>
<p class='target'>...le marché {{1}} <em>(s'effondrer)</em> demain.</p>
""",
            de="""
<p><strong>A:</strong> Ich würde jetzt nicht investieren. Die Bedingungen sind instabil...</p>
<p class='target'>...morgen wird der Markt {{1}} <em>(zusammenbrechen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今は投資しない方がいいよ。状況が不安定だから…</p>
<p class='target'>…明日、市場は{{1}}かもしれない。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # Item 4 — Prediction / Tomorrow / 60 %  (Robertson 1145)
    dict(
        id='p_tmr_60', robertson_src=1145,
        ftr_mode='prediction', temporal='tomorrow', modality='low_60', certainty=60,
        context_header=dict(
            en="Weather Forecast",
            fr="Prévisions météo",
            de="Wettervorhersage",
            ja="天気予報",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Weather presenter:</strong> The forecast for tomorrow is fairly uncertain, but there is reason for optimism...</p>
<p class='target'>...we {{1}} <em>(see)</em> nice weather tomorrow.</p>
""",
            fr="""
<p><strong>Présentateur météo :</strong> Les prévisions pour demain sont assez incertaines, mais il y a des raisons d'être optimiste...</p>
<p class='target'>...on {{1}} <em>(voir)</em> du beau temps demain.</p>
""",
            de="""
<p><strong>Wettermoderator:</strong> Die Vorhersage für morgen ist recht unsicher, aber es gibt Grund zum Optimismus...</p>
<p class='target'>...morgen werden wir schönes Wetter {{1}} <em>(sehen)</em>.</p>
""",
            ja="""
<p><strong>気象キャスター：</strong>明日の予報はかなり不確かですが、良い兆しもあります…</p>
<p class='target'>…明日は良い天気が{{1}}でしょう。<em>（見られる）</em></p>
""",
        ),
    ),

    # Item 5 — Prediction / Tomorrow / 100 %  (Robertson 1077)
    dict(
        id='p_tmr_cer', robertson_src=1077,
        ftr_mode='prediction', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Oil Prices",
            fr="Prix du pétrole",
            de="Ölpreise",
            ja="原油価格",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>Q:</strong> What is your prediction for oil prices tomorrow?</p>
<p class='target'><strong>A:</strong> They {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Quelle est votre prédiction pour les prix du pétrole demain ?</p>
<p class='target'><strong>R :</strong> Ils {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Was ist Ihre Prognose für die Ölpreise morgen?</p>
<p class='target'><strong>A:</strong> Sie werden {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>明日の原油価格の予想は？</p>
<p class='target'><strong>回答：</strong>{{1}}。<em>（上がる）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  PREDICTIONS — 3 MONTHS  (5 items)
    # ─────────────────────────────────────────────────────────

    # Item 6 — Prediction / 3 months / Neutral  (Robertson 1028)
    dict(
        id='p_3mo_neu', robertson_src=1028,
        ftr_mode='prediction', temporal='three_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Gold Investment",
            fr="Investissement dans l'or",
            de="Goldinvestition",
            ja="金への投資",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>A:</strong> The price of gold always goes up in the autumn. Let's invest now...</p>
<p class='target'>...we {{1}} <em>(make)</em> a profit in a few months.</p>
""",
            fr="""
<p><strong>A :</strong> Le prix de l'or monte toujours en automne. Investissons maintenant...</p>
<p class='target'>...on {{1}} <em>(faire)</em> un bénéfice dans quelques mois.</p>
""",
            de="""
<p><strong>A:</strong> Der Goldpreis steigt im Herbst immer. Investieren wir jetzt...</p>
<p class='target'>...in ein paar Monaten werden wir einen Gewinn {{1}} <em>(machen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>金の価格は秋にはいつも上がるよ。今投資しよう…</p>
<p class='target'>…数ヶ月で利益を{{1}}でしょう。<em>（出す）</em></p>
""",
        ),
    ),

    # Item 7 — Prediction / 3 months / 40 %  (Robertson 1143)
    dict(
        id='p_3mo_40', robertson_src=1143,
        ftr_mode='prediction', temporal='three_months', modality='low_40', certainty=40,
        context_header=dict(
            en="Patient Health",
            fr="Santé du patient",
            de="Patientengesundheit",
            ja="患者の健康",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Doctor to patient:</strong> These results are concerning, but they can be caused by stress. Try to sleep and get some exercise. In a few months...</p>
<p class='target'>...you {{1}} <em>(feel)</em> better.</p>
""",
            fr="""
<p><strong>Médecin au patient :</strong> Ces résultats sont préoccupants, mais ils peuvent être dus au stress. Essayez de dormir et de faire de l'exercice. Dans quelques mois...</p>
<p class='target'>...vous {{1}} <em>(se sentir)</em> mieux.</p>
""",
            de="""
<p><strong>Arzt zum Patienten:</strong> Diese Ergebnisse sind besorgniserregend, aber sie können durch Stress verursacht werden. Versuchen Sie zu schlafen und sich zu bewegen. In ein paar Monaten...</p>
<p class='target'>...werden Sie sich besser {{1}} <em>(fühlen)</em>.</p>
""",
            ja="""
<p><strong>医師から患者へ：</strong>この結果は心配ですが、ストレスが原因の可能性もあります。睡眠と運動を心がけてください。数ヶ月すれば…</p>
<p class='target'>…{{1}}と思いますよ。<em>（気分が良くなる）</em></p>
""",
        ),
    ),

    # Item 8 — Prediction / 3 months / 50 %  (Robertson 1140)
    dict(
        id='p_3mo_50', robertson_src=1140,
        ftr_mode='prediction', temporal='three_months', modality='low_50', certainty=50,
        context_header=dict(
            en="Student Adjustment",
            fr="Adaptation d'une élève",
            de="Eingewöhnung einer Schülerin",
            ja="生徒の適応",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>Teacher to parent:</strong> Ellie worries me but I think she just needs some time to adjust. In a few months...</p>
<p class='target'>...she {{1}} <em>(improve)</em>.</p>
""",
            fr="""
<p><strong>Professeur au parent :</strong> Ellie m'inquiète, mais je pense qu'elle a juste besoin de temps pour s'adapter. Dans quelques mois...</p>
<p class='target'>...elle {{1}} <em>(progresser)</em>.</p>
""",
            de="""
<p><strong>Lehrerin zu den Eltern:</strong> Ellie macht mir Sorgen, aber ich denke, sie braucht nur etwas Zeit zur Eingewöhnung. In ein paar Monaten...</p>
<p class='target'>...wird sie sich {{1}} <em>(verbessern)</em>.</p>
""",
            ja="""
<p><strong>先生から保護者へ：</strong>エリーのことが心配ですが、慣れるまでの時間が必要なだけだと思います。数ヶ月すれば…</p>
<p class='target'>…{{1}}と思います。<em>（上達する）</em></p>
""",
        ),
    ),

    # Item 9 — Prediction / 3 months / 60 %  (Robertson 1139)
    dict(
        id='p_3mo_60', robertson_src=1139,
        ftr_mode='prediction', temporal='three_months', modality='low_60', certainty=60,
        context_header=dict(
            en="Virus Spread",
            fr="Propagation du virus",
            de="Virusausbreitung",
            ja="ウイルスの拡散",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Doctor to panel:</strong> We need more research on the transmission vectors...</p>
<p class='target'>...the virus {{1}} <em>(kill)</em> another 10,000 in the next few months.</p>
""",
            fr="""
<p><strong>Médecin au comité :</strong> Nous avons besoin de plus de recherches sur les vecteurs de transmission...</p>
<p class='target'>...le virus {{1}} <em>(tuer)</em> encore 10 000 personnes dans les prochains mois.</p>
""",
            de="""
<p><strong>Arzt zum Gremium:</strong> Wir brauchen mehr Forschung zu den Übertragungswegen...</p>
<p class='target'>...das Virus wird in den nächsten Monaten weitere 10.000 Menschen {{1}} <em>(töten)</em>.</p>
""",
            ja="""
<p><strong>医師から委員会へ：</strong>感染経路についてさらなる研究が必要です…</p>
<p class='target'>…今後数ヶ月で、そのウイルスはさらに1万人を{{1}}でしょう。<em>（死に至らしめる）</em></p>
""",
        ),
    ),

    # Item 10 — Prediction / 3 months / 100 %  (Robertson 1087)
    dict(
        id='p_3mo_cer', robertson_src=1087,
        ftr_mode='prediction', temporal='three_months', modality='certain', certainty=100,
        context_header=dict(
            en="Summer Weather",
            fr="Météo estivale",
            de="Sommerwetter",
            ja="夏の天気",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>In the spring, a weather presenter:</strong> There hasn't been such a sustained series of high pressure systems in years...</p>
<p class='target'>...we {{1}} <em>(see)</em> a lot of nice weather this summer.</p>
""",
            fr="""
<p><strong>Au printemps, un présentateur météo :</strong> Cela fait des années que nous n'avons pas eu une telle série prolongée de hautes pressions...</p>
<p class='target'>...on {{1}} <em>(voir)</em> beaucoup de beau temps cet été.</p>
""",
            de="""
<p><strong>Im Frühling, ein Wettermoderator:</strong> Seit Jahren gab es keine so anhaltende Reihe von Hochdruckgebieten...</p>
<p class='target'>...diesen Sommer werden wir viel schönes Wetter {{1}} <em>(sehen)</em>.</p>
""",
            ja="""
<p><strong>春のこと。気象キャスター：</strong>ここ数年ないほどの高気圧の連続です…</p>
<p class='target'>…今年の夏はたくさんの良い天気が{{1}}でしょう。<em>（見られる）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  PREDICTIONS — 2 YEARS  (5 items)
    # ─────────────────────────────────────────────────────────

    # Item 11 — Prediction / 3 months / Neutral  (Robertson 1029, was backup)
    dict(
        id='p_3mo_neu_b', robertson_src=1029,
        ftr_mode='prediction', temporal='three_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Winter Snow Forecast",
            fr="Prévisions de neige hivernale",
            de="Winterliche Schneeprognose",
            ja="冬の降雪予報",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>In the autumn, a weather presenter:</strong> Good news for all you skiers out there...</p>
<p class='target'>...we {{1}} <em>(see)</em> a lot of snow in the next few months.</p>
""",
            fr="""
<p><strong>En automne, un présentateur météo :</strong> Bonne nouvelle pour tous les amateurs de ski...</p>
<p class='target'>...on {{1}} <em>(voir)</em> beaucoup de neige dans les prochains mois.</p>
""",
            de="""
<p><strong>Im Herbst, ein Wettermoderator:</strong> Gute Nachrichten für alle Skifahrer da draußen...</p>
<p class='target'>...in den nächsten Monaten werden wir viel Schnee {{1}} <em>(sehen)</em>.</p>
""",
            ja="""
<p><strong>秋のこと。気象キャスター：</strong>スキー愛好家の皆さんに朗報です…</p>
<p class='target'>…今後数ヶ月で、たくさんの雪が{{1}}でしょう。<em>（降る）</em></p>
""",
        ),
    ),

    # Item 12 — Prediction / 2 years / 40 %  (Robertson 1162)
    dict(
        id='p_2yr_40', robertson_src=1162,
        ftr_mode='prediction', temporal='two_years', modality='low_40', certainty=40,
        context_header=dict(
            en="Property Value",
            fr="Valeur immobilière",
            de="Immobilienwert",
            ja="不動産価値",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> Are you selling your house?</p>
<p><strong>A:</strong> We are not sure. The market is shaky right now. In two years...</p>
<p class='target'>...it {{1}} <em>(be)</em> more valuable.</p>
""",
            fr="""
<p><strong>Q :</strong> Vous vendez votre maison ?</p>
<p><strong>R :</strong> On n'est pas sûrs. Le marché est instable en ce moment. Dans deux ans...</p>
<p class='target'>...elle {{1}} <em>(valoir)</em> plus.</p>
""",
            de="""
<p><strong>F:</strong> Verkaufen Sie Ihr Haus?</p>
<p><strong>A:</strong> Wir sind uns nicht sicher. Der Markt ist gerade instabil. In zwei Jahren...</p>
<p class='target'>...wird es mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>家を売るんですか？</p>
<p><strong>回答：</strong>わからない。今は市場が不安定だから。2年後には…</p>
<p class='target'>…もっと価値が{{1}}かもしれない。<em>（上がる）</em></p>
""",
        ),
    ),

    # Item 13 — Prediction / 2 years / 50 %  (Robertson 1164)
    dict(
        id='p_2yr_50', robertson_src=1164,
        ftr_mode='prediction', temporal='two_years', modality='low_50', certainty=50,
        context_header=dict(
            en="Retirement Savings",
            fr="Épargne retraite",
            de="Altersvorsorge",
            ja="老後の貯蓄",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>A:</strong> You should put money into a retirement savings plan. Interest rates are shaky now, but in two years...</p>
<p class='target'>...it {{1}} <em>(be)</em> worth quite a bit more.</p>
""",
            fr="""
<p><strong>A :</strong> Tu devrais placer de l'argent dans un plan d'épargne-retraite. Les taux d'intérêt sont instables, mais dans deux ans...</p>
<p class='target'>...ça {{1}} <em>(valoir)</em> bien plus.</p>
""",
            de="""
<p><strong>A:</strong> Sie sollten Geld in einen Rentensparplan stecken. Die Zinsen sind zwar unbeständig, aber in zwei Jahren...</p>
<p class='target'>...wird es deutlich mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>老後の貯蓄プランにお金を入れた方がいいよ。金利は不安定だけど、2年後には…</p>
<p class='target'>…かなり価値が{{1}}でしょう。<em>（増える）</em></p>
""",
        ),
    ),

    # Item 14 — Prediction / 2 years / 40 %  (Robertson 1155, was backup)
    dict(
        id='p_2yr_40_b', robertson_src=1155,
        ftr_mode='prediction', temporal='two_years', modality='low_40', certainty=40,
        context_header=dict(
            en="National Elections",
            fr="Élections nationales",
            de="Nationale Wahlen",
            ja="国政選挙",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> What do you think will happen in the national elections in two years?</p>
<p><strong>A:</strong> The incumbent has a strong base, but you never know...</p>
<p class='target'>...the challenger {{1}} <em>(win)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Que pensez-vous qu'il se passera aux élections nationales dans deux ans ?</p>
<p><strong>R :</strong> Le sortant a une base solide, mais on ne sait jamais...</p>
<p class='target'>...le candidat d'opposition {{1}} <em>(gagner)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Was glauben Sie, was bei den nationalen Wahlen in zwei Jahren passieren wird?</p>
<p><strong>A:</strong> Der Amtsinhaber hat eine starke Basis, aber man weiß nie...</p>
<p class='target'>...der Herausforderer wird {{1}} <em>(gewinnen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>2年後の国政選挙はどうなると思いますか？</p>
<p><strong>回答：</strong>現職は強い支持基盤があるけど、何が起こるかわからない…</p>
<p class='target'>…挑戦者が{{1}}かもしれない。<em>（勝つ）</em></p>
""",
        ),
    ),

    # Item 15 — Prediction / 2 years / 100 %  (Robertson 1105)
    dict(
        id='p_2yr_cer', robertson_src=1105,
        ftr_mode='prediction', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Sea Level Rise",
            fr="Montée du niveau de la mer",
            de="Meeresspiegelanstieg",
            ja="海面上昇",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>Q:</strong> What do you expect sea levels to do in the next two years?</p>
<p><strong>A:</strong> I mean...</p>
<p class='target'>...they {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Que pensez-vous qu'il arrivera au niveau de la mer dans les deux prochaines années ?</p>
<p><strong>R :</strong> Écoutez...</p>
<p class='target'>...il {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Was erwarten Sie vom Meeresspiegel in den nächsten zwei Jahren?</p>
<p><strong>A:</strong> Also...</p>
<p class='target'>...er wird {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>今後2年間で海面水位はどうなると思いますか？</p>
<p><strong>回答：</strong>まあ…</p>
<p class='target'>…{{1}}でしょう。<em>（上昇する）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  INTENTIONS  (5 items: 40→tomorrow, 100→tomorrow,
    #               neutral→3mo, 50→3mo, 60→2yr)
    # ─────────────────────────────────────────────────────────

    # Item 16 — Intention / Tomorrow / 40 %  (Robertson 1142)
    dict(
        id='i_tmr_40', robertson_src=1142,
        ftr_mode='intention', temporal='tomorrow', modality='low_40', certainty=40,
        context_header=dict(
            en="Party Attendance",
            fr="Invitation à une fête",
            de="Einladung zur Party",
            ja="パーティーへの出席",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Boy:</strong> My birthday is tomorrow... are you coming to my party?</p>
<p><strong>Girl:</strong> I really don't think I can make it, but...</p>
<p class='target'>...I {{1}} <em>(come)</em>.</p>
""",
            fr="""
<p><strong>Garçon :</strong> Mon anniversaire est demain... tu viens à ma fête ?</p>
<p><strong>Fille :</strong> Je ne pense vraiment pas pouvoir venir, mais...</p>
<p class='target'>...je {{1}} <em>(venir)</em>.</p>
""",
            de="""
<p><strong>Junge:</strong> Mein Geburtstag ist morgen... kommst du zu meiner Party?</p>
<p><strong>Mädchen:</strong> Ich glaube wirklich nicht, dass ich es schaffe, aber...</p>
<p class='target'>...ich werde {{1}} <em>(kommen)</em>.</p>
""",
            ja="""
<p><strong>男の子：</strong>明日が僕の誕生日なんだ…パーティーに来てくれる？</p>
<p><strong>女の子：</strong>行けるかどうかわからないけど…</p>
<p class='target'>…{{1}}と思う。<em>（行く）</em></p>
""",
        ),
    ),

    # Item 17 — Intention / Tomorrow / 100 %  (adapted from Robertson 1074)
    dict(
        id='i_tmr_cer', robertson_src=1074,
        ftr_mode='intention', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Holiday Travel",
            fr="Voyage de vacances",
            de="Urlaubsreise",
            ja="休暇旅行",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>Q:</strong> Are you going on holiday this summer?</p>
<p><strong>A:</strong> Yes, in a couple of months. My boyfriend doesn't want to, but...</p>
<p class='target'>...we {{1}} <em>(travel)</em> to Georgia.</p>
""",
            fr="""
<p><strong>Q :</strong> Tu pars en vacances cet été ?</p>
<p><strong>R :</strong> Oui, dans quelques mois. Mon copain ne veut pas, mais...</p>
<p class='target'>...on {{1}} <em>(voyager)</em> en Géorgie.</p>
""",
            de="""
<p><strong>F:</strong> Fahren Sie diesen Sommer in den Urlaub?</p>
<p><strong>A:</strong> Ja, in ein paar Monaten. Mein Freund will nicht, aber...</p>
<p class='target'>...wir werden nach Georgien {{1}} <em>(reisen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>今年の夏は休暇に行きますか？</p>
<p><strong>回答：</strong>うん、あと数ヶ月後にね。彼氏は行きたがらないんだけど…</p>
<p class='target'>…ジョージアに{{1}}。<em>（旅行する）</em></p>
""",
        ),
    ),

    # Item 18 — Intention / 3 months / Neutral  (Robertson 1026)
    dict(
        id='i_3mo_neu', robertson_src=1026,
        ftr_mode='intention', temporal='three_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Birthday Party",
            fr="Fête d'anniversaire",
            de="Geburtstagsparty",
            ja="誕生日パーティー",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>Girl:</strong> My birthday is in three months... are you coming to my party?</p>
<p class='target'><strong>Boy:</strong> I {{1}} <em>(be)</em> there.</p>
""",
            fr="""
<p><strong>Fille :</strong> Mon anniversaire est dans trois mois... tu viens à ma fête ?</p>
<p class='target'><strong>Garçon :</strong> J'y {{1}} <em>(être)</em>.</p>
""",
            de="""
<p><strong>Mädchen:</strong> Mein Geburtstag ist in drei Monaten... kommst du zu meiner Party?</p>
<p class='target'><strong>Junge:</strong> Ich werde da {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>女の子：</strong>3ヶ月後が私の誕生日なんだけど…パーティーに来てくれる？</p>
<p class='target'><strong>男の子：</strong>{{1}}よ。<em>（行く）</em></p>
""",
        ),
    ),

    # Item 19 — Intention / 3 months / 50 %  (Robertson 1137)
    dict(
        id='i_3mo_50', robertson_src=1137,
        ftr_mode='intention', temporal='three_months', modality='low_50', certainty=50,
        context_header=dict(
            en="Holiday Travel",
            fr="Voyage de vacances",
            de="Urlaubsreise",
            ja="休暇旅行",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>Q:</strong> Are you going on holiday this summer?</p>
<p><strong>A:</strong> I don't know. My annual review is in a few months. After that...</p>
<p class='target'>...I {{1}} <em>(travel)</em> to Italy.</p>
""",
            fr="""
<p><strong>Q :</strong> Tu pars en vacances cet été ?</p>
<p><strong>R :</strong> Je ne sais pas. Mon évaluation annuelle est dans quelques mois. Après ça...</p>
<p class='target'>...je {{1}} <em>(voyager)</em> en Italie.</p>
""",
            de="""
<p><strong>F:</strong> Fahren Sie diesen Sommer in den Urlaub?</p>
<p><strong>A:</strong> Ich weiß nicht. Mein Jahresgespräch ist in ein paar Monaten. Danach...</p>
<p class='target'>...werde ich nach Italien {{1}} <em>(reisen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>今年の夏は休暇に行きますか？</p>
<p><strong>回答：</strong>わからない。年次評価が数ヶ月後にある。それが終わったら…</p>
<p class='target'>…イタリアに{{1}}と思ってる。<em>（旅行する）</em></p>
""",
        ),
    ),

    # Item 20 — Intention / 2 years / 60 %  (Robertson 1165)
    dict(
        id='i_2yr_60', robertson_src=1165,
        ftr_mode='intention', temporal='two_years', modality='low_60', certainty=60,
        context_header=dict(
            en="Career Plan",
            fr="Plan de carrière",
            de="Karriereplan",
            ja="キャリアプラン",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Q:</strong> Do you have a plan for the next two years?</p>
<p><strong>A:</strong> Things are looking quite promising at work...</p>
<p class='target'>...I {{1}} <em>(make)</em> partner at my firm.</p>
""",
            fr="""
<p><strong>Q :</strong> Tu as un plan pour les deux prochaines années ?</p>
<p><strong>R :</strong> Les choses se présentent plutôt bien au travail...</p>
<p class='target'>...je {{1}} <em>(devenir)</em> associé(e) dans mon cabinet.</p>
""",
            de="""
<p><strong>F:</strong> Haben Sie einen Plan für die nächsten zwei Jahre?</p>
<p><strong>A:</strong> Bei der Arbeit sieht es ziemlich vielversprechend aus...</p>
<p class='target'>...ich werde in meiner Firma Partner {{1}} <em>(werden)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>今後2年間の計画はありますか？</p>
<p><strong>回答：</strong>仕事はかなりうまくいっていて…</p>
<p class='target'>…事務所のパートナーに{{1}}つもり。<em>（なる）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  SCHEDULING  (5 items: neutral→tomorrow, 50→tomorrow,
    #               60→3mo, 40→2yr, 100→2yr)
    # ─────────────────────────────────────────────────────────

    # Item 21 — Scheduling / Tomorrow / Neutral  (Robertson 1020)
    dict(
        id='s_tmr_neu', robertson_src=1020,
        ftr_mode='scheduling', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Flight Departure",
            fr="Départ du vol",
            de="Flugabflug",
            ja="フライトの出発",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>Q:</strong> When do you fly out?</p>
<p class='target'><strong>A:</strong> My flight {{1}} <em>(leave)</em> tomorrow!</p>
""",
            fr="""
<p><strong>Q :</strong> Quand est-ce que tu prends l'avion ?</p>
<p class='target'><strong>R :</strong> Mon vol {{1}} <em>(partir)</em> demain !</p>
""",
            de="""
<p><strong>F:</strong> Wann fliegst du ab?</p>
<p class='target'><strong>A:</strong> Mein Flug wird morgen {{1}} <em>(starten)</em>!</p>
""",
            ja="""
<p><strong>質問：</strong>いつ飛行機に乗るの？</p>
<p class='target'><strong>回答：</strong>私の便は明日{{1}}！<em>（出発する）</em></p>
""",
        ),
    ),

    # Item 22 — Scheduling / Tomorrow / 50 %  (Robertson 1141)
    dict(
        id='s_tmr_50', robertson_src=1141,
        ftr_mode='scheduling', temporal='tomorrow', modality='low_50', certainty=50,
        context_header=dict(
            en="Concert Date",
            fr="Date du concert",
            de="Konzerttermin",
            ja="コンサートの日程",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>Q:</strong> When is the concert?</p>
<p><strong>A:</strong> I think...</p>
<p class='target'>...they {{1}} <em>(play)</em> tomorrow.</p>
""",
            fr="""
<p><strong>Q :</strong> C'est quand le concert ?</p>
<p><strong>R :</strong> Je crois que...</p>
<p class='target'>...ils {{1}} <em>(jouer)</em> demain.</p>
""",
            de="""
<p><strong>F:</strong> Wann ist das Konzert?</p>
<p><strong>A:</strong> Ich glaube...</p>
<p class='target'>...sie werden morgen {{1}} <em>(spielen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>コンサートはいつ？</p>
<p><strong>回答：</strong>たしか…</p>
<p class='target'>…明日{{1}}と思う。<em>（演奏する）</em></p>
""",
        ),
    ),

    # Item 23 — Scheduling / 3 months / 60 %  (Robertson 1146)
    dict(
        id='s_3mo_60', robertson_src=1146,
        ftr_mode='scheduling', temporal='three_months', modality='low_60', certainty=60,
        context_header=dict(
            en="Thesis Defense",
            fr="Soutenance de thèse",
            de="Verteidigung der Dissertation",
            ja="論文審査",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Student:</strong> When exactly do I defend?</p>
<p><strong>Supervisor:</strong> I'm fairly confident it has been set...</p>
<p class='target'>...your viva {{1}} <em>(be)</em> in three months.</p>
""",
            fr="""
<p><strong>Étudiant :</strong> Quand est-ce que je soutiens exactement ?</p>
<p><strong>Directeur :</strong> Je suis assez confiant(e) que c'est fixé...</p>
<p class='target'>...votre soutenance {{1}} <em>(être)</em> dans trois mois.</p>
""",
            de="""
<p><strong>Student:</strong> Wann genau verteidige ich?</p>
<p><strong>Betreuer:</strong> Ich bin ziemlich sicher, dass es festgelegt wurde...</p>
<p class='target'>...Ihre Prüfung wird in drei Monaten {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>学生：</strong>具体的にいつ口頭試問ですか？</p>
<p><strong>指導教員：</strong>決まっていると思いますが…</p>
<p class='target'>…口頭試問は3ヶ月後に{{1}}はずです。<em>（ある）</em></p>
""",
        ),
    ),

    # Item 24 — Scheduling / 2 years / 40 %  (Robertson 1156)
    dict(
        id='s_2yr_40', robertson_src=1156,
        ftr_mode='scheduling', temporal='two_years', modality='low_40', certainty=40,
        context_header=dict(
            en="Contract Expiry",
            fr="Expiration du contrat",
            de="Vertragsablauf",
            ja="契約の満了",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> How long do you have on your contract?</p>
<p><strong>A:</strong> I really need to check, it's been a while...</p>
<p class='target'>...it {{1}} <em>(expire)</em> in two years.</p>
""",
            fr="""
<p><strong>Q :</strong> Il te reste combien de temps sur ton contrat ?</p>
<p><strong>R :</strong> Il faut vraiment que je vérifie, ça fait un moment...</p>
<p class='target'>...il {{1}} <em>(expirer)</em> dans deux ans.</p>
""",
            de="""
<p><strong>F:</strong> Wie lange läuft Ihr Vertrag noch?</p>
<p><strong>A:</strong> Ich müsste wirklich nachschauen, es ist schon eine Weile her...</p>
<p class='target'>...in zwei Jahren wird er {{1}} <em>(auslaufen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>契約はあとどのくらいですか？</p>
<p><strong>回答：</strong>確認しないといけないんですが、しばらく見てなくて…</p>
<p class='target'>…2年後に{{1}}と思います。<em>（満了する）</em></p>
""",
        ),
    ),

    # Item 25 — Scheduling / 2 years / 100 %  (Robertson 1108)
    dict(
        id='s_2yr_cer', robertson_src=1108,
        ftr_mode='scheduling', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Bond Maturity",
            fr="Échéance de l'obligation",
            de="Fälligkeit der Anleihe",
            ja="債券の満期",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>Father to son:</strong> I have just checked...</p>
<p class='target'>...your bond {{1}} <em>(mature)</em> in two years.</p>
""",
            fr="""
<p><strong>Père à son fils :</strong> Je viens de vérifier...</p>
<p class='target'>...ton obligation {{1}} <em>(arriver à échéance)</em> dans deux ans.</p>
""",
            de="""
<p><strong>Vater zum Sohn:</strong> Ich habe gerade nachgesehen...</p>
<p class='target'>...deine Anleihe wird in zwei Jahren {{1}} <em>(fällig werden)</em>.</p>
""",
            ja="""
<p><strong>父から息子へ：</strong>今確認したところ…</p>
<p class='target'>…お前の債券は2年後に{{1}}。<em>（満期になる）</em></p>
""",
        ),
    ),


    # ══════════════════════════════════════════════════════════
    #  ATTENTION CHECKS  (2)
    #  Disguised as normal scenarios; embedded instruction asks
    #  participant to type "yes". Buried mid-page on Pages 1 & 3.
    #  IDs: ac_1, ac_2  (indices 25, 26)
    # ══════════════════════════════════════════════════════════

    # AC 1 — Looks like a prediction / tomorrow item (placed in Page 1)
    dict(
        id='ac_1', robertson_src=None,
        ftr_mode='attention_check', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Local Weather",
            fr="Météo locale",
            de="Lokales Wetter",
            ja="地元の天気",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>A:</strong> I heard the weather report on the radio this morning. There's a cold front coming through.</p>
<p><strong>B:</strong> Really? That would explain the clouds...</p>
<p class='target'>This is an attention check. Please simply enter the word <em>dance</em> for this question: {{1}}</p>
""",
            fr="""
<p><strong>A :</strong> J'ai entendu le bulletin météo à la radio ce matin. Un front froid approche.</p>
<p><strong>B :</strong> Vraiment ? Cela expliquerait les nuages...</p>
<p class='target'>Ceci est une question d'attention. Veuillez simplement entrer le mot <em>danse</em> pour cette question : {{1}}</p>
""",
            de="""
<p><strong>A:</strong> Ich habe heute Morgen den Wetterbericht im Radio gehört. Eine Kaltfront kommt durch.</p>
<p><strong>B:</strong> Wirklich? Das würde die Wolken erklären...</p>
<p class='target'>Dies ist eine Aufmerksamkeitsfrage. Bitte geben Sie einfach das Wort <em>Tanz</em> für diese Frage ein: {{1}}</p>
""",
            ja="""
<p><strong>A：</strong>今朝ラジオで天気予報を聞いたよ。寒冷前線が来ているらしい。</p>
<p><strong>B：</strong>本当に？それで曇っているのか…</p>
<p class='target'>これは注意確認の質問です。この質問には <em>ダンス</em> とだけ入力してください：{{1}}</p>
""",
        ),
    ),

    # AC 2 — Looks like a scheduling / 3-month item (placed in Page 3)
    dict(
        id='ac_2', robertson_src=None,
        ftr_mode='attention_check', temporal='three_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Office Relocation",
            fr="Déménagement du bureau",
            de="Büroumzug",
            ja="オフィスの移転",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>A:</strong> Have you heard anything about the office moving to the new building?</p>
<p><strong>B:</strong> Yes, management sent an email about it last week...</p>
<p class='target'>This is an attention check. Please simply enter the word <em>segue</em> for this question: {{1}}</p>
""",
            fr="""
<p><strong>A :</strong> Tu as des nouvelles concernant le déménagement du bureau dans le nouveau bâtiment ?</p>
<p><strong>B :</strong> Oui, la direction a envoyé un e-mail à ce sujet la semaine dernière...</p>
<p class='target'>Ceci est une question d'attention. Veuillez simplement entrer le mot <em>transition</em> pour cette question : {{1}}</p>
""",
            de="""
<p><strong>A:</strong> Haben Sie etwas über den Büroumzug ins neue Gebäude gehört?</p>
<p><strong>B:</strong> Ja, die Geschäftsführung hat letzte Woche eine E-Mail dazu geschickt...</p>
<p class='target'>Dies ist eine Aufmerksamkeitsfrage. Bitte geben Sie einfach das Wort <em>Übergang</em> für diese Frage ein: {{1}}</p>
""",
            ja="""
<p><strong>A：</strong>オフィスが新しいビルに移転する件、何か聞いた？</p>
<p><strong>B：</strong>うん、先週経営陣からメールが来たよ…</p>
<p class='target'>これは注意確認の質問です。この質問には <em>転換</em> とだけ入力してください：{{1}}</p>
""",
        ),
    ),


    # ══════════════════════════════════════════════════════════
    #  BACKUP PREDICTION ITEMS  (15)
    #  Same 3×5 factorial, alternate items from Robertson A.5
    # ══════════════════════════════════════════════════════════

    # ─────────────────────────────────────────────────────────
    #  BACKUP PREDICTIONS — TOMORROW
    # ─────────────────────────────────────────────────────────

    # Item 26 — Backup / Tomorrow / Neutral  (Robertson 1024)
    dict(
        id='bp_tmr_neu', robertson_src=1024,
        ftr_mode='prediction', temporal='tomorrow', modality='neutral', certainty=None,
        context_header=dict(
            en="Student Progress",
            fr="Progrès d'un élève",
            de="Fortschritte eines Schülers",
            ja="生徒の進歩",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>Teacher to parent:</strong> It can take some time for kids to adjust to a new school. Even by tomorrow...</p>
<p class='target'>...Johnny {{1}} <em>(improve)</em>.</p>
""",
            fr="""
<p><strong>Professeur au parent :</strong> Les enfants ont parfois besoin de temps pour s'adapter à une nouvelle école. Même d'ici demain...</p>
<p class='target'>...Johnny {{1}} <em>(progresser)</em>.</p>
""",
            de="""
<p><strong>Lehrerin zu den Eltern:</strong> Kinder brauchen manchmal Zeit, um sich an eine neue Schule zu gewöhnen. Schon morgen...</p>
<p class='target'>...wird Johnny sich {{1}} <em>(verbessern)</em>.</p>
""",
            ja="""
<p><strong>先生から保護者へ：</strong>新しい学校に慣れるには時間がかかることもあります。明日にはもう…</p>
<p class='target'>…ジョニーは{{1}}でしょう。<em>（上達する）</em></p>
""",
        ),
    ),

    # Item 27 — Backup / Tomorrow / 40 %  (Robertson 1138)
    dict(
        id='bp_tmr_40', robertson_src=1138,
        ftr_mode='prediction', temporal='tomorrow', modality='low_40', certainty=40,
        context_header=dict(
            en="Retail Price Drop",
            fr="Baisse des prix en magasin",
            de="Preissenkung im Handel",
            ja="小売価格の下落",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Salesman to customer:</strong> I'd try coming back tomorrow. People aren't buying too many...</p>
<p class='target'>...the price {{1}} <em>(drop)</em>.</p>
""",
            fr="""
<p><strong>Vendeur au client :</strong> Je reviendrais demain si j'étais vous. Les gens n'en achètent pas beaucoup...</p>
<p class='target'>...le prix {{1}} <em>(baisser)</em>.</p>
""",
            de="""
<p><strong>Verkäufer zum Kunden:</strong> Versuchen Sie morgen wiederzukommen. Die Leute kaufen nicht viele davon...</p>
<p class='target'>...der Preis wird {{1}} <em>(sinken)</em>.</p>
""",
            ja="""
<p><strong>店員から客へ：</strong>明日またお越しになってみてください。あまり売れていないので…</p>
<p class='target'>…価格は{{1}}かもしれません。<em>（下がる）</em></p>
""",
        ),
    ),

    # Item 28 — Backup / Tomorrow / 50 %  (Robertson 1144)
    dict(
        id='bp_tmr_50', robertson_src=1144,
        ftr_mode='prediction', temporal='tomorrow', modality='low_50', certainty=50,
        context_header=dict(
            en="Gold Investment",
            fr="Investissement dans l'or",
            de="Goldinvestition",
            ja="金への投資",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>A:</strong> Gold usually goes up when markets are nervous. Don't worry...</p>
<p class='target'>...we {{1}} <em>(start)</em> to make money by tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> L'or monte généralement quand les marchés sont agités. Ne t'inquiète pas...</p>
<p class='target'>...on {{1}} <em>(commencer)</em> à gagner de l'argent d'ici demain.</p>
""",
            de="""
<p><strong>A:</strong> Gold steigt normalerweise, wenn die Märkte nervös sind. Keine Sorge...</p>
<p class='target'>...bis morgen werden wir {{1}} <em>(anfangen)</em>, Geld zu verdienen.</p>
""",
            ja="""
<p><strong>A：</strong>市場が不安定なときは金が上がることが多い。心配しないで…</p>
<p class='target'>…明日には利益が{{1}}でしょう。<em>（出始める）</em></p>
""",
        ),
    ),

    # Item 29 — Backup / Tomorrow / 60 %  (Robertson 1134)
    dict(
        id='bp_tmr_60', robertson_src=1134,
        ftr_mode='prediction', temporal='tomorrow', modality='low_60', certainty=60,
        context_header=dict(
            en="Collectible Value",
            fr="Valeur d'un objet de collection",
            de="Sammlerwert",
            ja="コレクターズアイテムの価値",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Father to son:</strong> Don't throw out that action figure. We are going to the comic convention tomorrow...</p>
<p class='target'>...it {{1}} <em>(be)</em> worth something there.</p>
""",
            fr="""
<p><strong>Père à son fils :</strong> Ne jette pas cette figurine. On va au salon de la BD demain...</p>
<p class='target'>...elle {{1}} <em>(valoir)</em> quelque chose là-bas.</p>
""",
            de="""
<p><strong>Vater zum Sohn:</strong> Wirf die Actionfigur nicht weg. Wir gehen morgen zur Comic-Messe...</p>
<p class='target'>...sie wird dort etwas wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>父から息子へ：</strong>そのフィギュアを捨てるな。明日コミックコンベンションに行くだろう…</p>
<p class='target'>…あそこでなら価値が{{1}}はず。<em>（ある）</em></p>
""",
        ),
    ),

    # Item 30 — Backup / Tomorrow / 100 %  (Robertson 1075)
    dict(
        id='bp_tmr_cer', robertson_src=1075,
        ftr_mode='prediction', temporal='tomorrow', modality='certain', certainty=100,
        context_header=dict(
            en="Commodities Crash",
            fr="Effondrement des matières premières",
            de="Rohstoff-Crash",
            ja="商品市場の崩壊",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>A:</strong> Don't invest in commodities right now. The market is very shaky...</p>
<p class='target'>...it {{1}} <em>(crash)</em> by tomorrow.</p>
""",
            fr="""
<p><strong>A :</strong> N'investissez pas dans les matières premières maintenant. Le marché est très fragile...</p>
<p class='target'>...il {{1}} <em>(s'effondrer)</em> d'ici demain.</p>
""",
            de="""
<p><strong>A:</strong> Investieren Sie jetzt nicht in Rohstoffe. Der Markt ist sehr wackelig...</p>
<p class='target'>...bis morgen wird er {{1}} <em>(zusammenbrechen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>今は商品市場に投資しないで。市場がとても不安定だから…</p>
<p class='target'>…明日までに{{1}}よ。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  BACKUP PREDICTIONS — 3 MONTHS
    # ─────────────────────────────────────────────────────────

    # Item 31 — Backup / 3 months / Neutral  (Robertson 1029)
    dict(
        id='bp_3mo_neu', robertson_src=1029,
        ftr_mode='prediction', temporal='three_months', modality='neutral', certainty=None,
        context_header=dict(
            en="Winter Snow Forecast",
            fr="Prévisions de neige hivernale",
            de="Winterliche Schneeprognose",
            ja="冬の降雪予報",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>In the autumn, a weather presenter:</strong> Good news for all you skiers out there...</p>
<p class='target'>...we {{1}} <em>(see)</em> a lot of snow in the next few months.</p>
""",
            fr="""
<p><strong>En automne, un présentateur météo :</strong> Bonne nouvelle pour tous les amateurs de ski...</p>
<p class='target'>...on {{1}} <em>(voir)</em> beaucoup de neige dans les prochains mois.</p>
""",
            de="""
<p><strong>Im Herbst, ein Wettermoderator:</strong> Gute Nachrichten für alle Skifahrer da draußen...</p>
<p class='target'>...in den nächsten Monaten werden wir viel Schnee {{1}} <em>(sehen)</em>.</p>
""",
            ja="""
<p><strong>秋のこと。気象キャスター：</strong>スキー愛好家の皆さんに朗報です…</p>
<p class='target'>…今後数ヶ月で、たくさんの雪が{{1}}でしょう。<em>（降る）</em></p>
""",
        ),
    ),

    # Item 32 — Backup / 3 months / 40 %  (Robertson 1149)
    dict(
        id='bp_3mo_40', robertson_src=1149,
        ftr_mode='prediction', temporal='three_months', modality='low_40', certainty=40,
        context_header=dict(
            en="Upcoming Elections",
            fr="Prochaines élections",
            de="Bevorstehende Wahlen",
            ja="次の選挙",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> What do you think will happen to the ruling party?</p>
<p class='target'><strong>A:</strong> They {{1}} <em>(lose)</em> in a few months.</p>
""",
            fr="""
<p><strong>Q :</strong> Que pensez-vous qu'il arrivera au parti au pouvoir ?</p>
<p class='target'><strong>R :</strong> Ils {{1}} <em>(perdre)</em> dans quelques mois.</p>
""",
            de="""
<p><strong>F:</strong> Was glauben Sie, was mit der Regierungspartei passieren wird?</p>
<p class='target'><strong>A:</strong> In ein paar Monaten werden sie {{1}} <em>(verlieren)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>与党はどうなると思いますか？</p>
<p class='target'><strong>回答：</strong>数ヶ月後に{{1}}と思います。<em>（負ける）</em></p>
""",
        ),
    ),

    # Item 33 — Backup / 3 months / 50 %  (Robertson 1023)
    dict(
        id='bp_3mo_50', robertson_src=1023,
        ftr_mode='prediction', temporal='three_months', modality='low_50', certainty=50,
        context_header=dict(
            en="Epidemic Spread",
            fr="Propagation de l'épidémie",
            de="Epidemieausbreitung",
            ja="疫病の拡大",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>Doctor to panel:</strong> At current infection rates...</p>
<p class='target'>...the epidemic {{1}} <em>(kill)</em> another 10,000 in the next few months.</p>
""",
            fr="""
<p><strong>Médecin au comité :</strong> Au rythme actuel des infections...</p>
<p class='target'>...l'épidémie {{1}} <em>(tuer)</em> encore 10 000 personnes dans les prochains mois.</p>
""",
            de="""
<p><strong>Arzt zum Gremium:</strong> Bei den aktuellen Infektionsraten...</p>
<p class='target'>...wird die Epidemie in den nächsten Monaten weitere 10.000 Menschen {{1}} <em>(töten)</em>.</p>
""",
            ja="""
<p><strong>医師から委員会へ：</strong>現在の感染率では…</p>
<p class='target'>…この疫病は今後数ヶ月でさらに1万人を{{1}}でしょう。<em>（死に至らしめる）</em></p>
""",
        ),
    ),

    # Item 34 — Backup / 3 months / 60 %  (Robertson 1082)
    dict(
        id='bp_3mo_60', robertson_src=1082,
        ftr_mode='prediction', temporal='three_months', modality='low_60', certainty=60,
        context_header=dict(
            en="Student Settling In",
            fr="Adaptation d'un élève",
            de="Eingewöhnung eines Schülers",
            ja="生徒の適応",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Teacher to parent:</strong> Peter just needs time to settle in. In a few months...</p>
<p class='target'>...he {{1}} <em>(improve)</em>.</p>
""",
            fr="""
<p><strong>Professeur au parent :</strong> Peter a juste besoin de temps pour s'adapter. Dans quelques mois...</p>
<p class='target'>...il {{1}} <em>(progresser)</em>.</p>
""",
            de="""
<p><strong>Lehrerin zu den Eltern:</strong> Peter braucht nur Zeit zur Eingewöhnung. In ein paar Monaten...</p>
<p class='target'>...wird er sich {{1}} <em>(verbessern)</em>.</p>
""",
            ja="""
<p><strong>先生から保護者へ：</strong>ピーターは慣れるまでに時間が必要なだけです。数ヶ月すれば…</p>
<p class='target'>…{{1}}でしょう。<em>（上達する）</em></p>
""",
        ),
    ),

    # Item 35 — Backup / 3 months / 100 %  (Robertson 1086)
    dict(
        id='bp_3mo_cer', robertson_src=1086,
        ftr_mode='prediction', temporal='three_months', modality='certain', certainty=100,
        context_header=dict(
            en="Oil Investment",
            fr="Investissement dans le pétrole",
            de="Öl-Investition",
            ja="石油投資",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>A:</strong> The price of oil always goes up in the summer. Let's invest now...</p>
<p class='target'>...we {{1}} <em>(make)</em> a profit in a few months.</p>
""",
            fr="""
<p><strong>A :</strong> Le prix du pétrole monte toujours en été. Investissons maintenant...</p>
<p class='target'>...on {{1}} <em>(faire)</em> un bénéfice dans quelques mois.</p>
""",
            de="""
<p><strong>A:</strong> Der Ölpreis steigt im Sommer immer. Investieren wir jetzt...</p>
<p class='target'>...in ein paar Monaten werden wir einen Gewinn {{1}} <em>(machen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>石油の価格は夏にはいつも上がる。今投資しよう…</p>
<p class='target'>…数ヶ月で利益を{{1}}。<em>（出す）</em></p>
""",
        ),
    ),

    # ─────────────────────────────────────────────────────────
    #  BACKUP PREDICTIONS — 2 YEARS
    # ─────────────────────────────────────────────────────────

    # Item 36 — Backup / 2 years / Neutral  (Robertson 1034)
    dict(
        id='bp_2yr_neu', robertson_src=1034,
        ftr_mode='prediction', temporal='two_years', modality='neutral', certainty=None,
        context_header=dict(
            en="Tech Industry",
            fr="Industrie technologique",
            de="Technologiebranche",
            ja="テクノロジー業界",
        ),
        context_prob=_PROB[None],
        text=dict(
            en="""
<p><strong>A:</strong> Don't bother investing in the tech industry...</p>
<p class='target'>...it {{1}} <em>(crash)</em> within two years.</p>
""",
            fr="""
<p><strong>A :</strong> Ne vous donnez pas la peine d'investir dans le secteur technologique...</p>
<p class='target'>...il {{1}} <em>(s'effondrer)</em> d'ici deux ans.</p>
""",
            de="""
<p><strong>A:</strong> Investieren Sie nicht in die Technologiebranche...</p>
<p class='target'>...sie wird innerhalb von zwei Jahren {{1}} <em>(zusammenbrechen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>テクノロジー業界に投資しても無駄だよ…</p>
<p class='target'>…2年以内に{{1}}から。<em>（崩壊する）</em></p>
""",
        ),
    ),

    # Item 37 — Backup / 2 years / 40 %  (Robertson 1155)
    dict(
        id='bp_2yr_40', robertson_src=1155,
        ftr_mode='prediction', temporal='two_years', modality='low_40', certainty=40,
        context_header=dict(
            en="National Elections",
            fr="Élections nationales",
            de="Nationale Wahlen",
            ja="国政選挙",
        ),
        context_prob=_PROB[40],
        text=dict(
            en="""
<p><strong>Q:</strong> What do you think will happen in the national elections in two years?</p>
<p><strong>A:</strong> The incumbent has a strong base, but you never know...</p>
<p class='target'>...the challenger {{1}} <em>(win)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Que pensez-vous qu'il se passera aux élections nationales dans deux ans ?</p>
<p><strong>R :</strong> Le sortant a une base solide, mais on ne sait jamais...</p>
<p class='target'>...le candidat d'opposition {{1}} <em>(gagner)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Was glauben Sie, was bei den nationalen Wahlen in zwei Jahren passieren wird?</p>
<p><strong>A:</strong> Der Amtsinhaber hat eine starke Basis, aber man weiß nie...</p>
<p class='target'>...der Herausforderer wird {{1}} <em>(gewinnen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>2年後の国政選挙はどうなると思いますか？</p>
<p><strong>回答：</strong>現職は強い支持基盤があるけど、何が起こるかわからない…</p>
<p class='target'>…挑戦者が{{1}}かもしれない。<em>（勝つ）</em></p>
""",
        ),
    ),

    # Item 38 — Backup / 2 years / 50 %  (Robertson 1048)
    dict(
        id='bp_2yr_50', robertson_src=1048,
        ftr_mode='prediction', temporal='two_years', modality='low_50', certainty=50,
        context_header=dict(
            en="Savings Growth",
            fr="Croissance de l'épargne",
            de="Ersparniszuwachs",
            ja="貯蓄の成長",
        ),
        context_prob=_PROB[50],
        text=dict(
            en="""
<p><strong>A:</strong> You should put money into a savings plan. In just two years...</p>
<p class='target'>...it {{1}} <em>(be)</em> worth a lot more.</p>
""",
            fr="""
<p><strong>A :</strong> Tu devrais placer de l'argent dans un plan d'épargne. Dans seulement deux ans...</p>
<p class='target'>...ça {{1}} <em>(valoir)</em> beaucoup plus.</p>
""",
            de="""
<p><strong>A:</strong> Sie sollten Geld in einen Sparplan stecken. In nur zwei Jahren...</p>
<p class='target'>...wird es viel mehr wert {{1}} <em>(sein)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>貯蓄プランにお金を入れた方がいいよ。たった2年で…</p>
<p class='target'>…ずっと価値が{{1}}はず。<em>（増える）</em></p>
""",
        ),
    ),

    # Item 39 — Backup / 2 years / 60 %  (Robertson 1163)
    dict(
        id='bp_2yr_60', robertson_src=1163,
        ftr_mode='prediction', temporal='two_years', modality='low_60', certainty=60,
        context_header=dict(
            en="Global Temperatures",
            fr="Températures mondiales",
            de="Globale Temperaturen",
            ja="世界の気温",
        ),
        context_prob=_PROB[60],
        text=dict(
            en="""
<p><strong>Q:</strong> What do you expect temperatures to do in the next two years?</p>
<p><strong>A:</strong> The science is unclear, right?</p>
<p class='target'>...they {{1}} <em>(rise)</em>.</p>
""",
            fr="""
<p><strong>Q :</strong> Que pensez-vous qu'il arrivera aux températures dans les deux prochaines années ?</p>
<p><strong>R :</strong> La science n'est pas claire, n'est-ce pas ?</p>
<p class='target'>...elles {{1}} <em>(monter)</em>.</p>
""",
            de="""
<p><strong>F:</strong> Was erwarten Sie von den Temperaturen in den nächsten zwei Jahren?</p>
<p><strong>A:</strong> Die Wissenschaft ist nicht eindeutig, oder?</p>
<p class='target'>...sie werden {{1}} <em>(steigen)</em>.</p>
""",
            ja="""
<p><strong>質問：</strong>今後2年間で気温はどうなると思いますか？</p>
<p><strong>回答：</strong>科学的にもはっきりしていないけど…</p>
<p class='target'>…{{1}}と思う。<em>（上昇する）</em></p>
""",
        ),
    ),

    # Item 40 — Backup / 2 years / 100 %  (Robertson 1092)
    dict(
        id='bp_2yr_cer', robertson_src=1092,
        ftr_mode='prediction', temporal='two_years', modality='certain', certainty=100,
        context_header=dict(
            en="Market Bubble",
            fr="Bulle de marché",
            de="Marktblase",
            ja="市場バブル",
        ),
        context_prob=_PROB[100],
        text=dict(
            en="""
<p><strong>A:</strong> Don't bother investing in that market. There is a bubble...</p>
<p class='target'>...it {{1}} <em>(crash)</em> within two years.</p>
""",
            fr="""
<p><strong>A :</strong> Ne vous donnez pas la peine d'investir dans ce marché. Il y a une bulle...</p>
<p class='target'>...il {{1}} <em>(s'effondrer)</em> d'ici deux ans.</p>
""",
            de="""
<p><strong>A:</strong> Investieren Sie nicht in diesen Markt. Es gibt eine Blase...</p>
<p class='target'>...er wird innerhalb von zwei Jahren {{1}} <em>(zusammenbrechen)</em>.</p>
""",
            ja="""
<p><strong>A：</strong>あの市場に投資しても無駄だよ。バブルがあるから…</p>
<p class='target'>…2年以内に{{1}}。<em>（崩壊する）</em></p>
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

T2_PRACTICE_HTML = dict(
    en="""
<div class='ctx-header-practice'>Weekend Plans</div>
<p><strong>Q:</strong> What are you doing this weekend?</p>
<p><strong>A:</strong> I'm not sure yet, but I think I {{1}} <em>(visit)</em> my parents on Saturday.</p>
<p>And on Sunday, the weather looks nice, so we {{2}} <em>(go)</em> hiking.</p>
""",
    fr="""
<div class='ctx-header-practice'>Plans du week-end</div>
<p><strong>Q :</strong> Qu'est-ce que tu fais ce week-end ?</p>
<p><strong>R :</strong> Je ne sais pas encore, mais je pense que je {{1}} <em>(rendre visite)</em> \u00e0 mes parents samedi.</p>
<p>Et dimanche, il fera beau, alors on {{2}} <em>(faire)</em> une randonn\u00e9e.</p>
""",
    de="""
<div class='ctx-header-practice'>Wochenendpl\u00e4ne</div>
<p><strong>F:</strong> Was machst du dieses Wochenende?</p>
<p><strong>A:</strong> Ich bin mir noch nicht sicher, aber ich denke, ich werde am Samstag meine Eltern {{1}} <em>(besuchen)</em>.</p>
<p>Und am Sonntag sieht das Wetter gut aus, also werden wir {{2}} <em>(wandern)</em>.</p>
""",
    ja="""
<div class='ctx-header-practice'>\u9031\u672b\u306e\u4e88\u5b9a</div>
<p><strong>\u8cea\u554f\uff1a</strong>\u9031\u672b\u306f\u4f55\u3092\u3057\u307e\u3059\u304b\uff1f</p>
<p><strong>\u56de\u7b54\uff1a</strong>\u307e\u3060\u308f\u304b\u3089\u306a\u3044\u3051\u3069\u3001\u571f\u66dc\u65e5\u306b\u4e21\u89aa\u3092{{1}}\u3068\u601d\u3046\u3002<em>\uff08\u8a2a\u306d\u308b\uff09</em></p>
<p>\u65e5\u66dc\u65e5\u306f\u5929\u6c17\u304c\u3088\u3055\u305d\u3046\u3060\u304b\u3089\u3001\u30cf\u30a4\u30ad\u30f3\u30b0\u306b{{2}}\u3002<em>\uff08\u884c\u304f\uff09</em></p>
""",
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

    # Task 2.1 responses: {"p_tmr_neu": {"1": "will drop"}, ...}
    t2_production_data = models.LongStringField(initial='{}', blank=True)

    # Task 2.2 responses: {"It will rain...": 80, ...}
    t2_perception_data = models.LongStringField(initial='{}', blank=True)

    # Attention checks: True if participant typed the correct word
    t2_ac1_pass = models.BooleanField(initial=False)
    t2_ac2_pass = models.BooleanField(initial=False)


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
        ctx = _ctx(player, 50)
        ctx['t2_practice_html'] = T2_PRACTICE_HTML.get(lang, T2_PRACTICE_HTML['en'])
        return ctx


# ── Page layout ──────────────────────────────────────────
# Primary items (0–24) + 2 attention checks (25, 26)
# Backup  items (27–41): 1 page of 15
#
# AC1 (index 25) 3rd-to-last on Page 1; AC2 (index 26) 3rd-to-last on Page 3
PRIMARY_CHUNKS = [
    [0, 1, 2, 3, 4, 5, 6, 25, 7, 8],       # Page 1: 10 items (AC1 at pos 8/10)
    list(range(9, 17)),                       # Page 2: 8 items
    [17, 18, 19, 20, 21, 22, 26, 23, 24],   # Page 3: 9 items (AC2 at pos 7/9)
]
BACKUP_CHUNK = list(range(27, 42))  # Page 4: backup items 28–42

# Attention-check expected answers per language
# Attention-check expected answers per language
_AC_EXPECTED = dict(
    ac_1=dict(en='dance', fr='danse', de='tanz', ja='ダンス'),
    ac_2=dict(en='segue', fr='transition', de='übergang', ja='転換'),
)


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

    @staticmethod
    def before_next_page(player, timeout_happened):
        """Score attention checks after each page submission."""
        try:
            data = json.loads(player.t2_production_data or '{}')
        except (json.JSONDecodeError, TypeError):
            return
        lang = player.language
        # Check AC1
        ac1 = data.get('ac_1', {})
        if ac1:
            answer = ac1.get('1', '').strip().lower()
            player.t2_ac1_pass = (answer == _AC_EXPECTED['ac_1'].get(lang, ''))
        # Check AC2
        ac2 = data.get('ac_2', {})
        if ac2:
            answer = ac2.get('1', '').strip().lower()
            player.t2_ac2_pass = (answer == _AC_EXPECTED['ac_2'].get(lang, ''))


def _make_item_page(indices, progress, label):
    """Factory: generate one Task2Item page for a chunk of scenario indices."""
    class _ItemPage(Task2Item):
        @staticmethod
        def vars_for_template(player):
            return Task2Item._vars(player, indices, progress)

    _ItemPage.__name__     = f'Task2ItemPage_{label}'
    _ItemPage.__qualname__ = f'Task2ItemPage_{label}'
    return _ItemPage


# Build primary pages (progress 55 → 70 → 80)
_ITEM_PAGES = []
_primary_progresses = [55, 68, 80]
for i, chunk in enumerate(PRIMARY_CHUNKS):
    label = f'{chunk[0] + 1}_{chunk[-1] + 1}'
    _ITEM_PAGES.append(_make_item_page(chunk, _primary_progresses[i], label))

# Build backup page (progress 90)
# Backup page disabled for now
# _backup_label = f'{BACKUP_CHUNK[0] + 1}_{BACKUP_CHUNK[-1] + 1}'
# _ITEM_PAGES.append(_make_item_page(BACKUP_CHUNK, 90, _backup_label))


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