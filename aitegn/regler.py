"""Mønstre der afslører AI-skrevet tekst, ordnet efter reglerne i STIL.md.

Hver regel er (regel-nr, regex, besked). Regex matches case-insensitivt
med ordgrænser, medmindre andet står.
"""

# Regel 2: kilde uden navn
VAGE_KILDER = [
    (r"\b(flere |nyere |mange )?(studier|undersøgelser|forskning) (viser|har vist|peger på|tyder på)\b",
     "Hvilke studier? Navngiv kilden eller fjern påstanden."),
    (r"\beksperter (mener|siger|vurderer|anbefaler)\b", "Hvilke eksperter? Navngiv dem."),
    (r"\bdet er (alment )?(kendt|anerkendt|veldokumenteret) at\b", "Hvem siger det? Navngiv kilden."),
    (r"\b(studies|research|experts?) (show|shows|suggest|suggests|say|says|have shown)\b",
     "Name the source or drop the claim."),
    (r"\bit is (widely|well|generally) (known|accepted|established)\b", "Name the source."),
]

# Regel 3: processen i stedet for konklusionen
PROCES = [
    (r"\ben (gennemgang|analyse|undersøgelse) af (litteraturen|data|tallene) (viser|afslører)\b",
     "Skriv konklusionen direkte."),
    (r"\bman kan (se|konstatere|konkludere) at\b", "Skriv konklusionen direkte."),
    (r"\ba (review|analysis) of the (literature|data) (shows|reveals)\b", "State the finding directly."),
]

# Regel 4: meta
META = [
    (r"\bi (denne|dette) (tekst|artikel|opslag|indlæg|notat|mail|afsnit)\b.{0,30}\b(vil jeg|vil vi|gennemgår|ser vi på|kigger)\b",
     "Meta. Start med indholdet."),
    (r"\bsammenfattende\b", "Meta-afrunding. Slet eller skriv pointen."),
    (r"\bafslutningsvis\b", "Meta-afrunding."),
    (r"\b(kort sagt|alt i alt|samlet set|som nævnt|som tidligere nævnt)\b", "Meta. Kan som regel slettes."),
    (r"\blad os (se på|kigge på|dykke)\b", "Meta."),
    (r"\b(in this (article|post|text|essay)|in conclusion|to sum up|in summary|let's (dive|take a look))\b",
     "Meta."),
]

# Regel 6: oppustede ord. (mønster, erstatning)
OPPUSTEDE_ORD = [
    (r"\banvend(e|er|te|t|es|else|elsen)\b", "bruge"),
    (r"\bpåbegynd(e|er|te|t|es)\b", "starte"),
    (r"\bdemonstrer(e|er|ede|et|es)\b", "vise"),
    (r"\bdykke(r|de|t)? (dybere )?ned i\b", "se på / undersøge"),
    (r"\bfremvis(e|er|te|t|ning)\b", "vise"),
    (r"\bunderstreg(e|er|ede|et|es)\b", "slet eller sig det direkte"),
    (r"\bbemærkelsesværdig(e|t)?\b", "slet eller sig hvad der er overraskende"),
    (r"\bcentral(e|t)?\b(?! (subfield|retinal|retina|vision|visual|serous|scotoma|corneal|macular|fixation|nervous|vein|artery|synsfelt|nethinde|serøs|skotom|venetrombose|veneokklusion|nervesystem))",
     "vigtig, eller slet"),
    (r"\bmangfoldig(e|t|hed)?\b", "sig hvad der er forskelligt"),
    (r"\bet vidnesbyrd om\b", "viser"),
    (r"\ben overflod af\b", "mange"),
    (r"\bfacilitere(r|de|t)?\b", "hjælpe / gøre muligt"),
    (r"\bimplementere(r|de|t)?\b", "indføre / bruge"),
    (r"\boptimere(r|de|t)?\b", "forbedre"),
    (r"\bi bund og grund\b", "slet"),
    (r"\bspiller en (afgørende |vigtig |central |nøgle)rolle\b", "sig hvad det gør"),
    (r"\bbanebrydende\b", "sig hvad der er nyt"),
    (r"\bi en verden hvor\b", "slet"),
    (r"\bnavigere(r)? i\b", "håndtere"),
    (r"\b(delve|delves|delving)\b", "look at"),
    (r"\b(leverage|leverages|leveraging)\b", "use"),
    (r"\b(utilize|utilizes|utilizing|utilise|utilization)\b", "use"),
    (r"\bfurthermore\b", "slet"),
    (r"\btapestry\b", "slet"),
    (r"\b(showcase|showcases|showcasing)\b", "show"),
    (r"\b(underscore|underscores|underscoring)\b", "show, eller slet"),
    (r"\b(pivotal|crucial)\b", "important, eller slet"),
    (r"\b(seamless|seamlessly|robust)\b", "sig hvad det betyder konkret"),
    (r"\b(realm|landscape)\b", "field / area, eller slet"),
    (r"\b(foster|fosters|fostering)\b", "help / build"),
    (r"\b(testament to)\b", "shows"),
    (r"\bnavigat(e|es|ing) the\b", "handle"),
    (r"\bin today's (fast-paced )?(world|landscape)\b", "slet"),
]

# Regel 7: skriftsprogsord med talesprogsnær afløser
FORMELLE_ORD = [
    (r"\bintet\b", "ikke noget"),
    (r"\bingen som helst\b", "ingen"),
    (r"\bsåledes\b", "sådan"),
    (r"\bhvorvidt\b", "om"),
    (r"\bsåfremt\b", "hvis"),
    (r"\bendvidere\b", "også, eller slet"),
    (r"\bherudover\b", "slet"),
    (r"\bhvorledes\b", "hvordan"),
    (r"\beftersom\b", "fordi"),
    (r"\bhvorfor (det|dette) er\b", "så det er"),
    (r"\bi forbindelse med\b", "ved / når"),
    (r"\bmed henblik på\b", "for at"),
    (r"\bi henhold til\b", "efter"),
    (r"\bvedrørende\b", "om"),
]

# Regel 8: overgangsord i starten af en sætning
OVERGANGSORD = [
    "desuden", "dog", "derudover", "yderligere", "endvidere", "ydermere",
    "samtidig", "herudover", "derfor", "imidlertid", "endelig",
    "moreover", "additionally", "however", "furthermore", "consequently",
    "nevertheless", "importantly", "notably", "ultimately",
]

# Regel 9: stablede forbehold
FORBEHOLD = [
    (r"\b(kunne|kan|vil|ville) (potentielt|muligvis|eventuelt|måske|formentlig)\b.{0,25}\b(tænkes|være|have)\b",
     "Stablet forbehold. Sig det direkte."),
    (r"\b(potentielt|muligvis) (kunne|kan)\b", "Dobbelt forbehold."),
    (r"\bi et vist omfang\b", "Vagt. Hvor stort er omfanget?"),
    (r"\b(could|might|may) (potentially|possibly|perhaps)\b", "Stacked hedge."),
    (r"\bto some extent\b", "Vague."),
]

# Regel 10: faste AI-figurer
FIGURER = [
    (r"\bdet er ikke (bare|blot|kun)\b.{0,80}?\b(det er|men)\b", "\"Ikke bare X, men Y\"-figur."),
    (r"\bikke (bare|blot|kun)\b.{1,60}?\bmen (også)?\b", "\"Ikke bare X, men også Y\"-figur."),
    (r"\bdet er (vigtigt|værd|relevant) at (bemærke|nævne|understrege|huske)\b", "Slet. Skriv pointen."),
    (r"\bdet skal (bemærkes|nævnes|understreges)\b", "Slet. Skriv pointen."),
    (r"\b(it'?s|it is) not (just|only|merely)\b.{0,80}?\b(it'?s|it is|but)\b", "\"Not just X, it's Y\"."),
    (r"\bnot only\b.{1,60}?\bbut (also)?\b", "\"Not only X but also Y\"."),
    (r"\b(it'?s|it is) (important|worth) (to note|noting)\b", "Delete. Make the point."),
]

# Regel 17: besjæling
BESJAELING = [
    (r"\b(data|tallene|resultaterne|statistikken) (fortæller|taler|siger)\b", "Data fortæller ikke noget. Sig hvad tallene er."),
    (r"\bmarkedet (taler|siger|fortæller|mener)\b", "Markedet taler ikke."),
    (r"\b(data|numbers|the market) (tells?|speaks?|says?)\b", "Personification."),
    (r"\bfortæller en historie\b", "Besjæling."),
    (r"\btells a story\b", "Personification."),
]

# Regel 18: opmuntrende slutning (kun tjekket i sidste afsnit)
OPMUNTRING = [
    r"\b(spændende|lys(e)? fremtid|ser lys(t)? ud|i sidste ende|når alt kommer til alt|uanset hvad|mulighederne er|ser frem til|rejse)\b",
    r"\b(exciting|bright future|ultimately|at the end of the day|journey|the possibilities are)\b",
]

# Ord der er fagtermer i videnskabelig tekst og ikke markeres der
VIDENSKAB_UNDTAGET = {"robust", "central", "centrale", "centralt", "landscape", "implementere", "optimere"}

# Regel 13: tankestreger
LANG_TANKESTREG = "—"  # —
KORT_TANKESTREG_MELLEMRUM = " – "  # " – "
