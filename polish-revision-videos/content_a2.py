"""Lesson script for the Polish A2 revision video (see lesson.py for markup)."""
# pylint: disable=too-many-lines,line-too-long

from lesson import (
    Scene,
    big,
    card,
    drill,
    en,
    gap,
    grid,
    head,
    lst,
    note,
    ns,
    nt,
    pair,
    pl,
    quiz,
    rule,
    say,
    step,
)

META = {'title': 'Polish A2', 'slug': 'polish_a2'}

W3 = [0.2, 0.42, 0.38]  # pronoun | masculine | feminine tables
W4 = [0.31, 0.23, 0.23, 0.23]  # case | m | f | n
W7 = [0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]  # verb | 6 persons
W8 = [0.16, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12]  # case | 7 pronouns
WIDE = [0.6, 0.4]  # long Polish sentence | meaning
OP = [0.3, 0.16, 0.54]  # plural case | ending | examples


def mf(pron, masc, fem):
    """Pronoun | masculine form | feminine form, equal weight."""
    return grid([pron, masc, fem], size=30, w=W3, h=56)


def two_line_cards(scenes):
    """Use the two-line card layout on any slide with a long card."""
    for scene in scenes:
        for stp in scene.steps:
            cards = [r for r in stp.rows if r['k'] == 'card']
            long_text = any(
                len(r['c'][0]) > 22 or len(r['c'][1]) > 26 or len(r['c'][2]) > 32
                for r in cards
            )
            if long_text:
                for row in cards:
                    row['k'], row['w'] = 'card2', None


# ===================================================================== SCENES
COVER = Scene(
    'Polish A2',
    'Full revision',
    'a',
    cover=True,
    steps=[
        step(
            [
                big('Polish A2', 112, 'a', 150),
                big('Full Revision', 62, None, 90),
                big('Every A2 grammar topic  ·  real-life Polish', 29, None, 56),
                big(
                    'for English speakers  ·  32 chapters to jump between', 25, None, 50
                ),
            ],
            pl('Cześć! Witaj z powrotem!'),
            en(
                'Welcome to your Polish A two revision. This one is longer than '
                'the A one video, because A two is where Polish grammar really '
                'opens up: aspect, all seven cases, the plural, motion verbs, the '
                'imperative and the conditional. Use the chapters to jump around, '
                'pause often, and say everything out loud.'
            ),
        ),
        step(
            [
                head('THE MAP'),
                lst(
                    '1  Sounds+',
                    '2  Seven cases',
                    '3  Dative',
                    '4  Plural',
                    '5  Gen. plural',
                ),
                lst(
                    '6  More plurals',
                    '7  Pronouns',
                    '8  Verb + case',
                    '9  Tricky verbs',
                    '10  Aspect',
                ),
                lst(
                    '11  Past tense',
                    '12  Future',
                    '13  Motion',
                    '14  Imperative',
                    '15  Conditional',
                ),
                lst(
                    '16  Comparing',
                    '17  Must, should',
                    '18  Linking',
                    '19  Some / no-',
                    '20  Dates & time',
                ),
                lst(
                    '21  Time, weather',
                    '22  Doctor',
                    '23  Travel',
                    '24  Work, phone',
                    '25  Shopping',
                ),
                lst(
                    '26  Restaurant',
                    '27  Free time',
                    '28  Wishes',
                    '29  Story',
                    '30  Role-plays',
                ),
                lst('31  Quiz', '32  Recap & B1', '', '', ''),
            ],
            en(
                'Here is the map: thirty two chapters. Grammar first, then '
                'real-life topics, a story to listen to, two role-plays and a '
                'fourteen question quiz. Grab a pen, or better, just speak.'
            ),
            clear=True,
        ),
    ],
)

SOUNDS = Scene(
    'Pronunciation level-up',
    'What happens when sounds meet',
    'n',
    steps=[
        step(
            [
                head('AT THE END OF A WORD, VOICED → VOICELESS', w=[1]),
                card('chleb', 'hlep', 'bread: b sounds like p'),
                card('róg', 'rook', 'corner: g sounds like k'),
                card('Kraków', 'KRAH-koof', 'w at the end sounds like f'),
                card('obiad', 'OH-byaht', 'lunch: d sounds like t'),
            ],
            en(
                'At A one you learned the letters. At A two you learn what '
                'happens when sounds meet. Rule one: at the end of a word, voiced '
                'consonants lose their voice. B becomes p, g becomes k, w becomes '
                'f, d becomes t.'
            ),
            pl('chleb.'),
            pl('róg.'),
            pl('Kraków.'),
            pl('obiad.'),
        ),
        step(
            [
                head('NEIGHBOURS COPY EACH OTHER', w=[1]),
                card('wtorek', 'FTOH-rek', 'Tuesday: w before t → f'),
                card('wszystko', 'FSHIST-koh', 'everything: w before sz → f'),
                card('twój', 'tfooy', 'your: w after t → f'),
                card('przepraszam', 'psheh-PRAH-shahm', 'rz after p, t, k → sh'),
                card('trzy  ·  krzesło', 'tshih  ·  KSHEH-swoh', 'three  ·  chair'),
            ],
            en(
                'Rule two: consonants copy their neighbours. W next to a voiceless '
                'sound becomes f:'
            ),
            pl('wtorek, wszystko, twój.'),
            en('And r z after p, t or k is pronounced sh:'),
            pl('przepraszam, trzy, krzesło.'),
            clear=True,
        ),
        step(
            [
                head('NASAL VOWELS DEPEND ON THE NEXT SOUND', w=[1]),
                card(
                    'zęby  ·  kąpać', 'ZEM-bih  ·  KOM-pahch', 'before b / p → em / om'
                ),
                card(
                    'będę  ·  mądry', 'BEN-deh  ·  MON-drih', 'before t / d → en / on'
                ),
                card('ręka', 'RENG-kah', 'before k / g → eng'),
                card(
                    'wziął  ·  wzięła', 'vzhow  ·  VZHEH-wah', 'before ł / l → no nasal'
                ),
                card('idę  ·  są', 'EE-deh  ·  sohm', 'at the end: ę → eh, ą → om'),
            ],
            en(
                'Rule three: nasal vowels change shape. Before b or p they become em and om:'
            ),
            pl('zęby, kąpać.'),
            en('Before t or d, en and on:'),
            pl('będę, mądry.'),
            en('Before k, eng:'),
            pl('ręka.'),
            en('Before l, the nasal disappears completely:'),
            pl('wziął, wzięła.'),
            en('And at the end of a word, e with a tail is just eh:'),
            pl('idę.'),
            clear=True,
        ),
        step(
            [
                head('STRESS EXCEPTIONS', w=[1]),
                pair(
                    '{BY}-li-śmy  ·  {BY}-li-ście', 'past -śmy / -ście: third from last'
                ),
                pair(
                    '{MU}-zy-ka  ·  ma-te-{MA}-ty-ka',
                    'Greek and Latin -yka / -ika words',
                ),
                pair(
                    'chcia-{ŁA}-bym  ·  zro-{BI}-li-by-śmy',
                    'conditional: just before -by',
                ),
                note(
                    'These are the textbook rules. Many Poles use normal stress in '
                    'casual speech, and both are understood.'
                ),
            ],
            en(
                'Last, three stress exceptions. Past forms like [[byliśmy]] and '
                '[[byliście]] stress the third syllable from the end. Words like '
                '[[muzyka]] and [[matematyka]] do the same. And in the conditional '
                'the stress sits just before [[by]]: [[chciałabym]]. Many Poles '
                'simplify these in casual speech, so do not panic.'
            ),
            clear=True,
        ),
    ],
)

CASE_MAP = Scene(
    'All seven cases',
    'One noun per gender, every ending',
    'r',
    steps=[
        step(
            [
                head('', '{m|MASCULINE}', '{f|FEMININE}', '{n|NEUTER}', al='c', w=W4),
                grid(
                    ['Nominative · kto? co?', 'brat', 'kawa', 'okno'],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    ['Genitive · kogo? czego?', 'brat{a}', 'kaw{y}', 'okn{a}'],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    ['Dative · komu? czemu?', 'brat{u}', 'kaw{ie}', 'okn{u}'],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    ['Accusative · kogo? co?', 'brat{a}', 'kaw{ę}', 'okno'],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    ['Instrumental · kim? czym?', 'brat{em}', 'kaw{ą}', 'okn{em}'],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    [
                        'Locative · o kim? o czym?',
                        'o bra{cie}',
                        'o kaw{ie}',
                        'o okn{ie}',
                    ],
                    size=26,
                    w=W4,
                    h=56,
                ),
                grid(
                    ['Vocative · calling', 'bra{cie}!', 'kaw{o}!', 'okno!'],
                    size=26,
                    w=W4,
                    h=56,
                ),
            ],
            en(
                'Here is the full map of the seven cases in the singular, with one '
                'noun per gender: [[brat]], brother; [[kawa]], coffee; and '
                '[[okno]], window. Listen to brother go through all seven:'
            ),
            pl('brat, brata, bratu, brata, bratem, o bracie, bracie!'),
            en('Coffee:'),
            pl('kawa, kawy, kawie, kawę, kawą, o kawie, kawo!'),
            en('And window:'),
            pl('okno, okna, oknu, okno, oknem, o oknie.'),
            en(
                'Notice two shortcuts. Masculine people use the genitive form as '
                'their accusative. And for feminine nouns, the dative and the '
                'locative are identical.'
            ),
        ),
        step(
            [
                head('THE SOFTENING RULE before -e / -ie', 'CHANGE', 'EXAMPLE'),
                rule('siostra → sios{trze}', 'r → rz', 'o siostrze', 'f'),
                rule('woda → wo{dzie}', 'd → dzi', 'w wodzie', 'f'),
                rule('kobieta → kobie{cie}', 't → ci', 'o kobiecie', 'f'),
                rule('Polska → Pols{ce}', 'k → c', 'w Polsce', 'f'),
                rule('noga → no{dze}', 'g → dz', 'na nodze', 'f'),
                rule('stół → sto{le}', 'ł → l', 'na stole', 'm'),
            ],
            en(
                'The ending e or i e softens the consonant in front of it. This '
                'happens in the feminine dative and locative, and in the masculine '
                'and neuter locative.'
            ),
            say('o siostrze', 'about my sister'),
            say('w wodzie', 'in the water'),
            say('o kobiecie', 'about the woman'),
            say('w Polsce', 'in Poland'),
            say('na nodze', 'on the leg'),
            say('na stole', 'on the table'),
            en('Learn these six pairs and you can predict the rest.'),
            clear=True,
        ),
        step(
            [
                head('VOCATIVE IN REAL LIFE: calling or writing to someone', w=[1]),
                card(
                    'Panie Piotrze!',
                    'PAH-nyeh PYOHT-sheh',
                    'Piotr → Piotrze (Mr Piotr)',
                ),
                card('Pani Anno!', 'PAH-nee AHN-noh', 'Anna → Anno'),
                card(
                    'Kasiu!  ·  Tomku!',
                    'KAH-shoo  ·  TOM-koo',
                    'Kasia → Kasiu  ·  Tomek → Tomku',
                ),
                card('Panie doktorze!', 'PAH-nyeh dok-TOH-zheh', 'doktor → doktorze'),
                card(
                    'Cześć, Marku!',
                    'cheshch MAR-koo',
                    'Marek → Marku',
                ),
            ],
            en(
                'The vocative is used whenever you address someone, in speech and '
                'in emails. Notice that [[pan]] becomes [[panie]].'
            ),
            say('Panie Piotrze!', 'Mr Piotr!'),
            pl('Pani Anno! Kasiu! Tomku! Panie doktorze! Cześć, Marku!'),
            clear=True,
        ),
    ],
)

DATIVE = Scene(
    'The dative',
    'To whom? Giving, helping, thanking, liking',
    'm',
    steps=[
        step(
            [
                head('RULE', 'EXAMPLE', 'MEANING'),
                rule(
                    'student → student{owi}',
                    'Pomagam studentowi.',
                    'I help the student.',
                    'm',
                ),
                rule('Tomek → Tomk{owi}', 'Dziękuję Tomkowi.', 'I thank Tomek.', 'm'),
                rule(
                    'brat · pan · ojciec',
                    'brat{u} · pan{u} · ojc{u}',
                    'short irregulars: -u',
                    'm',
                ),
                rule(
                    'mama → ma{mie}', 'Daję mamie kwiaty.', 'I give Mum flowers.', 'f'
                ),
                rule(
                    'dziecko → dzieck{u}',
                    'Kupię dziecku zabawkę.',
                    'I will buy the child a toy.',
                    'n',
                ),
            ],
            en(
                'The dative answers to whom, or for whom. Masculine nouns usually add [[owi]]:'
            ),
            say('Pomagam studentowi.', 'I help the student.'),
            say('Dziękuję Tomkowi.', 'I thank Tomek.'),
            en('A few short masculine words take just u:'),
            pl('bratu, panu, ojcu.'),
            en('The feminine dative looks exactly like the feminine locative:'),
            say('Daję mamie kwiaty.', 'I give Mum flowers.'),
            en('And neuter nouns add u:'),
            say('Kupię dziecku zabawkę.', 'I will buy the child a toy.'),
        ),
        step(
            [
                head('ja', 'ty', 'on', 'ona', 'my', 'wy', 'oni', al='c'),
                grid(
                    ['mi', 'ci', 'mu', 'jej', 'nam', 'wam', 'im'],
                    p=['mee', 'chee', 'moo', 'yey', 'nahm', 'vahm', 'eem'],
                    e=[
                        'to me',
                        'to you',
                        'to him',
                        'to her',
                        'to us',
                        'to you (pl)',
                        'to them',
                    ],
                    size=32,
                    h=110,
                ),
                card('Daj mi chwilę.', 'dai mee HVEE-leh', 'Give me a moment.'),
                card(
                    'Powiem ci coś.',
                    'POH-vyem chee tsosh',
                    'I will tell you something.',
                ),
                note(
                    'Long forms for emphasis or after prepositions: {mnie, tobie, '
                    'jemu}. Dzięki {tobie}! = Thanks to you!'
                ),
            ],
            en('Dative pronouns are short and everywhere:'),
            pl('mi, ci, mu, jej, nam, wam, im.'),
            en('To me, to you, to him, to her, to us, to you plural, to them.'),
            say('Daj mi chwilę.', 'Give me a moment.'),
            say('Powiem ci coś.', 'I will tell you something.'),
            en('For emphasis you use the long forms: [[Dzięki tobie!]] Thanks to you!'),
            clear=True,
        ),
        step(
            [
                head('VERBS THAT TAKE THE DATIVE', w=[1]),
                pair('Podoba {mi} się Gdańsk.', 'I like Gdańsk. (It pleases me.)'),
                pair('Smakuje {ci} zupa?', 'Do you like the soup? (taste)'),
                pair('Pomagam {koledze}.', 'I help my colleague.'),
                pair('Dziękuję {pani} za pomoc.', 'Thank you (madam) for your help.'),
                pair('Wierzę {ci}.', 'I believe you.'),
                pair('Przeszkadza {ci} muzyka?', 'Does the music bother you?'),
            ],
            en(
                'Some verbs always take the dative. [[Podobać się]] means to '
                'please, so the person who likes something is in the dative:'
            ),
            say('Podoba mi się Gdańsk.', 'I like [[Gdańsk]].'),
            en('[[Smakować]] works the same way for food:'),
            say('Smakuje ci zupa?', 'Do you like the soup?'),
            en(
                'Also [[pomagać]], to help, [[dziękować]], to thank, [[wierzyć]], '
                'to believe, and [[przeszkadzać]], to bother.'
            ),
            pl(
                'Pomagam koledze. Dziękuję pani za pomoc. Wierzę ci. Przeszkadza ci muzyka?'
            ),
            clear=True,
        ),
        step(
            [
                head('HOW YOU FEEL = dative + adverb', w=[1]),
                card('Jest mi zimno.', 'yest mee ZHEEM-noh', 'I am cold.'),
                card('Jest mi gorąco.', 'yest mee goh-RON-tsoh', 'I am hot.'),
                card('Smutno mi.', 'SMOOT-noh mee', 'I feel sad.'),
                card(
                    'Chce mi się pić.',
                    'htseh mee sheh peech',
                    'I am thirsty.',
                ),
                card(
                    'Wydaje mi się, że…',
                    'vih-DAH-yeh mee sheh zheh',
                    'It seems to me that…',
                ),
            ],
            en(
                'One of the most Polish things in Polish: you do not say I am '
                'cold, you say it is cold to me.'
            ),
            drill('Jest mi zimno.'),
            say('Jest mi gorąco.', 'I am hot.'),
            say('Smutno mi.', 'I feel sad.'),
            say('Chce mi się pić.', 'I feel like a drink.'),
            say('Wydaje mi się, że…', 'It seems to me that.'),
            clear=True,
        ),
    ],
)

PLURAL = Scene(
    'Plural: men vs the rest',
    'The virile split',
    'f',
    steps=[
        step(
            [
                note(
                    'Polish plural has two genders. {m|Virile} = groups with at least '
                    'one man. {f|Non-virile} = everything else: women, children, '
                    'animals, things.'
                ),
                pair(
                    '{m|oni} są  ·  {m|ci} studenci  ·  {m|byli}',
                    'men or mixed groups',
                    'm',
                ),
                pair(
                    '{f|one} są  ·  {f|te} studentki  ·  {f|były}',
                    'women, animals, things',
                    'f',
                ),
            ],
            en(
                'In the plural, Polish asks one question: is there a man in the '
                'group? Groups with at least one man are called virile. Everything '
                'else, women, children, animals and things, is non-virile. It '
                'changes the pronoun, the adjective, the verb, and the noun itself.'
            ),
            pl('Oni są. One są.'),
        ),
        step(
            [
                head('NON-VIRILE PLURAL', 'RULE'),
                pair('dom → dom{y}  ·  kot → kot{y}', '-y after hard consonants', 'f'),
                pair('książka → książk{i}  ·  noga → nog{i}', '-i after k and g', 'f'),
                pair(
                    'ulica → ulic{e}  ·  pokój → pokoj{e}',
                    '-e after soft consonants',
                    'f',
                ),
                pair('okno → okn{a}  ·  morze → morz{a}', 'neuter: -a', 'f'),
                pair('dziecko → {dzieci}  ·  oko → {oczy}', 'irregular', 'f'),
            ],
            en('Non-virile first. Hard consonants take y:'),
            pl('domy, koty.'),
            en('K and g take i:'),
            pl('książki, nogi.'),
            en('Soft consonants take e:'),
            pl('ulice, pokoje.'),
            en('Neuter nouns take a:'),
            pl('okna, morza.'),
            en('And two irregulars:'),
            pl('dzieci, oczy.'),
            clear=True,
        ),
        step(
            [
                head('VIRILE PLURAL (male persons)', 'RULE'),
                pair('student → studen{ci}', 't → ci', 'm'),
                pair('Polak → Pola{cy}', 'k → cy', 'm'),
                pair('kolega → kole{dzy}', 'g → dzy', 'm'),
                pair('lekarz → lekarz{e}', 'soft consonant: -e', 'm'),
                pair(
                    'pan → pan{owie}  ·  syn → syn{owie}', 'titles & family: -owie', 'm'
                ),
                pair('człowiek → {ludzie}  ·  brat → {bracia}', 'irregular', 'm'),
            ],
            en('Virile nouns soften their last consonant, just like the locative did:'),
            say('studenci', 'students'),
            say('Polacy', 'Poles'),
            say('koledzy', 'colleagues'),
            say('lekarze', 'doctors'),
            en('Titles and family members often take [[owie]]:'),
            pl('panowie, synowie.'),
            en('And the irregular classics:'),
            pl('ludzie, bracia.'),
            clear=True,
        ),
        step(
            [
                head('', '{m|VIRILE}', '{f|NON-VIRILE}', al='c', w=[0.24, 0.38, 0.38]),
                grid(
                    ['dobry', 'dobrzy koledzy', 'dobre koleżanki'],
                    size=28,
                    w=[0.24, 0.38, 0.38],
                    h=58,
                ),
                grid(
                    ['nowy', 'nowi studenci', 'nowe książki'],
                    size=28,
                    w=[0.24, 0.38, 0.38],
                    h=58,
                ),
                grid(
                    ['polski', 'polscy lekarze', 'polskie miasta'],
                    size=28,
                    w=[0.24, 0.38, 0.38],
                    h=58,
                ),
                grid(
                    ['wysoki', 'wysocy chłopcy', 'wysokie drzewa'],
                    size=28,
                    w=[0.24, 0.38, 0.38],
                    h=58,
                ),
                grid(
                    ['młody', 'młodzi ludzie', 'młode dzieci'],
                    size=28,
                    w=[0.24, 0.38, 0.38],
                    h=58,
                ),
                note(
                    'These: {m|ci} panowie / {f|te} panie.  Past tense: {m|byli} / {f|były}.'
                ),
            ],
            en('Adjectives soften in the virile plural too:'),
            pl(
                'dobrzy koledzy, nowi studenci, polscy lekarze, wysocy chłopcy, młodzi ludzie.'
            ),
            en('Compare the non-virile forms:'),
            pl('dobre koleżanki, nowe książki, polskie miasta.'),
            en(
                'And this word: [[ci panowie]], these gentlemen, but [[te panie]], these ladies.'
            ),
            clear=True,
        ),
    ],
)

GEN_PLURAL = Scene(
    'Genitive plural & counting',
    'The plural you will use most',
    'a',
    steps=[
        step(
            [
                head('ENDING', 'EXAMPLES'),
                pair('masculine: {-ów}', 'dom{ów} · student{ów} · samochod{ów}', 'm'),
                pair(
                    'soft masculine: {-i / -y}',
                    'nauczycie{li} · goś{ci} · pienię{dzy}',
                    'm',
                ),
                pair(
                    'feminine & neuter: {no ending}',
                    'kobiet · godzin · miast · minut',
                    'f',
                ),
                pair('…plus a helper vowel', 'książ{e}k · ok{ie}n · jabł{e}k', 'f'),
                pair('…or o → ó', 'si{ó}str · szk{ó}ł · os{ó}b', 'f'),
                pair('irregular', 'ludzi · dzieci · przyjaciół · lat', 'r'),
            ],
            en(
                'The genitive plural is the plural you will use most, because '
                'every number from five up needs it. Masculine nouns add [[ów]]:'
            ),
            pl('domów, studentów, samochodów.'),
            en('Soft masculine nouns take i or y:'),
            pl('nauczycieli, gości, pieniędzy.'),
            en('Feminine and neuter nouns simply drop their ending:'),
            pl('kobiet, godzin, miast, minut.'),
            en(
                'If that leaves an awkward cluster, Polish slips in an e, or turns o into o with an accent:'
            ),
            pl('książek, okien, jabłek. Sióstr, szkół, osób.'),
            en('And the irregulars:'),
            pl('ludzi, dzieci, przyjaciół, lat.'),
        ),
        step(
            [
                head('HOW MANY?', 'NOUN FORM', 'EXAMPLE'),
                rule('1', 'nominative singular', 'jeden dom · jedna książka'),
                rule(
                    '2–4 · 22–24 · 32–34…',
                    'nominative plural',
                    'dwa domy · trzy książki',
                ),
                rule(
                    '5–21 · 25–31…', 'genitive plural', 'pięć domów · dwanaście książek'
                ),
                rule(
                    'dużo · mało · kilka · ile',
                    'genitive plural',
                    'dużo ludzi · kilka minut',
                ),
                note(
                    'With 5+ the verb goes singular neuter: {Pięć osób przyszło.} Five people came.'
                ),
            ],
            en(
                'Now the counting rule in full. One takes the singular. Two, three '
                'and four, and bigger numbers ending in them, except twelve to '
                'fourteen, take the nominative plural:'
            ),
            pl('dwa domy, trzy książki, dwadzieścia dwa domy.'),
            en('Five and up, and all the teens, take the genitive plural:'),
            pl('pięć domów, dwanaście książek.'),
            en('So do quantity words like [[dużo, mało, kilka]] and [[ile]]:'),
            pl('dużo ludzi, kilka minut.'),
            en(
                'And a detail that impresses teachers: with five or more, the verb goes singular neuter.'
            ),
            say('Pięć osób przyszło.', 'Five people came.'),
            clear=True,
        ),
        step(
            [
                head('COUNTING MEN', w=[1]),
                card(
                    'Mam dwóch braci.', 'mahm dvookh BRAH-chee', 'I have two brothers.'
                ),
                card('trzech kolegów', 'tshekh koh-LEH-goof', 'three colleagues'),
                card('pięciu studentów', 'PYEN-choo stoo-DEN-toof', 'five students'),
                note(
                    'Groups of men use special numbers + genitive: {dwóch, trzech, '
                    'czterech, pięciu}…  Przyszło {pięciu studentów}.'
                ),
            ],
            en(
                'Groups of men even get their own numbers, followed by the genitive plural:'
            ),
            say('Mam dwóch braci.', 'I have two brothers.'),
            say('trzech kolegów', 'three colleagues'),
            say('pięciu studentów', 'five students'),
            en('You will hear these all the time, so learn to recognise them first.'),
            clear=True,
        ),
    ],
)

MORE_PLURALS = Scene(
    'The other plural cases',
    'Good news: -om, -ami, -ach for every gender',
    'n',
    steps=[
        step(
            [
                head('CASE', 'ENDING', 'EXAMPLE', w=OP),
                rule('Dative', '-om', 'studentom · dzieciom · rodzicom', w=OP),
                rule('Instrumental', '-ami', 'z kolegami · z koleżankami', w=OP),
                rule('Locative', '-ach', 'w sklepach · w górach · o dzieciach', w=OP),
                rule(
                    'a few instrumentals',
                    '-mi',
                    'z dziećmi · z ludźmi · z przyjaciółmi',
                    w=OP,
                ),
                note(
                    'Accusative plural = nominative plural, except for men, who use '
                    'the genitive: {Widzę studentów} but {Widzę studentki}.'
                ),
            ],
            en(
                'Some relief now. Three plural cases have one ending for every '
                'gender. Dative, [[om]]:'
            ),
            pl('studentom, dzieciom, rodzicom.'),
            en('Instrumental, [[ami]]:'),
            pl('z kolegami, z koleżankami.'),
            en('Locative, [[ach]]:'),
            pl('w sklepach, w górach, o dzieciach.'),
            en('A few instrumentals take just [[mi]]:'),
            pl('z dziećmi, z ludźmi, z przyjaciółmi.'),
            en(
                'And the accusative plural copies the nominative, except for men, '
                'who copy the genitive:'
            ),
            say('Widzę studentów.', 'I see the students, men.'),
            say('Widzę studentki.', 'I see the students, women.'),
        ),
        step(
            [
                head('ADJECTIVES IN THE PLURAL', 'ENDING', 'EXAMPLE'),
                rule('Genitive / Locative', 'nowych · polskich', 'w nowych sklepach'),
                rule('Dative', 'nowym · polskim', 'nowym studentom'),
                rule('Instrumental', 'nowymi · polskimi', 'z nowymi kolegami'),
                rule('Nominative', 'nowi / nowe', 'nowi koledzy · nowe koleżanki'),
                card(
                    'Rozmawiam z polskimi przyjaciółmi.',
                    'roz-MAH-vyahm s pol-SKEE-mee pshih-yah-CHOOW-mee',
                    'I talk with Polish friends.',
                    w=[0.4, 0.36, 0.24],
                ),
            ],
            en(
                'Adjectives have their own plural set: [[ych]] or [[ich]] for '
                'genitive and locative, [[ym]] for dative, and [[ymi]] for '
                'instrumental.'
            ),
            pl('w nowych sklepach, nowym studentom, z nowymi kolegami.'),
            say('Rozmawiam z polskimi przyjaciółmi.', 'I talk with Polish friends.'),
            clear=True,
        ),
    ],
)

PRONOUNS = Scene(
    'Pronouns in every case',
    'Short forms by default, long forms for emphasis',
    'm',
    steps=[
        step(
            [
                head('', 'ja', 'ty', 'on', 'ona', 'my', 'wy', 'oni', al='c', w=W8),
                grid(
                    [
                        'Genitive',
                        'mnie',
                        'cię / ciebie',
                        'go / jego',
                        'jej',
                        'nas',
                        'was',
                        'ich',
                    ],
                    size=24,
                    w=W8,
                    h=56,
                ),
                grid(
                    [
                        'Dative',
                        'mi / mnie',
                        'ci / tobie',
                        'mu / jemu',
                        'jej',
                        'nam',
                        'wam',
                        'im',
                    ],
                    size=24,
                    w=W8,
                    h=56,
                ),
                grid(
                    [
                        'Accusative',
                        'mnie',
                        'cię / ciebie',
                        'go / jego',
                        'ją',
                        'nas',
                        'was',
                        'ich / je',
                    ],
                    size=24,
                    w=W8,
                    h=56,
                ),
                grid(
                    [
                        'Instrumental',
                        'mną',
                        'tobą',
                        'nim',
                        'nią',
                        'nami',
                        'wami',
                        'nimi',
                    ],
                    size=24,
                    w=W8,
                    h=56,
                ),
                grid(
                    ['Locative', 'mnie', 'tobie', 'nim', 'niej', 'nas', 'was', 'nich'],
                    size=24,
                    w=W8,
                    h=56,
                ),
                note(
                    'After a preposition, he / she / they start with {n}: do '
                    '{niego}, u {niej}, z {nimi}, dla {nich}.  With me: {ze mną}.'
                ),
            ],
            en(
                'Here is every personal pronoun in every case. You know many of '
                'them already. The short forms, like [[mi, ci, go, mu]], are the '
                'default. The long forms, like [[mnie, tobie, jego]], are for '
                'emphasis and after prepositions. One more rule: after a '
                'preposition, he, she and they gain an n.'
            ),
            say('Idę do niego.', 'I am going to his place.'),
            say('Byłam u niej.', 'I was at her place.'),
            say('Rozmawiam z nimi.', 'I am talking with them.'),
            say('Idziesz ze mną?', 'Are you coming with me?'),
        ),
        step(
            [
                head('SWÓJ = my / your / his own: points back to the subject', w=[1]),
                pair('Mam {swój} pokój.', 'I have my own room.', w=WIDE),
                pair(
                    'Piotr kocha {swoją} żonę.', 'Piotr loves his (own) wife.', w=WIDE
                ),
                pair('Piotr kocha {r|jego} żonę.', '…another man’s wife!', w=WIDE),
                head('SIEBIE / SOBIE = oneself', w=[1]),
                pair(
                    'Myślę o {sobie}.  ·  Kupiłem {sobie} rower.',
                    'about myself · bought myself a bike',
                    w=WIDE,
                ),
            ],
            en(
                'Two more pronouns. [[Swój]] means my own, your own or his own. '
                'It always points back to the subject of the sentence.'
            ),
            say('Mam swój pokój.', 'I have my own room.'),
            say('Piotr kocha swoją żonę.', 'Piotr loves his wife.'),
            en("Careful! With [[jego]] instead, he loves another man's wife."),
            pl('Piotr kocha jego żonę.'),
            en('And [[siebie]] or [[sobie]] means oneself:'),
            say('Kupiłem sobie rower.', 'I bought myself a bike.'),
            clear=True,
        ),
    ],
)

VERB_CASES = Scene(
    'Verbs that pick a case',
    'Learn the verb and its case as one package',
    'r',
    steps=[
        step(
            [
                head('VERB', 'CASE', 'EXAMPLE', w=[0.36, 0.2, 0.44]),
                rule(
                    'szukać · potrzebować',
                    '+ genitive',
                    'Szukam pracy. Potrzebuję pomocy.',
                    w=[0.36, 0.2, 0.44],
                ),
                rule(
                    'słuchać · bać się',
                    '+ genitive',
                    'Słucham muzyki. Boję się psów.',
                    w=[0.36, 0.2, 0.44],
                ),
                rule(
                    'uczyć się · używać',
                    '+ genitive',
                    'Uczę się polskiego. Używam Linuksa.',
                    w=[0.36, 0.2, 0.44],
                ),
                rule(
                    'czekać na',
                    '+ accusative',
                    'Czekam na autobus.',
                    w=[0.36, 0.2, 0.44],
                ),
                rule(
                    'myśleć o · mówić o',
                    '+ locative',
                    'Myślę o tobie.',
                    w=[0.36, 0.2, 0.44],
                ),
                rule(
                    'rozmawiać z · interesować się',
                    '+ instrumental',
                    'Rozmawiam z szefem.',
                    w=[0.36, 0.2, 0.44],
                ),
            ],
            en(
                'Many verbs choose a fixed case, and you simply learn them as a '
                'package. These take the genitive:'
            ),
            say('Szukam pracy.', 'I am looking for a job.'),
            say('Potrzebuję pomocy.', 'I need help.'),
            say('Słucham muzyki.', 'I listen to music.'),
            say('Boję się psów.', 'I am afraid of dogs.'),
            say('Używam Linuksa.', 'I use Linux.'),
            en('[[Czekać na]], to wait for, takes the accusative:'),
            say('Czekam na autobus.', 'I am waiting for the bus.'),
            en('[[Myśleć o]], to think about, takes the locative:'),
            say('Myślę o tobie.', 'I am thinking about you.'),
            en('And [[rozmawiać z]], to talk with, takes the instrumental:'),
            say('Rozmawiam z szefem.', 'I am talking to my boss.'),
        ),
    ],
)


TRICKY = Scene(
    'Tricky verbs',
    'Irregular presents, and four ways to know or can',
    'm',
    steps=[
        step(
            [
                head('', 'ja', 'ty', 'on / ona', 'my', 'wy', 'oni', al='c', w=W7),
                grid(
                    [
                        'pisać',
                        'piszę',
                        'piszesz',
                        'pisze',
                        'piszemy',
                        'piszecie',
                        'piszą',
                    ],
                    p=[
                        'to write',
                        'PEE-sheh',
                        'PEE-shesh',
                        'PEE-sheh',
                        'pee-SHEH-mih',
                        'pee-SHEH-cheh',
                        'PEE-shohm',
                    ],
                    size=26,
                    w=W7,
                    h=82,
                ),
                grid(
                    [
                        'brać',
                        'biorę',
                        'bierzesz',
                        'bierze',
                        'bierzemy',
                        'bierzecie',
                        'biorą',
                    ],
                    p=[
                        'to take',
                        'BYOH-reh',
                        'BYEH-zhesh',
                        'BYEH-zheh',
                        'byeh-ZHEH-mih',
                        'byeh-ZHEH-cheh',
                        'BYOH-rohm',
                    ],
                    size=26,
                    w=W7,
                    h=82,
                ),
                grid(
                    ['dać (pf)', 'dam', 'dasz', 'da', 'damy', 'dacie', 'dadzą'],
                    p=[
                        'will give',
                        'dahm',
                        'dahsh',
                        'dah',
                        'DAH-mih',
                        'DAH-cheh',
                        'DAH-dzohm',
                    ],
                    size=26,
                    w=W7,
                    h=82,
                ),
                grid(
                    ['wiedzieć', 'wiem', 'wiesz', 'wie', 'wiemy', 'wiecie', 'wiedzą'],
                    p=[
                        'to know',
                        'vyem',
                        'vyesh',
                        'vyeh',
                        'VYEH-mih',
                        'VYEH-cheh',
                        'VYEH-dzohm',
                    ],
                    size=26,
                    w=W7,
                    h=82,
                ),
                grid(
                    [
                        'wziąć (pf)',
                        'wezmę',
                        'weźmiesz',
                        'weźmie',
                        'weźmiemy',
                        'weźmiecie',
                        'wezmą',
                    ],
                    p=[
                        'will take',
                        'VEZ-meh',
                        'VEZH-myesh',
                        'VEZH-myeh',
                        'vezh-MYEH-mih',
                        'vezh-MYEH-cheh',
                        'VEZ-mohm',
                    ],
                    size=26,
                    w=W7,
                    h=82,
                ),
            ],
            en(
                'A two expects you to handle the tricky verbs. Watch the consonants and vowels change.'
            ),
            pl('piszę, piszesz, pisze, piszemy, piszecie, piszą.'),
            pl('biorę, bierzesz, bierze, bierzemy, bierzecie, biorą.'),
            en('And three verbs with their own pattern:'),
            pl('dam, dasz, da, damy, dacie, dadzą.'),
            pl('wiem, wiesz, wie, wiemy, wiecie, wiedzą.'),
            pl('wezmę, weźmiesz, weźmie, weźmiemy, weźmiecie, wezmą.'),
        ),
        step(
            [
                head('KNOW & CAN: four different verbs', w=[1]),
                card(
                    'Wiem, że…  ·  Nie wiem.',
                    'vyem zheh  ·  nyeh vyem',
                    'wiedzieć: know a fact',
                ),
                card(
                    'Znam Kraków. Znasz Anię?',
                    'znahm KRAH-koof. znahsh AH-nyeh',
                    'znać: know a place / person',
                ),
                card(
                    'Umiem pływać.',
                    'OO-myem PWIH-vahch',
                    'umieć: know how to (a skill)',
                ),
                card(
                    'Mogę jutro przyjść.',
                    'MOH-geh YOO-troh pshiyshch',
                    'móc: can, be able / allowed',
                ),
            ],
            en(
                'English has one verb to know. Polish has two. [[Wiedzieć]] is for facts:'
            ),
            say('Nie wiem.', 'I do not know.'),
            en('[[Znać]] is for people and places:'),
            say('Znam Kraków.', 'I know [[Kraków]].'),
            say('Znasz Anię?', 'Do you know Ania?'),
            en('And English can also splits in two. [[Umieć]] is a learned skill:'),
            say('Umiem pływać.', 'I can swim.'),
            en('[[Móc]] is being able, or being allowed:'),
            say('Mogę jutro przyjść.', 'I can come tomorrow.'),
            clear=True,
        ),
    ],
)


ASPECT = Scene(
    'Verb aspect',
    'The heart of A2: process vs result',
    'a',
    steps=[
        step(
            [
                note(
                    'Most verbs come in {pairs}. {Imperfective} = process, habit, '
                    'repetition. {g|Perfective} = one completed action, a result.'
                ),
                pair('{Czytałem} książkę.', 'I was reading a book. (process)'),
                pair(
                    '{g|Przeczytałem} książkę.', 'I read the book, all of it. (result)'
                ),
                pair('Codziennie {piję} kawę.', 'I drink coffee every day. (habit)'),
                pair(
                    '{g|Wypiłem} kawę i wyszedłem.',
                    'I drank up my coffee and left. (done)',
                ),
            ],
            en(
                'Aspect is the heart of A two. Almost every Polish verb comes in a '
                'pair. The imperfective describes a process, a habit or '
                'repetition. The perfective describes one completed action with a '
                'result. Compare:'
            ),
            say('Czytałem książkę.', 'I was reading a book.'),
            say('Przeczytałem książkę.', 'I read the book, all of it.'),
            say('Codziennie piję kawę.', 'Every day I drink coffee.'),
            say('Wypiłem kawę i wyszedłem.', 'I drank up my coffee and left.'),
        ),
        step(
            [
                head(
                    'HOW PAIRS ARE MADE',
                    'IMPERFECTIVE → PERFECTIVE',
                    'MEANING',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    'add a prefix',
                    'robić → {z}robić',
                    'to do / make',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    '',
                    'pisać → {na}pisać · czytać → {prze}czytać',
                    'write · read',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    '',
                    'jeść → {z}jeść · pić → {wy}pić',
                    'eat · drink',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    'change the suffix',
                    'kup{owa}ć → kupić · da{wa}ć → dać',
                    'buy · give',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    '',
                    'otwierać → otworzyć · zamykać → zamknąć',
                    'open · close',
                    w=[0.24, 0.48, 0.28],
                ),
                rule(
                    'a different verb',
                    'brać → {wziąć} · mówić → {powiedzieć}',
                    'take · say',
                    w=[0.24, 0.48, 0.28],
                ),
            ],
            en('How are pairs made? Most often with a prefix:'),
            pl(
                'robić, zrobić. Pisać, napisać. Czytać, przeczytać. Jeść, zjeść. Pić, wypić.'
            ),
            en('Sometimes the suffix changes:'),
            pl('kupować, kupić. Dawać, dać. Otwierać, otworzyć. Zamykać, zamknąć.'),
            en('And a few pairs are different words entirely:'),
            pl('brać, wziąć. Mówić, powiedzieć.'),
            en(
                'Always learn verbs in pairs, the same way you learn nouns with their gender.'
            ),
            clear=True,
        ),
        step(
            [
                head(
                    '',
                    '{IMPERFECTIVE}  robić',
                    '{g|PERFECTIVE}  zrobić',
                    al='c',
                    w=[0.18, 0.41, 0.41],
                ),
                grid(
                    ['present', 'robię', '—  no present!'],
                    e=['', 'I do / I am doing', ''],
                    size=30,
                    w=[0.18, 0.41, 0.41],
                    h=86,
                ),
                grid(
                    ['past', 'robiłem', 'zrobiłem'],
                    e=['', 'I was doing / used to do', 'I did it, it is done'],
                    size=30,
                    w=[0.18, 0.41, 0.41],
                    h=86,
                ),
                grid(
                    ['future', 'będę robić', 'zrobię'],
                    e=['', 'I will be doing', 'I will get it done'],
                    size=30,
                    w=[0.18, 0.41, 0.41],
                    h=86,
                ),
                note(
                    'The perfective has {no present tense}: its present-looking form '
                    'is the {future}.  {Zrobię to jutro.} = I will do it tomorrow.'
                ),
            ],
            en(
                'Here is the key consequence. The imperfective has three tenses: '
                'present, past and future. The perfective has no present tense. '
                'Its present-looking forms are the future.'
            ),
            say('Robię zadanie.', 'I am doing my homework.'),
            say('Zrobię to jutro.', 'I will do it tomorrow.'),
            en(
                'So [[zrobię]] can never mean I am doing. It always means I will get it done.'
            ),
            clear=True,
        ),
        step(
            [
                head('{IMPERFECTIVE} cue words', '{g|PERFECTIVE} cue words', al='c'),
                grid(
                    ['codziennie · często · zawsze', 'już · w końcu · nagle'],
                    e=['every day · often · always', 'already · finally · suddenly'],
                    size=28,
                    h=86,
                ),
                grid(
                    ['zwykle · długo · ciągle', 'raz · od razu · do końca'],
                    e=[
                        'usually · for a long time · constantly',
                        'once · at once · to the end',
                    ],
                    size=28,
                    h=86,
                ),
                pair(
                    'Kiedy {oglądałem} film, {g|zadzwonił} telefon.',
                    'background + event',
                    w=WIDE,
                ),
                pair(
                    'Długo {pisałem} list, ale w końcu go {g|napisałem}.',
                    'process, then result',
                    w=WIDE,
                ),
            ],
            en(
                'Listen for cue words. The imperfective loves [[codziennie, często, '
                'zawsze, zwykle, długo]]: every day, often, always, usually, for a '
                'long time. The perfective loves [[już, w końcu, nagle, od razu]]: '
                'already, finally, suddenly, at once. In stories they work '
                'together. The imperfective sets the scene, the perfective is the '
                'event.'
            ),
            say(
                'Kiedy oglądałem film, zadzwonił telefon.',
                'While I was watching a film, the phone rang.',
            ),
            say(
                'Długo pisałem list, ale w końcu go napisałem.',
                'I spent ages writing the letter, but I finally finished it.',
            ),
            clear=True,
        ),
    ],
)

PAST = Scene(
    'Past tense, fully',
    'Every person, both genders, the irregulars',
    'm',
    steps=[
        step(
            [
                head(
                    '', '{m|MAN · GROUP WITH A MAN}', '{f|WOMAN · NO MEN}', al='c', w=W3
                ),
                mf('ja', 'czytał{em}', 'czytał{am}'),
                mf('ty', 'czytał{eś}', 'czytał{aś}'),
                mf('on / ona / ono', 'czytał', 'czytał{a}  ·  czytał{o}'),
                mf('my', 'czyta{liśmy}', 'czyta{łyśmy}'),
                mf('wy', 'czyta{liście}', 'czyta{łyście}'),
                mf('oni / one', 'czyta{li}', 'czyta{ły}'),
            ],
            en(
                'The full past tense. Take the stem, add [[ł]], then an ending for '
                'person and gender. A man says:'
            ),
            pl('czytałem, czytałeś, czytał.'),
            en('A woman says:'),
            pl('czytałam, czytałaś, czytała.'),
            en('In the plural, groups with a man use [[li]]:'),
            pl('czytaliśmy, czytaliście, czytali.'),
            en('and groups without men use [[ły]]:'),
            pl('czytałyśmy, czytałyście, czytały.'),
        ),
        step(
            [
                head(
                    'INFINITIVE',
                    'HE  ·  SHE  ·  THEY (men)',
                    'MEANING',
                    w=[0.2, 0.5, 0.3],
                ),
                rule(
                    'mieć',
                    'mi{a}ł · mi{a}ła · mi{e}li',
                    'to have: a ↔ e',
                    w=[0.2, 0.5, 0.3],
                ),
                rule(
                    'chcieć',
                    'chci{a}ł · chci{a}ła · chci{e}li',
                    'to want',
                    w=[0.2, 0.5, 0.3],
                ),
                rule('iść', 'szedł · szła · szli', 'to go on foot', w=[0.2, 0.5, 0.3]),
                rule('jeść', 'jadł · jadła · jedli', 'to eat', w=[0.2, 0.5, 0.3]),
                rule('móc', 'mógł · mogła · mogli', 'can', w=[0.2, 0.5, 0.3]),
                rule('wziąć', 'wziął · wzięła · wzięli', 'to take', w=[0.2, 0.5, 0.3]),
            ],
            en('Verbs ending in [[eć]] switch between a and e:'),
            pl('miał, miała, mieli. Chciał, chciała, chcieli.'),
            en('And memorise the irregular four:'),
            pl(
                'szedł, szła, szli. Jadł, jadła, jedli. Mógł, mogła, mogli. Wziął, wzięła, wzięli.'
            ),
            clear=True,
        ),
        step(
            [
                card(
                    'Wczoraj poszedłem do kina.',
                    'VCHOH-rai poh-SHEH-dwem doh KEE-nah',
                    'Yesterday I went to the cinema.',
                ),
                card(
                    'Gdzie byłaś w weekend?',
                    'gjeh bih-WAHSH v WEE-kend',
                    'Where were you at the weekend? (to a woman)',
                ),
                card(
                    'Spotkaliśmy się w kawiarni.',
                    'spot-KAH-leesh-mih sheh f kah-VYAR-nee',
                    'We met in a café.',
                ),
                note(
                    'Listening tip: in speech the ending can jump forward. '
                    '{Gdzie byłeś?} = {Gdzieś był?}  Same meaning.'
                ),
            ],
            say('Wczoraj poszedłem do kina.', 'Yesterday I went to the cinema.'),
            say('Gdzie byłaś w weekend?', 'Where were you at the weekend?'),
            say('Spotkaliśmy się w kawiarni.', 'We met in a cafe.'),
            en(
                'A listening tip: in casual speech the personal ending can jump '
                'onto an earlier word. [[Gdzieś był?]] means the same as [[Gdzie '
                'byłeś?]]'
            ),
            clear=True,
        ),
    ],
)

FUTURE = Scene(
    'Two futures',
    'One for each aspect',
    'n',
    steps=[
        step(
            [
                head(
                    '{IMPERFECTIVE}: będę + infinitive',
                    '{g|PERFECTIVE}: just conjugate',
                    al='c',
                ),
                grid(
                    ['będę czytać', 'przeczytam'],
                    e=['I will be reading (process)', 'I will read it (to the end)'],
                    size=32,
                    h=86,
                ),
                grid(
                    ['będę pisać', 'napiszę'],
                    e=['I will be writing', 'I will write it'],
                    size=32,
                    h=86,
                ),
                grid(
                    ['będę kupować', 'kupię'],
                    e=['I will be buying (regularly)', 'I will buy (once)'],
                    size=32,
                    h=86,
                ),
                note(
                    'Also correct: {będę czytał / będę czytała} (będę + past form). Same meaning.'
                ),
            ],
            en(
                'Polish has two futures, one for each aspect. Imperfective verbs '
                'use [[będę]] plus the infinitive. Perfective verbs just '
                'conjugate, and that is the future.'
            ),
            pl('będę czytać, przeczytam. Będę pisać, napiszę. Będę kupować, kupię.'),
            say(
                'Jutro będę pracować cały dzień.', 'Tomorrow I will be working all day.'
            ),
            say('Jutro skończę projekt.', 'Tomorrow I will finish the project.'),
            en(
                'You will also hear [[będę czytał]] instead of [[będę czytać]]. Both are correct.'
            ),
        ),
        step(
            [
                grid(
                    ['jutro', 'pojutrze', 'za tydzień', 'w przyszłym roku'],
                    p=[
                        'YOO-troh',
                        'poh-YOO-tsheh',
                        'zah TIH-jen',
                        'f pshih-SHWIM ROH-koo',
                    ],
                    e=['tomorrow', 'day after tomorrow', 'in a week', 'next year'],
                    size=28,
                    h=110,
                ),
                grid(
                    ['za godzinę', 'wkrótce', 'w przyszły weekend', 'kiedyś'],
                    p=[
                        'zah goh-JEE-neh',
                        'FKROOT-tseh',
                        'f PSHIH-shwih WEE-kend',
                        'KYEH-dish',
                    ],
                    e=['in an hour', 'soon', 'next weekend', 'some day'],
                    size=28,
                    h=110,
                ),
                card(
                    'pójdę  ·  pojadę',
                    'POOY-deh  ·  poh-YAH-deh',
                    'I will go (on foot · by vehicle)',
                ),
            ],
            en('Future time words:'),
            pl(
                'jutro, pojutrze, za tydzień, w przyszłym roku, za godzinę, wkrótce, w przyszły weekend, kiedyś.'
            ),
            en(
                'Tomorrow, the day after tomorrow, in a week, next year, in an '
                'hour, soon, next weekend, some day. And the future of going:'
            ),
            say('Pójdę do domu.', 'I will go home.'),
            say('Pojadę do Zakopanego.', 'I will go to [[Zakopane]].'),
            clear=True,
        ),
    ],
)

MOTION = Scene(
    'Verbs of motion',
    'Now vs habit, foot vs wheels',
    'f',
    steps=[
        step(
            [
                head('', '{ON FOOT}', '{BY VEHICLE}', al='c', w=[0.26, 0.37, 0.37]),
                grid(
                    ['now, one direction', 'iść → idę', 'jechać → jadę'],
                    size=29,
                    w=[0.26, 0.37, 0.37],
                    h=58,
                ),
                grid(
                    ['habit, there & back', 'chodzić → chodzę', 'jeździć → jeżdżę'],
                    size=29,
                    w=[0.26, 0.37, 0.37],
                    h=58,
                ),
                pair('{Teraz} idę do pracy.', 'I am walking to work now.'),
                pair('{Codziennie} chodzę do pracy.', 'I walk to work every day.'),
                pair('{Często} jeżdżę do Warszawy.', 'I often go to Warsaw.'),
                pair('Lecę do Londynu.', 'I am flying to London. (lecieć / latać)'),
            ],
            en(
                'Polish motion verbs answer two questions. On foot, or by '
                'vehicle? And right now in one direction, or as a habit? [[Iść]] '
                'and [[jechać]] are now, one way. [[Chodzić]] and [[jeździć]] are '
                'habits, round trips and general ability.'
            ),
            say('Teraz idę do pracy.', 'I am walking to work now.'),
            say('Codziennie chodzę do pracy.', 'I walk to work every day.'),
            say('Często jeżdżę do Warszawy.', 'I often go to Warsaw.'),
            en('Flying works the same way, with [[lecieć]] and [[latać]].'),
            say('Lecę do Londynu.', 'I am flying to London.'),
        ),
        step(
            [
                head('', 'ja', 'ty', 'on / ona', 'my', 'wy', 'oni', al='c', w=W7),
                grid(
                    [
                        'chodzić',
                        'chodzę',
                        'chodzisz',
                        'chodzi',
                        'chodzimy',
                        'chodzicie',
                        'chodzą',
                    ],
                    p=[
                        'walk (habit)',
                        'HOH-dzeh',
                        'HOH-jeesh',
                        'HOH-jee',
                        'hoh-JEE-mih',
                        'hoh-JEE-cheh',
                        'HOH-dzohm',
                    ],
                    size=26,
                    w=W7,
                    h=84,
                ),
                grid(
                    [
                        'jeździć',
                        'jeżdżę',
                        'jeździsz',
                        'jeździ',
                        'jeździmy',
                        'jeździcie',
                        'jeżdżą',
                    ],
                    p=[
                        'ride (habit)',
                        'YEZH-jeh',
                        'YEZH-jeesh',
                        'YEZH-jee',
                        'yezh-JEE-mih',
                        'yezh-JEE-cheh',
                        'YEZH-johm',
                    ],
                    size=26,
                    w=W7,
                    h=84,
                ),
                grid(
                    ['lecieć', 'lecę', 'lecisz', 'leci', 'lecimy', 'lecicie', 'lecą'],
                    p=[
                        'fly (now)',
                        'LEH-tseh',
                        'LEH-cheesh',
                        'LEH-chee',
                        'leh-CHEE-mih',
                        'leh-CHEE-cheh',
                        'LEH-tsohm',
                    ],
                    size=26,
                    w=W7,
                    h=84,
                ),
            ],
            en('Here are their present tenses. Walking, as a habit:'),
            pl('chodzę, chodzisz, chodzi, chodzimy, chodzicie, chodzą.'),
            en('Riding, as a habit:'),
            pl('jeżdżę, jeździsz, jeździ, jeździmy, jeździcie, jeżdżą.'),
            en('Flying, right now:'),
            pl('lecę, lecisz, leci, lecimy, lecicie, lecą.'),
            clear=True,
        ),
        step(
            [
                head(
                    'PREFIX', 'ON FOOT  ·  BY VEHICLE', 'MEANING', w=[0.18, 0.47, 0.35]
                ),
                rule('po-', 'pójść · pojechać', 'set off, go', w=[0.18, 0.47, 0.35]),
                rule(
                    'przy-',
                    'przyjść · przyjechać',
                    'arrive, come',
                    w=[0.18, 0.47, 0.35],
                ),
                rule('wy-', 'wyjść · wyjechać', 'go out, leave', w=[0.18, 0.47, 0.35]),
                rule(
                    'w- / we-', 'wejść · wjechać', 'go in, enter', w=[0.18, 0.47, 0.35]
                ),
                rule('do-', 'dojść · dojechać', 'get to, reach', w=[0.18, 0.47, 0.35]),
                rule(
                    'prze-',
                    'przejść · przejechać',
                    'cross, go through',
                    w=[0.18, 0.47, 0.35],
                ),
            ],
            en('Add a prefix and you get a perfective verb with a direction.'),
            pl(
                'pójść, pojechać. Przyjść, przyjechać. Wyjść, wyjechać. Wejść, wjechać. Dojść, dojechać. Przejść, przejechać.'
            ),
            say('Przyjdę o szóstej.', 'I will come at six.'),
            say('Wyszedłem z domu o ósmej.', 'I left home at eight.'),
            say('Jak dojść do dworca?', 'How do I get to the station?'),
            clear=True,
        ),
        step(
            [
                head('WHERE TO?', 'WHERE?', 'WHERE FROM?', al='c'),
                grid(
                    ['do sklepu', 'w sklepie', 'ze sklepu'],
                    e=['do + genitive', 'w + locative', 'z + genitive'],
                    size=32,
                    h=86,
                ),
                grid(
                    ['na pocztę', 'na poczcie', 'z poczty'],
                    e=['na + accusative', 'na + locative', 'z + genitive'],
                    size=32,
                    h=86,
                ),
                grid(
                    ['do lekarza', 'u lekarza', 'od lekarza'],
                    e=['people: do', 'people: u + genitive', 'people: od'],
                    size=32,
                    h=86,
                ),
                pair(
                    'Jadę {autobusem} · {pociągiem} · {rowerem}.',
                    'by bus · train · bike = instrumental',
                    w=WIDE,
                ),
            ],
            en('Direction, location and origin come in sets of three. The shop:'),
            pl('do sklepu, w sklepie, ze sklepu.'),
            en('Places that use [[na]], like the post office:'),
            pl('na pocztę, na poczcie, z poczty.'),
            en('People use [[do]], [[u]] and [[od]]:'),
            pl('do lekarza, u lekarza, od lekarza.'),
            en('And transport goes in the instrumental:'),
            pl('Jadę autobusem, pociągiem, rowerem.'),
            clear=True,
        ),
    ],
)

IMPERATIVE = Scene(
    'Imperative',
    'Giving instructions, politely or not',
    'r',
    steps=[
        step(
            [
                head('HE / SHE NOW', 'TY', 'WY', "LET'S", al='c'),
                grid(['czyta', 'czytaj!', 'czytajcie!', 'czytajmy!'], size=30, h=58),
                grid(['pisze', 'pisz!', 'piszcie!', 'piszmy!'], size=30, h=58),
                grid(['robi', 'rób!', 'róbcie!', 'róbmy!'], size=30, h=58),
                grid(['idzie', 'idź!', 'idźcie!', 'chodźmy!'], size=30, h=58),
                grid(['je', 'jedz!', 'jedzcie!', 'jedzmy!'], size=30, h=58),
                note(
                    'Start from the {he / she} form and cut the ending: robi → {rób} (o → ó).'
                ),
            ],
            en(
                'The imperative. Start from the he or she form of the present '
                'tense and cut off the ending. [[Czyta]] becomes [[czytaj!]] Add '
                '[[cie]] for several people, and [[my]] for let us.'
            ),
            pl('czytaj, czytajcie, czytajmy.'),
            pl('pisz, piszcie, piszmy.'),
            pl('rób, róbcie, róbmy.'),
            pl('idź, idźcie, chodźmy.'),
            pl('jedz, jedzcie, jedzmy.'),
        ),
        step(
            [
                grid(
                    ['bądź!', 'miej!', 'weź!', 'powiedz!'],
                    e=[
                        'be! (być)',
                        'have! (mieć)',
                        'take! (wziąć)',
                        'say! (powiedzieć)',
                    ],
                    size=32,
                    h=86,
                ),
                grid(
                    ['zobacz!', 'daj!', 'usiądź!', 'chodź!'],
                    e=[
                        'look! (zobaczyć)',
                        'give! (dać)',
                        'sit down! (usiąść)',
                        'come here! (chodzić)',
                    ],
                    size=32,
                    h=86,
                ),
                note(
                    'Do it: usually {g|perfective}.  Don’t do it: {imperfective}.  '
                    '{g|Zamknij} okno!  but  {Nie zamykaj} okna!'
                ),
                pair('{g|Zrób} to!  ·  {Nie rób} tego!', 'Do it!  ·  Don’t do it!'),
            ],
            en('Learn these by heart:'),
            pl('bądź, miej, weź, powiedz, zobacz, daj, usiądź, chodź.'),
            en(
                'Be, have, take, say, look, give, sit down, come here. And a '
                'crucial rule: positive commands usually use the perfective, but '
                'negative commands use the imperfective.'
            ),
            say('Zamknij okno!', 'Close the window!'),
            say('Nie zamykaj okna!', 'Do not close the window!'),
            en('Notice the genitive after [[nie]] there too.'),
            clear=True,
        ),
        step(
            [
                card('Proszę usiąść.', 'PROH-sheh OO-shonshch', 'Please sit down.'),
                card('Niech pan wejdzie.', 'nyeh pahn VAY-jeh', 'Do come in, sir.'),
                card(
                    'Proszę pana / pani…',
                    'PROH-sheh PAH-nah / PAH-nee',
                    'Excuse me, sir / madam…',
                ),
                card(
                    'Nie palić!',
                    'nyeh PAH-leech',
                    'No smoking! (signs use the infinitive)',
                ),
                card('Uwaga!', 'oo-VAH-gah', 'Watch out! / Attention!'),
            ],
            en(
                'With strangers, avoid the bare imperative. Use [[proszę]] plus the infinitive:'
            ),
            say('Proszę usiąść.', 'Please sit down.'),
            en('or [[niech]] with pan or pani:'),
            say('Niech pan wejdzie.', 'Do come in, sir.'),
            en('On signs you will see the infinitive:'),
            say('Nie palić!', 'No smoking.'),
            say('Uwaga!', 'Attention!'),
            clear=True,
        ),
    ],
)

CONDITIONAL = Scene(
    'Conditional & politeness',
    'Would, could, if',
    'g',
    steps=[
        step(
            [
                head(
                    '', '{m|MAN · GROUP WITH A MAN}', '{f|WOMAN · NO MEN}', al='c', w=W3
                ),
                mf('ja', 'chciał{bym}', 'chciała{bym}'),
                mf('ty', 'chciał{byś}', 'chciała{byś}'),
                mf('on / ona', 'chciał{by}', 'chciała{by}'),
                mf('my', 'chcieli{byśmy}', 'chciały{byśmy}'),
                mf('oni / one', 'chcieli{by}', 'chciały{by}'),
                note(
                    'Past form + {by} + ending.  {Chciałbym…} = I would like… The politest word you own.'
                ),
            ],
            en(
                'The conditional is the past form plus [[by]] plus a personal '
                'ending. You already know the most useful word in Polish '
                'politeness. Said by a man:'
            ),
            drill('Chciałbym'),
            en('Said by a woman:'),
            drill('Chciałabym'),
            en('Both mean I would like. The other persons:'),
            pl('chciałbyś, chciałby, chcielibyśmy, chcieliby.'),
        ),
        step(
            [
                card(
                    'Chciałbym zamówić stolik.',
                    'HCHOW-bim zah-MOO-veech STOH-leek',
                    'I would like to book a table.',
                ),
                card(
                    'Czy mógłby pan mi pomóc?',
                    'chih MOOG-bih pahn mee POH-moots',
                    'Could you help me, sir?',
                ),
                card(
                    'Czy mogłaby pani powtórzyć?',
                    'chih moh-GWAH-bih PAH-nee pof-TOO-zhihch',
                    'Could you repeat that, madam?',
                ),
                card(
                    'Wolałbym herbatę.',
                    'voh-LOW-bim her-BAH-teh',
                    'I would prefer tea.',
                ),
                card('Byłoby super!', 'bih-WOH-bih SOO-per', 'That would be great!'),
            ],
            en('Use it to soften every request:'),
            say('Chciałbym zamówić stolik.', 'I would like to book a table.'),
            say('Czy mógłby pan mi pomóc?', 'Could you help me, sir?'),
            say('Czy mogłaby pani powtórzyć?', 'Could you repeat that, madam?'),
            say('Wolałbym herbatę.', 'I would prefer tea.'),
            say('Byłoby super!', 'That would be great!'),
            clear=True,
        ),
        step(
            [
                pair(
                    '{Gdybym} miał czas, {pojechałbym} w góry.',
                    'If I had time, I would go to the mountains.',
                    w=WIDE,
                ),
                pair(
                    'Co {byś} zrobił na moim miejscu?',
                    'What would you do in my place?',
                    w=WIDE,
                ),
                note(
                    '{Gdyby} + past form, then the conditional: just like English “if I had…, I would…”.'
                ),
            ],
            en('For imaginary situations, use [[gdyby]], if, with the past form:'),
            say(
                'Gdybym miał czas, pojechałbym w góry.',
                'If I had time, I would go to the mountains.',
            ),
            say('Co byś zrobił na moim miejscu?', 'What would you do in my place?'),
            clear=True,
        ),
    ],
)

COMPARE = Scene(
    'Comparing things',
    'Bigger, better, the best',
    'a',
    steps=[
        step(
            [
                head('ADJECTIVE', 'MORE', 'MOST', al='c'),
                grid(['nowy', 'now{szy}', '{naj}nowszy'], size=30, h=58),
                grid(['tani', 'ta{ńszy}', '{naj}tańszy'], size=30, h=58),
                grid(['ładny', 'ładn{iejszy}', '{naj}ładniejszy'], size=30, h=58),
                grid(['trudny', 'trudn{iejszy}', '{naj}trudniejszy'], size=30, h=58),
                grid(['drogi', 'dro{ższy}', '{naj}droższy'], size=30, h=58),
                grid(['lekki', 'l{żejszy}', '{naj}lżejszy'], size=30, h=58),
            ],
            en(
                'Comparatives. Short adjectives add [[szy]], others add '
                '[[ejszy]]. The superlative puts [[naj]] in front.'
            ),
            pl('nowy, nowszy, najnowszy. Tani, tańszy, najtańszy.'),
            pl(
                'ładny, ładniejszy, najładniejszy. Trudny, trudniejszy, najtrudniejszy.'
            ),
            en('Consonants shift, as always:'),
            pl('drogi, droższy. Lekki, lżejszy.'),
        ),
        step(
            [
                head('', 'MORE', 'MOST', al='c'),
                grid(
                    ['dobry', 'lepszy', 'najlepszy'],
                    e=['good', 'better', 'best'],
                    size=32,
                    h=84,
                ),
                grid(
                    ['zły', 'gorszy', 'najgorszy'],
                    e=['bad', 'worse', 'worst'],
                    size=32,
                    h=84,
                ),
                grid(
                    ['duży', 'większy', 'największy'],
                    e=['big', 'bigger', 'biggest'],
                    size=32,
                    h=84,
                ),
                grid(
                    ['mały', 'mniejszy', 'najmniejszy'],
                    e=['small', 'smaller', 'smallest'],
                    size=32,
                    h=84,
                ),
                note(
                    'Long adjectives: {bardziej / najbardziej} interesujący.  Less: {mniej}.'
                ),
            ],
            en('The irregular four, just like English:'),
            pl(
                'dobry, lepszy, najlepszy. Zły, gorszy, najgorszy. Duży, większy, największy. Mały, mniejszy, najmniejszy.'
            ),
            en(
                'For long adjectives, use [[bardziej]], more, and [[najbardziej]], most.'
            ),
            clear=True,
        ),
        step(
            [
                head('ADJECTIVE → ADVERB', w=[1]),
                grid(
                    [
                        'szybki → szybko',
                        'cichy → cicho',
                        'łatwy → łatwo',
                        'wolny → wolno',
                    ],
                    e=['fast', 'quietly', 'easily', 'slowly'],
                    size=28,
                    h=86,
                ),
                grid(
                    [
                        'ładny → ładnie',
                        'dobry → dobrze',
                        'zły → źle',
                        'głośny → głośno',
                    ],
                    e=['nicely', 'well', 'badly', 'loudly'],
                    size=28,
                    h=86,
                ),
                pair(
                    'On mówi {szybko}.  ·  To jest {szybki} pociąg.',
                    'adverb for verbs · adjective for nouns',
                    w=WIDE,
                ),
            ],
            en('Adverbs describe verbs. Most adjectives become adverbs with o or e:'),
            pl('szybki, szybko. Cichy, cicho. Łatwy, łatwo.'),
            en('With e, the consonant often softens:'),
            pl('ładny, ładnie. Dobry, dobrze. Zły, źle.'),
            say('On mówi szybko.', 'He speaks fast.'),
            say('To jest szybki pociąg.', 'This is a fast train.'),
            clear=True,
        ),
        step(
            [
                grid(
                    [
                        'dobrze → lepiej',
                        'źle → gorzej',
                        'dużo → więcej',
                        'mało → mniej',
                    ],
                    e=[
                        'well → better',
                        'badly → worse',
                        'a lot → more',
                        'little → less',
                    ],
                    size=26,
                    h=86,
                ),
                grid(
                    [
                        'szybko → szybciej',
                        'często → częściej',
                        'coraz lepiej',
                        'najlepiej',
                    ],
                    e=[
                        'fast → faster',
                        'often → more often',
                        'better and better',
                        'best',
                    ],
                    size=26,
                    h=86,
                ),
                pair(
                    'Kraków jest mniejszy {niż} Warszawa.',
                    'than: niż + nominative',
                    w=WIDE,
                ),
                pair(
                    'Kraków jest mniejszy {od} Warszawy.', 'or: od + genitive', w=WIDE
                ),
                pair(
                    'Mój rower jest lżejszy niż twój.',
                    'My bike is lighter than yours.',
                    w=WIDE,
                ),
            ],
            en('Adverbs compare too:'),
            pl('lepiej, gorzej, więcej, mniej, szybciej, częściej.'),
            en('Than is [[niż]] plus the nominative, or [[od]] plus the genitive:'),
            say(
                'Kraków jest mniejszy niż Warszawa.',
                '[[Kraków]] is smaller than Warsaw.',
            ),
            pl('Kraków jest mniejszy od Warszawy.'),
            say('Mój rower jest lżejszy niż twój.', 'My bike is lighter than yours.'),
            en(
                'And a favourite: [[coraz lepiej]], better and better. Like your Polish.'
            ),
            clear=True,
        ),
    ],
)

MODALS = Scene(
    'Must, can, should & się',
    'Impersonal phrases and daily routine',
    'n',
    steps=[
        step(
            [
                card(
                    'Trzeba kupić bilet.',
                    'TSHEH-bah KOO-peech BEE-let',
                    'You need to buy a ticket.',
                ),
                card(
                    'Można płacić kartą?',
                    'MOZH-nah PWAH-cheech KAR-tohm',
                    'Can one pay by card?',
                ),
                card(
                    'Tu nie wolno palić.',
                    'too nyeh VOL-noh PAH-leech',
                    'Smoking is not allowed here.',
                ),
                card(
                    'Warto zwiedzić Wawel.',
                    'VAR-toh ZVYEH-jeech VAH-vel',
                    'Wawel is worth visiting.',
                ),
                card(
                    'Nie da się tego zrobić.',
                    'nyeh dah sheh TEH-goh ZROH-beech',
                    'It cannot be done.',
                ),
            ],
            en('Impersonal words take an infinitive and no subject:'),
            say('Trzeba kupić bilet.', 'You need to buy a ticket.'),
            say('Można płacić kartą?', 'Can one pay by card?'),
            say('Tu nie wolno palić.', 'Smoking is not allowed here.'),
            say('Warto zwiedzić Wawel.', '[[Wawel]] is worth visiting.'),
            say('Nie da się tego zrobić.', 'It cannot be done.'),
        ),
        step(
            [
                head(
                    '', '{m|MAN · GROUP WITH A MAN}', '{f|WOMAN · NO MEN}', al='c', w=W3
                ),
                mf('ja', 'powinien{em}', 'powinn{am}'),
                mf('ty', 'powinien{eś}', 'powinn{aś}'),
                mf('on / ona', 'powinien', 'powinn{a}'),
                mf('my', 'powinn{iśmy}', 'powinn{yśmy}'),
                mf('oni / one', 'powinn{i}', 'powinn{y}'),
                pair('Powinieneś odpocząć.', 'You (m) should rest.'),
            ],
            en(
                'Should is [[powinien]]. It behaves like a past tense form. A man says:'
            ),
            pl('powinienem, powinieneś, powinien.'),
            en('A woman says:'),
            pl('powinnam, powinnaś, powinna.'),
            say('Powinieneś odpocząć.', 'You should rest.'),
            clear=True,
        ),
        step(
            [
                head('IMPERSONAL “SIĘ”', w=[1]),
                pair('Jak się mówi … po polsku?', 'How do you say … in Polish?'),
                pair('Tu się nie pali.', 'People don’t smoke here.'),
                pair('W Polsce je się dużo zup.', 'In Poland people eat lots of soup.'),
                head('REFLEXIVE ROUTINE', w=[1]),
                note(
                    'Budzę {się} o siódmej, myję {się}, ubieram {się} i jem '
                    'śniadanie. Wieczorem kładę {się} spać.'
                ),
            ],
            en(
                '[[Się]] also makes impersonal sentences, like the English one or people:'
            ),
            say('Jak się mówi to po polsku?', 'How do you say this in Polish?'),
            say('Tu się nie pali.', 'People do not smoke here.'),
            say('W Polsce je się dużo zup.', 'In Poland, people eat lots of soup.'),
            en('And with reflexive verbs it describes your daily routine:'),
            pl(
                'Budzę się o siódmej, myję się, ubieram się i jem śniadanie. Wieczorem kładę się spać.'
            ),
            en(
                'I wake up at seven, wash, get dressed and eat breakfast. In the evening I go to bed.'
            ),
            clear=True,
        ),
    ],
)

LINKING = Scene(
    'Linking words & który',
    'From simple sentences to real ones',
    'm',
    steps=[
        step(
            [
                grid(
                    ['że', 'bo', 'ponieważ', 'więc'],
                    p=['zheh', 'boh', 'poh-NYEH-vahsh', 'vyents'],
                    e=['that', 'because', 'because (formal)', 'so'],
                    size=30,
                    h=108,
                ),
                grid(
                    ['dlatego', 'kiedy / gdy', 'jeśli', 'żeby'],
                    p=['dlah-TEH-goh', 'KYEH-dih / gdih', 'YESH-lee', 'ZHEH-bih'],
                    e=['that is why', 'when', 'if', 'in order to'],
                    size=30,
                    h=108,
                ),
                grid(
                    ['chociaż', 'zanim', 'najpierw', 'potem'],
                    p=['HOH-chahsh', 'ZAH-neem', 'NAI-pyerf', 'POH-tem'],
                    e=['although', 'before', 'first', 'then'],
                    size=30,
                    h=108,
                ),
                note(
                    'Polish always puts a {comma} before że, bo, kiedy, jeśli, żeby and który.'
                ),
            ],
            en('Linking words turn A one sentences into A two sentences.'),
            pl(
                'że, bo, ponieważ, więc, dlatego, kiedy, jeśli, żeby, chociaż, zanim, najpierw, potem.'
            ),
            en(
                'That, because, because, so, that is why, when, if, in order to, '
                'although, before, first, then. And Polish always puts a comma '
                'before them.'
            ),
        ),
        step(
            [
                pair('Myślę, {że} masz rację.', 'I think that you’re right.', w=WIDE),
                pair(
                    'Nie przyjdę, {bo} jestem chory.',
                    'I won’t come because I’m ill.',
                    w=WIDE,
                ),
                pair(
                    'Pada, {więc} jadę tramwajem.',
                    'It’s raining, so I’m taking the tram.',
                    w=WIDE,
                ),
                pair(
                    '{Jeśli} będzie ładnie, pojedziemy nad Wisłę.',
                    'If it’s nice, we’ll go to the Vistula.',
                    w=WIDE,
                ),
                pair(
                    'Uczę się, {żeby} rozmawiać z sąsiadami.',
                    'I study so I can talk to my neighbours.',
                    w=WIDE,
                ),
                pair(
                    'Nie wiem, {czy} on przyjdzie.',
                    'I don’t know whether he’ll come.',
                    w=WIDE,
                ),
            ],
            say('Myślę, że masz rację.', 'I think that you are right.'),
            say('Nie przyjdę, bo jestem chory.', 'I will not come, because I am ill.'),
            say(
                'Pada, więc jadę tramwajem.', 'It is raining, so I am taking the tram.'
            ),
            say(
                'Jeśli będzie ładnie, pojedziemy nad Wisłę.',
                'If the weather is nice, we will go to the Vistula.',
            ),
            say(
                'Uczę się, żeby rozmawiać z sąsiadami.',
                'I study so that I can talk to my neighbours.',
            ),
            say('Nie wiem, czy on przyjdzie.', 'I do not know whether he will come.'),
            en(
                'Note the last one: in indirect yes or no questions, whether is [[czy]].'
            ),
            clear=True,
        ),
        step(
            [
                head('KTÓRY = who / which / that: it agrees like an adjective', w=[1]),
                pair(
                    'To jest kolega, {m|który} mieszka w Gdańsku.',
                    'masculine, subject',
                    w=WIDE,
                ),
                pair(
                    'Mam koleżankę, {f|która} pracuje w banku.',
                    'feminine, subject',
                    w=WIDE,
                ),
                pair(
                    'To jest książka, {f|którą} czytam.', 'feminine, accusative', w=WIDE
                ),
                pair(
                    'Restauracja, w {f|której} jedliśmy, była świetna.',
                    'feminine, locative',
                    w=WIDE,
                ),
                pair('To są ludzie, {m|którzy} mi pomogli.', 'virile plural', w=WIDE),
            ],
            en(
                '[[Który]] means who, which or that. It takes the gender of the '
                'noun it refers to, and the case of its own clause.'
            ),
            say(
                'To jest kolega, który mieszka w Gdańsku.',
                'This is a friend who lives in [[Gdańsk]].',
            ),
            say(
                'Mam koleżankę, która pracuje w banku.',
                'I have a friend who works in a bank.',
            ),
            say('To jest książka, którą czytam.', 'This is the book I am reading.'),
            say(
                'Restauracja, w której jedliśmy, była świetna.',
                'The restaurant where we ate was great.',
            ),
            say(
                'To są ludzie, którzy mi pomogli.',
                'These are the people who helped me.',
            ),
            clear=True,
        ),
    ],
)

INDEFINITE = Scene(
    'Somebody, nobody',
    'The some- and no- families',
    'r',
    steps=[
        step(
            [
                head('SOME-', 'NO-  (+ nie!)', 'MEANING'),
                rule('ktoś', 'nikt', 'someone · no one'),
                rule('coś', 'nic', 'something · nothing'),
                rule('gdzieś', 'nigdzie', 'somewhere · nowhere'),
                rule('kiedyś', 'nigdy', 'sometime · never'),
                rule('jakiś', 'żaden', 'some kind of · no, none'),
            ],
            en('The some family ends in a soft [[ś]]:'),
            pl('ktoś, coś, gdzieś, kiedyś, jakiś.'),
            en(
                'Someone, something, somewhere, sometime, some kind of. The no family starts with [[ni]]:'
            ),
            pl('nikt, nic, nigdzie, nigdy, żaden.'),
        ),
        step(
            [
                pair('{Nikt} {nie} wie.', 'Nobody knows.'),
                pair('{Nic} {nie} widzę.', 'I can’t see anything.'),
                pair('{Nigdzie} {nie} byłem.', 'I haven’t been anywhere.'),
                pair('{Nie} mam {żadnych} pytań.', 'I have no questions.'),
                pair(
                    '{Nie} piję {ani} kawy, {ani} herbaty.',
                    'I drink neither coffee nor tea.',
                ),
                pair(
                    'Czy {ktoś} tu mówi po angielsku?',
                    'Does anyone here speak English?',
                ),
            ],
            en(
                'The no family always needs [[nie]] on the verb. Double and even triple negatives are correct Polish.'
            ),
            say('Nikt nie wie.', 'Nobody knows.'),
            say('Nic nie widzę.', 'I cannot see anything.'),
            say('Nigdzie nie byłem.', 'I have not been anywhere.'),
            say('Nie mam żadnych pytań.', 'I have no questions.'),
            say('Nie piję ani kawy, ani herbaty.', 'I drink neither coffee nor tea.'),
            say('Czy ktoś tu mówi po angielsku?', 'Does anyone here speak English?'),
            clear=True,
        ),
    ],
)

DATES = Scene(
    'Big numbers, dates & time',
    'Prices, birthdays, timetables',
    'a',
    steps=[
        step(
            [
                grid(
                    [
                        '100  sto',
                        '200  dwieście',
                        '300  trzysta',
                        '400  czterysta',
                        '500  pięćset',
                    ],
                    p=[
                        'stoh',
                        'DVYESH-cheh',
                        'TSHIH-stah',
                        'chteh-RIH-stah',
                        'PYENCH-set',
                    ],
                    size=26,
                    h=82,
                ),
                grid(
                    [
                        '600  sześćset',
                        '700  siedemset',
                        '800  osiemset',
                        '900  dziewięćset',
                        '1000  tysiąc',
                    ],
                    p=[
                        'SHESHCH-set',
                        'shyeh-DEM-set',
                        'oh-SHEM-set',
                        'jeh-VYENCH-set',
                        'TIH-shonts',
                    ],
                    size=24,
                    h=82,
                ),
                rule(
                    '2 000  ·  5 000',
                    'dwa tysiące · pięć tysięcy',
                    'the same 2–4 / 5+ rule',
                ),
                pair('dwieście pięćdziesiąt złotych', '250 zloty', w=WIDE),
            ],
            en('Big numbers. The hundreds are irregular, so listen carefully:'),
            pl(
                'sto, dwieście, trzysta, czterysta, pięćset, sześćset, siedemset, osiemset, dziewięćset, tysiąc.'
            ),
            en('Thousands follow the counting rule you already know:'),
            pl('dwa tysiące, pięć tysięcy.'),
            say('dwieście pięćdziesiąt złotych', 'two hundred and fifty zloty'),
        ),
        step(
            [
                grid(
                    ['pierwszy', 'drugi', 'trzeci', 'czwarty', 'piąty'],
                    p=['PYERF-shih', 'DROO-gee', 'TSHEH-chee', 'CHFAR-tih', 'PYON-tih'],
                    e=['1st', '2nd', '3rd', '4th', '5th'],
                    size=28,
                    h=108,
                ),
                grid(
                    ['szósty', 'siódmy', 'ósmy', 'dziewiąty', 'dziesiąty'],
                    p=[
                        'SHOOS-tih',
                        'SHOOD-mih',
                        'OOS-mih',
                        'jeh-VYON-tih',
                        'jeh-SHON-tih',
                    ],
                    e=['6th', '7th', '8th', '9th', '10th'],
                    size=28,
                    h=108,
                ),
                note(
                    'Then {jedenasty, dwunasty… dwudziesty, trzydziesty}. They decline '
                    'like adjectives: na {drugim} piętrze = on the second floor.'
                ),
            ],
            en('Ordinal numbers, for dates, floors and centuries:'),
            pl(
                'pierwszy, drugi, trzeci, czwarty, piąty, szósty, siódmy, ósmy, dziewiąty, dziesiąty.'
            ),
            en('They behave like adjectives:'),
            say('Mieszkam na drugim piętrze.', 'I live on the second floor.'),
            clear=True,
        ),
        step(
            [
                card(
                    'Którego dzisiaj jest?',
                    'KTOO-reh-goh JEE-shai yest',
                    'What is the date today?',
                ),
                pair(
                    'Dzisiaj jest {dwudziesty siódmy} {października}.',
                    'ordinal + month in the genitive',
                    w=WIDE,
                ),
                pair('Urodziny mam {piątego maja}.', 'on a date: all genitive', w=WIDE),
                pair(
                    '{w październiku} · {w maju} · {we wrześniu}',
                    'in a month: locative',
                    w=WIDE,
                ),
                pair(
                    'w dwa tysiące {dwudziestym szóstym} roku',
                    'in 2026: locative ordinal',
                    w=WIDE,
                ),
            ],
            en(
                'Dates use ordinal numbers. The day is masculine, because '
                '[[dzień]] is masculine, and the month goes into the genitive.'
            ),
            say('Którego dzisiaj jest?', 'What is the date today?'),
            say(
                'Dzisiaj jest dwudziesty siódmy października.',
                'Today is the twenty seventh of October.',
            ),
            en('On a date, the whole thing goes into the genitive:'),
            say('Urodziny mam piątego maja.', 'My birthday is on the fifth of May.'),
            en('In a month, use the locative:'),
            pl('w październiku, w maju, we wrześniu.'),
            en('And a year is a locative ordinal. Twenty twenty six is:'),
            pl('w dwa tysiące dwudziestym szóstym roku.'),
            clear=True,
        ),
        step(
            [
                head('MONTHS IN THE GENITIVE (for dates)', w=[1]),
                grid(['stycznia', 'lutego', 'marca', 'kwietnia'], size=28, h=56),
                grid(['maja', 'czerwca', 'lipca', 'sierpnia'], size=28, h=56),
                grid(
                    ['września', 'października', 'listopada', 'grudnia'], size=28, h=56
                ),
                note(
                    'Seasons, in the instrumental: {wiosną} in spring · {latem} in '
                    'summer · {jesienią} in autumn · {zimą} in winter.'
                ),
            ],
            en('The months in the genitive, for dates:'),
            pl(
                'stycznia, lutego, marca, kwietnia, maja, czerwca, lipca, sierpnia, września, października, listopada, grudnia.'
            ),
            en('And the seasons, in the instrumental:'),
            pl('wiosną, latem, jesienią, zimą.'),
            en('In spring, in summer, in autumn, in winter.'),
            clear=True,
        ),
        step(
            [
                head('CLOCK', 'EVERYDAY', 'TRADITIONAL', w=[0.16, 0.42, 0.42]),
                rule(
                    '8:15', 'ósma piętnaście', 'kwadrans po ósmej', w=[0.16, 0.42, 0.42]
                ),
                rule(
                    '8:30',
                    'ósma trzydzieści',
                    'wpół do dziewiątej',
                    w=[0.16, 0.42, 0.42],
                ),
                rule(
                    '8:45',
                    'ósma czterdzieści pięć',
                    'za kwadrans dziewiąta',
                    w=[0.16, 0.42, 0.42],
                ),
                rule(
                    '17:20',
                    'siedemnasta dwadzieścia',
                    'timetables: 24 hours',
                    w=[0.16, 0.42, 0.42],
                ),
                note(
                    'At: {o} + locative: o ósmej, o wpół do dziewiątej.  From–to: {od} ósmej {do} szesnastej.'
                ),
            ],
            en(
                'Telling the time, full version. Everyday Polish just reads the '
                'numbers. Traditional Polish uses quarters and halves, and half '
                'past eight is literally half to nine:'
            ),
            say('kwadrans po ósmej', 'quarter past eight'),
            say('wpół do dziewiątej', 'half past eight'),
            say('za kwadrans dziewiąta', 'quarter to nine'),
            en('Timetables use the twenty four hour clock:'),
            say(
                'Pociąg odjeżdża o siedemnastej dwadzieścia.',
                'The train leaves at seventeen twenty.',
            ),
            en('And from, to: [[od ósmej do szesnastej]].'),
            clear=True,
        ),
    ],
)

TIME_WEATHER = Scene(
    'Time words & weather',
    'Before, after, in, for, ago, during',
    'n',
    steps=[
        step(
            [
                head('PREPOSITION', 'CASE', 'EXAMPLE', w=[0.2, 0.2, 0.6]),
                rule(
                    'przed',
                    '+ instr.',
                    'przed pracą · przed świętami',
                    w=[0.2, 0.2, 0.6],
                ),
                rule('po', '+ loc.', 'po pracy · po obiedzie', w=[0.2, 0.2, 0.6]),
                rule(
                    'za', '+ acc.', 'za godzinę · za tydzień  (in…)', w=[0.2, 0.2, 0.6]
                ),
                rule(
                    'przez',
                    '+ acc.',
                    'przez godzinę · przez cały dzień  (for…)',
                    w=[0.2, 0.2, 0.6],
                ),
                rule(
                    '… temu',
                    'acc. +',
                    'tydzień temu · dwa lata temu  (…ago)',
                    w=[0.2, 0.2, 0.6],
                ),
                rule(
                    'podczas',
                    '+ gen.',
                    'podczas urlopu · podczas meczu',
                    w=[0.2, 0.2, 0.6],
                ),
            ],
            en(
                'Prepositions of time. Before is [[przed]] with the instrumental, '
                'and after is [[po]] with the locative:'
            ),
            say('przed pracą', 'before work'),
            say('po pracy', 'after work'),
            en(
                '[[Za]] means in, looking forward. [[Przez]] means for, a '
                'duration. And [[temu]], ago, comes after the noun:'
            ),
            say('za godzinę', 'in an hour'),
            say('przez godzinę', 'for an hour'),
            say('tydzień temu', 'a week ago'),
            en('During is [[podczas]], with the genitive:'),
            say('podczas urlopu', 'during my holiday'),
        ),
        step(
            [
                card(
                    'Jaka będzie jutro pogoda?',
                    'YAH-kah BEN-jeh YOO-troh poh-GOH-dah',
                    'What will the weather be tomorrow?',
                ),
                card(
                    'Pada śnieg.  ·  Wieje wiatr.',
                    'PAH-dah shnyek  ·  VYEH-yeh vyahtr',
                    'It is snowing.  ·  It is windy.',
                ),
                card('Jest pochmurno.', 'yest poh-HMOOR-noh', 'It is cloudy.'),
                card('Będzie burza.', 'BEN-jeh BOO-zhah', 'There will be a storm.'),
                card(
                    'Jest minus dziesięć stopni.',
                    'yest MEE-noos JEH-shench STOP-nee',
                    'It is minus ten degrees.',
                ),
            ],
            en('Weather, A two style.'),
            say('Jaka będzie jutro pogoda?', 'What will the weather be like tomorrow?'),
            say('Pada śnieg.', 'It is snowing.'),
            say('Wieje wiatr.', 'It is windy.'),
            say('Jest pochmurno.', 'It is cloudy.'),
            say('Będzie burza.', 'There will be a storm.'),
            say('Jest minus dziesięć stopni.', 'It is minus ten degrees.'),
            en('And the future of rain is simply [[będzie padać]].'),
            clear=True,
        ),
    ],
)


HEALTH = Scene(
    'At the doctor',
    'What hurts and what to take',
    'r',
    steps=[
        step(
            [
                grid(
                    ['głowa', 'gardło', 'brzuch', 'plecy'],
                    p=['GWOH-vah', 'GAHR-dwoh', 'bzhookh', 'PLEH-tsih'],
                    e=['head', 'throat', 'stomach', 'back'],
                    size=30,
                    h=108,
                ),
                grid(
                    ['ręka', 'noga', 'kolano', 'ząb'],
                    p=['RENG-kah', 'NOH-gah', 'koh-LAH-noh', 'zomp'],
                    e=['hand / arm', 'leg / foot', 'knee', 'tooth'],
                    size=30,
                    h=108,
                ),
                note(
                    '{Boli mnie} + body part (the person is accusative!).  Plural: {Bolą mnie} plecy.'
                ),
            ],
            en('At the doctor. Body parts first:'),
            pl('głowa, gardło, brzuch, plecy, ręka, noga, kolano, ząb.'),
            en(
                'Head, throat, stomach, back, hand, leg, knee, tooth. To say '
                'something hurts, use [[boli mnie]], literally it hurts me:'
            ),
            drill('Boli mnie głowa.'),
            say('Bolą mnie plecy.', 'My back hurts.'),
        ),
        step(
            [
                card(
                    'Co panu dolega?',
                    'tsoh PAH-noo doh-LEH-gah',
                    'What seems to be the problem? (to a man)',
                ),
                card(
                    'Mam gorączkę i katar.',
                    'mahm goh-RONCH-keh ee KAH-tar',
                    'I have a fever and a runny nose.',
                ),
                card(
                    'Jestem przeziębiony / przeziębiona.',
                    'psheh-zhyem-BYOH-nih / -nah',
                    'I have a cold. (m / f)',
                ),
                pair(
                    'Proszę brać tabletki {trzy razy dziennie}.',
                    'Take the tablets three times a day.',
                    w=WIDE,
                ),
                pair(
                    'Spadłem z roweru i boli mnie kolano.',
                    'I fell off my bike and my knee hurts.',
                    w=WIDE,
                ),
            ],
            say('Co panu dolega?', 'What seems to be the problem?'),
            say('Mam gorączkę i katar.', 'I have a fever and a runny nose.'),
            say('Jestem przeziębiony.', 'I have a cold.'),
            say(
                'Proszę brać tabletki trzy razy dziennie.',
                'Take the tablets three times a day.',
            ),
            en('And one for the cyclist, hopefully never needed:'),
            say(
                'Spadłem z roweru i boli mnie kolano.',
                'I fell off my bike and my knee hurts.',
            ),
            clear=True,
        ),
    ],
)

TRAVEL = Scene(
    'Travel & accommodation',
    'Stations, hotels, flats',
    'n',
    steps=[
        step(
            [
                pair(
                    'Poproszę bilet do {Gdańska}.',
                    'A ticket to Gdańsk, please.',
                    w=WIDE,
                ),
                pair('W jedną stronę czy w obie strony?', 'One way or return?', w=WIDE),
                pair(
                    'Z którego peronu odjeżdża pociąg?',
                    'Which platform does it leave from?',
                    w=WIDE,
                ),
                pair('Pociąg ma {opóźnienie}.', 'The train is delayed.', w=WIDE),
                pair(
                    'Muszę się {przesiąść} w Warszawie.',
                    'I have to change in Warsaw.',
                    w=WIDE,
                ),
                pair(
                    'Gdzie jest przystanek {tramwajowy}?',
                    'Where is the tram stop?',
                    w=WIDE,
                ),
            ],
            en('At the station.'),
            say('Poproszę bilet do Gdańska.', 'A ticket to [[Gdańsk]], please.'),
            say('W jedną stronę czy w obie strony?', 'One way or return?'),
            say(
                'Z którego peronu odjeżdża pociąg?',
                'Which platform does the train leave from?',
            ),
            say('Pociąg ma opóźnienie.', 'The train is delayed.'),
            say(
                'Muszę się przesiąść w Warszawie.', 'I have to change trains in Warsaw.'
            ),
            say('Gdzie jest przystanek tramwajowy?', 'Where is the tram stop?'),
        ),
        step(
            [
                pair(
                    'Mam {rezerwację} na nazwisko Smith.',
                    'I have a booking under Smith.',
                    w=WIDE,
                ),
                pair(
                    'Chciałbym pokój {dwuosobowy} na dwie noce.',
                    'A double room for two nights, please.',
                    w=WIDE,
                ),
                pair(
                    'Czy śniadanie jest wliczone w cenę?',
                    'Is breakfast included?',
                    w=WIDE,
                ),
                pair(
                    'Szukam {mieszkania} do wynajęcia.',
                    'I’m looking for a flat to rent. (+ genitive)',
                    w=WIDE,
                ),
                pair('Ile wynosi czynsz?', 'How much is the rent?', w=WIDE),
            ],
            en(
                'At the hotel, and flat hunting. Notice that [[szukać]], to look for, takes the genitive.'
            ),
            say(
                'Mam rezerwację na nazwisko Smith.',
                'I have a booking under the name Smith.',
            ),
            say(
                'Chciałbym pokój dwuosobowy na dwie noce.',
                'I would like a double room for two nights.',
            ),
            say(
                'Czy śniadanie jest wliczone w cenę?',
                'Is breakfast included in the price?',
            ),
            say('Szukam mieszkania do wynajęcia.', 'I am looking for a flat to rent.'),
            say('Ile wynosi czynsz?', 'How much is the rent?'),
            clear=True,
        ),
    ],
)

WORK = Scene(
    'Work, phone & email',
    'Your job, meetings, calls and polite emails',
    'm',
    steps=[
        step(
            [
                pair(
                    'Pracuję {jako} inżynier.',
                    'I work as an engineer. (jako + nominative)',
                    w=WIDE,
                ),
                pair(
                    'Jestem {inżynierem}.', 'I am an engineer. (instrumental)', w=WIDE
                ),
                pair(
                    'Pracuję {zdalnie}  /  {w biurze}.',
                    'I work remotely / in the office.',
                    w=WIDE,
                ),
                pair(
                    'Mam {spotkanie} o dziesiątej.', 'I have a meeting at ten.', w=WIDE
                ),
                pair('Jestem na {urlopie}.', 'I am on leave.', w=WIDE),
                pair(
                    'Szukam {nowej pracy}.',
                    'I am looking for a new job. (genitive)',
                    w=WIDE,
                ),
            ],
            en(
                'Talking about work. There are two ways to give your job: [[jako]] '
                'with the nominative, or [[jestem]] with the instrumental.'
            ),
            say('Pracuję jako inżynier.', 'I work as an engineer.'),
            say('Jestem inżynierem.', 'I am an engineer.'),
            say('Pracuję zdalnie.', 'I work remotely.'),
            say('Pracuję w biurze.', 'I work in the office.'),
            say('Mam spotkanie o dziesiątej.', 'I have a meeting at ten.'),
            say('Jestem na urlopie.', 'I am on leave.'),
            say('Szukam nowej pracy.', 'I am looking for a new job.'),
        ),
        step(
            [
                card(
                    'Halo?  ·  Słucham.',
                    'HAH-loh  ·  SWOO-hahm',
                    'Hello? (answering the phone)',
                ),
                pair(
                    'Czy mogę rozmawiać z {panią} Nowak?',
                    'May I speak to Ms Nowak?',
                    w=WIDE,
                ),
                pair('Proszę chwilę poczekać.', 'Please hold on a moment.', w=WIDE),
                pair('{Oddzwonię} później.', 'I will call back later.', w=WIDE),
                pair(
                    'Szanowna Pani  /  Szanowny Panie',
                    'Dear Madam / Dear Sir (formal email)',
                    w=WIDE,
                ),
                pair(
                    'Pozdrawiam  ·  Z poważaniem',
                    'Best regards  ·  Yours faithfully',
                    w=WIDE,
                ),
            ],
            en('On the phone:'),
            say('Halo? Słucham.', 'Hello?'),
            say('Czy mogę rozmawiać z panią Nowak?', 'May I speak to Ms Nowak?'),
            say('Proszę chwilę poczekać.', 'Please hold on a moment.'),
            say('Oddzwonię później.', 'I will call back later.'),
            en(
                'In formal emails, start with [[Szanowna Pani]] or [[Szanowny '
                'Panie]], and end with [[Pozdrawiam]], or the very formal [[Z '
                'poważaniem]].'
            ),
            clear=True,
        ),
    ],
)


SHOPPING = Scene(
    'Shopping & describing people',
    'Clothes, sizes, looks and character',
    'f',
    steps=[
        step(
            [
                grid(
                    ['koszula', 'spodnie', 'sukienka', 'kurtka'],
                    p=['koh-SHOO-lah', 'SPOD-nyeh', 'soo-KYEN-kah', 'KOORT-kah'],
                    e=['shirt', 'trousers (plural)', 'dress', 'jacket'],
                    size=30,
                    h=108,
                ),
                grid(
                    ['buty', 'sweter', 'czapka', 'okulary'],
                    p=['BOO-tih', 'SFEH-ter', 'CHAHP-kah', 'oh-koo-LAH-rih'],
                    e=['shoes', 'jumper', 'hat', 'glasses (plural)'],
                    size=30,
                    h=108,
                ),
                pair('Czy mogę to {przymierzyć}?', 'Can I try this on?', w=WIDE),
                pair(
                    'To jest {za małe}. Czy jest większy rozmiar?',
                    'Too small. Is there a bigger size?',
                    w=WIDE,
                ),
                pair(
                    'Czy mogę to {zwrócić}? Mam paragon.',
                    'Can I return it? I have the receipt.',
                    w=WIDE,
                ),
            ],
            pl('koszula, spodnie, sukienka, kurtka, buty, sweter, czapka, okulary.'),
            en(
                'Shirt, trousers, dress, jacket, shoes, jumper, hat, glasses. '
                '[[Spodnie]] and [[okulary]] exist only in the plural.'
            ),
            say('Czy mogę to przymierzyć?', 'Can I try this on?'),
            say(
                'To jest za małe. Czy jest większy rozmiar?',
                'It is too small. Is there a bigger size?',
            ),
            say(
                'Czy mogę to zwrócić? Mam paragon.',
                'Can I return it? I have the receipt.',
            ),
        ),
        step(
            [
                head('JAK ON WYGLĄDA?  = looks', 'JAKI ON JEST?  = character', al='c'),
                grid(
                    ['Jest wysoki i szczupły.', 'Jest miły i zabawny.'],
                    e=['He is tall and slim.', 'He is nice and funny.'],
                    size=28,
                    h=84,
                ),
                grid(
                    ['Ma krótkie, ciemne włosy.', 'Jest pracowity, ale nieśmiały.'],
                    e=['He has short, dark hair.', 'He is hard-working but shy.'],
                    size=28,
                    h=84,
                ),
                grid(
                    ['Ma niebieskie oczy i brodę.', 'Jest cierpliwy, nie leniwy.'],
                    e=['He has blue eyes and a beard.', 'He is patient, not lazy.'],
                    size=28,
                    h=84,
                ),
                note(
                    'Looks often use {mieć} + accusative: ma brodę.  {Mam na sobie} kurtkę. = I am wearing a jacket.'
                ),
            ],
            en(
                'Describing people. [[Jak on wygląda?]] asks about looks. [[Jaki '
                'on jest?]] asks about character.'
            ),
            pl(
                'Jest wysoki i szczupły. Ma krótkie, ciemne włosy. Ma niebieskie oczy i brodę.'
            ),
            en('He is tall and slim, with short dark hair, blue eyes and a beard.'),
            pl(
                'Jest miły i zabawny. Jest pracowity, ale nieśmiały. Jest cierpliwy, nie leniwy.'
            ),
            en('He is nice and funny, hard-working but shy, patient and not lazy.'),
            clear=True,
        ),
    ],
)

RESTAURANT = Scene(
    'At the restaurant',
    'Ordering like a local, and what to order',
    'a',
    steps=[
        step(
            [
                pair(
                    'Czy jest wolny stolik dla dwóch osób?',
                    'Is there a free table for two?',
                    w=WIDE,
                ),
                pair(
                    'Co pan {poleca}?', 'What do you recommend? (to a waiter)', w=WIDE
                ),
                pair(
                    'Na pierwsze danie poproszę {żurek}.',
                    'For the starter, the żurek please.',
                    w=WIDE,
                ),
                pair(
                    'Jestem {wegetarianinem} / {wegetarianką}.',
                    'I am vegetarian. (m / f)',
                    w=WIDE,
                ),
                pair('Czy to jest ostre?', 'Is it spicy?', w=WIDE),
                pair('Poproszę {rachunek}.', 'The bill, please.', w=WIDE),
            ],
            en('At the restaurant.'),
            say(
                'Czy jest wolny stolik dla dwóch osób?',
                'Is there a free table for two?',
            ),
            say('Co pan poleca?', 'What do you recommend?'),
            say(
                'Na pierwsze danie poproszę żurek.',
                'For the starter, I would like [[żurek]], sour rye soup.',
            ),
            say('Jestem wegetarianinem.', 'I am vegetarian, said by a man.'),
            say('Jestem wegetarianką.', 'And by a woman.'),
            say('Czy to jest ostre?', 'Is it spicy?'),
            say('Poproszę rachunek.', 'The bill, please.'),
        ),
        step(
            [
                grid(
                    ['pierogi', 'żurek', 'bigos', 'kotlet schabowy'],
                    p=['pyeh-ROH-gee', 'ZHOO-rek', 'BEE-gos', 'KOT-let shah-BOH-vih'],
                    e=[
                        'dumplings',
                        'sour rye soup',
                        "hunter's stew",
                        'breaded pork cutlet',
                    ],
                    size=28,
                    h=108,
                ),
                grid(
                    ['gołąbki', 'rosół', 'sernik', 'pączki'],
                    p=['goh-WOMP-kee', 'ROH-soow', 'SER-neek', 'PONCH-kee'],
                    e=['cabbage rolls', 'chicken broth', 'cheesecake', 'doughnuts'],
                    size=28,
                    h=108,
                ),
            ],
            en('And what to order:'),
            pl(
                'pierogi, żurek, bigos, kotlet schabowy, gołąbki, rosół, sernik, pączki.'
            ),
            en(
                'Dumplings, sour rye soup, hunters stew, pork cutlet, cabbage '
                'rolls, chicken broth, cheesecake and doughnuts. [[Smacznego!]]'
            ),
            clear=True,
        ),
    ],
)


FREE_TIME = Scene(
    'Free time & opinions',
    'Hobbies, preferences, agreeing and disagreeing',
    'a',
    steps=[
        step(
            [
                pair(
                    'Interesuję się {sportem} i {historią}.',
                    'I’m into sport and history. (+ instr.)',
                    w=WIDE,
                ),
                pair(
                    'Gram {w tenisa}  ·  gram {na gitarze}.',
                    'sport: w + acc.  ·  instrument: na + loc.',
                    w=WIDE,
                ),
                pair(
                    'W wolnym czasie jeżdżę na rowerze.',
                    'In my free time I cycle.',
                    w=WIDE,
                ),
                pair(
                    'Wolę góry {niż} morze.',
                    'I prefer the mountains to the sea.',
                    w=WIDE,
                ),
                pair(
                    'Uwielbiam jazz, ale {nie znoszę} hałasu.',
                    'I love jazz but can’t stand noise.',
                    w=WIDE,
                ),
            ],
            en('Hobbies.'),
            say(
                'Interesuję się sportem i historią.',
                'I am interested in sport and history.',
            ),
            en(
                'Interested in takes the instrumental. Playing a sport is [[grać '
                'w]] with the accusative, playing an instrument is [[grać na]] '
                'with the locative:'
            ),
            say('Gram w tenisa.', 'I play tennis.'),
            say('Gram na gitarze.', 'I play the guitar.'),
            say('W wolnym czasie jeżdżę na rowerze.', 'In my free time I cycle.'),
            say('Wolę góry niż morze.', 'I prefer the mountains to the sea.'),
            say(
                'Uwielbiam jazz, ale nie znoszę hałasu.',
                'I love jazz, but I cannot stand noise.',
            ),
        ),
        step(
            [
                card('Moim zdaniem…', 'MOH-eem ZDAH-nyem', 'In my opinion…'),
                card('Masz rację.', 'mahsh RAH-tsyeh', 'You are right.'),
                card(
                    'Zgadzam się. / Nie zgadzam się.',
                    'ZGAH-dzahm sheh',
                    'I agree. / I disagree.',
                ),
                card('Cieszę się!', 'CHEH-sheh sheh', 'I am glad!'),
                card(
                    'Martwię się o ciebie.',
                    'MAR-tvyeh sheh oh CHEH-byeh',
                    'I am worried about you.',
                ),
            ],
            en('Opinions and feelings.'),
            say('Moim zdaniem…', 'In my opinion.'),
            say('Masz rację.', 'You are right.'),
            say('Zgadzam się. Nie zgadzam się.', 'I agree. I disagree.'),
            say('Cieszę się!', 'I am glad!'),
            say('Martwię się o ciebie.', 'I am worried about you.'),
            clear=True,
        ),
    ],
)

WISHES = Scene(
    'Celebrations & wishes',
    'Wishes are genitive: they hide “życzę”',
    'g',
    steps=[
        step(
            [
                card(
                    'Wszystkiego najlepszego!',
                    'fshist-KYEH-goh nai-lep-SHEH-goh',
                    'All the best! (birthdays, name days)',
                ),
                card('Sto lat!', 'stoh laht', 'A hundred years! (the birthday song)'),
                card(
                    'Wesołych Świąt!',
                    'veh-SOH-wikh SHVYONT',
                    'Merry Christmas / Happy Easter!',
                ),
                card(
                    'Szczęśliwego Nowego Roku!',
                    'shchen-shlee-VEH-goh noh-VEH-goh ROH-koo',
                    'Happy New Year!',
                ),
                card('Gratuluję!', 'grah-too-LOO-yeh', 'Congratulations!'),
            ],
            en(
                'Celebrations. Polish wishes are in the genitive, because they '
                'hide the verb [[życzę]], I wish, which takes the genitive.'
            ),
            drill('Wszystkiego najlepszego!'),
            say('Sto lat!', 'A hundred years, the birthday song.'),
            say('Wesołych Świąt!', 'Happy holidays, for Christmas and Easter.'),
            say('Szczęśliwego Nowego Roku!', 'Happy New Year!'),
            say('Gratuluję!', 'Congratulations!'),
        ),
        step(
            [
                pair(
                    'Życzę {ci} {zdrowia} i {szczęścia}!',
                    'I wish you health and happiness!',
                    w=WIDE,
                ),
                pair('Wigilia', 'Christmas Eve supper, 24 December', w=[0.4, 0.6]),
                pair('imieniny', 'name day: often bigger than birthdays', w=[0.4, 0.6]),
                pair('Wielkanoc', 'Easter', w=[0.4, 0.6]),
                pair('Boże Narodzenie', 'Christmas', w=[0.4, 0.6]),
                pair(
                    'Andrzejki',
                    'St Andrew’s Eve (29 Nov): fortune-telling party',
                    w=[0.4, 0.6],
                ),
            ],
            say('Życzę ci zdrowia i szczęścia!', 'I wish you health and happiness.'),
            en(
                'That one sentence uses the dative for the person and the '
                'genitive for the wish. And the big days:'
            ),
            say('Wigilia', 'Christmas Eve supper, on the twenty fourth of December.'),
            say('imieniny', 'name day, often celebrated more than birthdays.'),
            say('Wielkanoc', 'Easter.'),
            say('Boże Narodzenie', 'Christmas.'),
            say(
                'Andrzejki',
                'Saint Andrews Eve, a fortune-telling party at the end of November.',
            ),
            clear=True,
        ),
    ],
)

STORY_LINES = [
    (
        'W sobotę {g|pojechałem} rowerem do Tyńca.',
        'On Saturday I rode my bike to Tyniec.',
    ),
    (
        'Było ciepło, więc {jechałem} powoli wzdłuż Wisły.',
        'It was warm, so I rode slowly along the Vistula.',
    ),
    (
        'Po drodze {g|zatrzymałem się} w kawiarni i {g|wypiłem} kawę.',
        'On the way I stopped at a café for a coffee.',
    ),
    (
        'Kiedy {wracałem}, {g|zaczęło} padać.',
        'As I was heading back, it started to rain.',
    ),
    (
        'Do domu {g|przyjechałem} mokry, ale bardzo zadowolony.',
        'I got home wet, but very happy.',
    ),
]
STORY_TEXT = ' '.join(
    line.replace('{g|', '').replace('{', '').replace('}', '') for line, _ in STORY_LINES
)

STORY = Scene(
    'Listening: a bike ride',
    'Kraków to Tyniec abbey along the Vistula',
    'n',
    steps=[
        step(
            [
                big('Listen first.', 64, 'a', 110),
                big('No reading yet: what happened, and in what order?', 30, None, 60),
            ],
            en(
                'Story time. Listen to the whole story first, without reading. It '
                'is about a bike ride from [[Kraków]] to [[Tyniec]], an old abbey '
                'on the Vistula river.'
            ),
            gap(0.6),
            nt(STORY_TEXT),
        ),
        step(
            [pair(line, meaning, w=[0.62, 0.38]) for line, meaning in STORY_LINES],
            en('Now read along, slowly.'),
            [
                [
                    ns(line.replace('{g|', '').replace('{', '').replace('}', '')),
                    gap(0.6),
                ]
                for line, _ in STORY_LINES
            ],
            clear=True,
        ),
        step(
            [
                note(
                    'Aspect: {jechałem, wracałem} = background · {g|pojechałem, '
                    'zatrzymałem się, wypiłem, zaczęło, przyjechałem} = events.  '
                    'Cases: do Tyńca, wzdłuż Wisły (gen.) · rowerem (instr.) · w kawiarni (loc.)'
                ),
            ],
            en(
                'Spot the aspect. [[Jechałem]] and [[wracałem]] are imperfective: '
                'the background. [[Pojechałem, zatrzymałem się, wypiłem, zaczęło]] '
                'and [[przyjechałem]] are perfective: the events. And the cases: '
                '[[do Tyńca]] and [[wzdłuż Wisły]] are genitive, [[rowerem]] is '
                'instrumental, and [[w kawiarni]] is locative.'
            ),
        ),
    ],
)

ROLE_PLAYS = Scene(
    'Role-plays',
    'Pause after each line and answer before the model',
    'f',
    steps=[
        step(
            [
                pair(
                    'Dzień dobry. Co pani dolega?',
                    'Hello. What seems to be the problem?',
                    'm',
                    w=WIDE,
                ),
                pair(
                    'Od wczoraj boli mnie gardło i mam gorączkę.',
                    'My throat has hurt since yesterday, and I have a fever.',
                    'f',
                    w=WIDE,
                ),
                pair(
                    'To przeziębienie. Proszę dużo pić i odpoczywać.',
                    'It’s a cold. Drink a lot and rest.',
                    'm',
                    w=WIDE,
                ),
                pair(
                    'Czy potrzebuję antybiotyku?',
                    'Do I need antibiotics? (+ genitive)',
                    'f',
                    w=WIDE,
                ),
                pair(
                    'Nie. Wystarczy syrop i trzy dni w domu.',
                    'No. Syrup and three days at home will do.',
                    'm',
                    w=WIDE,
                ),
                pair(
                    'Dziękuję, panie doktorze.',
                    'Thank you, doctor. (vocative)',
                    'f',
                    w=WIDE,
                ),
            ],
            en(
                'Role-play one: at the doctor. You are the patient, in pink. '
                'After each doctor line, answer out loud before you hear the model.'
            ),
            nt('Dzień dobry. Co pani dolega?'),
            gap(2.2),
            pl('Od wczoraj boli mnie gardło i mam gorączkę.'),
            gap(0.4),
            nt('To przeziębienie. Proszę dużo pić i odpoczywać.'),
            gap(2.2),
            pl('Czy potrzebuję antybiotyku?'),
            gap(0.4),
            nt('Nie. Wystarczy syrop i trzy dni w domu.'),
            gap(2.2),
            pl('Dziękuję, panie doktorze.'),
        ),
        step(
            [
                pair(
                    'Poproszę bilet do Wrocławia na jutro rano.',
                    'A ticket to Wrocław for tomorrow morning.',
                    'f',
                    w=WIDE,
                ),
                pair(
                    'W jedną stronę czy w obie strony?',
                    'One way or return?',
                    'm',
                    w=WIDE,
                ),
                pair(
                    'W obie strony. Ile to kosztuje?',
                    'Return. How much is it?',
                    'f',
                    w=WIDE,
                ),
                pair(
                    'Sto osiemdziesiąt złotych. Odjazd o siódmej piętnaście.',
                    '180 zloty. It leaves at 7:15.',
                    'm',
                    w=WIDE,
                ),
                pair(
                    'Z którego peronu? Czy muszę się przesiadać?',
                    'Which platform? Do I have to change?',
                    'f',
                    w=WIDE,
                ),
                pair(
                    'Z peronu trzeciego. Nie, to pociąg bezpośredni.',
                    'Platform three. No, it’s a direct train.',
                    'm',
                    w=WIDE,
                ),
            ],
            en(
                'Role-play two: the ticket office. This time you speak first. Read '
                'the pink line out loud, then listen to the model.'
            ),
            gap(2.5),
            pl('Poproszę bilet do Wrocławia na jutro rano.'),
            gap(0.4),
            nt('W jedną stronę czy w obie strony?'),
            gap(2.0),
            pl('W obie strony. Ile to kosztuje?'),
            gap(0.4),
            nt('Sto osiemdziesiąt złotych. Odjazd o siódmej piętnaście.'),
            gap(2.0),
            pl('Z którego peronu? Czy muszę się przesiadać?'),
            gap(0.4),
            nt('Z peronu trzeciego. Nie, to pociąg bezpośredni.'),
            clear=True,
        ),
    ],
)

QUIZ_TOTAL = 14
QUIZ = Scene(
    'Quiz time',
    'Answer out loud before the timer ends',
    'a',
    steps=(
        quiz(
            1,
            QUIZ_TOTAL,
            'Perfective partner of robić?',
            en('Question one. What is the perfective partner of [[robić]]?'),
            'zrobić',
            'Prefix z-: robić → zrobić.',
            en('Just add the prefix [[z]].'),
        )
        + quiz(
            2,
            QUIZ_TOTAL,
            'Say: Yesterday I read the whole book. (man, finished)',
            en(
                'Question two. Say: yesterday I read the whole book, if you are a man and you finished it.'
            ),
            'Wczoraj przeczytałem całą książkę.',
            'Finished result → perfective.',
            en('A finished result needs the perfective, [[przeczytałem]].'),
        )
        + quiz(
            3,
            QUIZ_TOTAL,
            'Say: I help my mum.',
            en('Question three. Say: I help my mum.'),
            'Pomagam mamie.',
            'pomagać + dative: mama → mamie.',
            en('[[Pomagać]] takes the dative, so [[mama]] becomes [[mamie]].'),
        )
        + quiz(
            4,
            QUIZ_TOTAL,
            'Plural of student (a group of men)?',
            en('Question four. What is the plural of [[student]], for a group of men?'),
            'studenci',
            'Virile plural: t → ci.',
            en('Virile plural softens t to c i.'),
        )
        + quiz(
            5,
            QUIZ_TOTAL,
            'Five books = pięć … ?',
            en('Question five. How do you say five books?'),
            'pięć książek',
            'Five and up → genitive plural.',
            en('Five and up takes the genitive plural, with a helper e.'),
        )
        + quiz(
            6,
            QUIZ_TOTAL,
            'Tell a friend: Don’t do it!',
            en('Question six. Tell a friend: do not do it!'),
            'Nie rób tego!',
            'Negative command: imperfective + genitive.',
            en('Negative commands use the imperfective, and [[to]] becomes [[tego]].'),
        )
        + quiz(
            7,
            QUIZ_TOTAL,
            'Politely: I would like… (said by a woman)',
            en('Question seven. Say I would like, politely, if you are a woman.'),
            'Chciałabym',
            'Past form + by + m.',
            en('The past form [[chciała]], plus [[bym]].'),
        )
        + quiz(
            8,
            QUIZ_TOTAL,
            'Comparative of dobry?',
            en('Question eight. What is the comparative of [[dobry]]?'),
            'lepszy',
            'Irregular: dobry, lepszy, najlepszy.',
            en('Irregular, just like good, better, best.'),
        )
        + quiz(
            9,
            QUIZ_TOTAL,
            'Say: Every day I walk to work.',
            en('Question nine. Say: every day I walk to work.'),
            'Codziennie chodzę do pracy.',
            'A habit → chodzić, not iść.',
            en('A habit needs [[chodzić]], not [[iść]].'),
        )
        + quiz(
            10,
            QUIZ_TOTAL,
            'Say: I am going by train.',
            en('Question ten. Say: I am going by train.'),
            'Jadę pociągiem.',
            'Transport → instrumental.',
            en('Transport goes in the instrumental.'),
        )
        + quiz(
            11,
            QUIZ_TOTAL,
            'Say the date: on the 5th of May',
            en('Question eleven. Say: on the fifth of May.'),
            'Piątego maja.',
            'On a date → genitive day + genitive month.',
            en('On a date, both the day and the month are genitive.'),
        )
        + quiz(
            12,
            QUIZ_TOTAL,
            'Tell the doctor: I have a headache.',
            en('Question twelve. Tell the doctor that you have a headache.'),
            'Boli mnie głowa.',
            'boleć + mnie: literally “my head hurts me”.',
            en('Literally, the head hurts me.'),
        )
        + quiz(
            13,
            QUIZ_TOTAL,
            'Say: I know Kraków (I am familiar with it).',
            en(
                'Question thirteen. Say: I know [[Kraków]], meaning you are familiar with the city.'
            ),
            'Znam Kraków.',
            'Places and people → znać, not wiedzieć.',
            en('Places and people need [[znać]].'),
        )
        + quiz(
            14,
            QUIZ_TOTAL,
            'Say: I am waiting for the bus.',
            en('Question fourteen. Say: I am waiting for the bus.'),
            'Czekam na autobus.',
            'czekać na + accusative.',
            en('[[Czekać na]] takes the accusative.'),
        )
    ),
)

RECAP = Scene(
    'Recap & what is next',
    'Five anchors for A2, then on to B1',
    'g',
    steps=[
        step(
            [
                card(
                    'Zrobię to jutro.',
                    'ZROH-byeh toh YOO-troh',
                    'ASPECT: perfective = future',
                    'a',
                ),
                card('Pomagam mamie.', 'poh-MAH-gahm MAH-myeh', 'DATIVE: to whom', 'm'),
                card(
                    'Mam dużo książek.',
                    'mahm DOO-zhoh KSHON-zhek',
                    'GENITIVE PLURAL: amounts',
                    'f',
                ),
                card(
                    'Codziennie chodzę, teraz idę.',
                    'tsoh-JEN-nyeh HOH-dzeh, TEH-rahs EE-deh',
                    'MOTION: habit vs now',
                    'n',
                ),
                card(
                    'Chciałbym lepszą kawę.',
                    'HCHOW-bim LEP-shohm KAH-veh',
                    'CONDITIONAL + COMPARATIVE',
                    'r',
                ),
            ],
            en('Time to wrap up. Five anchor sentences hold almost all of A two.'),
            say('Zrobię to jutro.', 'I will do it tomorrow: perfective means future.'),
            say('Pomagam mamie.', 'I help my mum: the dative.'),
            say('Mam dużo książek.', 'I have lots of books: the genitive plural.'),
            say(
                'Codziennie chodzę, teraz idę.',
                'Every day I walk, right now I am walking: motion verbs.',
            ),
            say(
                'Chciałbym lepszą kawę.',
                'I would like a better coffee: conditional and comparative.',
            ),
        ),
        step(
            [
                head('COMING IN B1'),
                pair('Participles', 'czytający · przeczytany'),
                pair('Passive voice', 'Most został zbudowany.'),
                pair('Verbal nouns', 'czytanie · pływanie · jazda na rowerze'),
                pair('Reported speech', 'Powiedział, że przyjdzie.'),
                note(
                    'Practice: retell the bike story as if a woman rode to Tyniec: '
                    '{pojechała, jechała, zatrzymała się…}'
                ),
            ],
            en(
                'In B one you will meet participles, the passive voice, verbal '
                'nouns and reported speech. Before that, one exercise: retell the '
                'bike story out loud as if a woman rode to [[Tyniec]]. '
                '[[Pojechała, jechała, zatrzymała się.]] If you can do that, your '
                'A two is solid.'
            ),
            clear=True,
        ),
        step(
            [
                big('Powodzenia!', 100, 'a', 140),
                big('Good luck with A2 and beyond', 30, None, 60),
            ],
            pl('Powodzenia! Do zobaczenia na poziomie B1!'),
            en('Good luck, and see you at B one.'),
            clear=True,
        ),
    ],
)

SCENES = [
    COVER,
    SOUNDS,
    CASE_MAP,
    DATIVE,
    PLURAL,
    GEN_PLURAL,
    MORE_PLURALS,
    PRONOUNS,
    VERB_CASES,
    TRICKY,
    ASPECT,
    PAST,
    FUTURE,
    MOTION,
    IMPERATIVE,
    CONDITIONAL,
    COMPARE,
    MODALS,
    LINKING,
    INDEFINITE,
    DATES,
    TIME_WEATHER,
    HEALTH,
    TRAVEL,
    WORK,
    SHOPPING,
    RESTAURANT,
    FREE_TIME,
    WISHES,
    STORY,
    ROLE_PLAYS,
    QUIZ,
    RECAP,
]

two_line_cards(SCENES)
