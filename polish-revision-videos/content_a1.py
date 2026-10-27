"""Lesson script for the Polish A1 revision video (see lesson.py for markup)."""
# pylint: disable=too-many-lines

from lesson import (
    Scene,
    big,
    card,
    conj,
    drill,
    en,
    gap,
    grid,
    head,
    lst,
    note,
    nt,
    pair,
    pl,
    ps,
    rule,
    say,
    step,
)

META = {'title': 'Polish A1', 'slug': 'polish_a1'}

# ===================================================================== SCENES
COVER = Scene(
    'Polish A1',
    'Full revision',
    'a',
    cover=True,
    steps=[
        step(
            [
                big('Polish A1', 112, 'a', 150),
                big('Full Revision', 62, None, 90),
                big('Grammar  ·  Vocabulary  ·  Pronunciation', 29, None, 56),
                big('20 minutes  ·  made for English speakers', 25, None, 50),
            ],
            pl('Cześć!'),
            en(
                'Welcome to your Polish A one revision sprint. Twenty minutes, '
                'everything you need before your A two class tonight. I will '
                'explain in English, say every Polish word out loud, and show '
                'you an English friendly respelling on screen.'
            ),
        ),
        step(
            [
                head('THE MAP'),
                lst('1  Sounds & stress', '2  Greetings', '3  About me'),
                lst('4  To be', '5  Gender & plurals', '6  Adjectives'),
                lst('7  Verbs', '8  Questions & no', '9  The four cases'),
                lst('10  Prepositions', '11  Numbers & time', '12  Survival words'),
                lst('13  False friends', '14  Past & future', '15  Café scene'),
                lst('16  Quiz time', '17  Recap & A2', ''),
            ],
            en(
                'Here is the map. Sounds, greetings, talking about yourself, '
                'the verb to be, gender and plurals, adjectives, verbs, '
                'questions, the four cases, prepositions of place, numbers and time, '
                'survival vocabulary, false friends, past and future, a café '
                'scene, then a quiz. Say everything out '
                'loud with me. Your mouth needs the practice more than your eyes.'
            ),
            clear=True,
        ),
    ],
)

SOUNDS = Scene(
    'Sounds & stress',
    'Polish is spelled exactly as it sounds',
    'n',
    steps=[
        step(
            [
                note(
                    'Good news: Polish is phonetic. Learn about 30 sounds once and '
                    'you can read any word aloud. {No silent letters.}'
                ),
                head('STRESS = the second-to-last syllable', w=[1]),
                pair('{PRO}-szę', 'please'),
                pair('dzię-{KU}-ję', 'thank you'),
                pair('u-ni-{WER}-sy-tet', 'university'),
            ],
            en(
                'Good news first. Polish is phonetic. Learn the sounds once, '
                'and you can read any word aloud. No silent letters. And stress '
                'is almost always on the second to last syllable. '
            ),
            pl('proszę'),
            gap(0.2),
            pl('dziękuję'),
            gap(0.2),
            pl('uniwersytet'),
        ),
        step(
            [
                head('LETTER', 'SOUNDS LIKE', 'EXAMPLE'),
                card('ą', 'nasal “on”', 'są = they are'),
                card('ę', 'nasal “en” (at the end: “eh”)', 'proszę = please'),
                card('ó', 'exactly like u: “oo”', 'córka = daughter'),
                card('y', 'short i, as in bit', 'dobry = good'),
            ],
            en('Four vowels to watch. A with a tail is a nasal on, as in'),
            pl('są'),
            en(
                'they are. E with a tail is a nasal en, but at the end of a word '
                'it is just eh, as in'
            ),
            pl('proszę'),
            en('O with a bar is simply oo, as in'),
            pl('córka'),
            en('daughter. And y is a short i, like in bit:'),
            pl('dobry'),
            clear=True,
        ),
        step(
            [
                head('LETTER', 'SOUNDS LIKE', 'EXAMPLE'),
                card('ł', 'English “w”', 'mały = small  (MAH-wih)'),
                card('w', 'English “v”', 'woda = water  (VOH-dah)'),
                card('j', 'English “y”', 'jak = how  (yahk)'),
                card('c', '“ts” as in cats', 'co = what  (tsoh)'),
                card('ch / h', 'rough “h” in the throat', 'chleb = bread  (hlep)'),
            ],
            en('Next, the letters that trick English speakers. L with a slash is a w:'),
            pl('mały.'),
            en('Plain w is a v:'),
            pl('woda.'),
            en('J is a y:'),
            pl('jak.'),
            en('C is ts:'),
            pl('co.'),
            en('And ch and h are the same rough h sound:'),
            pl('chleb.'),
            clear=True,
        ),
        step(
            [
                head('SPELLING', 'SOUNDS LIKE', 'EXAMPLE'),
                card('sz', '“sh”', 'szkoła = school  (SHKOH-wah)'),
                card('cz', '“ch”', 'czas = time  (chahs)'),
                card('ż  /  rz', '“zh” as in pleasure', 'żona = wife  (ZHOH-nah)'),
                card('dż', 'English “j”', 'dżem = jam  (jem)'),
                card('szcz', '“shch” – say both', 'szczęście = luck'),
            ],
            en('Now the hushing sounds. S Z is sh:'),
            pl('szkoła.'),
            en('C Z is ch:'),
            pl('czas.'),
            en('Both z with a dot, and r z, are the zh in pleasure:'),
            pl('żona,'),
            pl('rzeka.'),
            en('D z with a dot is a j:'),
            pl('dżem.'),
            clear=True,
        ),
        step(
            [
                head('SOFT SOUND', 'SOUNDS LIKE', 'EXAMPLE'),
                card('ś / si', 'soft “sh”', 'siostra = sister  (SHOH-strah)'),
                card('ć / ci', 'soft “ch”', 'ciocia = aunt  (CHOH-chah)'),
                card('ź / zi', 'soft “zh”', 'zima = winter  (ZHEE-mah)'),
                card('ń / ni', '“ny” as in canyon', 'nie = no  (nyeh)'),
                card('dź / dzi', 'soft “j”', 'dziecko = child  (JETS-koh)'),
            ],
            en(
                'Last family: the soft sounds. The trick: an i after s, c, z, n '
                'or d z softens the letter, and it is not a separate vowel. '
            ),
            pl('siostra,'),
            pl('ciocia,'),
            pl('zima,'),
            en('and'),
            pl('nie.'),
            en('Same sounds as the four accented letters.'),
            clear=True,
        ),
        step(
            [
                big('{W Szczebrzeszynie} chrząszcz brzmi w trzcinie', 40, None, 70),
                big(
                    'v shcheh-bzheh-SHIH-nyeh  khshonshch  bzhmee  v tshee-CHEE-nyeh',
                    24,
                    'a',
                    44,
                ),
                big('“In Szczebrzeszyn, a beetle buzzes in the reeds.”', 26, None, 50),
            ],
            en(
                'Ready for a challenge? The most famous Polish tongue twister. '
                'Slowly first.'
            ),
            ps('W Szczebrzeszynie chrząszcz brzmi w trzcinie.'),
            gap(0.8),
            en('Now at speed.'),
            pl('W Szczebrzeszynie chrząszcz brzmi w trzcinie.'),
            en('If you can say that, tonight is easy.'),
            clear=True,
        ),
    ],
)

GREETINGS = Scene(
    'Greetings & politeness',
    'Say them out loud, twice',
    'a',
    steps=[
        step(
            [
                card('Cześć!', 'cheshch', 'Hi!  or  Bye!  (friends)'),
                card('Dzień dobry', 'jen DOH-bri', 'Good day / morning (formal)'),
                card('Dobry wieczór', 'DOH-bri VYEH-choor', 'Good evening'),
                card('Dobranoc', 'doh-BRAH-nots', 'Good night'),
            ],
            en('Greetings. With friends, one word does hello and goodbye:'),
            drill('Cześć!'),
            en('With anyone else, use'),
            drill('Dzień dobry'),
            en('all day, until the evening, then'),
            pl('Dobry wieczór.'),
            en('At bedtime:'),
            pl('Dobranoc.'),
        ),
        step(
            [
                card('Do widzenia', 'doh vee-JEN-yah', 'Goodbye (formal)'),
                card('Na razie / Pa', 'nah RAH-zhyeh / pah', 'See you / Bye (casual)'),
                card('Proszę', 'PROH-sheh', 'Please / Here you go / You’re welcome'),
                card('Dziękuję', 'jen-KOO-yeh', 'Thank you'),
                card('Przepraszam', 'psheh-PRAH-shahm', 'Sorry / Excuse me'),
            ],
            en('To leave politely:'),
            pl('Do widzenia.'),
            en('Casually:'),
            pl('Na razie.'),
            en('The big three:'),
            drill('Proszę'),
            drill('Dziękuję'),
            drill('Przepraszam'),
            clear=True,
        ),
        step(
            [
                pair('{ty}', 'informal you: friends, family, kids'),
                pair('{Pan}  /  {Pani}', 'formal you: Mr / Ms'),
                pair(
                    'Czy {pani} mówi po angielsku?',
                    'Do you speak English? (to a woman)',
                ),
                pair('{Tak}  /  {Nie}', 'yes  /  no'),
            ],
            en(
                'One cultural rule. Polish has an informal you, [[ty]], for friends '
                'and family. For strangers and professionals you say [[pan]] to a '
                'man and [[pani]] to a woman, in the third person. '
            ),
            pl('Czy pani mówi po angielsku?'),
            en('Do you speak English? And yes and no are'),
            pl('tak'),
            en('and'),
            pl('nie.'),
            clear=True,
        ),
    ],
)

ABOUT_ME = Scene(
    'Introducing yourself',
    'A mini conversation you will use all week',
    'f',
    steps=[
        step(
            [
                card(
                    'Cześć! Jak się masz?',
                    'cheshch. yak sheh mahsh',
                    'Hi! How are you?',
                ),
                card(
                    'Dobrze, dziękuję. A ty?',
                    'DOB-zheh jen-KOO-yeh. ah tih',
                    'Fine, thanks. And you?',
                ),
                card(
                    'Jak masz na imię?', 'yak mahsh nah EE-myeh', 'What is your name?'
                ),
                card(
                    'Mam na imię Tom. Miło mi!',
                    'mahm nah EE-myeh tom. MEE-woh mee',
                    'I am Tom. Nice to meet you!',
                ),
            ],
            en('Listen to a mini conversation.'),
            nt('Cześć! Jak się masz?'),
            gap(0.2),
            pl('Dobrze, dziękuję. A ty?'),
            gap(0.2),
            nt('Dobrze. Jak masz na imię?'),
            gap(0.2),
            pl('Mam na imię Anna. Miło mi!'),
            gap(0.3),
            en('You can also say'),
            pl('Nazywam się Anna.'),
            en('Both mean my name is.'),
        ),
        step(
            [
                card('Skąd jesteś?', 'skont YES-tesh', 'Where are you from?'),
                card('Jestem z Anglii.', 'YES-tem z AHN-glee', 'I am from England.'),
                card(
                    'Mieszkam w Krakowie.',
                    'MYESH-kahm v krah-KOH-vyeh',
                    'I live in Kraków.',
                ),
                card(
                    'Uczę się polskiego.',
                    'OO-cheh sheh pol-SKEH-goh',
                    'I am learning Polish.',
                ),
                card(
                    'Lubię jeździć na rowerze.',
                    'LOO-byeh YEZH-jeech nah roh-VEH-zheh',
                    'I like riding my bike.',
                ),
            ],
            en('Now the answers.'),
            say('Skąd jesteś?', 'Where are you from?'),
            say('Jestem z Anglii.', 'I am from England. Swap in your own country.'),
            say('Mieszkam w Krakowie.', 'I live in Kraków.'),
            say('Uczę się polskiego.', 'I am learning Polish.'),
            say('Lubię jeździć na rowerze.', 'I like riding my bike.'),
            clear=True,
        ),
    ],
)

TO_BE = Scene(
    'To be: być',
    'The most important verb in the language',
    'm',
    steps=[
        step(
            [
                head('ja', 'ty', 'on / ona / ono', 'my', 'wy', 'oni / one', al='c'),
                grid(
                    ['jestem', 'jesteś', 'jest', 'jesteśmy', 'jesteście', 'są'],
                    p=[
                        'YES-tem',
                        'YES-tesh',
                        'yest',
                        'yes-TESH-mih',
                        'yes-TESH-cheh',
                        'sohm',
                    ],
                    e=[
                        'I am',
                        'you are',
                        'he / she / it is',
                        'we are',
                        'you (pl) are',
                        'they are',
                    ],
                    size=30,
                    h=108,
                ),
            ],
            en('[[Być]], to be. The most important verb in the language.'),
            pl('jestem, jesteś, jest, jesteśmy, jesteście, są.'),
            gap(0.5),
            en('Again, slower, and say it with me.'),
            ps('jestem, jesteś, jest, jesteśmy, jesteście, są.'),
            gap(1.0),
        ),
        step(
            [
                pair(
                    'Nie ma “a” or “the”!', 'Jestem studentem. = I am a student.', 'g'
                ),
                pair('Pronouns are optional', 'Jestem Tom. = I (am) Tom.'),
                pair('Adjectives match gender', 'Jestem zmęczon{m|y} / zmęczon{f|a}'),
                pair(
                    'Negative: put {nie} first',
                    '{Nie} jestem głodny. = I am not hungry.',
                ),
            ],
            en(
                'Three relief points. Polish has no articles, no a and no the. '
                'You can drop the pronoun, because the ending already says who. '
                'And adjectives after [[jestem]] match your gender: a man says'
            ),
            pl('jestem zmęczony,'),
            en('a woman says'),
            pl('jestem zmęczona.'),
            en('To say not, put [[nie]] in front:'),
            pl('nie jestem głodny.'),
            clear=True,
        ),
    ],
)

GENDER = Scene(
    'Gender & plurals',
    'Three genders, three colours',
    'n',
    steps=[
        step(
            [
                head('GENDER', 'USUAL ENDING  →  EXAMPLES'),
                pair('{m|MASCULINE}  (m)', 'consonant: dom · rower · pies · stół', 'm'),
                pair('{f|FEMININE}  (f)', '-a: kawa · książka · woda · siostra', 'f'),
                pair('{n|NEUTER}  (n)', '-o / -e: okno · miasto · piwo · morze', 'n'),
                note(
                    'Exceptions: {m|mężczyzna} (man) looks feminine but is masculine; '
                    '{f|noc} (night) looks masculine but is feminine.'
                ),
            ],
            en(
                'Every noun has a gender, and you can usually see it in the '
                'ending. Masculine ends in a consonant. '
            ),
            say('dom', 'house'),
            say('rower', 'bike'),
            say('pies', 'dog'),
            en('Feminine ends in a:'),
            say('kawa', 'coffee'),
            say('książka', 'book'),
            say('woda', 'water'),
            en('Neuter ends in o or e:'),
            say('okno', 'window'),
            say('miasto', 'city'),
            say('piwo', 'beer'),
            en(
                'Watch out for [[mężczyzna]], man, which is masculine, and [[noc]], '
                'night, which is feminine.'
            ),
        ),
        step(
            [
                head('SINGULAR  →  PLURAL', 'RULE'),
                pair('dom → dom{y}', 'm: add -y  (house → houses)', 'm'),
                pair('rower → rower{y}', 'm: add -y  (bike → bikes)', 'm'),
                pair('kawa → kaw{y}', 'f: -a becomes -y', 'f'),
                pair('książka → książk{i}', 'f: -i after k and g', 'f'),
                pair('okno → okn{a}', 'n: -o becomes -a', 'n'),
                pair('miasto → miast{a}', 'n: -o becomes -a', 'n'),
            ],
            en(
                'Plurals. Masculine adds y. Feminine swaps a for y, or for i '
                'after k and g. Neuter swaps o for a.'
            ),
            say('domy', 'houses'),
            say('kawy', 'coffees'),
            say('książki', 'books'),
            say('okna', 'windows'),
            say('miasta', 'cities'),
            clear=True,
        ),
        step(
            [
                note(
                    'Learn these by heart: {dziecko → dzieci} (child → children), '
                    '{człowiek → ludzie} (person → people), '
                    '{brat → bracia} (brother → brothers).'
                ),
            ],
            en('Three irregular plurals worth memorising:'),
            say('dziecko, dzieci', 'child, children'),
            say('człowiek, ludzie', 'person, people'),
            say('brat, bracia', 'brother, brothers'),
            clear=True,
        ),
    ],
)

ADJECTIVES = Scene(
    'Adjectives & possessives',
    'They copy the gender of the noun',
    'f',
    steps=[
        step(
            [
                head('{m|MASCULINE}', '{f|FEMININE}', '{n|NEUTER}', al='c'),
                grid(
                    ['dobry rower', 'dobra kawa', 'dobre piwo'],
                    p=['DOH-bri ROH-vehr', 'DOH-brah KAH-vah', 'DOH-breh PEE-voh'],
                    e=['a good bike', 'a good coffee', 'a good beer'],
                    h=104,
                ),
                grid(
                    ['nowy dom', 'nowa książka', 'nowe okno'],
                    p=['NOH-vih dom', 'NOH-vah KSHONSH-kah', 'NOH-veh OHK-noh'],
                    e=['a new house', 'a new book', 'a new window'],
                    h=104,
                ),
                grid(
                    ['duży pies', 'duża kawa', 'duże miasto'],
                    p=['DOO-zhih pyes', 'DOO-zhah KAH-vah', 'DOO-zheh MYAH-stoh'],
                    e=['a big dog', 'a big coffee', 'a big city'],
                    h=104,
                ),
            ],
            en(
                'Adjectives match the noun. Masculine ends in y, feminine in a, '
                'neuter in e. '
            ),
            say('dobry rower', 'a good bike'),
            say('dobra kawa', 'a good coffee'),
            say('dobre piwo', 'a good beer'),
            say('nowy dom', 'a new house'),
            say('nowa książka', 'a new book'),
            say('nowe okno', 'a new window'),
            say('duży pies', 'a big dog'),
            say('duża kawa', 'a big coffee'),
            say('duże miasto', 'a big city'),
        ),
        step(
            [
                head('{m|MASCULINE}', '{f|FEMININE}', '{n|NEUTER}', al='c'),
                grid(
                    ['mój', 'moja', 'moje'],
                    p=['mooy', 'MOH-yah', 'MOH-yeh'],
                    e=['my', 'my', 'my'],
                    h=104,
                ),
                grid(
                    ['twój', 'twoja', 'twoje'],
                    p=['tvooy', 'TVOH-yah', 'TVOH-yeh'],
                    e=['your', 'your', 'your'],
                    h=104,
                ),
                grid(
                    ['nasz', 'nasza', 'nasze'],
                    p=['nahsh', 'NAH-shah', 'NAH-sheh'],
                    e=['our', 'our', 'our'],
                    h=104,
                ),
                note('{jego} (his) · {jej} (her) · {ich} (their) never change.'),
            ],
            en(
                'Possessives work the same way. My: [[mój, moja, moje.]] Your: [[twój, '
                'twoja, twoje.]] Our: [[nasz, nasza, nasze.]] His, her and their never '
                'change: [[jego, jej, ich.]] For example:'
            ),
            pl('To jest mój rower. To jest moja kawa. To jest moje miasto.'),
            clear=True,
        ),
        step(
            [
                head('{m|MASCULINE}', '{f|FEMININE}', '{n|NEUTER}', al='c'),
                grid(
                    ['ten dom', 'ta kawa', 'to miasto'],
                    p=['ten dohm', 'tah KAH-vah', 'toh MYAH-stoh'],
                    e=['this house', 'this coffee', 'this city'],
                    h=104,
                ),
                pair('{To jest} mój dom.', 'This is my house.'),
                pair('{To są} moje książki.', 'These are my books.'),
                pair(
                    '{Co to jest?}  —  To jest ser.', 'What is this?  —  It is cheese.'
                ),
            ],
            en(
                'To point at things, use [[ten, ta, to]]. This house, this coffee, '
                'this city.'
            ),
            say('ten dom', 'this house'),
            say('ta kawa', 'this coffee'),
            say('to miasto', 'this city'),
            en(
                'And to introduce anything, use [[to jest]] for one thing and '
                '[[to są]] for many.'
            ),
            say('To jest mój dom.', 'This is my house.'),
            say('To są moje książki.', 'These are my books.'),
            say('Co to jest?', 'What is this?'),
            clear=True,
        ),
        step(
            [
                grid(
                    ['czerwony', 'niebieski', 'zielony', 'żółty'],
                    p=['cher-VOH-nih', 'nyeh-BYES-kee', 'zhyeh-LOH-nih', 'ZHOOW-tih'],
                    e=['red', 'blue', 'green', 'yellow'],
                    size=31,
                    h=112,
                ),
                grid(
                    ['czarny', 'biały', 'brązowy', 'różowy'],
                    p=['CHAR-nih', 'BYAH-wih', 'bron-ZOH-vih', 'roo-ZHOH-vih'],
                    e=['black', 'white', 'brown', 'pink'],
                    size=31,
                    h=112,
                ),
                pair('czerwon{m|y} rower', 'czerwon{f|a} róża · czerwon{n|e} auto'),
                note('Colours are adjectives, so they take {-y / -a / -e} too.'),
            ],
            en('Colours are adjectives, so they agree with the noun. '),
            pl('czerwony, niebieski, zielony, żółty, czarny, biały, brązowy, różowy.'),
            en('Red, blue, green, yellow, black, white, brown, pink. '),
            say('czerwony rower', 'a red bike'),
            say('czerwona róża', 'a red rose'),
            say('czerwone auto', 'a red car'),
            clear=True,
        ),
    ],
)

VERBS = Scene(
    'Verbs: present tense',
    'Drop the -ć, add the endings',
    'm',
    steps=[
        step(
            [
                head(
                    '',
                    'ja',
                    'ty',
                    'on / ona',
                    'my',
                    'wy',
                    'oni',
                    al='c',
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    [
                        'czytać',
                        'czyt{am}',
                        'czyta{sz}',
                        'czyta',
                        'czyta{my}',
                        'czyta{cie}',
                        'czyta{ją}',
                    ],
                    p=[
                        'to read',
                        'CHIH-tahm',
                        'CHIH-tahsh',
                        'CHIH-tah',
                        'chih-TAH-mih',
                        'chih-TAH-cheh',
                        'chih-TAH-yohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
            ],
            en(
                'Verbs. Take the infinitive, which ends in c with an accent, and add '
                'endings. [[Czytać]], to read: '
            ),
            pl('czytam, czytasz, czyta, czytamy, czytacie, czytają.'),
            en('The endings are:'),
            pl('am, asz, a, amy, acie, ają.'),
            en('You will recognise the pattern everywhere.'),
        ),
        step(
            [
                grid(
                    [
                        'robić',
                        'rob{ię}',
                        'rob{isz}',
                        'rob{i}',
                        'rob{imy}',
                        'rob{icie}',
                        'rob{ią}',
                    ],
                    p=[
                        'to do / make',
                        'ROH-byeh',
                        'ROH-beesh',
                        'ROH-bee',
                        'roh-BEE-mih',
                        'roh-BEE-cheh',
                        'ROH-byohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    [
                        'pracować',
                        'pracu{ję}',
                        'pracu{jesz}',
                        'pracu{je}',
                        'pracu{jemy}',
                        'pracu{jecie}',
                        'pracu{ją}',
                    ],
                    p=[
                        'to work',
                        'prah-TSOO-yeh',
                        'prah-TSOO-yesh',
                        'prah-TSOO-yeh',
                        'prah-tsoo-YEH-mih',
                        'prah-tsoo-YEH-cheh',
                        'prah-TSOO-yohn',
                    ],
                    size=24,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
            ],
            en('Verbs with i, like [[robić]], to do or make: '),
            pl('robię, robisz, robi, robimy, robicie, robią.'),
            en('And verbs ending in [[ować]], like [[pracować]], to work: '),
            pl('pracuję, pracujesz, pracuje, pracujemy, pracujecie, pracują.'),
            en('These three patterns cover most of the verbs you meet at A one.'),
        ),
        step(
            [
                head(
                    '',
                    'ja',
                    'ty',
                    'on / ona',
                    'my',
                    'wy',
                    'oni',
                    al='c',
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['mieć', 'mam', 'masz', 'ma', 'mamy', 'macie', 'mają'],
                    p=[
                        'to have',
                        'mahm',
                        'mahsh',
                        'mah',
                        'MAH-mih',
                        'MAH-cheh',
                        'MAH-yohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['chcieć', 'chcę', 'chcesz', 'chce', 'chcemy', 'chcecie', 'chcą'],
                    p=[
                        'to want',
                        'htseh',
                        'htsesh',
                        'htseh',
                        'HTSEH-mih',
                        'HTSEH-cheh',
                        'htsohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['móc', 'mogę', 'możesz', 'może', 'możemy', 'możecie', 'mogą'],
                    p=[
                        'can',
                        'MOH-geh',
                        'MOH-zhesh',
                        'MOH-zheh',
                        'moh-ZHEH-mih',
                        'moh-ZHEH-cheh',
                        'MOH-gohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['musieć', 'muszę', 'musisz', 'musi', 'musimy', 'musicie', 'muszą'],
                    p=[
                        'must',
                        'MOO-sheh',
                        'MOO-sheesh',
                        'MOO-shee',
                        'moo-SHEE-mih',
                        'moo-SHEE-cheh',
                        'MOO-shohn',
                    ],
                    size=26,
                    h=84,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
            ],
            en('Now the four heroes: to have, to want, can, and must. '),
            pl('mam, masz, ma, mamy, macie, mają.'),
            pl('chcę, chcesz, chce, chcemy, chcecie, chcą.'),
            pl('mogę, możesz, może, możemy, możecie, mogą.'),
            pl('muszę, musisz, musi, musimy, musicie, muszą.'),
            clear=True,
        ),
        step(
            [
                head(
                    '',
                    'ja',
                    'ty',
                    'on / ona',
                    'my',
                    'wy',
                    'oni',
                    al='c',
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['iść', 'idę', 'idziesz', 'idzie', 'idziemy', 'idziecie', 'idą'],
                    p=[
                        'to go (walk)',
                        'EE-deh',
                        'EE-jesh',
                        'EE-jeh',
                        'ee-JEH-mih',
                        'ee-JEH-cheh',
                        'EE-dohn',
                    ],
                    size=26,
                    h=82,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    [
                        'jechać',
                        'jadę',
                        'jedziesz',
                        'jedzie',
                        'jedziemy',
                        'jedziecie',
                        'jadą',
                    ],
                    p=[
                        'to go (ride)',
                        'YAH-deh',
                        'YEH-jesh',
                        'YEH-jeh',
                        'yeh-JEH-mih',
                        'yeh-JEH-cheh',
                        'YAH-dohn',
                    ],
                    size=26,
                    h=82,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['jeść', 'jem', 'jesz', 'je', 'jemy', 'jecie', 'jedzą'],
                    p=[
                        'to eat',
                        'yem',
                        'yesh',
                        'yeh',
                        'YEH-mih',
                        'YEH-cheh',
                        'YEH-dzohn',
                    ],
                    size=26,
                    h=82,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                grid(
                    ['pić', 'piję', 'pijesz', 'pije', 'pijemy', 'pijecie', 'piją'],
                    p=[
                        'to drink',
                        'PEE-yeh',
                        'PEE-yesh',
                        'PEE-yeh',
                        'pee-YEH-mih',
                        'pee-YEH-cheh',
                        'PEE-yohn',
                    ],
                    size=26,
                    h=82,
                    w=[0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
                ),
                note(
                    '{iść} = on foot · {jechać} = by vehicle or bike: '
                    'Jadę rowerem. · Idę do sklepu.'
                ),
            ],
            en('Four everyday verbs that break the pattern. To go on foot, [[iść]]: '),
            pl('idę, idziesz, idzie, idziemy, idziecie, idą.'),
            en('To go by vehicle or bike, [[jechać]]: '),
            pl('jadę, jedziesz, jedzie, jedziemy, jedziecie, jadą.'),
            en('To eat, [[jeść]]: '),
            pl('jem, jesz, je, jemy, jecie, jedzą.'),
            en('To drink, [[pić]]: '),
            pl('piję, pijesz, pije, pijemy, pijecie, piją.'),
            say('Jadę rowerem.', 'I go by bike.'),
            say('Idę do sklepu.', 'I walk to the shop.'),
            clear=True,
        ),
        step(
            [
                card(
                    'Chcę jechać do Krakowa.',
                    'htseh YEH-hahch doh krah-KOH-vah',
                    'I want to go to Kraków.',
                ),
                card('Muszę pracować.', 'MOO-sheh prah-TSOH-vahch', 'I have to work.'),
                card(
                    'Mogę mówić po polsku.',
                    'MOH-geh MOO-veech poh POHL-skoo',
                    'I can speak Polish.',
                ),
                card('Lubię gotować.', 'LOO-byeh goh-TOH-vahch', 'I like cooking.'),
                note(
                    'Second verb stays in the {infinitive}. {się} = reflexive: '
                    'uczę {się} = I teach myself = I study.'
                ),
            ],
            en('The magic combo: a modal verb plus an infinitive. '),
            say('Chcę jechać do Krakowa.', 'I want to go to Kraków.'),
            say('Muszę pracować.', 'I have to work.'),
            say('Mogę mówić po polsku.', 'I can speak Polish.'),
            say('Lubię gotować.', 'I like cooking.'),
            en('The second verb always stays in the infinitive.'),
            clear=True,
        ),
    ],
)

QUESTIONS = Scene(
    'Questions & negation',
    'Nine question words and one little word: nie',
    'r',
    steps=[
        step(
            [
                grid(
                    ['Kto?', 'Co?', 'Gdzie?'],
                    p=['ktoh', 'tsoh', 'gjeh'],
                    e=['who', 'what', 'where'],
                    size=34,
                    h=112,
                ),
                grid(
                    ['Kiedy?', 'Jak?', 'Dlaczego?'],
                    p=['KYEH-dih', 'yahk', 'dlah-CHEH-goh'],
                    e=['when', 'how', 'why'],
                    size=34,
                    h=112,
                ),
                grid(
                    ['Ile?', 'Skąd?', 'Dokąd?'],
                    p=['EE-leh', 'skont', 'DOH-kont'],
                    e=['how much / many', 'where from', 'where to'],
                    size=34,
                    h=112,
                ),
            ],
            en('Questions. Nine words open almost every question you will ask.'),
            say('Kto?', 'who'),
            say('Co?', 'what'),
            say('Gdzie?', 'where'),
            say('Kiedy?', 'when'),
            say('Jak?', 'how'),
            say('Dlaczego?', 'why'),
            say('Ile?', 'how much or how many'),
            say('Skąd?', 'where from'),
            say('Dokąd?', 'where to'),
        ),
        step(
            [
                pair('{Czy} mieszkasz w Krakowie?', 'Do you live in Kraków?'),
                pair('Mieszkasz w Krakowie{?}', 'same thing, just rising voice'),
                pair(
                    'Tak, mieszkam.  /  Nie, nie mieszkam.',
                    'Yes, I do.  /  No, I don’t.',
                ),
                pair('{Nie} mówię po rosyjsku.', 'I don’t speak Russian.'),
                pair('Nic {nie} rozumiem.', 'I don’t understand anything.', 'r'),
                pair('{Nie} mam kawy.', 'I have no coffee. (genitive!)'),
            ],
            en(
                'Yes or no questions: put [[czy]] at the start, or just raise your '
                'voice. '
            ),
            say('Czy mieszkasz w Krakowie?', 'Do you live in Kraków?'),
            en('To make a sentence negative, put [[nie]] before the verb. '),
            say('Nie mówię po rosyjsku.', 'I do not speak Russian.'),
            en('Polish loves double negatives. They are required!'),
            say('Nic nie rozumiem.', 'I do not understand anything.'),
            en(
                'And notice [[nie mam kawy]]. The coffee changed. That is our next topic.'
            ),
            clear=True,
        ),
    ],
)

CASES = Scene(
    'The cases',
    'Nouns change endings to show their job',
    'r',
    steps=[
        step(
            [
                head('CASE', 'ASKS', 'USED FOR', w=[0.2, 0.42, 0.38]),
                conj('Nominative', 'Kto? Co?', 'the subject, dictionary form'),
                conj('Accusative', 'Kogo? Co?', 'the thing you do something to', 'a'),
                conj('Genitive', 'Kogo? Czego?', 'no / not, of, amounts, “from”', 'a'),
                conj('Locative', 'O kim? O czym?', 'where? (after w, na, o)', 'a'),
                conj('Instrumental', 'Z kim? Z czym?', 'with, and “to be” + job', 'a'),
                conj('Dative', 'Komu? Czemu?', 'to / for someone (set phrases)'),
                conj('Vocative', '—', 'calling someone by name'),
            ],
            en(
                'Now the part everyone fears: cases. Polish nouns change their '
                'ending depending on their job in the sentence. There are seven. '
                'At A one, four do almost all the work: accusative for the thing '
                'you act on, genitive for not having and amounts, locative for '
                'where, and instrumental for with.'
            ),
        ),
        step(
            [
                head('RULE', 'EXAMPLE', 'MEANING'),
                rule('kawa → kaw{ę}', 'Piję kaw{ę}.', 'I drink coffee.', 'f'),
                rule('książka → książk{ę}', 'Czytam książk{ę}.', 'I read a book.', 'f'),
                rule('rower → rower', 'Mam rower.', 'I have a bike. (no change)', 'm'),
                rule(
                    'brat → brat{a}',
                    'Widzę brat{a}.',
                    'I see my brother. (person)',
                    'm',
                ),
                rule('pies → ps{a}', 'Mam ps{a}.', 'I have a dog. (animal)', 'm'),
                rule('piwo → piwo', 'Chcę piwo.', 'I want a beer. (no change)', 'n'),
            ],
            en(
                'Accusative, the thing being acted on. Feminine nouns swap a for '
                'e with a tail. '
            ),
            say('Piję kawę.', 'I drink coffee.'),
            say('Czytam książkę.', 'I read a book.'),
            en('Masculine things do not change:'),
            say('Mam rower.', 'I have a bike.'),
            en('but masculine people and animals take a:'),
            say('Widzę brata.', 'I see my brother.'),
            say('Mam psa.', 'I have a dog.'),
            en('Neuter stays the same:'),
            say('Chcę piwo.', 'I want a beer.'),
            clear=True,
        ),
        step(
            [
                head('ja', 'ty', 'on', 'ona', 'my', 'wy', 'oni', al='c'),
                grid(
                    ['mnie', 'cię', 'go', 'ją', 'nas', 'was', 'ich'],
                    p=['mnyeh', 'cheh', 'goh', 'yohn', 'nahs', 'vahs', 'eekh'],
                    e=['me', 'you', 'him', 'her', 'us', 'you (pl)', 'them'],
                    size=30,
                    h=108,
                ),
                card('Widzę cię.', 'VEE-jeh cheh', 'I see you.'),
                card('Znam ją.', 'znahm yohn', 'I know her.'),
                card('Nie znam go.', 'nyeh znahm goh', 'I don’t know him.'),
            ],
            en('Pronouns change in the accusative too. Learn the object forms: '),
            pl('mnie, cię, go, ją, nas, was, ich.'),
            en('Me, you, him, her, us, you plural, them.'),
            say('Widzę cię.', 'I see you.'),
            say('Znam ją.', 'I know her.'),
            say('Nie znam go.', 'I do not know him.'),
            clear=True,
        ),
        step(
            [
                head('RULE', 'EXAMPLE', 'MEANING'),
                rule(
                    'Kraków → Krakow{ie}',
                    'Mieszkam w Krakow{ie}.',
                    'I live in Kraków.',
                    'm',
                ),
                rule('Polska → Pols{ce}', 'Jestem w Pols{ce}.', 'I am in Poland.', 'f'),
                rule('dom → dom{u}', 'Jestem w dom{u}.', 'I am at home.', 'm'),
                rule(
                    'miasto → mieś{cie}',
                    'Jestem w mieś{cie}.',
                    'I am in the city.',
                    'n',
                ),
                rule('praca → prac{y}', 'Jestem w prac{y}.', 'I am at work.', 'f'),
                rule('rower → rower{ze}', 'Jeżdżę na rower{ze}.', 'I cycle.', 'm'),
            ],
            en('Locative, answering where. It comes after w, in, and na, on or at. '),
            say('Mieszkam w Krakowie.', 'I live in Kraków.'),
            en('Consonants soften: k becomes c in'),
            say('w Polsce.', 'in Poland'),
            en('and t becomes c with an accent in'),
            say('w mieście.', 'in the city'),
            say('Jestem w domu.', 'I am at home.'),
            say('Jestem w pracy.', 'I am at work.'),
            en('And for the cyclist:'),
            say('Jeżdżę na rowerze.', 'I cycle.'),
            clear=True,
        ),
        step(
            [
                head('RULE', 'EXAMPLE', 'MEANING'),
                rule('kawa → kaw{y}', 'Nie ma kaw{y}.', 'There is no coffee.', 'f'),
                rule('czas → czas{u}', 'Nie mam czas{u}.', 'I have no time.', 'm'),
                rule('woda → wod{y}', 'Szklanka wod{y}.', 'A glass of water.', 'f'),
                rule(
                    'Polska → Polsk{i}', 'Jestem z Polsk{i}.', 'I am from Poland.', 'f'
                ),
                rule('dom → dom{u}', 'Idę do dom{u}.', 'I am going home.', 'm'),
                rule(
                    'cukier → cukr{u}',
                    'Kawa bez cukr{u}.',
                    'Coffee without sugar.',
                    'm',
                ),
            ],
            en(
                'Genitive: absence, amounts, and starting points. Feminine a '
                'becomes y or i. Masculine takes a or u. '
            ),
            say('Nie ma kawy.', 'There is no coffee.'),
            say('Nie mam czasu.', 'I have no time.'),
            say('Szklanka wody.', 'A glass of water.'),
            en('It follows [[do]], meaning to, and [[bez]], meaning without.'),
            say('Jestem z Polski.', 'I am from Poland.'),
            say('Idę do domu.', 'I am going home.'),
            say('Kawa bez cukru.', 'Coffee without sugar.'),
            clear=True,
        ),
        step(
            [
                head('RULE', 'EXAMPLE', 'MEANING'),
                rule(
                    'brat → z brat{em}', 'Idę z brat{em}.', 'I go with my brother.', 'm'
                ),
                rule(
                    'siostra → z siostr{ą}',
                    'Mieszkam z siostr{ą}.',
                    'I live with my sister.',
                    'f',
                ),
                rule(
                    'mleko → z mlek{iem}', 'Kawa z mlek{iem}.', 'Coffee with milk.', 'n'
                ),
                rule(
                    'student → student{em}',
                    'Jestem student{em}.',
                    'I am a student (m).',
                    'm',
                ),
                rule(
                    'studentka → studentk{ą}',
                    'Jestem studentk{ą}.',
                    'I am a student (f).',
                    'f',
                ),
            ],
            en('Instrumental: with, and being. Masculine and neuter add em. '),
            say('Idę z bratem.', 'I go with my brother.'),
            say('Kawa z mlekiem.', 'Coffee with milk.'),
            en('Feminine a becomes a with a tail:'),
            say('Mieszkam z siostrą.', 'I live with my sister.'),
            en('And after to be, jobs and roles use the instrumental:'),
            say('Jestem studentem.', 'I am a student, said by a man.'),
            say('Jestem studentką.', 'And said by a woman.'),
            clear=True,
        ),
        step(
            [
                head('QUESTION', 'PREPOSITION + CASE', 'EXAMPLE'),
                rule('Where? (in / at)', 'w / na + {Locative}', 'Jestem w pracy.'),
                rule('Where to?', 'do + {Genitive}', 'Idę do domu.'),
                rule('Where from?', 'z / od + {Genitive}', 'Jestem z Polski.'),
                rule('With whom?', 'z + {Instrumental}', 'Kawa z mlekiem.'),
                rule('Without?', 'bez + {Genitive}', 'Bez cukru.'),
                note(
                    'Bonus: {Podoba mi się Kraków.} (dative: mi) · '
                    '{Pani Anno! Tomku! Mamo!} (vocative, when you call someone)'
                ),
            ],
            en(
                'Here is your cheat code. Where: [[w pracy]], locative. Where to: '
                '[[do domu]], genitive. Where from: [[z Polski]], genitive. With: '
                '[[z mlekiem]], instrumental. Without: [[bez cukru]], genitive. '
                'Two bonus items: the dative phrase'
            ),
            pl('Podoba mi się Kraków,'),
            en('I like Kraków. And the vocative, for calling people:'),
            pl('Pani Anno! Tomku! Mamo!'),
            clear=True,
        ),
    ],
)

PREPOSITIONS = Scene(
    'Where is it?',
    'Prepositions of place: the case depends on the word',
    'n',
    steps=[
        step(
            [
                head('{n|LOCATIVE}   ·   {a|GENITIVE}   ·   {m|INSTRUMENTAL}', w=[1]),
                card('na stole', 'nah STOH-leh', 'on the table', 'n'),
                card('przy oknie', 'pshih OHK-nyeh', 'by the window', 'n'),
                card('obok domu', 'OH-bok DOH-moo', 'next to the house', 'a'),
            ],
            en(
                'Where is it? Each preposition picks its case. '
                '[[Na]] and [[przy]] take the locative. '
            ),
            say('na stole', 'on the table'),
            say('przy oknie', 'by the window'),
            en('[[Obok]] takes the genitive. '),
            say('obok domu', 'next to the house'),
        ),
        step(
            [
                head('{n|LOCATIVE}   ·   {a|GENITIVE}   ·   {m|INSTRUMENTAL}', w=[1]),
                card('pod stołem', 'pot STOH-wem', 'under the table', 'm'),
                card('nad morzem', 'nat MOH-zhem', 'by the sea', 'm'),
                card('przed domem', 'pshet DOH-mem', 'in front of the house', 'm'),
                card('za domem', 'zah DOH-mem', 'behind the house', 'm'),
            ],
            en('And four that take the instrumental when you say where something is. '),
            say('pod stołem', 'under the table'),
            say('nad morzem', 'by the sea'),
            say('przed domem', 'in front of the house'),
            say('za domem', 'behind the house'),
            clear=True,
        ),
    ],
)

NUMBERS = Scene(
    'Numbers, time & dates',
    'Count it, tell it, schedule it',
    'a',
    steps=[
        step(
            [
                grid(
                    ['1  jeden', '2  dwa', '3  trzy', '4  cztery', '5  pięć'],
                    p=['YEH-den', 'dvah', 'tshih', 'CHTEH-rih', 'pyench'],
                    size=32,
                    h=118,
                ),
                grid(
                    [
                        '6  sześć',
                        '7  siedem',
                        '8  osiem',
                        '9  dziewięć',
                        '10  dziesięć',
                    ],
                    p=['sheshch', 'SHEH-dem', 'OH-shem', 'JEH-vyench', 'JEH-shench'],
                    size=30,
                    h=118,
                ),
            ],
            en('Numbers one to ten. Say them with me.'),
            ps(
                'jeden, dwa, trzy, cztery, pięć, sześć, siedem, osiem, dziewięć, '
                'dziesięć.'
            ),
            gap(0.8),
            pl(
                'jeden, dwa, trzy, cztery, pięć, sześć, siedem, osiem, dziewięć, '
                'dziesięć.'
            ),
        ),
        step(
            [
                grid(
                    ['11  jedenaście', '12  dwanaście', '15  piętnaście'],
                    p=['yeh-deh-NAHSH-cheh', 'dvah-NAHSH-cheh', 'pyent-NAHSH-cheh'],
                    size=30,
                    h=100,
                ),
                grid(
                    ['20  dwadzieścia', '30  trzydzieści', '40  czterdzieści'],
                    p=['dvah-JESH-chah', 'tshih-JESH-chee', 'chter-JESH-chee'],
                    size=30,
                    h=100,
                ),
                grid(
                    ['50  pięćdziesiąt', '90  dziewięćdziesiąt', '100  sto'],
                    p=['pyen-JEH-shont', 'jeh-vyen-JEH-shont', 'stoh'],
                    size=29,
                    h=100,
                ),
            ],
            en('Eleven to nineteen all end in [[naście]].'),
            pl('jedenaście, dwanaście, piętnaście.'),
            en('Twenty, and then the tens:'),
            pl(
                'dwadzieścia, trzydzieści, czterdzieści, pięćdziesiąt, '
                'sześćdziesiąt, dziewięćdziesiąt, sto.'
            ),
            clear=True,
        ),
        step(
            [
                head('NUMBER', 'FORM', 'EXAMPLE'),
                rule('1', 'złot{y}', 'jeden złoty'),
                rule('2 – 4', 'złot{e}', 'dwa złote, trzy złote'),
                rule('5 and up', 'złot{ych}', 'pięć złotych, dwadzieścia złotych'),
                card('Ile to kosztuje?', 'EE-leh toh kosh-TOO-yeh', 'How much is it?'),
                note(
                    'Same trick for age: {jeden rok}, {dwa lata}, {pięć lat}. '
                    'Ile masz lat? Mam … lat.'
                ),
            ],
            en(
                'Counting things has a rule. One takes the singular. Two to four '
                'take the plural. Five and up take the genitive plural. So:'
            ),
            say('jeden złoty', 'one zloty'),
            say('dwa złote', 'two zloty'),
            say('pięć złotych', 'five zloty'),
            say('Ile to kosztuje?', 'How much is it?'),
            en('And the same rule gives you age: [[jeden rok, dwa lata, pięć lat.]] '),
            clear=True,
        ),
        step(
            [
                grid(
                    ['1  pierwsza', '2  druga', '3  trzecia', '4  czwarta', '5  piąta'],
                    p=['PYER-vshah', 'DROO-gah', 'TSHEH-chah', 'CHVAR-tah', 'PYON-tah'],
                    size=25,
                    h=82,
                ),
                grid(
                    [
                        '6  szósta',
                        '7  siódma',
                        '8  ósma',
                        '9  dziewiąta',
                        '10  dziesiąta',
                    ],
                    p=[
                        'SHOOS-tah',
                        'SHOOD-mah',
                        'OOS-mah',
                        'jeh-VYON-tah',
                        'jeh-SHON-tah',
                    ],
                    size=25,
                    h=82,
                ),
                card(
                    'Która jest godzina?',
                    'KTOO-rah yest goh-JEE-nah',
                    'What time is it?',
                ),
                card(
                    'Jest {ósma}.  /  O {ósmej}.',
                    'yest OOS-mah / oh OOS-may',
                    'It is eight.  /  At eight.',
                ),
            ],
            en(
                'Telling the time uses feminine ordinal numbers, because '
                '[[godzina]], hour, is feminine. '
            ),
            pl(
                'pierwsza, druga, trzecia, czwarta, piąta, szósta, siódma, ósma, '
                'dziewiąta, dziesiąta.'
            ),
            say('Która jest godzina?', 'What time is it?'),
            say('Jest ósma.', 'It is eight.'),
            en('For at what time, switch to locative:'),
            say('O ósmej.', 'At eight.'),
            en(
                'Add minutes with plain numbers: [[jest ósma trzydzieści]], eight thirty.'
            ),
            clear=True,
        ),
        step(
            [
                grid(
                    ['poniedziałek', 'wtorek', 'środa', 'czwartek'],
                    p=['poh-nyeh-JAH-wek', 'VTOH-rek', 'SHROH-dah', 'CHVAR-tek'],
                    e=['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
                    size=24,
                    h=108,
                ),
                grid(
                    ['piątek', 'sobota', 'niedziela', ''],
                    p=['PYON-tek', 'soh-BOH-tah', 'nyeh-JEH-lah', ''],
                    e=['Friday', 'Saturday', 'Sunday', ''],
                    size=24,
                    h=108,
                ),
                note(
                    '“On Monday” = {w poniedziałek}, {we wtorek}, {w środę}, '
                    '{w sobotę}, {w niedzielę}: it is the accusative!'
                ),
            ],
            en('Days of the week. '),
            pl('poniedziałek, wtorek, środa, czwartek, piątek, sobota, niedziela.'),
            en('To say on Monday, use w plus the accusative: '),
            pl('w poniedziałek, we wtorek, w środę, w sobotę, w niedzielę.'),
            clear=True,
        ),
        step(
            [
                grid(['styczeń', 'luty', 'marzec', 'kwiecień'], size=28, h=56),
                grid(['maj', 'czerwiec', 'lipiec', 'sierpień'], size=28, h=56),
                grid(
                    ['wrzesień', 'październik', 'listopad', 'grudzień'], size=28, h=56
                ),
                note(
                    'Months are lowercase and masculine. {w maju} = in May, '
                    '{w lipcu} = in July.'
                ),
            ],
            en('And the twelve months, quickly. '),
            pl(
                'styczeń, luty, marzec, kwiecień, maj, czerwiec, lipiec, sierpień, '
                'wrzesień, październik, listopad, grudzień.'
            ),
            clear=True,
        ),
    ],
)

SURVIVAL = Scene(
    'Survival vocabulary',
    'Café, family, directions, and lifelines',
    'n',
    steps=[
        step(
            [
                card('Poproszę kawę.', 'poh-PROH-sheh KAH-veh', 'A coffee, please.'),
                card(
                    'Poproszę rachunek.',
                    'poh-PROH-sheh rah-HOO-nek',
                    'The bill, please.',
                ),
                card(
                    'Czy mogę zapłacić kartą?',
                    'chih MOH-geh zah-PWAH-cheech KAR-tohn',
                    'Can I pay by card?',
                ),
                card('Smacznego!', 'smahch-NEH-goh', 'Enjoy your meal!'),
                card('Na zdrowie!', 'nah ZDROH-vyeh', 'Cheers!'),
            ],
            en('At the café. The golden phrase is [[poproszę]], I would like. '),
            say('Poproszę kawę.', 'A coffee, please.'),
            say('Poproszę rachunek.', 'The bill, please.'),
            say('Czy mogę zapłacić kartą?', 'Can I pay by card?'),
            say('Smacznego!', 'Enjoy your meal!'),
            say('Na zdrowie!', 'Cheers!'),
        ),
        step(
            [
                grid(
                    ['mama', 'tata', 'brat', 'siostra'],
                    p=['MAH-mah', 'TAH-tah', 'braht', 'SHOH-strah'],
                    e=['mum', 'dad', 'brother', 'sister'],
                    size=28,
                    h=106,
                ),
                grid(
                    ['syn', 'córka', 'babcia', 'dziadek'],
                    p=['sihn', 'TSOOR-kah', 'BAHP-chah', 'JAH-dek'],
                    e=['son', 'daughter', 'grandma', 'grandpa'],
                    size=28,
                    h=106,
                ),
                grid(
                    ['rodzice', 'mąż', 'żona', 'dziecko'],
                    p=['roh-JEE-tseh', 'monzh', 'ZHOH-nah', 'JETS-koh'],
                    e=['parents', 'husband', 'wife', 'child'],
                    size=28,
                    h=106,
                ),
            ],
            en('Family. '),
            pl(
                'mama, tata, brat, siostra, syn, córka, babcia, dziadek, rodzice, '
                'mąż, żona, dziecko.'
            ),
            en(
                'Mum, dad, brother, sister, son, daughter, grandma, grandpa, '
                'parents, husband, wife, child.'
            ),
            clear=True,
        ),
        step(
            [
                card(
                    'Gdzie jest dworzec?',
                    'gjeh yest DVOH-zhets',
                    'Where is the station?',
                ),
                card('prosto', 'PROH-stoh', 'straight on'),
                card('w lewo  /  w prawo', 'v LEH-voh / v PRAH-voh', 'left  /  right'),
                card('blisko  /  daleko', 'BLEES-koh / dah-LEH-koh', 'near  /  far'),
                card('tutaj  /  tam', 'TOO-tai / tahm', 'here  /  there'),
            ],
            en('Directions. '),
            say('Gdzie jest dworzec?', 'Where is the station?'),
            say('prosto', 'straight on'),
            say('w lewo', 'left'),
            say('w prawo', 'right'),
            say('blisko', 'near'),
            say('daleko', 'far'),
            clear=True,
        ),
        step(
            [
                grid(
                    ['sklep', 'apteka', 'bank'],
                    p=['sklep', 'ahp-TEH-kah', 'bank'],
                    e=['shop', 'pharmacy', 'bank'],
                    size=32,
                    h=112,
                ),
                grid(
                    ['poczta', 'dworzec', 'przystanek'],
                    p=['POHCH-tah', 'DVOH-zhets', 'pshih-STAH-nek'],
                    e=['post office', 'station', 'bus stop'],
                    size=32,
                    h=112,
                ),
                card(
                    'Idę na pocztę.',
                    'EE-deh nah POHCH-teh',
                    'I am going to the post office.',
                ),
                note(
                    'Most places: {do} + genitive (do sklepu, do apteki). '
                    'Post office, station, stop: {na} + accusative.'
                ),
            ],
            en('Places in town. '),
            pl('sklep, apteka, bank, poczta, dworzec, przystanek.'),
            en(
                'Shop, pharmacy, bank, post office, station, bus stop. '
                'Going somewhere takes [[do]] plus genitive: '
            ),
            say('Idę do sklepu.', 'I am going to the shop.'),
            say('Idę do apteki.', 'I am going to the pharmacy.'),
            en(
                'But for the post office, station and stops, use [[na]] plus '
                'accusative: '
            ),
            say('Idę na pocztę.', 'I am going to the post office.'),
            clear=True,
        ),
        step(
            [
                card(
                    'Jaka jest pogoda?',
                    'YAH-kah yest poh-GOH-dah',
                    'What is the weather like?',
                ),
                card('Jest zimno.', 'yest ZHEEM-noh', 'It is cold.'),
                card('Jest ciepło.', 'yest CHEHP-woh', 'It is warm.'),
                card('Jest gorąco.', 'yest goh-RON-tsoh', 'It is hot.'),
                card('Pada deszcz.', 'PAH-dah deshch', 'It is raining.'),
            ],
            say('Jaka jest pogoda?', 'What is the weather like?'),
            say('Jest zimno.', 'It is cold.'),
            say('Jest ciepło.', 'It is warm.'),
            say('Jest gorąco.', 'It is hot.'),
            say('Pada deszcz.', 'It is raining.'),
            clear=True,
        ),
        step(
            [
                card('Nie rozumiem.', 'nyeh roh-ZOO-myem', 'I don’t understand.'),
                card(
                    'Proszę mówić wolniej.',
                    'PROH-sheh MOO-veech VOL-nyay',
                    'Please speak more slowly.',
                ),
                card('Co to znaczy?', 'tsoh toh ZNAH-chih', 'What does it mean?'),
                card(
                    'Mówię trochę po polsku.',
                    'MOO-vyeh TROH-heh poh POHL-skoo',
                    'I speak a little Polish.',
                ),
            ],
            en('Finally, your four lifelines for any conversation. '),
            drill('Nie rozumiem.'),
            drill('Proszę mówić wolniej.'),
            say('Co to znaczy?', 'What does it mean?'),
            say('Mówię trochę po polsku.', 'I speak a little Polish.'),
            clear=True,
        ),
        step(
            [
                grid(
                    ['i', 'ale', 'bo', 'też'],
                    p=['ee', 'AH-leh', 'boh', 'tesh'],
                    e=['and', 'but', 'because', 'also'],
                    size=34,
                    h=106,
                ),
                grid(
                    ['bardzo', 'trochę', 'dużo', 'już'],
                    p=['BAR-dzoh', 'TROH-heh', 'DOO-zhoh', 'yoosh'],
                    e=['very', 'a little', 'a lot', 'already'],
                    size=34,
                    h=106,
                ),
                grid(
                    ['zawsze', 'często', 'czasem', 'nigdy'],
                    p=['ZAHF-sheh', 'CHEN-stoh', 'CHAH-sem', 'NEEG-dih'],
                    e=['always', 'often', 'sometimes', 'never'],
                    size=34,
                    h=106,
                ),
                card(
                    'Nigdy nie piję kawy wieczorem.',
                    'NEEG-dih nyeh PEE-yeh KAH-vih vyeh-CHOH-rem',
                    'I never drink coffee in the evening.',
                ),
            ],
            en('Twelve little words that glue sentences together. '),
            pl('i, ale, bo, też.'),
            en('And, but, because, also.'),
            pl('bardzo, trochę, dużo, już.'),
            en('Very, a little, a lot, already.'),
            pl('zawsze, często, czasem, nigdy.'),
            en('Always, often, sometimes, never.'),
            en('Remember the double negative: '),
            say(
                'Nigdy nie piję kawy wieczorem.', 'I never drink coffee in the evening.'
            ),
            clear=True,
        ),
    ],
)

TRAPS = Scene(
    'False friends',
    'Words that look English but are not',
    'r',
    steps=[
        step(
            [
                card('ser', 'sehr', 'cheese  (not “sir”)'),
                card('kolega', 'koh-LEH-gah', 'male friend  (not “college”)'),
                card('sympatyczny', 'sim-pah-TIH-chnih', 'nice  (not “sympathetic”)'),
                card('aktualnie', 'ahk-too-AHL-nyeh', 'currently  (not “actually”)'),
                card(
                    'ewentualnie', 'eh-ven-too-AHL-nyeh', 'possibly  (not “eventually”)'
                ),
            ],
            en('Five false friends that trap English speakers. '),
            pl('ser.'),
            en('Looks like sir. It means cheese.'),
            pl('kolega.'),
            en('Not a college. It is a male friend or colleague.'),
            pl('sympatyczny.'),
            en('Not sympathetic. It means nice.'),
            pl('aktualnie.'),
            en('Not actually. It means currently.'),
            pl('ewentualnie.'),
            en('Not eventually. It means possibly.'),
        ),
    ],
)

PAST_FUTURE = Scene(
    'Past & future',
    'Just enough to survive until A2',
    'm',
    steps=[
        step(
            [
                head('', '{m|MASCULINE}', '{f|FEMININE}', w=[0.2, 0.4, 0.4]),
                conj('ja', 'był{em}', 'był{am}'),
                conj('ty', 'był{eś}', 'był{aś}'),
                conj('on / ona', 'był', 'był{a}'),
                conj('my', 'byli{śmy}', 'był{yśmy}'),
                note(
                    'Past = infinitive stem + {ł / ła / li / ły} + ending. '
                    'Wczoraj {byłem} w pracy. = Yesterday I was at work (man).'
                ),
            ],
            en(
                'The past tense. Take the verb stem, add l, and the ending shows '
                'your gender. A man says [[byłem]], a woman says [[byłam]]. '
            ),
            say('byłem', 'I was, a man'),
            say('byłam', 'I was, a woman'),
            say('był, była', 'he was, she was'),
            say('Wczoraj byłem w pracy.', 'Yesterday I was at work.'),
        ),
        step(
            [
                grid(
                    ['będę', 'będziesz', 'będzie', 'będziemy', 'będziecie', 'będą'],
                    p=[
                        'BEN-deh',
                        'BEN-jesh',
                        'BEN-jeh',
                        'ben-JEH-mih',
                        'ben-JEH-cheh',
                        'BEN-dohn',
                    ],
                    e=[
                        'I will',
                        'you will',
                        'he / she will',
                        'we will',
                        'you (pl) will',
                        'they will',
                    ],
                    size=27,
                    h=108,
                ),
                card(
                    'Jutro będę pracować.',
                    'YOO-troh BEN-deh prah-TSOH-vahch',
                    'Tomorrow I will work.',
                ),
                card(
                    'wczoraj · dzisiaj · jutro',
                    'VCHOH-rai · JEE-shai · YOO-troh',
                    'yesterday · today · tomorrow',
                ),
            ],
            en(
                'The future is easy: [[będę, będziesz, będzie, będziemy, będziecie, '
                'będą,]] plus an infinitive. '
            ),
            pl('Jutro będę pracować.'),
            en('Tomorrow I will work. And the three time words you need:'),
            pl('wczoraj, dzisiaj, jutro.'),
            clear=True,
        ),
    ],
)


CAFE = Scene(
    'Café scene',
    'Everything together: listen, then say the customer lines',
    'f',
    steps=[
        step(
            [
                card(
                    'Dzień dobry! Co podać?',
                    'jen DOH-bri! tsoh POH-dahch',
                    'Good day! What can I get you?',
                ),
                card(
                    'Poproszę kawę z mlekiem.',
                    'poh-PROH-sheh KAH-veh z MLEH-kyem',
                    'A coffee with milk, please.',
                ),
                card('Coś jeszcze?', 'tsosh YESH-cheh', 'Anything else?'),
                card(
                    'Tak, szklankę wody.',
                    'tahk SHKLAHN-keh VOH-dih',
                    'Yes, a glass of water.',
                ),
            ],
            en(
                'Time to put it all together. A café in [[Kraków]]. You are the '
                'customer.'
            ),
            nt('Dzień dobry! Co podać?'),
            gap(1.6),
            pl('Poproszę kawę z mlekiem.'),
            gap(0.4),
            nt('Coś jeszcze?'),
            gap(1.6),
            pl('Tak, szklankę wody.'),
            gap(0.4),
        ),
        step(
            [
                card(
                    'To będzie dwadzieścia złotych.',
                    'toh BEN-jeh dvah-JESH-chah ZWOH-tihkh',
                    'That will be twenty zloty.',
                ),
                card(
                    'Proszę. Dziękuję!',
                    'PROH-sheh. jen-KOO-yeh',
                    'Here you go. Thanks!',
                ),
                card(
                    'Smacznego! Miłego dnia!',
                    'smahch-NEH-goh! mee-WEH-goh dnyah',
                    'Enjoy! Have a nice day!',
                ),
                note(
                    'Spot the cases: {kawę} accusative · {z mlekiem} instrumental · '
                    '{wody} genitive · {złotych} genitive plural.'
                ),
            ],
            nt('To będzie dwadzieścia złotych.'),
            gap(1.4),
            pl('Proszę. Dziękuję!'),
            gap(0.3),
            nt('Smacznego! Miłego dnia!'),
            gap(1.4),
            pl('Do widzenia!'),
            gap(0.3),
            en(
                'Count the cases you just used: accusative, instrumental, genitive, '
                'and the genitive plural of zloty. That is A one in action.'
            ),
            clear=True,
        ),
    ],
)


def _quiz(num, question, q_narr, answer, explain, a_narr):  # noqa: PLR0917
    """Question step with a countdown, then the revealed answer."""
    return [
        step(
            [head(f'QUESTION {num} OF 8', al='c'), big(question, 54, 'w', 190)],
            q_narr,
            gap(0.2),
            clear=True,
            cd=4,
        ),
        step(
            [big(answer, 64, 'g', 120), big(explain, 30, None, 56)],
            pl(answer),
            gap(0.25),
            a_narr,
        ),
    ]


QUIZ = Scene(
    'Quiz time',
    'Answer out loud before the timer ends',
    'a',
    steps=(
        _quiz(
            1,
            'How do you say: I live in Kraków?',
            en('Question one. How do you say: I live in [[Kraków]]?'),
            'Mieszkam w Krakowie.',
            'Locative after w: Kraków becomes Krakowie.',
            en('Locative after [[w]]: [[Kraków]] becomes [[Krakowie.]]'),
        )
        + _quiz(
            2,
            'Fill the gap: Piję … (kawa)',
            en(
                'Question two. Complete the sentence: [[Piję]], and then coffee, '
                'in the accusative.'
            ),
            'Piję kawę.',
            'Accusative: feminine -a becomes -ę.',
            en('Accusative: feminine a becomes e with a tail.'),
        )
        + _quiz(
            3,
            'Plural of okno (window)?',
            en('Question three. What is the plural of [[okno]], window?'),
            'okna',
            'Neuter: -o becomes -a.',
            en('Neuter nouns swap o for a.'),
        )
        + _quiz(
            4,
            'Fill the gap: Nie ma … (woda)',
            en(
                'Question four. Complete the sentence: [[Nie ma]], and then '
                'water, in the genitive.'
            ),
            'Nie ma wody.',
            'Genitive after nie ma: -a becomes -y.',
            en('Genitive after [[nie ma]]: a becomes y.'),
        )
        + _quiz(
            5,
            'Say: coffee with milk',
            en(
                'Question five. How do you say: coffee with milk? Use the instrumental.'
            ),
            'Kawa z mlekiem.',
            'Instrumental after z: mleko becomes mlekiem.',
            en('Instrumental after [[z]]: [[mleko]] becomes [[mlekiem.]]'),
        )
        + _quiz(
            6,
            'Say: I was at work. (a man speaking)',
            en('Question six. How do you say: I was at work, if you are a man?'),
            'Byłem w pracy.',
            'Past: był + em (man).  w pracy = locative.',
            en(
                'Past tense: [[był]] plus [[em]] for a man. And [[w pracy]] is '
                'locative.'
            ),
        )
        + _quiz(
            7,
            'Politely ask: speak more slowly',
            en('Question seven. Politely ask someone to speak more slowly.'),
            'Proszę mówić wolniej.',
            'Proszę + infinitive. A lifesaver!',
            en('[[Proszę]] plus an infinitive. A lifesaver.'),
        )
        + _quiz(
            8,
            'Say: It is eight o’clock.',
            en('Question eight. Say: it is eight o clock.'),
            'Jest ósma.',
            'Feminine ordinal, because godzina is feminine.',
            en('Feminine ordinal, because [[godzina]] is feminine.'),
        )
    ),
)

RECAP = Scene(
    'Recap & what is next',
    'You are ready for A2',
    'g',
    steps=[
        step(
            [
                pair('{1} Sounds', 'ą ę ó · sz cz ż · stress: 2nd-last syllable'),
                pair('{2} To be & to have', 'jestem, jesteś … · mam, masz …'),
                pair('{3} Gender', 'm consonant · f -a · n -o/-e'),
                pair('{4} Verbs', '-am · -ię · -uję patterns + modals'),
                pair('{5} Cases', 'accusative · locative · genitive · instrumental'),
                pair('{6} Life', 'numbers · time · family · café · directions'),
            ],
            en(
                'That is Polish A one. Sounds. To be and to have. Gender, and '
                'adjectives that follow it. The three verb patterns plus the '
                'modals. And the four cases: accusative, locative, genitive, '
                'instrumental. Plus numbers, time, and the survival words.'
            ),
        ),
        step(
            [
                head('MEMORY ANCHOR  ·  one sentence per case', w=[1]),
                card('Piję kawę.', 'PEE-yeh KAH-veh', 'ACCUSATIVE: what I drink', 'a'),
                card(
                    'Mieszkam w Krakowie.',
                    'MYESH-kahm v krah-KOH-vyeh',
                    'LOCATIVE: where I live',
                    'n',
                ),
                card(
                    'Nie mam czasu.', 'nyeh mahm CHAH-soo', 'GENITIVE: what I lack', 'r'
                ),
                card(
                    'Kawa z mlekiem.',
                    'KAH-vah z MLEH-kyem',
                    'INSTRUMENTAL: with what',
                    'm',
                ),
            ],
            en(
                'One last trick for tonight. Anchor each case to a single sentence '
                'you can say without thinking. Accusative: '
            ),
            say('Piję kawę.', 'I drink coffee.'),
            en('Locative: '),
            say('Mieszkam w Krakowie.', 'I live in Kraków.'),
            en('Genitive: '),
            say('Nie mam czasu.', 'I have no time.'),
            en('Instrumental: '),
            say('Kawa z mlekiem.', 'Coffee with milk.'),
            en(
                'When a new noun appears in class, ask: which of my four sentences '
                'is this? Then copy that ending.'
            ),
            clear=True,
        ),
        step(
            [
                head('COMING IN A2'),
                pair('Aspect', 'perfective vs imperfective: robić / zrobić'),
                pair('Cases in the plural', 'and the dative in depth'),
                pair('Imperative & conditional', 'Zrób to!  ·  Chciałbym …'),
                pair('Comparatives', 'większy, lepszy, najlepszy'),
                note(
                    'Tonight’s warm-up: say five sentences about your day, out loud, '
                    'before class. {Cześć} to your teacher in Polish!'
                ),
            ],
            en(
                'In A two, expect verb aspect, cases in the plural, the '
                'imperative, and comparisons. Warm up tonight by saying five '
                'sentences about your day, out loud, before class.'
            ),
            clear=True,
        ),
        step(
            [
                big('Powodzenia!', 100, 'a', 140),
                big('Good luck!  ·  see you in A2', 30, None, 60),
            ],
            pl('Powodzenia! Do zobaczenia!'),
            en('Good luck, and see you soon.'),
            clear=True,
        ),
    ],
)

SCENES = [
    COVER,
    SOUNDS,
    GREETINGS,
    ABOUT_ME,
    TO_BE,
    GENDER,
    ADJECTIVES,
    VERBS,
    QUESTIONS,
    CASES,
    PREPOSITIONS,
    NUMBERS,
    SURVIVAL,
    TRAPS,
    PAST_FUTURE,
    CAFE,
    QUIZ,
    RECAP,
]
