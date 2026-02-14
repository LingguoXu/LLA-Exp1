from otree.api import *
import json

doc = """
Cross-linguistic FTR & Loss Aversion — Task 1 trial.
Languages: English (en), French (fr), German (de).
"""


class C(BaseConstants):
    NAME_IN_URL = 'study'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


# ═══════════════════════════════════════════════════════════
# UI STRINGS  — keyed by language code
# ═══════════════════════════════════════════════════════════
UI = dict(
    # chrome
    btn_continue  = dict(en='Continue', fr='Continuer', de='Weiter'),
    btn_read_more = dict(en='Continue reading\u2026', fr='Lire la suite\u2026', de='Weiterlesen\u2026'),
    btn_start     = dict(en="Let's begin", fr='Commençons', de="Los geht's"),
    btn_finish    = dict(en='Finish', fr='Terminer', de='Fertig'),
    required_msg  = dict(
        en='Please fill in every blank before continuing.',
        fr='Veuillez remplir tous les espaces avant de continuer.',
        de='Bitte f\u00fcllen Sie alle L\u00fccken aus, bevor Sie fortfahren.',
    ),
    # Task 1
    task1_title = dict(
        en='Part 1 \u2014 Complete the Stories',
        fr='Partie 1 \u2014 Compl\u00e9ter les histoires',
        de='Teil 1 \u2014 Geschichten vervollst\u00e4ndigen',
    ),
    task1_intro = dict(
        en='You will read four short stories. Some words are missing \u2014 please fill each gap with the word or phrase that feels most natural to you, as if you were talking to a close friend. There are no right or wrong answers.',
        fr='Vous allez lire quatre courtes histoires. Certains mots manquent \u2014 veuillez compl\u00e9ter chaque espace avec le mot ou l\u2019expression qui vous semble le plus naturel, comme si vous parliez \u00e0 un ami proche. Il n\u2019y a pas de bonne ou de mauvaise r\u00e9ponse.',
        de='Sie werden vier kurze Geschichten lesen. Einige W\u00f6rter fehlen \u2014 bitte f\u00fcllen Sie jede L\u00fccke mit dem Wort oder Ausdruck, der Ihnen am nat\u00fcrlichsten erscheint, als w\u00fcrden Sie mit einem guten Freund sprechen. Es gibt keine richtigen oder falschen Antworten.',
    ),
    thankyou_title = dict(en='Thank you!', fr='Merci !', de='Vielen Dank!'),
    thankyou_msg = dict(
        en='Your responses have been recorded. You may now close this window.',
        fr='Vos r\u00e9ponses ont \u00e9t\u00e9 enregistr\u00e9es. Vous pouvez maintenant fermer cette fen\u00eatre.',
        de='Ihre Antworten wurden gespeichert. Sie k\u00f6nnen dieses Fenster jetzt schlie\u00dfen.',
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
#
# Each story: title + list of paragraphs.
# Inside a paragraph string, {{N}} marks blank number N.
# JavaScript will replace these with <input> elements.
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
            'Alex sighed and thought to himself: \u201cGreat. If I walk to the station in this weather, my suit {{3}} be completely ruined before the interview.\u201d',
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
    # Task 1 JSON: {"story_1":{"1":"when","2":"will",...}, "story_2":{...}, ...}
    task1_responses = models.LongStringField(blank=True, initial='{}')


# ═══════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════

def _ctx(player, progress):
    """Base template context."""
    lang = player.language
    return dict(lang=lang, ui=ui_dict(lang), progress=progress)


class Task1Intro(Page):
    def vars_for_template(self):
        lang = self.session.config.get('language', 'en')
        self.player.language = lang
        self.participant.language = lang
        return _ctx(self.player, 2)


class Task1Story1(Page):
    template_name = 'experiment/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def vars_for_template(self):
        return dict(
            story=STORIES[self.player.language][0],
            story_num=1, total=4,
            existing=self.player.task1_responses or '{}',
            **_ctx(self.player, 10),
        )


class Task1Story2(Page):
    template_name = 'experiment/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def vars_for_template(self):
        return dict(
            story=STORIES[self.player.language][1],
            story_num=2, total=4,
            existing=self.player.task1_responses or '{}',
            **_ctx(self.player, 28),
        )


class Task1Story3(Page):
    template_name = 'experiment/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def vars_for_template(self):
        return dict(
            story=STORIES[self.player.language][2],
            story_num=3, total=4,
            existing=self.player.task1_responses or '{}',
            **_ctx(self.player, 48),
        )


class Task1Story4(Page):
    template_name = 'experiment/Task1Story.html'
    form_model = 'player'
    form_fields = ['task1_responses']

    def vars_for_template(self):
        return dict(
            story=STORIES[self.player.language][3],
            story_num=4, total=4,
            existing=self.player.task1_responses or '{}',
            **_ctx(self.player, 68),
        )


class ThankYou(Page):
    def vars_for_template(self):
        return _ctx(self.player, 100)


page_sequence = [
    Task1Intro,
    Task1Story1,
    Task1Story2,
    Task1Story3,
    Task1Story4,
    ThankYou,
]
