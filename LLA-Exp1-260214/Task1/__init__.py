from otree.api import *
import json

doc = """
Cross-linguistic FTR & Loss Aversion — Task 1 trial.
Languages: English (en), French (fr), German (de), Japanese (ja), Chinese (zh).
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# ═══════════════════════════════════════════════════════════
# UI STRINGS
# ═══════════════════════════════════════════════════════════
UI = dict(
    # General buttons & messages
    btn_continue=dict(en='Continue', fr='Continuer', de='Weiter', ja='次へ', zh='继续'),
    btn_read_more=dict(en='Continue reading\u2026', fr='Lire la suite\u2026', de='Weiterlesen\u2026', ja='続きを読む...', zh='继续阅读\u2026'),
    btn_start=dict(en="Let's begin", fr='Commençons', de="Los geht's", ja='始めましょう', zh='开始'),
    btn_finish=dict(en='Finish', fr='Terminer', de='Fertig', ja='終了', zh='完成'),
    required_msg=dict(
        en='Please fill in every blank before continuing.',
        fr='Veuillez remplir tous les espaces avant de continuer.',
        de='Bitte f\u00fcllen Sie alle L\u00fccken aus, bevor Sie fortfahren.',
        ja='先に進む前にすべての空欄を埋めてください。',
        zh='请填写所有空格后再继续。',
    ),

    # ── Prolific ID ──
    prolific_title=dict(en='Your Prolific ID', fr='Votre identifiant Prolific', de='Ihre Prolific-ID', ja='Prolific ID', zh='您的Prolific ID'),
    prolific_intro=dict(
        en='Please enter your unique Prolific ID below. This is used to match your responses and process your payment.',
        fr='Veuillez entrer votre identifiant Prolific ci-dessous. Il est utilisé pour associer vos réponses et traiter votre paiement.',
        de='Bitte geben Sie unten Ihre Prolific-ID ein. Diese wird benötigt, um Ihre Antworten zuzuordnen und Ihre Vergütung zu verarbeiten.',
        ja='以下にProlific IDを入力してください。回答の紐付けと報酬の処理に使用されます。',
        zh='请在下方输入您的Prolific ID。这将用于匹配您的回答并处理您的报酬。',
    ),
    prolific_label=dict(en='Prolific ID', fr='Identifiant Prolific', de='Prolific-ID', ja='Prolific ID', zh='Prolific ID'),
    prolific_hint=dict(
        en='You can find this on your Prolific dashboard.',
        fr='Vous pouvez le trouver sur votre tableau de bord Prolific.',
        de='Sie finden diese auf Ihrem Prolific-Dashboard.',
        ja='Prolificのダッシュボードで確認できます。',
        zh='您可以在Prolific控制面板中找到。',
    ),
    prolific_error=dict(
        en='Please enter your Prolific ID to continue.',
        fr='Veuillez entrer votre identifiant Prolific pour continuer.',
        de='Bitte geben Sie Ihre Prolific-ID ein, um fortzufahren.',
        ja='続行するにはProlific IDを入力してください。',
        zh='请输入您的Prolific ID以继续。',
    ),

    # ── Consent ──
    consent_title=dict(en='Consent Form', fr='Formulaire de consentement', de='Einwilligungserklärung', ja='同意書', zh='知情同意书'),
    consent_btn_yes=dict(en='I Consent', fr='Je consens', de='Ich stimme zu', ja='同意する', zh='我同意'),
    consent_btn_no=dict(en='I Do Not Consent', fr='Je ne consens pas', de='Ich stimme nicht zu', ja='同意しない', zh='我不同意'),
    noconsent_msg=dict(
        en='Thank you for your time. Because you did not consent to participate, the study cannot proceed. You may now close this window.',
        fr='Merci pour votre temps. Comme vous n\'avez pas donné votre consentement, l\'étude ne peut pas continuer. Vous pouvez maintenant fermer cette fenêtre.',
        de='Vielen Dank für Ihre Zeit. Da Sie nicht zugestimmt haben, kann die Studie nicht fortgesetzt werden. Sie können dieses Fenster jetzt schließen.',
        ja='お時間をいただきありがとうございます。同意いただけなかったため、本研究を進めることができません。このウィンドウを閉じてください。',
        zh='感谢您的时间。由于您未同意参与，本研究无法继续。您现在可以关闭此窗口。',
    ),

    # ── Welcome / Study Introduction ──
    welcome_title=dict(
        en='Welcome',
        fr='Bienvenue',
        de='Willkommen',
        ja='ようこそ',
        zh='欢迎',
    ),
    welcome_body=dict(
        en='Thank you for taking part in this study. It takes <strong>about 20 minutes</strong> to complete. You will complete a series of short language tasks — reading stories, filling in blanks, and rating sentences. There are no right or wrong answers; we are interested in how you naturally use language.',
        fr='Merci de participer à cette étude. Vous allez réaliser une série de courtes tâches linguistiques — lire des histoires, compléter des phrases et évaluer des énoncés. Il n\u2019y a pas de bonnes ou de mauvaises réponses ; nous nous intéressons à votre usage naturel de la langue.',
        de='Vielen Dank für Ihre Teilnahme an dieser Studie. Sie werden eine Reihe kurzer Sprachaufgaben bearbeiten — Geschichten lesen, Lücken ausfüllen und Sätze bewerten. Es gibt keine richtigen oder falschen Antworten; uns interessiert, wie Sie Sprache natürlich verwenden.',
        ja='この調査にご参加いただきありがとうございます。短い言語タスク（物語を読む、空欄を埋める、文を評価する）に取り組んでいただきます。正解や不正解はありません。あなたが自然に言葉を使う様子に関心があります。',
        zh='感谢您参加本研究。您将完成一系列简短的语言任务——阅读故事、填写空格和评价句子。没有正确或错误的答案，我们感兴趣的是您自然使用语言的方式。',
    ),
    welcome_bonus=dict(
        en='In addition to your £3.50 participation fee, you may have the opportunity to <strong>earn a bonus payment</strong> based on your decisions in the study, so please read the instructions carefully and pay close attention throughout.',
        fr='En plus de votre indemnité de participation, vous pourrez <strong>gagner un bonus</strong> en fonction de vos décisions dans l\u2019étude. Veuillez donc lire attentivement les instructions et rester concentré(e) tout au long de l\u2019étude.',
        de='Zusätzlich zu Ihrer Teilnahmegebühr haben Sie die Möglichkeit, <strong>einen Bonus zu verdienen</strong>, basierend auf Ihren Entscheidungen in der Studie. Bitte lesen Sie die Anweisungen sorgfältig und achten Sie durchgehend aufmerksam.',
        ja='参加謝金に加えて、調査中の意思決定に基づいて<strong>ボーナスを獲得</strong>できる場合があります。説明をよくお読みになり、最後まで注意深くご参加ください。',
        zh='除参与费外，您还有机会根据研究中的决策<strong>获得额外奖金</strong>，请仔细阅读说明并全程认真作答。',
    ),
    btn_begin=dict(
        en='Begin',
        fr='Commencer',
        de='Beginnen',
        ja='始める',
        zh='开始',
    ),

    # ── Screening Page ──
    screen_title=dict(
        en='About You',
        fr='À propos de vous',
        de='Über Sie',
        ja='あなたについて',
        zh='关于您',
    ),
    screen_subtitle=dict(
        en='Please answer the following questions before we begin.',
        fr='Veuillez répondre aux questions suivantes avant de commencer.',
        de='Bitte beantworten Sie die folgenden Fragen, bevor wir beginnen.',
        ja='始める前に、以下の質問にお答えください。',
        zh='在开始之前，请回答以下问题。',
    ),

    # ── Q1: Age Range (distractor) ──
    q_age=dict(
        en='What is your age?',
        fr='Quel est votre âge ?',
        de='Wie alt sind Sie?',
        ja='あなたの年齢は？',
        zh='您的年龄是？',
    ),
    age_18=dict(en='18–24', fr='18–24', de='18–24', ja='18〜24歳', zh='18-24岁'),
    age_25=dict(en='25–34', fr='25–34', de='25–34', ja='25〜34歳', zh='25-34岁'),
    age_35=dict(en='35–44', fr='35–44', de='35–44', ja='35〜44歳', zh='35-44岁'),
    age_45=dict(en='45–54', fr='45–54', de='45–54', ja='45〜54歳', zh='45-54岁'),
    age_55=dict(en='55–64', fr='55–64', de='55–64', ja='55〜64歳', zh='55-64岁'),
    age_65=dict(en='65+', fr='65+', de='65+', ja='65歳以上', zh='65岁以上'),

    # ── Q2: Mother tongue (CRITICAL) ──
    q_mother_tongue=dict(
        en='Is your mother tongue English?',
        fr='Votre langue maternelle est-elle le français ?',
        de='Ist Ihre Muttersprache Deutsch?',
        ja='あなたの母国語は日本語ですか？',
        zh='您的母语是中文吗？',
    ),
    yes=dict(en='Yes', fr='Oui', de='Ja', ja='はい', zh='是'),
    no=dict(en='No', fr='Non', de='Nein', ja='いいえ', zh='否'),

    # ── Q3: Education (distractor) ──
    q_education=dict(
        en='What is the highest level of education you have completed?',
        fr='Quel est le plus haut niveau d\u2019études que vous avez atteint ?',
        de='Was ist Ihr höchster Bildungsabschluss?',
        ja='最終学歴を教えてください。',
        zh='您的最高学历是？',
    ),
    edu_high=dict(
        en='Secondary school / High school',
        fr='Lycée / Baccalauréat',
        de='Abitur / Mittlere Reife',
        ja='高等学校卒業',
        zh='高中 / 中专',
    ),
    edu_bachelor=dict(
        en='Bachelor\u2019s degree',
        fr='Licence',
        de='Bachelor',
        ja='学士号',
        zh='本科学士',
    ),
    edu_master=dict(
        en='Master\u2019s degree',
        fr='Master',
        de='Master',
        ja='修士号',
        zh='硕士',
    ),
    edu_phd=dict(
        en='Doctorate / PhD',
        fr='Doctorat',
        de='Promotion / Doktortitel',
        ja='博士号',
        zh='博士',
    ),
    edu_other=dict(
        en='Other',
        fr='Autre',
        de='Sonstiges',
        ja='その他',
        zh='其他',
    ),

    # ── Q4: Other language proficiency (CRITICAL) ──
    q_other_lang=dict(
        en='Apart from English, what is your highest level of proficiency in any other language?',
        fr='En dehors du français, quel est votre plus haut niveau de maîtrise dans une autre langue ?',
        de='Abgesehen von Deutsch, wie hoch ist Ihr höchstes Sprachniveau in einer anderen Sprache?',
        ja='日本語以外の言語で、あなたの最も高い習熟度はどのレベルですか？',
        zh='除中文外，您其他语言的最高熟练程度是？',
    ),

    # Proficiency Levels
    lvl_0=dict(
        en="Level 0: I only know a few words. I cannot communicate at the sentence level at all, or I do not understand it at all.",
        fr="Niveau 0 : Je ne connais que quelques mots. Je ne peux pas du tout communiquer au niveau de la phrase, ou je ne comprends pas du tout.",
        de="Stufe 0: Ich kenne nur ein paar Wörter. Ich kann überhaupt nicht auf Satzebene kommunizieren oder verstehe es gar nicht.",
        ja="レベル0：いくつかの単語を知っている程度です。文レベルでのコミュニケーションは全くできないか、全く理解できません。",
        zh="等级0：我只认识几个单词。完全无法用句子交流，或者完全不理解。",
    ),
    lvl_1=dict(
        en="Level 1: I can ask for directions and answer simple questions.",
        fr="Niveau 1 : Je peux demander mon chemin et répondre à des questions simples.",
        de="Stufe 1: Ich kann nach dem Weg fragen und einfache Fragen beantworten.",
        ja="レベル1：道を尋ねたり、簡単な質問に答えたりすることができます。",
        zh="等级1：我能问路和回答简单的问题。",
    ),
    lvl_2=dict(
        en="Level 2: I can have basic conversations on familiar topics.",
        fr="Niveau 2 : Je peux avoir des conversations de base sur des sujets familiers.",
        de="Stufe 2: Ich kann einfache Gespräche über vertraute Themen führen.",
        ja="レベル2：身近な話題について基本的な会話ができます。",
        zh="等级2：我能就熟悉的话题进行基本对话。",
    ),
    lvl_3=dict(
        en="Level 3: I can communicate effectively in most situations (e.g. telling a story or filling out forms), but not fluently.",
        fr="Niveau 3 : Je peux communiquer efficacement dans la plupart des situations, mais pas couramment.",
        de="Stufe 3: Ich kann in den meisten Situationen effektiv kommunizieren, aber nicht fließend.",
        ja="レベル3：多くの状況で効果的にコミュニケーションをとることができますが、流暢ではありません。",
        zh="等级3：我能在大多数情境中有效沟通（如讲故事或填表），但不够流利。",
    ),
    lvl_4=dict(
        en="Level 4: Fluent but occasionally make mistakes; clearly sound like a foreigner.",
        fr="Niveau 4 : Courant mais je fais parfois des erreurs ; on entend clairement que je suis étranger.",
        de="Stufe 4: Fließend, aber gelegentlich mache ich Fehler; ich klinge eindeutig wie ein Ausländer.",
        ja="レベル4：流暢ですが、時々間違いをします。明らかに外国人のように聞こえます。",
        zh="等级4：流利但偶尔犯错；明显像外国人。",
    ),
    lvl_5=dict(
        en="Level 5: Very fluent; I can use the language like a native speaker.",
        fr="Niveau 5 : Très courant ; je peux utiliser la langue comme un locuteur natif.",
        de="Stufe 5: Sehr fließend; ich kann die Sprache wie ein Muttersprachler verwenden.",
        ja="レベル5：非常に流暢で、ネイティブスピーカーのように言語を使用できます。",
        zh="等级5：非常流利，能像母语者一样使用该语言。",
    ),

    # ── Q5: Device (distractor) ──
    q_device=dict(
        en='What device are you using to complete this study?',
        fr='Quel appareil utilisez-vous pour répondre à cette étude ?',
        de='Welches Gerät verwenden Sie, um an dieser Studie teilzunehmen?',
        ja='この調査にはどのデバイスを使用していますか？',
        zh='您使用什么设备完成本研究？',
    ),
    dev_computer=dict(
        en='Desktop / Laptop computer',
        fr='Ordinateur de bureau / portable',
        de='Desktop / Laptop',
        ja='デスクトップ / ノートパソコン',
        zh='台式电脑 / 笔记本电脑',
    ),
    dev_tablet=dict(
        en='Tablet',
        fr='Tablette',
        de='Tablet',
        ja='タブレット',
        zh='平板电脑',
    ),
    dev_phone=dict(
        en='Smartphone',
        fr='Smartphone',
        de='Smartphone',
        ja='スマートフォン',
        zh='智能手机',
    ),

    # Screenout Message
    screenout_msg=dict(
        en="Unfortunately you do not fit the profile for this survey. You will still receive <strong>£0.15</strong> for your time. Thank you for participating.",
        fr="Malheureusement, vous ne correspondez pas au profil pour cette enquête. Merci de votre participation.",
        de="Leider entsprechen Sie nicht dem Profil für diese Umfrage. Vielen Dank für Ihre Teilnahme.",
        ja="残念ながら、この調査の対象プロファイルに適合しません。ご参加ありがとうございました。",
        zh="很抱歉，您不符合本调查的参与条件。感谢您的参与。",
    ),

    # ── Task 1 ──
    task1_title=dict(
        en='Part 1 \u2014 Complete the Stories',
        fr='Partie 1 \u2014 Compl\u00e9ter les histoires',
        de='Teil 1 \u2014 Geschichten vervollst\u00e4ndigen',
        ja='パート1 — ストーリーを完成させる',
        zh='第一部分 \u2014 完成故事',
    ),
    task1_intro=dict(
        en='You will read four short stories. Some words are missing \u2014 please fill each gap with the word or phrase that feels most natural to you, as if you were talking to a close friend. There are no right or wrong answers.',
        fr='Vous allez lire quatre courtes histoires. Certains mots manquent \u2014 veuillez compl\u00e9ter chaque espace avec le mot ou l\u2019expression qui vous semble le plus naturel, comme si vous parliez \u00e0 un ami proche. Il n\u2019y a pas de bonne ou de mauvaise r\u00e9ponse.',
        de='Sie werden vier kurze Geschichten lesen. Einige W\u00f6rter fehlen \u2014 bitte f\u00fcllen Sie jede L\u00fccke mit dem Wort oder Ausdruck, der Ihnen am nat\u00fcrlichsten erscheint, als w\u00fcrden Sie mit einem guten Freund sprechen. Es gibt keine richtigen oder falschen Antworten.',
        ja='4つの短い物語を読みます。いくつかの言葉が抜けています。親しい友人と話しているようなつもりで、最も自然だと感じる言葉やフレーズで空欄を埋めてください。正しい答えや間違った答えはありません。',
        zh='您将阅读四个短故事。有些词语缺失了——请用您觉得最自然的词语或短语来填写每个空格，就像您在跟好朋友聊天一样。没有正确或错误的答案。',
    ),
    thankyou_title=dict(en='Thank you!', fr='Merci !', de='Vielen Dank!', ja='ありがとうございました！', zh='谢谢！'),
    thankyou_msg=dict(
        en='Your responses have been recorded. You may now close this window.',
        fr='Vos r\u00e9ponses ont \u00e9t\u00e9 enregistr\u00e9es. Vous pouvez maintenant fermer cette fen\u00eatre.',
        de='Ihre Antworten wurden gespeichert. Sie k\u00f6nnen dieses Fenster jetzt schlie\u00dfen.',
        ja='回答が記録されました。このウィンドウを閉じてください。',
        zh='您的回答已记录。您现在可以关闭此窗口。',
    ),

    # ── Task 1 Instructions ──
    task1_how_title=dict(
        en='How it works',
        fr='Comment ça marche',
        de='So funktioniert es',
        ja='やり方',
        zh='任务说明',
    ),
    task1_how_step1=dict(
        en='You will read short stories with some words missing. The missing words appear as <span style="color: black;"><strong>blue hints inside the gaps</strong></span>.',
        fr='Vous lirez de courtes histoires avec des mots manquants. Les mots manquants apparaissent sous forme d\u2019indices en bleu dans les espaces.',
        de='Sie lesen kurze Geschichten, in denen einige W\u00f6rter fehlen. Die fehlenden W\u00f6rter erscheinen als blaue Hinweise in den L\u00fccken.',
        ja='短い物語を読みます。いくつかの単語が欠けています。欠けている単語は空欄の中に青いヒントとして表示されます。',
        zh='您将阅读一些短故事，其中有些词语缺失。缺失的词语会以<span style="color: black;"><strong>蓝色提示词</strong></span>的形式显示在空格中。',
    ),
    task1_how_step2=dict(
        en='Click on a blue hint to open the gap. <span style="color: black;"><strong>Use the hint word in any form — add extra words if they feel natural.</strong></span>',
        fr='Cliquez sur un indice bleu pour ouvrir l\u2019espace. <span style="color: black;"><strong>Utilisez le mot-indice sous n\u2019importe quelle forme — ajoutez des mots si cela vous semble naturel.</strong></span>',
        de='Klicken Sie auf einen blauen Hinweis, um die L\u00fccke zu \u00f6ffnen. <span style="color: black;"><strong>Verwenden Sie das Hinweiswort in beliebiger Form — f\u00fcgen Sie weitere W\u00f6rter hinzu, wenn es sich nat\u00fcrlich anf\u00fchlt.</strong></span>',
        ja='青いヒントをクリックして空欄を開いてください。<span style="color: black;"><strong>ヒントの言葉をどんな形でも使い、自然に感じるなら言葉を追加してください。</strong></span>',
        zh='点击蓝色提示词打开空格。<span style="color: black;"><strong>可以用任何形式使用提示词——如果觉得自然，可以添加额外的词语。</strong></span>',
    ),
    task1_how_step3=dict(
        en='If you click away without typing anything, the blue hint will reappear so you can come back to it later.',
        fr='Si vous cliquez ailleurs sans rien taper, l\u2019indice bleu r\u00e9appara\u00eetra pour que vous puissiez y revenir plus tard.',
        de='Wenn Sie woanders klicken, ohne etwas einzugeben, erscheint der blaue Hinweis wieder, damit Sie sp\u00e4ter darauf zur\u00fcckkommen k\u00f6nnen.',
        ja='何も入力せずに他の場所をクリックすると、青いヒントが再表示され、後で戻ってくることができます。',
        zh='如果您没有输入任何内容就点击了其他地方，蓝色提示词会重新出现，方便您稍后返回填写。',
    ),
    task1_practice_label=dict(
        en='\u270f\ufe0f Try it yourself',
        fr='\u270f\ufe0f Essayez vous-m\u00eame',
        de='\u270f\ufe0f Probieren Sie es aus',
        ja='\u270f\ufe0f 練習してみましょう',
        zh='\u270f\ufe0f 试一试',
    ),
    task1_guidelines_title=dict(
        en='Tips',
        fr='Conseils',
        de='Tipps',
        ja='ヒント',
        zh='提示',
    ),
    task1_guideline_1=dict(
        en='\u2714\ufe0f Write whatever feels most natural \u2014 <strong>there are no right or wrong answers</strong>.',
        fr='\u2714\ufe0f \u00c9crivez ce qui vous semble le plus naturel \u2014 <strong>il n\u2019y a pas de bonne ou de mauvaise r\u00e9ponse</strong>.',
        de='\u2714\ufe0f Schreiben Sie, was Ihnen am nat\u00fcrlichsten vorkommt \u2014 <strong>es gibt keine richtigen oder falschen Antworten</strong>.',
        ja='\u2714\ufe0f 最も自然だと感じるものを書いてください。<strong>正解や不正解はありません</strong>。',
        zh='\u2714\ufe0f 写下您觉得最自然的内容——<strong>没有正确或错误的答案</strong>。',
    ),
    task1_guideline_2=dict(
        en='\u2714\ufe0f Imagine you are telling the story to a close friend.',
        fr='\u2714\ufe0f Imaginez que vous racontez l\u2019histoire \u00e0 un ami proche.',
        de='\u2714\ufe0f Stellen Sie sich vor, Sie erz\u00e4hlen die Geschichte einem guten Freund.',
        ja='\u2714\ufe0f 親しい友人に話しているつもりで書いてください。',
        zh='\u2714\ufe0f 想象您正在给好朋友讲这个故事。',
    ),
    task1_guideline_3=dict(
        en='\u2714\ufe0f Use the hint word in any form \u2014 add extra words if they feel natural.',
        fr='\u2714\ufe0f Utilisez le mot-indice sous n\u2019importe quelle forme \u2014 ajoutez des mots si cela vous semble naturel.',
        de='\u2714\ufe0f Verwenden Sie das Hinweiswort in beliebiger Form \u2014 f\u00fcgen Sie weitere W\u00f6rter hinzu, wenn es sich nat\u00fcrlich anf\u00fchlt.',
        ja='\u2714\ufe0f ヒントの単語はどんな形でも使えます。自然に感じるなら言葉を加えてください。',
        zh='\u2714\ufe0f 提示词可以用任何形式——如果觉得自然，可以添加其他词语。',
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
            'Anna was having dinner with her friend. Suddenly, she {{1}} **{FEEL}** a sharp pain in her wisdom tooth. Her friend warned her: "You must see a dentist immediately, otherwise the tooth {{2}} **{SWELL}** up very soon."',
            'Anna was lucky and got an appointment for 4:00 PM. She thought to herself, "Although I am afraid of pain, this doctor is very skilled. I believe the surgery {{3}} **{GO}** smoothly."',
            'Anna arrived at the clinic. The dentist {{4}} **{EXAMINE}** her teeth and said, "We must pull it out today. It\u2019s a quick procedure. The wound {{5}} **{HEAL}** completely within a week, and by then you {{6}} **{BE}** able to eat normally."',
            'Anna {{7}} **{RETURN}** home after the surgery was finished. However, the pain was still intense. She looked in the mirror and then realized: the doctor had pulled the wrong one! The painful left tooth was still there; the doctor {{8}} **{REMOVE}** the good one, which hadn\u2019t hurt at all. Her friend told her, "Then the dentist {{9}} **{NEED}** to pull the bad tooth as well."',
            'Anna {{10}} **{CRY}**: "Oh no, does that mean I have to do this again?"'
        ]),

        # ── Story 2: Alex's Interview ──
        dict(title="Alex\u2019s Interview", paragraphs=[
            'In the morning, Alex woke up with a feeling of worry. He {{1}} **{PULL}** back the curtains and immediately noticed the dark, heavy clouds {{2}} **{MOVE}** over the city. He turned on the television news. The weatherman announced: "Be prepared, everyone. The heavy rain {{3}} **{CONTINUE}** all afternoon."',
            'Alex sighed and thought to herself: "This is bad. If I walk to the station in this weather, my suit {{4}} **{BE}** completely ruined before the interview."',
            'Suddenly, a notification popped up on {{5}} **{HE}** phone: the downtown subway line had been {{6}} **{CLOSE}** due to a technical problem.',
            'Alex said, "With this traffic, the drive {{7}} **{TAKE}** at least an hour. I need to call a taxi right now."',
            'He took a deep breath to calm down. "If I\u2019m late, the interviewer {{8}} **{THINK}** I\u2019m unprofessional," he thought.',
            'He began to gather his documents, {{9}} **{TRY}** to stay positive. He whispered to himself. "Even with the rain, I know this interview {{10}} **{GO}** well."'
        ]),

        # ── Story 3: Marco's Panic Morning ──
        dict(title="Marco\u2019s Panic Morning", paragraphs=[
            'Marco woke up and he {{1}} **{NOTICE}** his alarm didn\u2019t ring. He rushed to the bus stop, only to find the next bus wasn\u2019t coming until 8:30. Suddenly, it started to rain. Looking at the dark sky, He worried, "Oh no, I {{2}} **{MISS}** the morning meeting."',
            'He called a taxi. Inside, he {{3}} **{HEAR}** the radio announcer say, "The rain is heavy, and it {{4}} **{NOT STOP}** until this afternoon."',
            'At that moment, his girlfriend Sarah called and asked, "What are you {{5}} **{DO}** this afternoon?" Marco replied anxiously, "Today {{6}} **{BE}** very busy; I have to prepare materials for next week\u2019s meeting."',
            'Sarah was surprised: "But today is Sunday!" Marco was shocked. Sarah laughed, "Yes, Sunday is a rest day! Let\u2019s {{7}} **{HAVE}** lunch instead."',
            'Marco sighed with relief. He immediately {{8}} **{FEEL}** much better. "No problem. The restaurant {{9}} **{BE}** crowded on a Sunday. Let me book it right now. Afterwards, we can go for a walk in the park."',
            'The taxi arrived. Marco paid the driver and thought, "this {{10}} **{BE}** a wonderful day after all!"'
        ]),

        # ── Story 4: Lee's Camping Trip ──
        dict(title="Lee\u2019s Camping Trip", paragraphs=[
            'The sky was dark with heavy clouds, and the temperature began to {{1}} **{DROP}**. Lee looked at his phone and said to his wife, "The forecast says it {{2}} **{SNOW}** tonight." Lee felt cold and wanted a cup of hot coffee. While he was {{3}} **{MAKE}** the coffee, his wife stopped him and {{4}} **{SAY}**, "If you drink that coffee now, it {{5}} **{KEEP}** you awake all night."',
            'Lee hesitated and put down the cup. "You\u2019re right. I have to get up early tomorrow. If I don\u2019t sleep well, driving {{6}} **{BE}** dangerous."',
            'Before going to bed, he checked his map app and {{7}} **{FIND}** that the drive to the mountain takes about three hours.',
            'The next morning, his wife asked, "Do we need thick coats?"',
            'Lee checked the weather again and said, "We should bring them. The temperature in the mountains is much lower than here. If we don\u2019t {{8}} **{DRESS}** warmly, we {{9}} **{CATCH}** a cold."',
            'They smiled at each other, both expecting that this camping trip {{10}} **{BE}** very fun."'
        ]),
    ],

# STORIES = dict(
#     en=[
#         # ── Story 1: Anna's Toothache ──
#         dict(title="Anna\u2019s Toothache", paragraphs=[
#             'Anna was having dinner {{1}} suddenly, she felt a sharp pain in her wisdom tooth. Her friend warned her: \u201cYou must see a dentist immediately, otherwise the tooth {{2}} swell up very soon.\u201d',
#             'Anna was lucky and got an appointment for 4:00 PM. She thought to herself, \u201cAlthough I am afraid of pain, this doctor is very skilled. I believe the surgery {{3}} go smoothly.\u201d',
#             'Anna arrived at the clinic. The dentist examined {{4}} teeth and said, \u201cWe must pull it out today. It\u2019s a quick procedure. The wound {{5}} heal completely within a week, and by then you {{6}} be able to eat normally.\u201d',
#             'Anna returned home after she had finished {{7}} the extraction. However, the pain was still intense. She looked in the mirror and {{8}} realized: the doctor had pulled the wrong one! The painful left tooth was still there; the one removed was {{9}} the right one, which hadn\u2019t hurt at all.',
#             'Anna burst into tears: \u201cOh my god, does that mean I {{10}} suffer through this all over again? Just my luck!\u201d',
#         ]),
#         # ── Story 2: Alex's Interview ──
#         dict(title="Alex\u2019s Interview", paragraphs=[
#             'Yesterday morning, Alex woke up with a feeling of dread. He pulled back the curtains and immediately {{1}} the dark, heavy clouds rolling over the city skyline.',
#             'He turned on the television news. The weatherman announced: \u201cBe prepared, everyone. The heavy rain {{2}} continue all afternoon.\u201d',
#             'Alex sighed and thought to herself: \u201cGreat. If I walk to the station in this weather, my suit {{3}} be completely ruined before the interview.\u201d',
#             'He ran to the hallway closet, frantically searching {{4}} his large umbrella. Suddenly, a notification popped up on his phone: the downtown subway line had {{5}} due to a signal failure.',
#             '\u201cThat\u2019s it!\u201d Alex shouted, grabbing his keys {{6}} the table. \u201cI {{7}} drive my car instead. It\u2019s the only way.\u201d',
#             'He took a deep breath to calm down. \u201cI {{8}} call the recruiter from the car to let them know I might be late,\u201d he decided.',
#             'He began {{9}} gather his documents, trying to stay positive. \u201cCome on, Alex,\u201d he whispered to himself. \u201cEven with the rain, I know this interview {{10}} go well.\u201d',
#         ]),
#         # ── Story 3: Marco's Panic Morning ──
#         dict(title="Marco\u2019s Panic Morning", paragraphs=[
#             'Marco woke up and {{1}} realized his alarm hadn\u2019t gone off. He rushed to the bus stop, only to find the next bus wasn\u2019t coming until 8:30. Suddenly, it started to rain. Looking at the gloomy sky, he was worried that he {{2}} miss the morning meeting.',
#             'He quickly hailed a taxi. Inside, he {{3}} the radio announcer say, \u201cThe rain is heavy, and it {{4}} not stop until this afternoon.\u201d',
#             'At that moment, his girlfriend Sarah called and asked, \u201cWhat are you {{5}} this afternoon?\u201d Marco replied anxiously, \u201cToday {{6}} be very busy; I have to prepare materials for next week\u2019s meeting.\u201d',
#             'Sarah was surprised: \u201cBut today is Sunday!\u201d Marco was stunned. Sarah laughed, \u201cYes, Sunday is a rest day! Let\u2019s go have lunch instead.\u201d',
#             'Marco sighed with relief, his mood instantly lifting. \u201cNo problem. I {{7}} book the restaurant right now, and afterwards we can go for a {{8}} in the park.\u201d',
#             'The taxi arrived. Marco paid {{9}} driver and felt that this {{10}} be a wonderful day after all.',
#         ]),
#         # ── Story 4: Lee's Camping Trip ──
#         dict(title="Lee\u2019s Camping Trip", paragraphs=[
#             'The sky was dark with heavy clouds, and the temperature began to drop. Lee pointed out the window and said to his wife, \u201cLook at those clouds. It {{1}} definitely snow tonight.\u201d',
#             'Lee felt cold and wanted a cup of hot coffee. While he was {{2}} the coffee, his wife stopped him and said, \u201cIf you drink that coffee now, you {{3}} not sleep all night.\u201d',
#             'Lee hesitated and put down the cup. \u201cYou\u2019re right. I have to get up early tomorrow. If I don\u2019t sleep well, driving {{4}} be dangerous.\u201d',
#             'Before going to bed, he checked the train schedule and found {{5}} the weekend train departed at 10:00 AM on Saturday.',
#             'The next morning, planning for the weekend camping trip, Lee assigned tasks before work: \u201cAfter work tonight, I {{6}} go to the supermarket to buy groceries.\u201d',
#             'His wife nodded, \u201cOkay, then I am responsible {{7}} packing the luggage. By the way, do we need thick coats?\u201d',
#             'Lee checked the weather forecast on his phone and said, \u201cBetter bring them. The temperature in the mountains is {{8}} lower than here. If we don\u2019t dress warmly, we {{9}} catch a cold.\u201d',
#             'They smiled at each other, both expecting that this camping trip {{10}} be very fun.',
#         ]),
#     ],

    # ── FRENCH ─────────────────────────────────────────────
    fr=[
        # ── Story 1: Le mal de dent d'Anna ──
        dict(title='Le mal de dent d’Anna', paragraphs=[
            'Anna dînait avec son amie. Soudain, elle {{1}} **{RESSENTIR}** une douleur vive dans sa dent de sagesse. Son amie l’a prévenue : « Tu dois voir un dentiste immédiatement, sinon la dent {{2}} **{ENFLER}** très vite. »',
            'Anna a eu de la chance et a obtenu un rendez-vous à 16 heures. Elle a pensé : « Même si j’ai peur de la douleur, ce médecin est très compétent. Je crois que l’opération {{3}} **{SE PASSER}** bien. »',
            'Anna est arrivée à la clinique. Le dentiste {{4}} **{EXAMINER}** ses dents et a dit : « Il faut l’arracher aujourd’hui. C’est une intervention rapide. La plaie {{5}} **{GUÉRIR}** complètement en une semaine, et à ce moment-là vous {{6}} **{POUVOIR}** manger normalement. »',
            'Anna {{7}} **{RENTRER}** chez elle après l’opération. Cependant, la douleur était encore intense. Elle s’est regardée dans le miroir et a alors réalisé : le dentiste avait arraché la mauvaise dent ! La dent gauche douloureuse était toujours là ; le dentiste {{8}} **{ARRACHER}** la bonne, qui n’avait pas fait mal du tout. Son amie lui a dit : « Alors le dentiste {{9}} **{DEVOIR}** aussi arracher la mauvaise dent. »',
            'Anna {{10}} **{PLEURER}** : « Oh non, ça veut dire que je dois recommencer tout ça ? »',
        ]),

        # ── Story 2: L'entretien d'Alex ──
        dict(title='L’entretien d’Alex', paragraphs=[
            'Le matin, Alex s’est réveillé avec un sentiment d’inquiétude. Il {{1}} **{TIRER}** les rideaux et a immédiatement remarqué les nuages sombres et lourds qui {{2}} **{SE DÉPLACER}** au-dessus de la ville. Il a allumé la télévision. Le présentateur météo a annoncé : « Préparez-vous, tout le monde. La pluie forte {{3}} **{CONTINUER}** tout l’après-midi. »',
            'Alex a soupiré et a pensé : « C’est mauvais. Si je marche jusqu’à la gare par ce temps, mon costume {{4}} **{ÊTRE}** complètement fichu avant l’entretien. »',
            'Soudain, une notification est apparue sur {{5}} **{SON}** téléphone : la ligne de métro du centre-ville avait été {{6}} **{FERMER}** à cause d’un problème technique.',
            'Alex a dit : « Avec cette circulation, le trajet {{7}} **{PRENDRE}** au moins une heure. Je dois appeler un taxi tout de suite. »',
            'Il a pris une grande inspiration pour se calmer. « Si je suis en retard, le recruteur {{8}} **{PENSER}** que je ne suis pas professionnel », a-t-il pensé.',
            'Il a commencé à rassembler ses documents, {{9}} **{ESSAYER}** de rester positif. Il s’est murmuré : « Même avec la pluie, je sais que cet entretien {{10}} **{SE PASSER}** bien. »',
        ]),

        # ── Story 3: La matinée de panique de Marco ──
        dict(title='La matinée de panique de Marco', paragraphs=[
            'Marco s’est réveillé et il {{1}} **{REMARQUER}** que son réveil n’avait pas sonné. Il s’est précipité à l’arrêt de bus, pour découvrir que le prochain bus n’arrivait pas avant 8 h 30. Soudain, il s’est mis à pleuvoir. En regardant le ciel sombre, il s’est inquiété : « Oh non, je {{2}} **{RATER}** la réunion du matin. »',
            'Il a appelé un taxi. À l’intérieur, il {{3}} **{ENTENDRE}** le présentateur radio dire : « La pluie est forte, et elle {{4}} **{S’ARRÊTER}** pas avant cet après-midi. »',
            'À ce moment-là, sa copine Sarah a appelé et demandé : « Qu’est-ce que tu {{5}} **{FAIRE}** cet après-midi ? » Marco a répondu anxieusement : « Aujourd’hui {{6}} **{ÊTRE}** très chargé ; je dois préparer des documents pour la réunion de la semaine prochaine. »',
            'Sarah a été surprise : « Mais on est dimanche ! » Marco était stupéfait. Sarah a ri : « Oui, le dimanche c’est repos ! Allons plutôt {{7}} **{DÉJEUNER}**. »',
            'Marco a soupiré de soulagement. Il {{8}} **{SE SENTIR}** tout de suite beaucoup mieux. « Pas de problème. Le restaurant {{9}} **{ÊTRE}** plein un dimanche. Laisse-moi le réserver tout de suite. Après, on pourra faire une promenade dans le parc. »',
            'Le taxi est arrivé. Marco a payé le chauffeur et a pensé : « Cette journée {{10}} **{ÊTRE}** finalement une belle journée ! »',
        ]),

        # ── Story 4: Le camping de Lee ──
        dict(title='Le camping de Lee', paragraphs=[
            'Le ciel était sombre avec de gros nuages, et la température a commencé à {{1}} **{BAISSER}**. Lee a regardé son téléphone et a dit à sa femme : « La météo annonce qu’il {{2}} **{NEIGER}** ce soir. » Lee avait froid et voulait un café chaud. Pendant qu’il {{3}} **{PRÉPARER}** le café, sa femme l’a arrêté et {{4}} **{DIRE}** : « Si tu bois ce café maintenant, tu {{5}} **{RESTER}** éveillé toute la nuit. »',
            'Lee a hésité et a posé la tasse. « Tu as raison. Je dois me lever tôt demain. Si je ne dors pas bien, conduire {{6}} **{ÊTRE}** dangereux. »',
            'Avant de se coucher, il a vérifié son application de carte et {{7}} **{TROUVER}** que le trajet jusqu’à la montagne prend environ trois heures.',
            'Le lendemain matin, sa femme a demandé : « Est-ce qu’on a besoin de manteaux épais ? »',
            'Lee a vérifié la météo de nouveau et a dit : « Mieux vaut les prendre. La température en montagne est beaucoup plus basse qu’ici. Si on ne {{8}} **{S’HABILLER}** pas chaudement, on {{9}} **{ATTRAPER}** un rhume. »',
            'Ils se sont souri, tous les deux pensant que ce voyage de camping {{10}} **{ÊTRE}** très amusant. »',
        ]),
    ],

    # ── GERMAN ─────────────────────────────────────────────
    de=[
        # ── Story 1: Annas Zahnschmerzen ──
        dict(title='Annas Zahnschmerzen', paragraphs=[
            'Anna war mit ihrer Freundin beim Abendessen. Plötzlich {{1}} **{SPÜREN}** sie einen stechenden Schmerz in ihrem Weisheitszahn. Ihre Freundin warnte sie: „Du musst sofort zum Zahnarzt, sonst {{2}} **{ANSCHWELLEN}** der Zahn sehr bald.“',
            'Anna hatte Glück und bekam einen Termin um 16 Uhr. Sie dachte sich: „Obwohl ich Angst vor Schmerzen habe, ist dieser Arzt sehr geschickt. Ich glaube, die Operation {{3}} **{VERLAUFEN}** gut.“',
            'Anna kam in der Klinik an. Der Zahnarzt {{4}} **{UNTERSUCHEN}** ihre Zähne und sagte: „Wir müssen ihn heute ziehen. Es ist ein schneller Eingriff. Die Wunde {{5}} **{HEILEN}** innerhalb einer Woche vollständig, und bis dahin {{6}} **{KÖNNEN}** Sie wieder normal essen.“',
            'Anna {{7}} **{ZURÜCKKEHREN}** nach Hause, nachdem die Operation beendet war. Allerdings war der Schmerz noch heftig. Sie schaute in den Spiegel und erkannte dann: Der Arzt hatte den falschen Zahn gezogen! Der schmerzende linke Zahn war noch da; der Arzt {{8}} **{ENTFERNEN}** den guten, der gar nicht wehgetan hatte. Ihre Freundin sagte ihr: „Dann {{9}} **{MÜSSEN}** der Zahnarzt auch noch den schlechten Zahn ziehen.“',
            'Anna {{10}} **{WEINEN}**: „Oh nein, heißt das, ich muss das alles noch einmal durchmachen?“',
        ]),

        # ── Story 2: Alex' Vorstellungsgespräch ──
        dict(title='Alex’ Vorstellungsgespräch', paragraphs=[
            'Am Morgen wachte Alex mit einem Gefühl der Sorge auf. Er {{1}} **{ZURÜCKZIEHEN}** die Vorhänge und bemerkte sofort die dunklen, schweren Wolken, die über die Stadt {{2}} **{ZIEHEN}**. Er schaltete den Fernseher ein. Der Wettermoderator verkündete: „Bereiten Sie sich vor, alle. Der starke Regen {{3}} **{ANHALTEN}** den ganzen Nachmittag.“',
            'Alex seufzte und dachte: „Das ist schlecht. Wenn ich bei diesem Wetter zum Bahnhof laufe, {{4}} **{SEIN}** mein Anzug vor dem Gespräch völlig ruiniert.“',
            'Plötzlich erschien eine Benachrichtigung auf {{5}} **{SEIN}** Handy: Die U-Bahn-Linie in die Innenstadt war wegen eines technischen Problems {{6}} **{SPERREN}** worden.',
            'Alex sagte: „Bei diesem Verkehr {{7}} **{DAUERN}** die Fahrt mindestens eine Stunde. Ich muss sofort ein Taxi rufen.“',
            'Er holte tief Luft, um sich zu beruhigen. „Wenn ich zu spät komme, {{8}} **{DENKEN}** der Interviewer, dass ich unprofessionell bin“, dachte er.',
            'Er begann seine Unterlagen zusammenzusuchen und {{9}} **{VERSUCHEN}**, positiv zu bleiben. Er flüsterte sich zu: „Auch bei Regen, ich weiß, dass dieses Gespräch {{10}} **{LAUFEN}** gut.“',
        ]),

        # ── Story 3: Marcos panischer Morgen ──
        dict(title='Marcos panischer Morgen', paragraphs=[
            'Marco wachte auf und er {{1}} **{BEMERKEN}**, dass sein Wecker nicht geklingelt hatte. Er rannte zur Bushaltestelle, nur um festzustellen, dass der nächste Bus erst um 8:30 kam. Plötzlich fing es an zu regnen. Als er in den dunklen Himmel schaute, machte er sich Sorgen: „Oh nein, ich {{2}} **{VERPASSEN}** die Morgenbesprechung.“',
            'Er rief ein Taxi. Drinnen {{3}} **{HÖREN}** er den Radiosprecher sagen: „Der Regen ist stark, und er {{4}} **{AUFHÖREN}** nicht vor heute Nachmittag.“',
            'In dem Moment rief seine Freundin Sarah an und fragte: „Was {{5}} **{MACHEN}** du heute Nachmittag?“ Marco antwortete ängstlich: „Heute {{6}} **{SEIN}** sehr stressig; ich muss Unterlagen für die Besprechung nächste Woche vorbereiten.“',
            'Sarah war überrascht: „Aber heute ist Sonntag!“ Marco war verblüfft. Sarah lachte: „Ja, Sonntag ist Ruhetag! Lass uns stattdessen {{7}} **{ESSEN}** gehen.“',
            'Marco seufzte erleichtert. Er {{8}} **{FÜHLEN}** sich sofort viel besser. „Kein Problem. Das Restaurant {{9}} **{SEIN}** an einem Sonntag bestimmt voll. Lass mich jetzt gleich reservieren. Danach können wir einen Spaziergang im Park machen.“',
            'Das Taxi kam an. Marco bezahlte den Fahrer und dachte: „Dieser Tag {{10}} **{SEIN}** doch noch ein schöner Tag!“',
        ]),

        # ── Story 4: Lees Campingausflug ──
        dict(title='Lees Campingausflug', paragraphs=[
            'Der Himmel war dunkel mit schweren Wolken, und die Temperatur begann zu {{1}} **{SINKEN}**. Lee schaute auf sein Handy und sagte zu seiner Frau: „Die Vorhersage sagt, es {{2}} **{SCHNEIEN}** heute Nacht.“ Lee fror und wollte eine Tasse heißen Kaffee. Während er den Kaffee {{3}} **{MACHEN}**, hielt seine Frau ihn auf und {{4}} **{SAGEN}**: „Wenn du jetzt diesen Kaffee trinkst, {{5}} **{HALTEN}** er dich die ganze Nacht wach.“',
            'Lee zögerte und stellte die Tasse ab. „Du hast recht. Ich muss morgen früh aufstehen. Wenn ich nicht gut schlafe, {{6}} **{SEIN}** das Fahren gefährlich.“',
            'Vor dem Schlafengehen überprüfte er seine Karten-App und {{7}} **{FESTSTELLEN}**, dass die Fahrt zum Berg etwa drei Stunden dauert.',
            'Am nächsten Morgen fragte seine Frau: „Brauchen wir dicke Mäntel?“',
            'Lee überprüfte die Wettervorhersage erneut und sagte: „Besser mitnehmen. Die Temperatur in den Bergen ist viel niedriger als hier. Wenn wir uns nicht warm {{8}} **{ANZIEHEN}**, {{9}} **{ERKÄLTEN}** wir uns.“',
            'Sie lächelten einander an und beide erwarteten, dass dieser Campingausflug {{10}} **{SEIN}** sehr lustig.“',
        ]),
    ],

    # ── CHINESE ─────────────────────────────────────────────
    zh=[
        # ── Story 1: 安娜的牙疼 ──
        dict(title='安娜的牙疼', paragraphs=[
            '安娜正在跟朋友吃晚饭。突然，她{{1}} **{感到}**智齿一阵剧痛。朋友提醒她："你得赶紧去看牙医，不然牙齿很快就{{2}} **{肿}**起来了。"',
            '安娜运气不错，挂到了下午四点的号。她心想："虽然我怕疼，但是这个医生技术很好，我相信手术{{3}} **{顺利}**。"',
            '安娜到了诊所。牙医{{4}} **{检查}**了她的牙，说："今天就得拔掉。手术很快的。伤口一个星期就{{5}} **{愈合}**，到时候你就{{6}} **{可以}**正常吃东西了。"',
            '手术做完后，安娜{{7}} **{回到}**了家。可是还是很疼。她照了照镜子，才发现：医生拔错牙了！疼的那颗还好好的，医生把不疼的那颗给{{8}} **{拔}**了。朋友跟她说："那医生还{{9}} **{得}**把坏牙也拔了。"',
            '安娜{{10}} **{哭}**了起来："天哪，我还得再来一次吗？"',
        ]),

        # ── Story 2: 小明的面试 ──
        dict(title='小明的面试', paragraphs=[
            '早上，小明带着不安的心情醒来。他{{1}} **{拉开}**窗帘，马上看到乌云正在城市上空{{2}} **{移动}**。他打开电视看新闻。天气预报员说："请大家做好准备，大雨整个下午都{{3}} **{持续}**。"',
            '小明叹了口气，心想："糟了。要是这种天气走去车站，西装{{4}} **{淋}**湿了。"',
            '突然，{{5}} **{他的}**手机弹出一条消息：市中心地铁因为技术故障已经{{6}} **{停运}**了。',
            '小明说："这种路况开车的话，至少{{7}} **{花}**一个小时。我得赶紧叫出租车。"',
            '他深吸一口气让自己冷静下来。"要是迟到了，面试官{{8}} **{觉得}**我不靠谱，"他想。',
            '他开始收拾材料，{{9}} **{努力}**保持积极心态。他小声跟自己说："就算下雨，我知道这次面试{{10}} **{顺利}**。"',
        ]),

        # ── Story 3: 马可慌张的早晨 ──
        dict(title='马可慌张的早晨', paragraphs=[
            '马可醒来，{{1}} **{发现}**闹钟没有响。他赶到公交站，结果下一班车要八点半才来。突然开始下雨了。看着阴沉沉的天，他着急地想："完了，我{{2}} **{赶不上}**早上的会了。"',
            '他叫了辆出租车。在车里，他{{3}} **{听到}**广播里说："雨下得很大，要到下午才{{4}} **{停}**。"',
            '这时候，女朋友小丽打来电话："你今天下午{{5}} **{做}**什么？"马可焦急地说："今天{{6}} **{很忙}**，我得准备下周开会的材料。"',
            '小丽很惊讶："可今天是星期天啊！"马可愣住了。小丽笑着说："对呀，星期天休息！咱们去{{7}} **{吃}**午饭吧。"',
            '马可松了口气，心情一下子就{{8}} **{好}**了。"没问题。星期天餐厅{{9}} **{挤}**，我先订个位。吃完还可以去公园逛逛。"',
            '出租车到了。马可付了车费，心想："今天{{10}} **{是}**美好的一天！"',
        ]),

        # ── Story 4: 小李的露营之旅 ──
        dict(title='小李的露营之旅', paragraphs=[
            '天空乌云密布，气温开始{{1}} **{下降}**。小李看了看手机，跟妻子说："天气预报说今晚{{2}} **{下雪}**。"小李觉得冷，想喝杯热咖啡。他正在{{3}} **{泡}**咖啡，妻子拦住他{{4}} **{说}**："你现在喝了咖啡，晚上{{5}} **{睡不着}**的。"',
            '小李犹豫了一下，放下了杯子。"你说得对。明天得早起。要是睡不好，开车{{6}} **{危险}**。"',
            '睡觉前，他查了查地图，{{7}} **{发现}**开车到山里大概要三个小时。',
            '第二天早上，妻子问："需要带厚外套吗？"',
            '小李又看了一下天气预报，说："带上吧。山里气温比这儿低多了。穿少了的话，我们{{8}} **{着凉}**，还容易{{9}} **{感冒}**。"',
            '两人相视一笑，都觉得这次露营{{10}} **{好玩}**。',
        ]),
    ],

    # ── JAPANESE ───────────────────────────────────────────
    ja=[
        # ── Story 1: アンナの歯痛 ──
        dict(title='アンナの歯痛', paragraphs=[
            'アンナは友人と夕食を食べていました。突然、親知らずに鋭い痛みを{{1}} **{感じる}**。友人は彼女に警告しました。「すぐに歯医者に行かないと、その歯はすぐに{{2}} **{腫れる}**よ。」',
            'アンナは運良く午後4時の予約が取れました。「痛みは怖いけれど、この先生はとても腕がいい。手術は{{3}} **{うまくいく}**と信じているわ」と心の中で思いました。',
            'アンナはクリニックに到着しました。歯科医は彼女の歯を{{4}} **{診察する}**、こう言いました。「今日抜かなければなりません。すぐに終わる処置です。傷は1週間以内に完全に{{5}} **{治る}**、そうすれば普通に食事が{{6}} **{できる}**ようになります。」',
            '手術が終わり、アンナは家に{{7}} **{帰る}**。しかし、痛みはまだ激しいものでした。鏡を見て気づきました。医者は間違った歯を抜いてしまったのです！痛む左の歯はまだそこにあり、医者は全く痛くなかった右の歯を{{8}} **{抜く}**のでした。友人は彼女に言いました。「じゃあ歯医者はあの悪い歯も{{9}} **{抜く}**わね。」',
            'アンナは{{10}} **{泣く}**：「そんな、もう一度やり直さなきゃいけないの？」',
        ]),

        # ── Story 2: アレックスの面接 ──
        dict(title='アレックスの面接', paragraphs=[
            'その朝、アレックスは不安な気持ちで目を覚ましました。カーテンを{{1}} **{開ける}**と、暗く重い雲が街の上を{{2}} **{移動する}**のがすぐに目に入りました。テレビのニュースをつけました。気象予報士が告げました。「皆さん、備えてください。大雨は午後ずっと{{3}} **{続く}**でしょう。」',
            'アレックスはため息をつき、心の中で思いました。「最悪だ。この天気の中を駅まで歩いたら、面接の前にスーツが完全に{{4}} **{だめになる}**。」',
            '突然、{{5}} **{彼の}**携帯に通知が来ました。都心の地下鉄が技術的な問題で{{6}} **{運休する}**というのです。',
            'アレックスは言いました。「この交通状況では、移動に少なくとも1時間は{{7}} **{かかる}**。今すぐタクシーを呼ばないと。」',
            '彼は深呼吸をして落ち着こうとしました。「遅刻したら、面接官はプロ意識がないと{{8}} **{思う}**だろう」と考えました。',
            '彼は書類をまとめ始め、前向きに{{9}} **{なる}**よう努めました。「しっかりしろ、アレックス」と自分に言い聞かせました。「雨でも、この面接は{{10}} **{うまくいく}**と分かってる。」',
        ]),

        # ── Story 3: マルコのパニックな朝 ──
        dict(title='マルコのパニックな朝', paragraphs=[
            'マルコは目を覚まし、目覚ましが鳴らなかったことに{{1}} **{気づく}**。バス停へ急ぎましたが、次のバスは8時半まで来ないことがわかりました。突然、雨が降り出しました。暗い空を見上げ、「まずい、朝の会議に{{2}} **{遅れる}**」と心配になりました。',
            '彼はタクシーを呼びました。車内で、ラジオのアナウンサーの声が{{3}} **{聞こえる}**。「雨は激しく、午後まで{{4}} **{止む}**ことはないでしょう。」',
            'その瞬間、恋人のサラから電話があり、「今日の午後は何を{{5}} **{する}**の？」と尻ねました。マルコは不安そうに答えました。「今日はとても{{6}} **{忙しい}**。来週の会議の資料を準備しなきゃいけないんだ。」',
            'サラは驚きました。「でも今日は日曜日よ！」マルコは呆然としました。サラは笑いました。「そうよ、日曜日は休みの日！代わりにランチに{{7}} **{行く}**！」',
            'マルコは安堵のため息をつきました。たちまち気分が{{8}} **{良くなる}**。「問題ないよ。日曜日だからレストランは{{9}} **{混む}**だろう。今すぐ予約しよう。その後、公園を散歩しよう。」',
            'タクシーが到着しました。マルコは運転手に料金を払い、「結局今日は素晴らしい一日に{{10}} **{なる}**！」と思いました。',
        ]),

        # ── Story 4: リーのキャンプ旅行 ──
        dict(title='リーのキャンプ旅行', paragraphs=[
            '空は重い雲で暗く、気温が{{1}} **{下がる}**始めていました。リーは携帯を見て妻に言いました。「天気予報によると、今夜{{2}} **{雪が降る}**らしいよ。」リーは寒気を感じ、温かいコーヒーが欲しくなりました。彼がコーヒーを{{3}} **{入れる}**いると、妻が止めて{{4}} **{言う}**。「今そのコーヒーを飲んだら、一晩中目が{{5}} **{覚める}**わよ。」',
            'リーは踊躇してカップを置きました。「君の言う通りだ。明日は早起きしなきゃいけない。よく眠れないと、運転は{{6}} **{危険}**。」',
            '寝る前に、地図アプリを確認し、山までの運転に約3時間かかることが{{7}} **{わかる}**。',
            '翌朝、妻が尻ねました。「厚手のコートは必要かしら？」',
            'リーは天気予報をもう一度確認して言いました。「持っていったほうがいい。山の気温はここよりずっと低い。暖かく{{8}} **{する}**ないと、{{9}} **{風邪をひく}**よ。」',
            '二人は微笑み合い、このキャンプ旅行はとても{{10}} **{楽しい}**と予感しました。',
        ]),
    ],
)

PRACTICE_PARAS = dict(
    en=[
        'It was a rainy morning. Tom {{1}} **{LOOK}** out the window and noticed the streets were completely wet.',
        'He grabbed his coat and thought, "I {{2}} **{NEED}** an umbrella today. Otherwise I {{3}} **{GET}** soaked on my way to work."',
    ],
    fr=[
        'C\u2019\u00e9tait un matin pluvieux. Tom {{1}} **{REGARDER}** par la fen\u00eatre et a remarqu\u00e9 que les rues \u00e9taient compl\u00e8tement mouill\u00e9es.',
        'Il a pris son manteau et a pens\u00e9 : \u00ab Il me {{2}} **{FALLOIR}** un parapluie aujourd\u2019hui. Sinon, je {{3}} **{\u00caTRE}** tremp\u00e9 en allant au travail. \u00bb',
    ],
    de=[
        'Es war ein verregneter Morgen. Tom {{1}} **{SCHAUEN}** aus dem Fenster und bemerkte, dass die Stra\u00dfen v\u00f6llig nass waren.',
        'Er griff nach seinem Mantel und dachte: \u201eIch {{2}} **{BRAUCHEN}** heute einen Regenschirm. Sonst {{3}} **{WERDEN}** ich auf dem Weg zur Arbeit durchn\u00e4sst.\u201c',
    ],
    ja=[
        '\u96e8\u306e\u671d\u3067\u3057\u305f\u3002\u30c8\u30e0\u306f\u7a93\u306e\u5916\u3092{{1}} **{\u898b\u308b}**\u3001\u901a\u308a\u304c\u3059\u3063\u304b\u308a\u6fe1\u308c\u3066\u3044\u308b\u3053\u3068\u306b\u6c17\u3065\u304d\u307e\u3057\u305f\u3002',
        '\u5f7c\u306f\u30b3\u30fc\u30c8\u3092\u624b\u306b\u53d6\u308a\u3001\u300c\u4eca\u65e5\u306f\u5098\u304c{{2}} **{\u5fc5\u8981}**\u3060\u3002\u305d\u3046\u3057\u306a\u3044\u3068\u3001\u4ed5\u4e8b\u306b\u884c\u304f\u9014\u4e2d\u3067{{3}} **{\u6fe1\u308c\u308b}**\u300d\u3068\u601d\u3044\u307e\u3057\u305f\u3002',
    ],
    zh=[
        '那是一个下雨的早晨。小明往窗外{{1}} **{看}**了一眼，发现街上全是水。',
        '他拿起外套，心想："今天{{2}} **{需要}**带把伞。不然上班路上{{3}} **{淋}**湿了。"',
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

    # ── Consent ──
    gave_consent = models.BooleanField(initial=False, blank=True)

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
    prolific_id = models.StringField(blank=True, initial='')
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


class Consent(Page):
    form_model = 'player'
    form_fields = ['gave_consent']

    @staticmethod
    def vars_for_template(player):
        lang = player.session.config.get('language', 'en')
        player.language = lang
        player.participant.language = lang
        return _ctx(player, 0)

class NoConsent(Page):
    @staticmethod
    def is_displayed(player):
        return not player.gave_consent

    @staticmethod
    def vars_for_template(player):
        return _ctx(player, 0)


class ProlificID(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    @staticmethod
    def is_displayed(player):
        return player.gave_consent

    @staticmethod
    def vars_for_template(player):
        return _ctx(player, 0)

    @staticmethod
    def error_message(player, values):
        if not values['prolific_id'] or not values['prolific_id'].strip():
            lang = player.language
            return ui_dict(lang).get('prolific_error', 'Please enter your Prolific ID.')


class Screening(Page):
    form_model = 'player'
    form_fields = ['age_range', 'is_native', 'education', 'other_language_level']

    @staticmethod
    def is_displayed(player):
        return player.gave_consent

    @staticmethod
    def vars_for_template(player):
        # Get the base context (lang + ui + progress)
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
        # Pass if: Native Speaker (True) AND Other Language Level is 0 or 1
        if player.is_native and player.other_language_level <= 1:
            player.screened_out = False
        else:
            player.screened_out = True


class ScreenOut(Page):
    def is_displayed(player):
        return player.gave_consent and player.screened_out

    @staticmethod
    def vars_for_template(player):
        # Still need to pass base context so Base.html can render the head/css correctly
        return _ctx(player, 0)


class Task1Intro(Page):
    def is_displayed(player):
        return player.gave_consent and not player.screened_out

    @staticmethod
    def vars_for_template(player):
        lang = player.language
        practice = PRACTICE_PARAS.get(lang, PRACTICE_PARAS['en'])
        ctx = _ctx(player, 5)
        ctx['practice_paras'] = practice
        return ctx

class Task1Story1(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return player.gave_consent and not player.screened_out

    @staticmethod
    def vars_for_template(player):
        # Safely get stories for current language
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[0],
            story_num=1, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 10),
        )


class Task1Story2(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return player.gave_consent and not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[1],
            story_num=2, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 16),
        )


class Task1Story3(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return player.gave_consent and not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[2],
            story_num=3, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 22),
        )


class Task1Story4(Page):
    template_name = 'Task1/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def is_displayed(player):
        return player.gave_consent and not player.screened_out

    @staticmethod
    def vars_for_template(player):
        stories = STORIES.get(player.language, STORIES['en'])
        return dict(
            story=stories[3],
            story_num=4, total=4,
            existing=player.task1_responses or '{}',
            **_ctx(player, 28),
        )


page_sequence = [
    Consent,
    NoConsent,
    ProlificID,
    Screening,
    ScreenOut,
    Task1Intro,
    Task1Story1,
    Task1Story2,
    Task1Story3,
    Task1Story4,
]

# steps to get latest code from github, then push it to heroku for testing (for Lin)
# pull from git, cd to root folder, then pull git with: git pull
# then push to heroku: git push heroku `git subtree split --prefix LLA-Exp1-260214 main`:main --force
# Then reset database: heroku run otree resetdb