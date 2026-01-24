from otree.api import *
import random
import csv

author = 'Lingguo Xu'
doc = """
Survey 1: demographics & participants experiences
"""

class Constants(BaseConstants):
    name_in_url = 'Survey'
    players_per_group = None
    num_rounds = 1
    nationalities = [
        ['Australian', 'Australian'],
        ['New Zealander', 'New Zealander'],
        ['Afghan', 'Afghan'],
        ['Albanian', 'Albanian'],
        ['Algerian', 'Algerian'],
        ['American', 'American'],
        ['Andorran', 'Andorran'],
        ['Angolan', 'Angolan'],
        ['Anguillan', 'Anguillan'],
        ['Argentine', 'Argentine'],
        ['Armenian', 'Armenian'],
        ['Austrian', 'Austrian'],
        ['Azerbaijani', 'Azerbaijani'],
        ['Bahamian', 'Bahamian'],
        ['Bahraini', 'Bahraini'],
        ['Bangladeshi', 'Bangladeshi'],
        ['Barbadian', 'Barbadian'],
        ['Belarusian', 'Belarusian'],
        ['Belgian', 'Belgian'],
        ['Belizean', 'Belizean'],
        ['Beninese', 'Beninese'],
        ['Bermudian', 'Bermudian'],
        ['Bhutanese', 'Bhutanese'],
        ['Bolivian', 'Bolivian'],
        ['Botswanan', 'Botswanan'],
        ['Brazilian', 'Brazilian'],
        ['British', 'British'],
        ['British Virgin Islander', 'British Virgin Islander'],
        ['Bruneian', 'Bruneian'],
        ['Bulgarian', 'Bulgarian'],
        ['Burkinan', 'Burkinan'],
        ['Burmese', 'Burmese'],
        ['Burundian', 'Burundian'],
        ['Cambodian', 'Cambodian'],
        ['Cameroonian', 'Cameroonian'],
        ['Canadian', 'Canadian'],
        ['Cape Verdean', 'Cape Verdean'],
        ['Cayman Islander', 'Cayman Islander'],
        ['Central African', 'Central African'],
        ['Chadian', 'Chadian'],
        ['Chilean', 'Chilean'],
        ['Chinese', 'Chinese'],
        ['Citizen of Antigua and Barbuda', 'Citizen of Antigua and Barbuda'],
        ['Citizen of Bosnia and Herzegovina', 'Citizen of Bosnia and Herzegovina'],
        ['Citizen of Guinea-Bissau', 'Citizen of Guinea-Bissau'],
        ['Citizen of Kiribati', 'Citizen of Kiribati'],
        ['Citizen of Seychelles', 'Citizen of Seychelles'],
        ['Citizen of the Dominican Republic', 'Citizen of the Dominican Republic'],
        ['Citizen of Vanuatu', 'Citizen of Vanuatu'],
        ['Colombian', 'Colombian'],
        ['Comoran', 'Comoran'],
        ['Congolese (Congo)', 'Congolese (Congo)'],
        ['Congolese (DRC)', 'Congolese (DRC)'],
        ['Cook Islander', 'Cook Islander'],
        ['Costa Rican', 'Costa Rican'],
        ['Croatian', 'Croatian'],
        ['Cuban', 'Cuban'],
        ['Cymraes', 'Cymraes'],
        ['Cymro', 'Cymro'],
        ['Cypriot', 'Cypriot'],
        ['Czech', 'Czech'],
        ['Danish', 'Danish'],
        ['Djiboutian', 'Djiboutian'],
        ['Dominican', 'Dominican'],
        ['Dutch', 'Dutch'],
        ['East Timorese', 'East Timorese'],
        ['Ecuadorean', 'Ecuadorean'],
        ['Egyptian', 'Egyptian'],
        ['Emirati', 'Emirati'],
        ['English', 'English'],
        ['Equatorial Guinean', 'Equatorial Guinean'],
        ['Eritrean', 'Eritrean'],
        ['Estonian', 'Estonian'],
        ['Ethiopian', 'Ethiopian'],
        ['Faroese', 'Faroese'],
        ['Fijian', 'Fijian'],
        ['Filipino', 'Filipino'],
        ['Finnish', 'Finnish'],
        ['French', 'French'],
        ['Gabonese', 'Gabonese'],
        ['Gambian', 'Gambian'],
        ['Georgian', 'Georgian'],
        ['German', 'German'],
        ['Ghanaian', 'Ghanaian'],
        ['Gibraltarian', 'Gibraltarian'],
        ['Greek', 'Greek'],
        ['Greenlandic', 'Greenlandic'],
        ['Grenadian', 'Grenadian'],
        ['Guamanian', 'Guamanian'],
        ['Guatemalan', 'Guatemalan'],
        ['Guinean', 'Guinean'],
        ['Guyanese', 'Guyanese'],
        ['Haitian', 'Haitian'],
        ['Honduran', 'Honduran'],
        ['Hong Konger', 'Hong Konger'],
        ['Hungarian', 'Hungarian'],
        ['Icelandic', 'Icelandic'],
        ['Indian', 'Indian'],
        ['Indonesian', 'Indonesian'],
        ['Iranian', 'Iranian'],
        ['Iraqi', 'Iraqi'],
        ['Irish', 'Irish'],
        ['Israeli', 'Israeli'],
        ['Italian', 'Italian'],
        ['Ivorian', 'Ivorian'],
        ['Jamaican', 'Jamaican'],
        ['Japanese', 'Japanese'],
        ['Jordanian', 'Jordanian'],
        ['Kazakh', 'Kazakh'],
        ['Kenyan', 'Kenyan'],
        ['Kittitian', 'Kittitian'],
        ['Kosovan', 'Kosovan'],
        ['Kuwaiti', 'Kuwaiti'],
        ['Kyrgyz', 'Kyrgyz'],
        ['Lao', 'Lao'],
        ['Latvian', 'Latvian'],
        ['Lebanese', 'Lebanese'],
        ['Liberian', 'Liberian'],
        ['Libyan', 'Libyan'],
        ['Liechtenstein citizen', 'Liechtenstein citizen'],
        ['Lithuanian', 'Lithuanian'],
        ['Luxembourger', 'Luxembourger'],
        ['Macanese', 'Macanese'],
        ['Macedonian', 'Macedonian'],
        ['Malagasy', 'Malagasy'],
        ['Malawian', 'Malawian'],
        ['Malaysian', 'Malaysian'],
        ['Maldivian', 'Maldivian'],
        ['Malian', 'Malian'],
        ['Maltese', 'Maltese'],
        ['Marshallese', 'Marshallese'],
        ['Martiniquais', 'Martiniquais'],
        ['Mauritanian', 'Mauritanian'],
        ['Mauritian', 'Mauritian'],
        ['Mexican', 'Mexican'],
        ['Micronesian', 'Micronesian'],
        ['Moldovan', 'Moldovan'],
        ['Monegasque', 'Monegasque'],
        ['Mongolian', 'Mongolian'],
        ['Montenegrin', 'Montenegrin'],
        ['Montserratian', 'Montserratian'],
        ['Moroccan', 'Moroccan'],
        ['Mosotho', 'Mosotho'],
        ['Mozambican', 'Mozambican'],
        ['Namibian', 'Namibian'],
        ['Nauruan', 'Nauruan'],
        ['Nepalese', 'Nepalese'],
        ['New Zealander', 'New Zealander'],
        ['Nicaraguan', 'Nicaraguan'],
        ['Nigerian', 'Nigerian'],
        ['Nigerien', 'Nigerien'],
        ['Niuean', 'Niuean'],
        ['North Korean', 'North Korean'],
        ['Northern Irish', 'Northern Irish'],
        ['Norwegian', 'Norwegian'],
        ['Omani', 'Omani'],
        ['Pakistani', 'Pakistani'],
        ['Palauan', 'Palauan'],
        ['Palestinian', 'Palestinian'],
        ['Panamanian', 'Panamanian'],
        ['Papua New Guinean', 'Papua New Guinean'],
        ['Paraguayan', 'Paraguayan'],
        ['Peruvian', 'Peruvian'],
        ['Pitcairn Islander', 'Pitcairn Islander'],
        ['Polish', 'Polish'],
        ['Portuguese', 'Portuguese'],
        ['Prydeinig', 'Prydeinig'],
        ['Puerto Rican', 'Puerto Rican'],
        ['Qatari', 'Qatari'],
        ['Romanian', 'Romanian'],
        ['Russian', 'Russian'],
        ['Rwandan', 'Rwandan'],
        ['Salvadorean', 'Salvadorean'],
        ['Sammarinese', 'Sammarinese'],
        ['Samoan', 'Samoan'],
        ['Sao Tomean', 'Sao Tomean'],
        ['Saudi Arabian', 'Saudi Arabian'],
        ['Scottish', 'Scottish'],
        ['Senegalese', 'Senegalese'],
        ['Serbian', 'Serbian'],
        ['Sierra Leonean', 'Sierra Leonean'],
        ['Singaporean', 'Singaporean'],
        ['Slovak', 'Slovak'],
        ['Slovenian', 'Slovenian'],
        ['Solomon Islander', 'Solomon Islander'],
        ['Somali', 'Somali'],
        ['South African', 'South African'],
        ['South Korean', 'South Korean'],
        ['South Sudanese', 'South Sudanese'],
        ['Spanish', 'Spanish'],
        ['Sri Lankan', 'Sri Lankan'],
        ['St Helenian', 'St Helenian'],
        ['St Lucian', 'St Lucian'],
        ['Stateless', 'Stateless'],
        ['Sudanese', 'Sudanese'],
        ['Surinamese', 'Surinamese'],
        ['Swazi', 'Swazi'],
        ['Swedish', 'Swedish'],
        ['Swiss', 'Swiss'],
        ['Syrian', 'Syrian'],
        ['Taiwanese', 'Taiwanese'],
        ['Tajik', 'Tajik'],
        ['Tanzanian', 'Tanzanian'],
        ['Thai', 'Thai'],
        ['Togolese', 'Togolese'],
        ['Tongan', 'Tongan'],
        ['Trinidadian', 'Trinidadian'],
        ['Tristanian', 'Tristanian'],
        ['Tunisian', 'Tunisian'],
        ['Turkish', 'Turkish'],
        ['Turkmen', 'Turkmen'],
        ['Turks and Caicos Islander', 'Turks and Caicos Islander'],
        ['Tuvaluan', 'Tuvaluan'],
        ['Ugandan', 'Ugandan'],
        ['Ukrainian', 'Ukrainian'],
        ['Uruguayan', 'Uruguayan'],
        ['Uzbek', 'Uzbek'],
        ['Vatican citizen', 'Vatican citizen'],
        ['Venezuelan', 'Venezuelan'],
        ['Vietnamese', 'Vietnamese'],
        ['Vincentian', 'Vincentian'],
        ['Wallisian', 'Wallisian'],
        ['Welsh', 'Welsh'],
        ['Yemeni', 'Yemeni'],
        ['Zambian', 'Zambian'],
        ['Zimbabwean', 'Zimbabwean'],
        ['OTHER', 'Other (please state below)'],
        ['NOTGIVEN', 'Prefer not to say'],
    ]
    nationality_list = nationalities.copy()
    countries = [
        ['AU', 'Australia'],
        ['NZ', 'New Zealand'],
        ['AF', 'Afghanistan'],
        ['AL', 'Albania'],
        ['DZ', 'Algeria'],
        ['AD', 'Andorra'],
        ['AO', 'Angola'],
        ['AG', 'Antigua and Barbuda'],
        ['AR', 'Argentina'],
        ['AM', 'Armenia'],
        ['AT', 'Austria'],
        ['AZ', 'Azerbaijan'],
        ['BS', 'Bahamas'],
        ['BH', 'Bahrain'],
        ['BD', 'Bangladesh'],
        ['BB', 'Barbados'],
        ['BY', 'Belarus'],
        ['BE', 'Belgium'],
        ['BZ', 'Belize'],
        ['BJ', 'Benin'],
        ['BT', 'Bhutan'],
        ['BO', 'Bolivia (Plurinational State of)'],
        ['BA', 'Bosnia and Herzegovina'],
        ['BW', 'Botswana'],
        ['BR', 'Brazil'],
        ['BN', 'Brunei Darussalam'],
        ['BG', 'Bulgaria'],
        ['BF', 'Burkina Faso'],
        ['BI', 'Burundi'],
        ['CV', 'Cabo Verde'],
        ['KH', 'Cambodia'],
        ['CM', 'Cameroon'],
        ['CA', 'Canada'],
        ['CF', 'Central African Republic'],
        ['TD', 'Chad'],
        ['CL', 'Chile'],
        ['CN', 'China'],
        ['CO', 'Colombia'],
        ['KM', 'Comoros'],
        ['CG', 'Congo'],
        ['CK', 'Cook Islands'],
        ['CR', 'Costa Rica'],
        ['HR', 'Croatia'],
        ['CU', 'Cuba'],
        ['CY', 'Cyprus'],
        ['CZ', 'Czechia'],
        ['CI', 'Côte d\'Ivoire'],
        ['KP', 'Democratic People\'s Republic of Korea'],
        ['CD', 'Democratic Republic of the Congo'],
        ['DK', 'Denmark'],
        ['DJ', 'Djibouti'],
        ['DM', 'Dominica'],
        ['DO', 'Dominican Republic'],
        ['EC', 'Ecuador'],
        ['EG', 'Egypt'],
        ['SV', 'El Salvador'],
        ['GB', 'United Kingdom of Great Britain and Northern Ireland'],
        ['GQ', 'Equatorial Guinea'],
        ['ER', 'Eritrea'],
        ['EE', 'Estonia'],
        ['SZ', 'Eswatini'],
        ['ET', 'Ethiopia'],
        ['FO', 'Faroe Islands'],
        ['FJ', 'Fiji'],
        ['FI', 'Finland'],
        ['FR', 'France'],
        ['GA', 'Gabon'],
        ['GM', 'Gambia'],
        ['GE', 'Georgia'],
        ['DE', 'Germany'],
        ['GH', 'Ghana'],
        ['GR', 'Greece'],
        ['GD', 'Grenada'],
        ['GT', 'Guatemala'],
        ['GN', 'Guinea'],
        ['GW', 'Guinea-Bissau'],
        ['GY', 'Guyana'],
        ['HT', 'Haiti'],
        ['HN', 'Honduras'],
        ['HU', 'Hungary'],
        ['IS', 'Iceland'],
        ['IN', 'India'],
        ['ID', 'Indonesia'],
        ['IR', 'Iran (Islamic Republic of)'],
        ['IQ', 'Iraq'],
        ['IE', 'Ireland'],
        ['IL', 'Israel'],
        ['IT', 'Italy'],
        ['JM', 'Jamaica'],
        ['JP', 'Japan'],
        ['JO', 'Jordan'],
        ['KZ', 'Kazakhstan'],
        ['KE', 'Kenya'],
        ['KI', 'Kiribati'],
        ['KW', 'Kuwait'],
        ['KG', 'Kyrgyzstan'],
        ['LA', 'Lao People\'s Democratic Republic'],
        ['LV', 'Latvia'],
        ['LB', 'Lebanon'],
        ['LS', 'Lesotho'],
        ['LR', 'Liberia'],
        ['LY', 'Libya'],
        ['LT', 'Lithuania'],
        ['LU', 'Luxembourg'],
        ['MG', 'Madagascar'],
        ['MW', 'Malawi'],
        ['MY', 'Malaysia'],
        ['MV', 'Maldives'],
        ['ML', 'Mali'],
        ['MT', 'Malta'],
        ['MH', 'Marshall Islands'],
        ['MR', 'Mauritania'],
        ['MU', 'Mauritius'],
        ['MX', 'Mexico'],
        ['FM', 'Micronesia (Federated States of)'],
        ['MC', 'Monaco'],
        ['MN', 'Mongolia'],
        ['ME', 'Montenegro'],
        ['MA', 'Morocco'],
        ['MZ', 'Mozambique'],
        ['MM', 'Myanmar'],
        ['NA', 'Namibia'],
        ['NR', 'Nauru'],
        ['NP', 'Nepal'],
        ['NL', 'Netherlands'],
        ['NI', 'Nicaragua'],
        ['NE', 'Niger'],
        ['NG', 'Nigeria'],
        ['NU', 'Niue'],
        ['MK', 'North Macedonia'],
        ['NO', 'Norway'],
        ['OM', 'Oman'],
        ['PK', 'Pakistan'],
        ['PW', 'Palau'],
        ['PA', 'Panama'],
        ['PG', 'Papua New Guinea'],
        ['PY', 'Paraguay'],
        ['PE', 'Peru'],
        ['PH', 'Philippines'],
        ['PL', 'Poland'],
        ['PT', 'Portugal'],
        ['QA', 'Qatar'],
        ['KR', 'Republic of Korea'],
        ['MD', 'Republic of Moldova'],
        ['RO', 'Romania'],
        ['RU', 'Russian Federation'],
        ['RW', 'Rwanda'],
        ['KN', 'Saint Kitts and Nevis'],
        ['LC', 'Saint Lucia'],
        ['VC', 'Saint Vincent and the Grenadines'],
        ['WS', 'Samoa'],
        ['SM', 'San Marino'],
        ['ST', 'Sao Tome and Principe'],
        ['SA', 'Saudi Arabia'],
        ['SN', 'Senegal'],
        ['RS', 'Serbia'],
        ['SC', 'Seychelles'],
        ['SL', 'Sierra Leone'],
        ['SG', 'Singapore'],
        ['SK', 'Slovakia'],
        ['SI', 'Slovenia'],
        ['SB', 'Solomon Islands'],
        ['SO', 'Somalia'],
        ['ZA', 'South Africa'],
        ['SS', 'South Sudan'],
        ['ES', 'Spain'],
        ['LK', 'Sri Lanka'],
        ['SD', 'Sudan'],
        ['SR', 'Suriname'],
        ['SE', 'Sweden'],
        ['CH', 'Switzerland'],
        ['SY', 'Syrian Arab Republic'],
        ['TJ', 'Tajikistan'],
        ['TH', 'Thailand'],
        ['TL', 'Timor-Leste'],
        ['TG', 'Togo'],
        ['TK', 'Tokelau'],
        ['TO', 'Tonga'],
        ['TT', 'Trinidad and Tobago'],
        ['TN', 'Tunisia'],
        ['TR', 'Turkey'],
        ['TM', 'Turkmenistan'],
        ['TV', 'Tuvalu'],
        ['UG', 'Uganda'],
        ['UA', 'Ukraine'],
        ['AE', 'United Arab Emirates'],
        ['TZ', 'United Republic of Tanzania'],
        ['US', 'United States of America'],
        ['UY', 'Uruguay'],
        ['UZ', 'Uzbekistan'],
        ['VU', 'Vanuatu'],
        ['VE', 'Venezuela (Bolivarian Republic of)'],
        ['VN', 'Viet Nam'],
        ['YE', 'Yemen'],
        ['ZM', 'Zambia'],
        ['ZW', 'Zimbabwe'],
        ['OTHER', 'Other (please state below)'],
        ['NOTGIVEN', 'Prefer not to say'],
    ]
    country_born_list = countries.copy()
    anti_payment = 25
    survey_payment_1 = 80
    survey_payment_2 = 50

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    #Demographic
    year_birth = models.IntegerField(
        label="What is your year of birth?",
        min=1900,
        max=2010,
        blank=True,
    )

    gender = models.IntegerField(
        label="What is your gender?",
        choices=[
            [0, 'Male'],
            [1, 'Female'],
            [2, 'Trans/Intersex/Other'],
            [3, 'Prefer not to say'],
        ]
    )

    major = models.StringField(
        label="What is your main field of study at the University?",
        choices=[
            'Agriculture',
            'Arts/ Social Sciences',
            'Biomedicine',
            'Commerce (non-Economics)',
            'Commerce (Economics)',
            'Dentistry/ Oral Health',
            'Education',
            'Engineering',
            'Environments',
            'Fine Arts',
            'Law',
            'Medicine',
            'Music',
            'Nursing',
            'Pharmacy',
            'Psychology',
            'Science',
            'Veterinary Science',
            'Other',
            'Not a student',
        ]
    )

    colleglevel = models.IntegerField(
        label="Are you an undergraduate or a graduate student?",
        choices = [
            [0, "Not a student"],
            [1, "1st-year undergraduate"],
            [2, "2nd-year undergraduate"],
            [3, "3rd-year undergraduate"],
            [4, "Master’s"],
            [5, "PhD"],
        ]
    )

    nationality = models.StringField(
        label="What is your nationality?",
        choices=Constants.nationality_list,
    )

    other_nationality = models.StringField(
        label='If you selected "Other", please specify in here.',
        blank=True,
    )

    country_born = models.StringField(
        label="In what country were you born?",
        choices=Constants.country_born_list
    )

    other_country_born = models.StringField(
        label='If you selected "Other", please specify in here.',
        blank=True,
    )

    yearsinau = models.IntegerField(
        label="How long have you lived in Australia?",
        choices=[
            [99, 'Born in Australia'],
            [4, 'More than 5 years'],
            [3, '2-5 years'],
            [2, '1-2 years'],
            [1, 'Less than 1 year'],
        ]
    )

    past_experiments = models.IntegerField(
        label="How many economics experiments have you participated in before this one?",
        min=0,
        max=999,
    )

    # decisions_clear = models.StringField(
    #     label = "",
    #     choices = [
    #         "Strongly Disagree",
    #         "Disagree",
    #         "Agree",
    #         "Strongly Agree"
    #     ],
    #     widget=widgets.RadioSelectHorizontal
    # )
    #
    # earnings_clear = models.StringField(
    #     label = "",
    #     choices = [
    #         "Strongly Disagree",
    #         "Disagree",
    #         "Agree",
    #         "Strongly Agree"
    #     ],
    #     widget=widgets.RadioSelectHorizontal
    # )
    #
    # comments_unclear = models.LongStringField(label = "", blank = True)

    # Explanation for choice of advance information
    advance_info_reason = models.LongStringField(label="")
    advance_info_wtp = models.LongStringField(label="")

    # Explanation for WTA of gold
    wta_reason = models.LongStringField(label="")
    wta_delay_reason = models.LongStringField(label="", blank = True)

    # Experience while waiting for mining to complete
    check_progress = models.LongStringField(label="")
    delay_rec = models.LongStringField(label="")

    waiting_exp_1 = models.LongStringField(label="")
    waiting_exp_2 = models.LongStringField(label="")

    waiting_anti_1 = models.IntegerField(
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label = "Please select a level of excitement"
    )
    waiting_anti_2 = models.IntegerField(
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label = "Please select a level of excitement"
    )
    waiting_boredom_1 = models.IntegerField(
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label = "Please select a level of boredom"
    )
    waiting_boredom_2 = models.IntegerField(
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label = "Please select a level of boredom"
    )

    # Survey on preference for anticipation
    def make_field():
        return models.IntegerField(
            choices=[[1, 'I disagree strongly'],
                     [2, 'I disagree '],
                     [3, 'I neither agree nor disagree'],
                     [4, 'I agree'],
                     [5, 'I strongly agree']],
            label="",
            widget=widgets.RadioSelect,
        )

    # anticipation_1 = make_field()
    # anticipation_2 = make_field()
    # anticipation_3 = make_field()
    # anticipation_4 = make_field()
    # anticipation_5 = make_field()
    # anticipation_6 = make_field()
    # anticipation_7 = make_field()
    # anticipation_8 = make_field()
    # anticipation_9 = make_field()
    # anticipation_10 = make_field()

    advance_info_uncertainty = make_field()
    advance_info_anticipation = make_field()

    check_progress_bored = make_field()
    check_progress_curious = make_field()
    check_progress_anticipation  = make_field()


# FUNCTIONS

# PAGES
class Introduction(Page):
    pass

# class General(Page):
#     form_model = 'player'
#     form_fields = ["decisions_clear", "earnings_clear", "comments_unclear"]

class Demographic(Page):
    form_model = 'player'
    form_fields = [
        'year_birth',
        'gender',
        'colleglevel',
        'major',
        'country_born',
        'other_country_born',
        'nationality',
        'other_nationality',
        'yearsinau',
        'past_experiments',
    ]

# class Anticipation_1(Page):
#     form_model = 'player'
#     form_fields = ['anticipation_1', 'anticipation_2', 'anticipation_3', 'anticipation_4', 'anticipation_5']
#
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         participant = player.participant
#
#         participant.finalpayoff_ECU = participant.finalpayoff_ECU + Constants.anti_payment
#
# class Anticipation_2(Page):
#     form_model = 'player'
#     form_fields = ['anticipation_6', 'anticipation_7', 'anticipation_8', 'anticipation_9', 'anticipation_10']
#
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         participant = player.participant
#         participant.finalpayoff_ECU = participant.finalpayoff_ECU + Constants.anti_payment

class advance_info_1(Page):
    form_model = 'player'
    form_fields = ['advance_info_reason', 'advance_info_wtp']

class advance_info_2(Page):
    form_model = 'player'
    form_fields = ['advance_info_uncertainty', 'advance_info_anticipation']

class check_progress_1(Page):
    form_model = 'player'
    form_fields = ['check_progress']

    def is_displayed(player):
        return player.participant.checkprogress != 0

class check_progress_2(Page):
    form_model = 'player'
    form_fields = ["check_progress_bored", "check_progress_curious", "check_progress_anticipation"]

    def is_displayed(player):
        return player.participant.checkprogress != 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        participant.finalpayoff_ECU = participant.finalpayoff_ECU + Constants.survey_payment_1

class waiting_exp_t1(Page):
    form_model = 'player'
    form_fields = ['waiting_exp_1']

class delay_reaction(Page):
    form_model = 'player'
    form_fields = ['delay_rec']

    def is_displayed(player):
        return player.participant.treatment == 2

class waiting_exp_t2(Page):
    form_model = 'player'
    form_fields = ['waiting_exp_2']

    def is_displayed(player):
        return player.participant.treatment == 2

class waiting_anti_t1(Page):
    form_model = 'player'
    form_fields = ['waiting_anti_1']

    def is_displayed(player):
        return player.participant.treatment == 1

class waiting_anti_t2(Page):
    form_model = 'player'
    form_fields = ['waiting_anti_1', 'waiting_anti_2']

    def is_displayed(player):
        return player.participant.treatment == 2

class waiting_bord_t1(Page):
    form_model = 'player'
    form_fields = ['waiting_boredom_1']

    def is_displayed(player):
        return player.participant.treatment == 1

class waiting_bord_t2(Page):
    form_model = 'player'
    form_fields = ['waiting_boredom_1', 'waiting_boredom_2']

    def is_displayed(player):
        return player.participant.treatment == 2

class wta_reason(Page):
    form_model = 'player'
    form_fields = ['wta_reason', 'wta_delay_reason']

    def is_displayed(player):
        return player.participant.found_gold == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.finalpayoff_ECU = participant.finalpayoff_ECU + Constants.survey_payment_2

# class Results(Page):
#     @staticmethod
#     def js_vars(player):
#         return dict(
#             finalpayoff = player.finalpayoff,
#         )

# page_sequence = [advance_info, reason_wta, anticipation, PayID]

# page_sequence = [Introduction, advance_info, anticipation_1, anticipation_2, PayID, Results, DropoutPage, FinalPage]

# page_sequence = [Introduction, advance_info, reason_wta, anticipation_1, anticipation_2, PayID, waiting_exp_t1,
#                  waiting_exp_t2, waiting_anti_t1, waiting_anti_t2, Results, DropoutPage, FinalPage]

page_sequence = [Introduction, Demographic,
                 advance_info_1, advance_info_2, check_progress_1, check_progress_2,
                 waiting_exp_t1, delay_reaction, waiting_exp_t2, waiting_bord_t1, waiting_bord_t2, waiting_anti_t1, waiting_anti_t2,
                 wta_reason]
# page_sequence = [Part1_4_Survey_Difficulty]

