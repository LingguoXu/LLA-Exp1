from otree.api import *
import json

doc = """
Cross-linguistic FTR & Loss Aversion — Task 1 trial.
Languages: English (en), French (fr), German (de), Japanese (ja).
"""


class C(BaseConstants):
    NAME_IN_URL = 'task1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# ═══════════════════════════════════════════════════════════
# UI STRINGS
# ═══════════════════════════════════════════════════════════
UI = dict(
    # General buttons & messages
    btn_continue=dict(en='Continue', fr='Continuer', de='Weiter', ja='次へ'),
    btn_read_more=dict(en='Continue reading\u2026', fr='Lire la suite\u2026', de='Weiterlesen\u2026', ja='続きを読む...'),
    btn_start=dict(en="Let's begin", fr='Commençons', de="Los geht's", ja='始めましょう'),
    btn_finish=dict(en='Finish', fr='Terminer', de='Fertig', ja='終了'),
    required_msg=dict(
        en='Please fill in every blank before continuing.',
        fr='Veuillez remplir tous les espaces avant de continuer.',
        de='Bitte f\u00fcllen Sie alle L\u00fccken aus, bevor Sie fortfahren.',
        ja='先に進む前にすべての空欄を埋めてください。',
    ),

    # ── Welcome / Study Introduction ──
    welcome_title=dict(
        en='Welcome',
        fr='Bienvenue',
        de='Willkommen',
        ja='ようこそ',
    ),
    welcome_body=dict(
        en='Thank you for taking part in this study. You will complete a series of short language tasks — reading stories, filling in blanks, and rating sentences. There are no right or wrong answers; we are interested in how you naturally use language.',
        fr='Merci de participer à cette étude. Vous allez réaliser une série de courtes tâches linguistiques — lire des histoires, compléter des phrases et évaluer des énoncés. Il n\u2019y a pas de bonnes ou de mauvaises réponses ; nous nous intéressons à votre usage naturel de la langue.',
        de='Vielen Dank für Ihre Teilnahme an dieser Studie. Sie werden eine Reihe kurzer Sprachaufgaben bearbeiten — Geschichten lesen, Lücken ausfüllen und Sätze bewerten. Es gibt keine richtigen oder falschen Antworten; uns interessiert, wie Sie Sprache natürlich verwenden.',
        ja='この調査にご参加いただきありがとうございます。短い言語タスク（物語を読む、空欄を埋める、文を評価する）に取り組んでいただきます。正解や不正解はありません。あなたが自然に言葉を使う様子に関心があります。',
    ),
    welcome_duration=dict(
        en='The study takes approximately 15–20 minutes.',
        fr='L\u2019étude dure environ 15 à 20 minutes.',
        de='Die Studie dauert etwa 15–20 Minuten.',
        ja='所要時間は約15〜20分です。',
    ),
    welcome_anon=dict(
        en='All responses are anonymous and will be used for research purposes only.',
        fr='Toutes les réponses sont anonymes et seront utilisées uniquement à des fins de recherche.',
        de='Alle Antworten sind anonym und werden ausschließlich zu Forschungszwecken verwendet.',
        ja='すべての回答は匿名であり、研究目的にのみ使用されます。',
    ),
    btn_begin=dict(
        en='Begin',
        fr='Commencer',
        de='Beginnen',
        ja='始める',
    ),

    # ── Screening Page ──
    screen_title=dict(
        en='About You',
        fr='À propos de vous',
        de='Über Sie',
        ja='あなたについて',
    ),
    screen_subtitle=dict(
        en='Please answer the following questions before we begin.',
        fr='Veuillez répondre aux questions suivantes avant de commencer.',
        de='Bitte beantworten Sie die folgenden Fragen, bevor wir beginnen.',
        ja='始める前に、以下の質問にお答えください。',
    ),

    # ── Q1: Age Range (distractor) ──
    q_age=dict(
        en='What is your age?',
        fr='Quel est votre âge ?',
        de='Wie alt sind Sie?',
        ja='あなたの年齢は？',
    ),
    age_18=dict(en='18–24', fr='18–24', de='18–24', ja='18〜24歳'),
    age_25=dict(en='25–34', fr='25–34', de='25–34', ja='25〜34歳'),
    age_35=dict(en='35–44', fr='35–44', de='35–44', ja='35〜44歳'),
    age_45=dict(en='45–54', fr='45–54', de='45–54', ja='45〜54歳'),
    age_55=dict(en='55–64', fr='55–64', de='55–64', ja='55〜64歳'),
    age_65=dict(en='65+', fr='65+', de='65+', ja='65歳以上'),

    # ── Q2: Mother tongue (CRITICAL) ──
    q_mother_tongue=dict(
        en='Is your mother tongue English?',
        fr='Votre langue maternelle est-elle le français ?',
        de='Ist Ihre Muttersprache Deutsch?',
        ja='あなたの母国語は日本語ですか？',
    ),
    yes=dict(en='Yes', fr='Oui', de='Ja', ja='はい'),
    no=dict(en='No', fr='Non', de='Nein', ja='いいえ'),

    # ── Q3: Education (distractor) ──
    q_education=dict(
        en='What is the highest level of education you have completed?',
        fr='Quel est le plus haut niveau d\u2019études que vous avez atteint ?',
        de='Was ist Ihr höchster Bildungsabschluss?',
        ja='最終学歴を教えてください。',
    ),
    edu_high=dict(
        en='Secondary school / High school',
        fr='Lycée / Baccalauréat',
        de='Abitur / Mittlere Reife',
        ja='高等学校卒業',
    ),
    edu_bachelor=dict(
        en='Bachelor\u2019s degree',
        fr='Licence',
        de='Bachelor',
        ja='学士号',
    ),
    edu_master=dict(
        en='Master\u2019s degree',
        fr='Master',
        de='Master',
        ja='修士号',
    ),
    edu_phd=dict(
        en='Doctorate / PhD',
        fr='Doctorat',
        de='Promotion / Doktortitel',
        ja='博士号',
    ),
    edu_other=dict(
        en='Other',
        fr='Autre',
        de='Sonstiges',
        ja='その他',
    ),

    # ── Q4: Other language proficiency (CRITICAL) ──
    q_other_lang=dict(
        en='Apart from English, what is your highest level of proficiency in any other language?',
        fr='En dehors du français, quel est votre plus haut niveau de maîtrise dans une autre langue ?',
        de='Abgesehen von Deutsch, wie hoch ist Ihr höchstes Sprachniveau in einer anderen Sprache?',
        ja='日本語以外の言語で、あなたの最も高い習熟度はどのレベルですか？',
    ),

    # Proficiency Levels
    lvl_0=dict(
        en="Level 0: I only know a few words. I cannot communicate at the sentence level at all, or I do not understand it at all.",
        fr="Niveau 0 : Je ne connais que quelques mots. Je ne peux pas du tout communiquer au niveau de la phrase, ou je ne comprends pas du tout.",
        de="Stufe 0: Ich kenne nur ein paar Wörter. Ich kann überhaupt nicht auf Satzebene kommunizieren oder verstehe es gar nicht.",
        ja="レベル0：いくつかの単語を知っている程度です。文レベルでのコミュニケーションは全くできないか、全く理解できません。"
    ),
    lvl_1=dict(
        en="Level 1: I can ask for directions and answer simple questions.",
        fr="Niveau 1 : Je peux demander mon chemin et répondre à des questions simples.",
        de="Stufe 1: Ich kann nach dem Weg fragen und einfache Fragen beantworten.",
        ja="レベル1：道を尋ねたり、簡単な質問に答えたりすることができます。"
    ),
    lvl_2=dict(
        en="Level 2: I can have basic conversations on familiar topics.",
        fr="Niveau 2 : Je peux avoir des conversations de base sur des sujets familiers.",
        de="Stufe 2: Ich kann einfache Gespräche über vertraute Themen führen.",
        ja="レベル2：身近な話題について基本的な会話ができます。"
    ),
    lvl_3=dict(
        en="Level 3: I can communicate effectively in most situations (e.g. telling a story or filling out forms), but not fluently.",
        fr="Niveau 3 : Je peux communiquer efficacement dans la plupart des situations, mais pas couramment.",
        de="Stufe 3: Ich kann in den meisten Situationen effektiv kommunizieren, aber nicht fließend.",
        ja="レベル3：多くの状況で効果的にコミュニケーションをとることができますが、流暢ではありません。"
    ),
    lvl_4=dict(
        en="Level 4: Fluent but occasionally make mistakes; clearly sound like a foreigner.",
        fr="Niveau 4 : Courant mais je fais parfois des erreurs ; on entend clairement que je suis étranger.",
        de="Stufe 4: Fließend, aber gelegentlich mache ich Fehler; ich klinge eindeutig wie ein Ausländer.",
        ja="レベル4：流暢ですが、時々間違いをします。明らかに外国人のように聞こえます。"
    ),
    lvl_5=dict(
        en="Level 5: Very fluent; I can use the language like a native speaker.",
        fr="Niveau 5 : Très courant ; je peux utiliser la langue comme un locuteur natif.",
        de="Stufe 5: Sehr fließend; ich kann die Sprache wie ein Muttersprachler verwenden.",
        ja="レベル5：非常に流暢で、ネイティブスピーカーのように言語を使用できます。"
    ),

    # ── Q5: Device (distractor) ──
    q_device=dict(
        en='What device are you using to complete this study?',
        fr='Quel appareil utilisez-vous pour répondre à cette étude ?',
        de='Welches Gerät verwenden Sie, um an dieser Studie teilzunehmen?',
        ja='この調査にはどのデバイスを使用していますか？',
    ),
    dev_computer=dict(
        en='Desktop / Laptop computer',
        fr='Ordinateur de bureau / portable',
        de='Desktop / Laptop',
        ja='デスクトップ / ノートパソコン',
    ),
    dev_tablet=dict(
        en='Tablet',
        fr='Tablette',
        de='Tablet',
        ja='タブレット',
    ),
    dev_phone=dict(
        en='Smartphone',
        fr='Smartphone',
        de='Smartphone',
        ja='スマートフォン',
    ),

    # Screenout Message
    screenout_msg=dict(
        en="Unfortunately you do not fit the profile for this survey. Thank you for participating.",
        fr="Malheureusement, vous ne correspondez pas au profil pour cette enquête. Merci de votre participation.",
        de="Leider entsprechen Sie nicht dem Profil für diese Umfrage. Vielen Dank für Ihre Teilnahme.",
        ja="残念ながら、この調査の対象プロファイルに適合しません。ご参加ありがとうございました。",
    ),

    # ── Task 1 ──
    task1_title=dict(
        en='Part 1 \u2014 Complete the Stories',
        fr='Partie 1 \u2014 Compl\u00e9ter les histoires',
        de='Teil 1 \u2014 Geschichten vervollst\u00e4ndigen',
        ja='パート1 — ストーリーを完成させる',
    ),
    task1_intro=dict(
        en='You will read four short stories. Some words are missing \u2014 please fill each gap with the word or phrase that feels most natural to you, as if you were talking to a close friend. There are no right or wrong answers.',
        fr='Vous allez lire quatre courtes histoires. Certains mots manquent \u2014 veuillez compl\u00e9ter chaque espace avec le mot ou l\u2019expression qui vous semble le plus naturel, comme si vous parliez \u00e0 un ami proche. Il n\u2019y a pas de bonne ou de mauvaise r\u00e9ponse.',
        de='Sie werden vier kurze Geschichten lesen. Einige W\u00f6rter fehlen \u2014 bitte f\u00fcllen Sie jede L\u00fccke mit dem Wort oder Ausdruck, der Ihnen am nat\u00fcrlichsten erscheint, als w\u00fcrden Sie mit einem guten Freund sprechen. Es gibt keine richtigen oder falschen Antworten.',
        ja='4つの短い物語を読みます。いくつかの言葉が抜けています。親しい友人と話しているようなつもりで、最も自然だと感じる言葉やフレーズで空欄を埋めてください。正しい答えや間違った答えはありません。',
    ),
    thankyou_title=dict(en='Thank you!', fr='Merci !', de='Vielen Dank!', ja='ありがとうございました！'),
    thankyou_msg=dict(
        en='Your responses have been recorded. You may now close this window.',
        fr='Vos r\u00e9ponses ont \u00e9t\u00e9 enregistr\u00e9es. Vous pouvez maintenant fermer cette fen\u00eatre.',
        de='Ihre Antworten wurden gespeichert. Sie k\u00f6nnen dieses Fenster jetzt schlie\u00dfen.',
        ja='回答が記録されました。このウィンドウを閉じてください。',
    ),
)


def t(key, lang):
    """Get UI string for key + language, fallback to English."""
    entry = UI.get(key, {})
    return entry.get(lang, entry.get('en', key))


def ui_dict(lang):
    """Flatten all UI strings for one language \u2014 for template context."""
    return {k: v.get(lang, v.get('en', '')) for k, v in UI.items()}


# ═══════════════════════════════════════════════════════════
# TASK 1 STORIES
# ═══════════════════════════════════════════════════════════

STORIES = dict(
    en=[
        # ── Story 1: Anna's Toothache ──
        dict(title="Anna\u2019s Toothache", paragraphs=[
            'Anna was having dinner {{1}} suddenly, she felt a sharp pain in her wisdom tooth. Her friend warned her: \u201cYou must see a dentist immediately, otherwise the tooth {{2}} swell up very soon.\u201d',
            'Anna was lucky and got an appointment for 4:00 PM. She thought to herself, \u201cAlthough I am afraid of pain, this doctor is very skilled. I believe the surgery {{3}} go smoothly.\u201d',
            'Anna arrived at the clinic. The dentist examined {{4}} teeth and said, \u201cWe must pull it out today. It\u2019s a quick procedure. The wound {{5}} heal completely within a week, and by then you {{6}} be able to eat normally.\u201d',
            'Anna returned home after she had finished {{7}} the extraction. However, the pain was still intense. She looked in the mirror and {{8}} realized: the doctor had pulled the wrong one! The painful left tooth was still there; the one removed was {{9}} the right one, which hadn\u2019t hurt at all.',
            'Anna burst into tears: \u201cOh my god, does that mean I {{10}} suffer through this all over again? Just my luck!\u201d',
        ]),
        # ── Story 2: Alex's Interview ──
        dict(title="Alex\u2019s Interview", paragraphs=[
            'Yesterday morning, Alex woke up with a feeling of dread. He pulled back the curtains and immediately {{1}} the dark, heavy clouds rolling over the city skyline.',
            'He turned on the television news. The weatherman announced: \u201cBe prepared, everyone. The heavy rain {{2}} continue all afternoon.\u201d',
            'Alex sighed and thought to herself: \u201cGreat. If I walk to the station in this weather, my suit {{3}} be completely ruined before the interview.\u201d',
            'He ran to the hallway closet, frantically searching {{4}} his large umbrella. Suddenly, a notification popped up on his phone: the downtown subway line had {{5}} due to a signal failure.',
            '\u201cThat\u2019s it!\u201d Alex shouted, grabbing his keys {{6}} the table. \u201cI {{7}} drive my car instead. It\u2019s the only way.\u201d',
            'He took a deep breath to calm down. \u201cI {{8}} call the recruiter from the car to let them know I might be late,\u201d he decided.',
            'He began {{9}} gather his documents, trying to stay positive. \u201cCome on, Alex,\u201d he whispered to himself. \u201cEven with the rain, I know this interview {{10}} go well.\u201d',
        ]),
        # ── Story 3: Marco's Panic Morning ──
        dict(title="Marco\u2019s Panic Morning", paragraphs=[
            'Marco woke up and {{1}} realized his alarm hadn\u2019t gone off. He rushed to the bus stop, only to find the next bus wasn\u2019t coming until 8:30. Suddenly, it started to rain. Looking at the gloomy sky, he was worried that he {{2}} miss the morning meeting.',
            'He quickly hailed a taxi. Inside, he {{3}} the radio announcer say, \u201cThe rain is heavy, and it {{4}} not stop until this afternoon.\u201d',
            'At that moment, his girlfriend Sarah called and asked, \u201cWhat are you {{5}} this afternoon?\u201d Marco replied anxiously, \u201cToday {{6}} be very busy; I have to prepare materials for next week\u2019s meeting.\u201d',
            'Sarah was surprised: \u201cBut today is Sunday!\u201d Marco was stunned. Sarah laughed, \u201cYes, Sunday is a rest day! Let\u2019s go have lunch instead.\u201d',
            'Marco sighed with relief, his mood instantly lifting. \u201cNo problem. I {{7}} book the restaurant right now, and afterwards we can go for a {{8}} in the park.\u201d',
            'The taxi arrived. Marco paid {{9}} driver and felt that this {{10}} be a wonderful day after all.',
        ]),
        # ── Story 4: Lee's Camping Trip ──
        dict(title="Lee\u2019s Camping Trip", paragraphs=[
            'The sky was dark with heavy clouds, and the temperature began to drop. Lee pointed out the window and said to his wife, \u201cLook at those clouds. It {{1}} definitely snow tonight.\u201d',
            'Lee felt cold and wanted a cup of hot coffee. While he was {{2}} the coffee, his wife stopped him and said, \u201cIf you drink that coffee now, you {{3}} not sleep all night.\u201d',
            'Lee hesitated and put down the cup. \u201cYou\u2019re right. I have to get up early tomorrow. If I don\u2019t sleep well, driving {{4}} be dangerous.\u201d',
            'Before going to bed, he checked the train schedule and found {{5}} the weekend train departed at 10:00 AM on Saturday.',
            'The next morning, planning for the weekend camping trip, Lee assigned tasks before work: \u201cAfter work tonight, I {{6}} go to the supermarket to buy groceries.\u201d',
            'His wife nodded, \u201cOkay, then I am responsible {{7}} packing the luggage. By the way, do we need thick coats?\u201d',
            'Lee checked the weather forecast on his phone and said, \u201cBetter bring them. The temperature in the mountains is {{8}} lower than here. If we don\u2019t dress warmly, we {{9}} catch a cold.\u201d',
            'They smiled at each other, both expecting that this camping trip {{10}} be very fun.',
        ]),
    ],

    # ── FRENCH ─────────────────────────────────────────────
    fr=[
        dict(title='Le mal de dent d\u2019Anna', paragraphs=[
            'Anna \u00e9tait en train de d\u00eener {{1}} soudain, elle a ressenti une douleur vive dans sa dent de sagesse. Son amie l\u2019a pr\u00e9venue\u00a0: \u00ab\u00a0Tu dois voir un dentiste imm\u00e9diatement, sinon la dent {{2}} enfler tr\u00e8s vite.\u00a0\u00bb',
            'Anna a eu de la chance et a obtenu un rendez-vous \u00e0 16\u00a0heures. Elle a pens\u00e9\u00a0: \u00ab\u00a0M\u00eame si j\u2019ai peur de la douleur, ce m\u00e9decin est tr\u00e8s comp\u00e9tent. Je crois que l\u2019op\u00e9ration {{3}} bien se passer.\u00a0\u00bb',
            'Anna est arriv\u00e9e \u00e0 la clinique. Le dentiste a examin\u00e9 {{4}} dents et a dit\u00a0: \u00ab\u00a0Il faut l\u2019arracher aujourd\u2019hui. C\u2019est une intervention rapide. La plaie {{5}} gu\u00e9rir compl\u00e8tement en une semaine, et \u00e0 ce moment-l\u00e0 vous {{6}} pouvoir manger normalement.\u00a0\u00bb',
            'Anna est rentr\u00e9e chez elle apr\u00e8s avoir termin\u00e9 {{7}} l\u2019extraction. Cependant, la douleur \u00e9tait encore intense. Elle s\u2019est regard\u00e9e dans le miroir et {{8}} a r\u00e9alis\u00e9\u00a0: le dentiste avait arrach\u00e9 la mauvaise dent\u00a0! La dent gauche douloureuse \u00e9tait toujours l\u00e0\u00a0; celle retir\u00e9e \u00e9tait {{9}} la droite, qui n\u2019avait pas fait mal du tout.',
            'Anna a fondu en larmes\u00a0: \u00ab\u00a0Oh mon Dieu, \u00e7a veut dire que je {{10}} devoir subir tout \u00e7a encore une fois\u00a0? Quelle malchance\u00a0!\u00a0\u00bb',
        ]),
        dict(title='L\u2019entretien d\u2019Alex', paragraphs=[
            'Hier matin, Alex s\u2019est r\u00e9veill\u00e9 avec un sentiment d\u2019angoisse. Il a tir\u00e9 les rideaux et imm\u00e9diatement {{1}} les nuages sombres et lourds qui s\u2019\u00e9tendaient au-dessus de la ville.',
            'Il a allum\u00e9 la t\u00e9l\u00e9vision. Le pr\u00e9sentateur m\u00e9t\u00e9o a annonc\u00e9\u00a0: \u00ab\u00a0Pr\u00e9parez-vous, tout le monde. La pluie forte {{2}} continuer tout l\u2019apr\u00e8s-midi.\u00a0\u00bb',
            'Alex a soupir\u00e9 et a pens\u00e9\u00a0: \u00ab\u00a0Super. Si je marche jusqu\u2019\u00e0 la gare par ce temps, mon costume {{3}} \u00eatre compl\u00e8tement fichu avant l\u2019entretien.\u00a0\u00bb',
            'Il a couru vers le placard de l\u2019entr\u00e9e, cherchant fr\u00e9n\u00e9tiquement {{4}} son grand parapluie. Soudain, une notification est apparue sur son t\u00e9l\u00e9phone\u00a0: la ligne de m\u00e9tro du centre-ville avait {{5}} \u00e0 cause d\u2019une panne de signalisation.',
            '\u00ab\u00a0C\u2019est d\u00e9cid\u00e9\u00a0!\u00a0\u00bb a cri\u00e9 Alex en attrapant ses cl\u00e9s {{6}} la table. \u00ab\u00a0Je {{7}} prendre ma voiture \u00e0 la place. C\u2019est la seule solution.\u00a0\u00bb',
            'Il a pris une grande inspiration pour se calmer. \u00ab\u00a0Je {{8}} appeler le recruteur depuis la voiture pour le pr\u00e9venir que je pourrais \u00eatre en retard\u00a0\u00bb, a-t-il d\u00e9cid\u00e9.',
            'Il a commenc\u00e9 {{9}} rassembler ses documents, essayant de rester positif. \u00ab\u00a0Allez, Alex\u00a0\u00bb, s\u2019est-il murmur\u00e9. \u00ab\u00a0M\u00eame avec la pluie, je sais que cet entretien {{10}} bien se passer.\u00a0\u00bb',
        ]),
        dict(title='La matin\u00e9e de panique de Marco', paragraphs=[
            'Marco s\u2019est r\u00e9veill\u00e9 et {{1}} a r\u00e9alis\u00e9 que son r\u00e9veil n\u2019avait pas sonn\u00e9. Il s\u2019est pr\u00e9cipit\u00e9 \u00e0 l\u2019arr\u00eat de bus, pour d\u00e9couvrir que le prochain bus n\u2019arrivait pas avant 8\u00a0h\u00a030. Soudain, il s\u2019est mis \u00e0 pleuvoir. En regardant le ciel gris, il s\u2019est inqui\u00e9t\u00e9 qu\u2019il {{2}} rater la r\u00e9union du matin.',
            'Il a vite h\u00e9l\u00e9 un taxi. \u00c0 l\u2019int\u00e9rieur, il {{3}} le pr\u00e9sentateur radio dire\u00a0: \u00ab\u00a0La pluie est forte, et elle {{4}} ne pas s\u2019arr\u00eater avant cet apr\u00e8s-midi.\u00a0\u00bb',
            '\u00c0 ce moment-l\u00e0, sa copine Sarah a appel\u00e9 et demand\u00e9\u00a0: \u00ab\u00a0Qu\u2019est-ce que tu {{5}} cet apr\u00e8s-midi\u00a0?\u00a0\u00bb Marco a r\u00e9pondu anxieusement\u00a0: \u00ab\u00a0Aujourd\u2019hui {{6}} \u00eatre tr\u00e8s charg\u00e9\u00a0; je dois pr\u00e9parer des documents pour la r\u00e9union de la semaine prochaine.\u00a0\u00bb',
            'Sarah a \u00e9t\u00e9 surprise\u00a0: \u00ab\u00a0Mais on est dimanche\u00a0!\u00a0\u00bb Marco \u00e9tait stup\u00e9fait. Sarah a ri\u00a0: \u00ab\u00a0Oui, le dimanche c\u2019est repos\u00a0! Allons plut\u00f4t d\u00e9jeuner.\u00a0\u00bb',
            'Marco a soupir\u00e9 de soulagement, son humeur s\u2019est aussit\u00f4t am\u00e9lior\u00e9e. \u00ab\u00a0Pas de probl\u00e8me. Je {{7}} r\u00e9server le restaurant tout de suite, et apr\u00e8s on pourra faire une {{8}} dans le parc.\u00a0\u00bb',
            'Le taxi est arriv\u00e9. Marco a pay\u00e9 {{9}} chauffeur et a senti que cette journ\u00e9e {{10}} \u00eatre finalement une belle journ\u00e9e.',
        ]),
        dict(title='Le camping de Lee', paragraphs=[
            'Le ciel \u00e9tait sombre avec de gros nuages, et la temp\u00e9rature a commenc\u00e9 \u00e0 baisser. Lee a montr\u00e9 la fen\u00eatre du doigt et a dit \u00e0 sa femme\u00a0: \u00ab\u00a0Regarde ces nuages. Il {{1}} certainement neiger ce soir.\u00a0\u00bb',
            'Lee avait froid et voulait un caf\u00e9 chaud. Pendant qu\u2019il \u00e9tait en train de {{2}} le caf\u00e9, sa femme l\u2019a arr\u00eat\u00e9 et a dit\u00a0: \u00ab\u00a0Si tu bois ce caf\u00e9 maintenant, tu {{3}} ne pas dormir de la nuit.\u00a0\u00bb',
            'Lee a h\u00e9sit\u00e9 et a pos\u00e9 la tasse. \u00ab\u00a0Tu as raison. Je dois me lever t\u00f4t demain. Si je ne dors pas bien, conduire {{4}} \u00eatre dangereux.\u00a0\u00bb',
            'Avant de se coucher, il a v\u00e9rifi\u00e9 les horaires de train et a trouv\u00e9 {{5}} le train du week-end partait \u00e0 10\u00a0h\u00a000 le samedi.',
            'Le lendemain matin, en pr\u00e9parant le voyage de camping, Lee a r\u00e9parti les t\u00e2ches avant le travail\u00a0: \u00ab\u00a0Apr\u00e8s le travail ce soir, je {{6}} aller au supermarch\u00e9 acheter les courses.\u00a0\u00bb',
            'Sa femme a acquiesc\u00e9\u00a0: \u00ab\u00a0D\u2019accord, alors je suis responsable {{7}} pr\u00e9parer les bagages. Au fait, est-ce qu\u2019on a besoin de manteaux \u00e9pais\u00a0?\u00a0\u00bb',
            'Lee a v\u00e9rifi\u00e9 la m\u00e9t\u00e9o sur son t\u00e9l\u00e9phone et a dit\u00a0: \u00ab\u00a0Mieux vaut les prendre. La temp\u00e9rature en montagne est {{8}} plus basse qu\u2019ici. Si on ne s\u2019habille pas chaudement, on {{9}} attraper un rhume.\u00a0\u00bb',
            'Ils se sont souri, tous les deux pensant que ce voyage de camping {{10}} \u00eatre tr\u00e8s amusant.',
        ]),
    ],

    # ── GERMAN ─────────────────────────────────────────────
    de=[
        dict(title='Annas Zahnschmerzen', paragraphs=[
            'Anna war beim Abendessen, {{1}} pl\u00f6tzlich sp\u00fcrte sie einen stechenden Schmerz in ihrem Weisheitszahn. Ihre Freundin warnte sie: \u201eDu musst sofort zum Zahnarzt gehen, sonst {{2}} der Zahn sehr bald anschwellen.\u201c',
            'Anna hatte Gl\u00fcck und bekam einen Termin um 16\u00a0Uhr. Sie dachte sich: \u201eObwohl ich Angst vor Schmerzen habe, ist dieser Arzt sehr geschickt. Ich glaube, die Operation {{3}} gut verlaufen.\u201c',
            'Anna kam in der Klinik an. Der Zahnarzt untersuchte {{4}} Z\u00e4hne und sagte: \u201eWir m\u00fcssen ihn heute ziehen. Es ist ein schneller Eingriff. Die Wunde {{5}} innerhalb einer Woche vollst\u00e4ndig heilen, und bis dahin {{6}} Sie wieder normal essen k\u00f6nnen.\u201c',
            'Anna kam nach Hause, nachdem sie {{7}} Extraktion abgeschlossen hatte. Allerdings war der Schmerz noch heftig. Sie schaute in den Spiegel und {{8}} erkannte: Der Arzt hatte den falschen Zahn gezogen! Der schmerzende linke Zahn war noch da; der entfernte war {{9}} der rechte, der gar nicht wehgetan hatte.',
            'Anna brach in Tr\u00e4nen aus: \u201eOh Gott, hei\u00dft das, ich {{10}} das alles noch einmal durchmachen m\u00fcssen? So ein Pech!\u201c',
        ]),
        dict(title='Alex\u2019 Vorstellungsgespr\u00e4ch', paragraphs=[
            'Gestern Morgen wachte Alex mit einem Gef\u00fchl der Beklemmung auf. Er zog die Vorh\u00e4nge zur\u00fcck und {{1}} sofort die dunklen, schweren Wolken \u00fcber der Skyline der Stadt.',
            'Er schaltete den Fernseher ein. Der Wettermoderator verk\u00fcndete: \u201eBereiten Sie sich vor, alle. Der starke Regen {{2}} den ganzen Nachmittag anhalten.\u201c',
            'Alex seufzte und dachte: \u201eToll. Wenn ich bei diesem Wetter zum Bahnhof laufe, {{3}} mein Anzug vor dem Gespr\u00e4ch v\u00f6llig ruiniert sein.\u201c',
            'Er rannte zum Flurschrank und suchte hektisch {{4}} seinem gro\u00dfen Regenschirm. Pl\u00f6tzlich erschien eine Benachrichtigung auf seinem Handy: Die U-Bahn-Linie in die Innenstadt war {{5}} wegen einer Signalst\u00f6rung.',
            '\u201eDas war\u2019s!\u201c rief Alex und griff nach seinen Schl\u00fcsseln {{6}} dem Tisch. \u201eIch {{7}} stattdessen mit dem Auto fahren. Es ist die einzige M\u00f6glichkeit.\u201c',
            'Er holte tief Luft, um sich zu beruhigen. \u201eIch {{8}} den Personalverantwortlichen vom Auto aus anrufen, um Bescheid zu geben, dass ich mich versp\u00e4ten k\u00f6nnte\u201c, beschloss er.',
            'Er begann {{9}} seine Unterlagen zusammenzusuchen und versuchte, positiv zu bleiben. \u201eKomm schon, Alex\u201c, fl\u00fcsterte er sich zu. \u201eAuch bei Regen, ich wei\u00df, dass dieses Gespr\u00e4ch {{10}} gut laufen.\u201c',
        ]),
        dict(title='Marcos panischer Morgen', paragraphs=[
            'Marco wachte auf und {{1}} stellte fest, dass sein Wecker nicht geklingelt hatte. Er rannte zur Bushaltestelle, nur um festzustellen, dass der n\u00e4chste Bus erst um 8:30 kam. Pl\u00f6tzlich fing es an zu regnen. Als er in den grauen Himmel schaute, machte er sich Sorgen, dass er {{2}} die Morgenbesprechung verpassen.',
            'Er rief schnell ein Taxi. Drinnen {{3}} er den Radiosprecher sagen: \u201eDer Regen ist stark, und er {{4}} nicht vor heute Nachmittag aufh\u00f6ren.\u201c',
            'In dem Moment rief seine Freundin Sarah an und fragte: \u201eWas {{5}} du heute Nachmittag?\u201c Marco antwortete \u00e4ngstlich: \u201eHeute {{6}} sehr stressig sein; ich muss Unterlagen f\u00fcr die Besprechung n\u00e4chste Woche vorbereiten.\u201c',
            'Sarah war \u00fcberrascht: \u201eAber heute ist Sonntag!\u201c Marco war verbl\u00fcfft. Sarah lachte: \u201eJa, Sonntag ist Ruhetag! Lass uns stattdessen Mittagessen gehen.\u201c',
            'Marco seufzte erleichtert, seine Stimmung besserte sich sofort. \u201eKein Problem. Ich {{7}} jetzt sofort das Restaurant reservieren, und danach k\u00f6nnen wir einen {{8}} im Park machen.\u201c',
            'Das Taxi kam an. Marco bezahlte {{9}} Fahrer und hatte das Gef\u00fchl, dass dieser Tag {{10}} doch noch ein sch\u00f6ner Tag sein.',
        ]),
        dict(title='Lees Campingausflug', paragraphs=[
            'Der Himmel war dunkel mit schweren Wolken, und die Temperatur begann zu sinken. Lee zeigte aus dem Fenster und sagte zu seiner Frau: \u201eSchau dir die Wolken an. Es {{1}} heute Nacht auf jeden Fall schneien.\u201c',
            'Lee fror und wollte eine Tasse hei\u00dfen Kaffee. W\u00e4hrend er den Kaffee {{2}}, hielt seine Frau ihn auf und sagte: \u201eWenn du jetzt diesen Kaffee trinkst, {{3}} du die ganze Nacht nicht schlafen.\u201c',
            'Lee z\u00f6gerte und stellte die Tasse ab. \u201eDu hast recht. Ich muss morgen fr\u00fch aufstehen. Wenn ich nicht gut schlafe, {{4}} das Fahren gef\u00e4hrlich sein.\u201c',
            'Vor dem Schlafengehen \u00fcberpr\u00fcfte er den Zugfahrplan und fand heraus, {{5}} der Wochenendzug am Samstag um 10:00\u00a0Uhr abfuhr.',
            'Am n\u00e4chsten Morgen, bei der Planung des Campingausflugs, verteilte Lee die Aufgaben vor der Arbeit: \u201eNach der Arbeit heute Abend {{6}} ich zum Supermarkt gehen und Lebensmittel kaufen.\u201c',
            'Seine Frau nickte: \u201eOkay, dann bin ich zust\u00e4ndig {{7}} das Kofferpacken. \u00dcbrigens, brauchen wir dicke M\u00e4ntel?\u201c',
            'Lee \u00fcberpr\u00fcfte die Wettervorhersage auf seinem Handy und sagte: \u201eBesser mitnehmen. Die Temperatur in den Bergen ist {{8}} niedriger als hier. Wenn wir uns nicht warm anziehen, {{9}} wir uns erk\u00e4lten.\u201c',
            'Sie l\u00e4chelten einander an und beide erwarteten, dass dieser Campingausflug {{10}} sehr lustig sein.',
        ]),
    ],

    # ── JAPANESE ───────────────────────────────────────────
    ja=[
        dict(title='アンナの歯痛', paragraphs=[
            'アンナが夕食を食べている{{1}}、突然親知らずに鋭い痛みを感じました。友人は彼女に警告しました：「すぐに歯医者に見てもらわないと、その歯はすぐに{{2}}よ。」',
            'アンナは運良く午後4時の予約が取れました。彼女は心の中で思いました。「痛みは怖いけれど、この先生はとても腕がいい。手術は{{3}}と信じているわ。」',
            'アンナはクリニックに到着しました。歯科医は{{4}}歯を診察して言いました。「今日抜かなければなりません。すぐに終わりますよ。傷は1週間以内に完全に{{5}}。そうすれば普通に食事が{{6}}。」',
            '抜歯を{{7}}アンナは家に帰りました。しかし、痛みはまだ激しいものでした。鏡を見て{{8}}気づきました。医者は違う歯を抜いてしまったのです！痛む左の歯はまだそこにあり、抜かれたのは{{9}}右側の歯で、そこは全く痛くなかったのです。',
            'アンナは泣き出しました。「なんてこと、つまり私はまた最初からこの痛みに{{10}}いけないってこと？なんてついてないの！」',
        ]),
        dict(title='アレックスの面接', paragraphs=[
            '昨日の朝、アレックスは不安な気持ちで目を覚ましました。カーテンを開けると、すぐに暗く重い雲が街を覆っているの{{1}}。',
            '彼はテレビのニュースをつけました。気象予報士が告げました。「皆さん、備えてください。大雨は午後ずっと{{2}}。」',
            'アレックスはため息をつき、心の中で思いました。「最悪だ。この天気の中を駅まで歩いたら、面接の前にスーツが台無しに{{3}}。」',
            '彼は廊下のクローゼットに走り、大きな傘を{{4}}探しました。突然、携帯に通知が来ました。都心の地下鉄が信号故障で{{5}}というのです。',
            '「もうだめだ！」アレックスは叫び、テーブル{{6}}鍵を掴みました。「代わりに車で{{7}}。それしかない。」',
            '彼は深呼吸をして落ち着こうとしました。「車から採用担当者に電話して、遅れるかもしれないと{{8}}」と彼は決めました。',
            '彼は書類を{{9}}始め、前向きになろうと努めました。「しっかりしろ、アレックス」と自分に言い聞かせました。「雨でも、この面接は{{10}}と分かってる。」',
        ]),
        dict(title='マルコのパニックな朝', paragraphs=[
            'マルコは目を覚まし、目覚ましが鳴らなかったことに{{1}}。バス停へ急ぎましたが、次のバスは8時半まで来ないことがわかりました。突然、雨が降り出しました。どんよりした空を見上げ、彼は朝の会議に{{2}}と心配になりました。',
            '彼は素早くタクシーを拾いました。車内で、ラジオのアナウンサーが「雨は激しく、午後まで{{3}}」と言っているのを聞きました。',
            'その瞬間、恋人のサラから電話があり、「今日の午後は何を{{4}}？」と尋ねました。マルコは不安そうに答えました。「今日はとても{{5}}。来週の会議の資料を準備しなきゃいけないんだ。」',
            'サラは驚きました。「でも今日は日曜日よ！」マルコは呆然としました。サラは笑いました。「そうよ、日曜日は休みの日！代わりにランチに行きましょう。」',
            'マルコは安堵のため息をつき、気分は一気に晴れました。「問題ないよ。今すぐレストランを{{6}}、その後公園で{{7}}をしよう。」',
            'タクシーが到着しました。マルコは{{8}}運転手に料金を払い、結局今日は素晴らしい一日に{{9}}と感じました。',
        ]),
        dict(title='リーのキャンプ旅行', paragraphs=[
            '空は重い雲で暗く、気温が下がり始めました。リーは窓を指差して妻に言いました。「あの雲を見て。今夜は間違いなく{{1}}。」',
            'リーは寒気を感じ、温かいコーヒーを欲しがりました。彼がコーヒーを{{2}}いると、妻が止めて言いました。「今そのコーヒーを飲んだら、一晩中{{3}}わよ。」',
            'リーは躊躇してカップを置きました。「君の言う通りだ。明日は早起きしなきゃいけない。よく眠れないと、運転は{{4}}。」',
            '寝る前に列車のスケジュールを確認すると、週末の列車が土曜日の朝10時に出発{{5}}ことがわかりました。',
            '翌朝、週末のキャンプ旅行の計画を立てながら、リーは仕事の前のタスクを割り振りました。「今夜仕事の後、食料品を買いにスーパーへ{{6}}。」',
            '妻は頷きました。「わかった、じゃあ私は荷造りを{{7}}。ところで、厚手のコートは必要かしら？」',
            'リーは携帯で天気予報を確認して言いました。「持っていったほうがいい。山の気温はここより{{8}}低い。暖かくしないと、{{9}}よ。」',
            '二人は微笑み合い、このキャンプ旅行はとても{{10}}と予感しました。',
        ]),
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

    # ── Screening Fields ──
    # Distractor: Age range
    age_range = models.StringField()

    # CRITICAL: Native speaker check
    # True = Native, False = Not Native
    is_native = models.BooleanField()

    # Distractor: Education level
    education = models.StringField()

    # CRITICAL: Other language proficiency (Level 0-5)
    other_language_level = models.IntegerField()

    # Distractor: Device type
    device = models.StringField()

    # Track if user failed screening
    screened_out = models.BooleanField(initial=False)

    # Task 1 JSON: {"story_1":{"1":"when","2":"will",...}, ...}
    task1_responses = models.LongStringField(blank=True, initial='{}')


# ═══════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════

def _ctx(player, progress):
    """Base template context."""
    lang = player.language
    return dict(lang=lang, ui=ui_dict(lang), progress=progress)


class Screening(Page):
    form_model = 'player'
    form_fields = ['age_range', 'is_native', 'education', 'other_language_level', 'device']

    @staticmethod
    def vars_for_template(player):
        # 1. Detect language from config or participant label
        lang = player.session.config.get('language', 'en')
        player.language = lang
        player.participant.language = lang

        # 2. Get the base context (lang + ui + progress)
        ctx = _ctx(player, 0)
        ui = ctx['ui']

        # 3. Build choice lists for template
        age_choices = [
            ('18-24', ui['age_18']),
            ('25-34', ui['age_25']),
            ('35-44', ui['age_35']),
            ('45-54', ui['age_45']),
            ('55-64', ui['age_55']),
            ('65+',   ui['age_65']),
        ]

        edu_choices = [
            ('high_school', ui['edu_high']),
            ('bachelor',    ui['edu_bachelor']),
            ('master',      ui['edu_master']),
            ('phd',         ui['edu_phd']),
            ('other',       ui['edu_other']),
        ]

        level_choices = [
            (0, ui['lvl_0']),
            (1, ui['lvl_1']),
            (2, ui['lvl_2']),
            (3, ui['lvl_3']),
            (4, ui['lvl_4']),
            (5, ui['lvl_5']),
        ]

        device_choices = [
            ('computer', ui['dev_computer']),
            ('tablet',   ui['dev_tablet']),
            ('phone',    ui['dev_phone']),
        ]

        return dict(
            age_choices=age_choices,
            level_choices=level_choices,
            edu_choices=edu_choices,
            device_choices=device_choices,
            **ctx
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # SCREENING LOGIC:
        # Pass if: Native Speaker (True) AND Other Language Level is 0
        if player.is_native and player.other_language_level == 0:
            player.screened_out = False
        else:
            player.screened_out = True


class ScreenOut(Page):
    def is_displayed(player):
        return player.screened_out

    @staticmethod
    def vars_for_template(player):
        # Still need to pass base context so Base.html can render the head/css correctly
        return _ctx(player, 0)


class Task1Intro(Page):
    def is_displayed(player):
        return not player.screened_out

    @staticmethod
    def vars_for_template(player):
        return _ctx(player, 5)


class Task1Story1(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return not player.screened_out

    @staticmethod
    def vars_for_template(player):
        # Safely get stories for current language
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[0],
            story_num=1, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 14),
        )


class Task1Story2(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[1],
            story_num=2, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 23),
        )


class Task1Story3(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[2],
            story_num=3, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 32),
        )


class Task1Story4(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[3],
            story_num=4, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 41),
        )


page_sequence = [
    Screening,
    ScreenOut,
    Task1Intro,
    Task1Story1,
    Task1Story2,
    Task1Story3,
    Task1Story4,
]