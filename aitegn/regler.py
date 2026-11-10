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


# ---------------------------------------------------------------------------
# Tilføjet efter Wikipedia:Signs of AI writing (hentet november 2026).
# Regelnumre 19-26 svarer til tillægget i STIL.md.
# ---------------------------------------------------------------------------

# Udvidelse af regel 2: vage tilskrivninger
VAGE_KILDER += [
    (r"\b(industry reports|observers have (cited|noted)|experts argue|some critics argue|several (sources|publications))\b",
     "Vag tilskrivning. Hvem præcis?"),
    (r"\b(kritikere|iagttagere|observatører|nogle) (mener|påpeger|argumenterer|hævder)\b", "Vag tilskrivning. Hvem præcis?"),
    (r"\bflere kilder (peger på|nævner|beskriver)\b", "Hvor mange kilder er der egentlig?"),
]

# Udvidelse af regel 4: opsummerende afslutninger
META += [
    (r"(?:^|(?<=[.!?]\s))(overall|overordnet set),", "Opsummering. Slet eller skriv pointen."),
]

# Udvidelse af regel 6: Wikipedias liste over "AI vocabulary" og reklamesprog
OPPUSTEDE_ORD += [
    (r"\badditionally\b", "slet, eller also"),
    (r"\balign(s|ed)? with\b", "match / fit"),
    (r"\bboasts?\b", "has"),
    (r"\bbolster(s|ed|ing)?\b", "strengthen / support"),
    (r"\bdeep dive\b", "close look"),
    (r"\bemphasiz(e|es|ed|ing)\b", "slet eller sig det direkte"),
    (r"\benduring\b", "lasting, eller slet"),
    (r"\benhanc(e|es|ed|ing)\b", "improve"),
    (r"\bgarner(s|ed|ing)?\b", "get / receive"),
    (r"\bhighlight(s|ed|ing)\b", "show, eller slet"),
    (r"\binterplay\b", "relationship"),
    (r"\bintricac(y|ies)|\bintricate\b", "complex, eller slet"),
    (r"\bmeticulous(ly)?\b", "careful(ly)"),
    (r"\bvaluable\b", "useful, eller sig hvorfor"),
    (r"\bvibrant\b", "slet"),
    (r"\bmultifaceted\b", "sig hvilke sider"),
    (r"\bprioritiz(e|es|ed|ing)\b", "put first"),
    (r"\bquietly\b", "slet"),
    (r"\buniversally\b", "slet"),
    (r"\bnestled\b", "located / lies"),
    (r"\bin the heart of\b", "in"),
    (r"\bgroundbreaking\b", "sig hvad der er nyt"),
    (r"\brenowned\b", "known, eller slet"),
    (r"\bdiverse array\b", "range / many"),
    (r"\bcommitment to\b", "sig hvad de gør"),
    (r"\bexemplif(y|ies|ied)\b", "is an example of"),
    (r"\bprofound\b", "slet eller sig hvor stor"),
    (r"\bauthored\b", "wrote"),
    (r"\brelocated\b", "moved"),
    (r"\battempted\b", "tried"),
    (r"\bfremhæv(e|er|ede|et|es)\b", "vise, eller slet"),
    (r"\bsamspil(let)?\b", "sammenhæng / forhold"),
    (r"\bdybdegående\b", "grundig, eller slet"),
    (r"\bmangefacetteret\b", "sig hvilke sider"),
    (r"\bomhyggelig(t|e)?\b", "grundig(t), eller slet"),
    (r"\bværdifuld(e|t)?\b", "nyttig, eller sig hvorfor"),
    (r"\bi hjertet af\b", "i / midt i"),
    (r"\bbeliggende\b", "ligger"),
    (r"\banerkendt(e)?\b", "kendt, eller slet"),
]

# Regel 19: oppustet betydning, arv og mediedækning
BETYDNING = [
    (r"\b(stands|serves) as an? (testament|reminder|symbol|example)\b", "Oppustet betydning."),
    (r"\b(is|was|remains) an? (testament|reminder)\b", "Oppustet betydning."),
    (r"\ba (crucial|pivotal|vital|significant|key) (role|moment|turning point)\b", "Oppustet betydning."),
    (r"\b(underscores|highlights) (its|their|the) (importance|significance)\b", "Oppustet betydning."),
    (r"\breflects? (a )?broader\b", "Oppustet betydning."),
    (r"\b(symbolizing|marking|shaping) (its|the|a)\b", "Oppustet betydning."),
    (r"\bsetting the stage for\b", "Oppustet betydning."),
    (r"\b(represents?|marks?|marked|represented) a (significant |major )?shift\b", "Oppustet betydning."),
    (r"\b(key turning point|evolving landscape|focal point|indelible mark|deeply rooted|lasting legacy|enduring legacy)\b",
     "Oppustet betydning."),
    (r"\b(contributes|contributing) to the broader\b", "Oppustet betydning."),
    (r"\b(prompted|sparked|generated) (broader )?(debate|reflection|discussion)s?\b", "Hvilken debat? Hvem?"),
    (r"\bvidner om\b", "Oppustet betydning. Sig hvad det viser."),
    (r"\b(markerer|markerede) (et|en) (vendepunkt|milepæl|skift|nyt kapitel)\b", "Oppustet betydning."),
    (r"\b(et|en) (afgørende|skelsættende|vigtig) (vendepunkt|milepæl)\b", "Oppustet betydning."),
    (r"\bsætter scenen for\b", "Oppustet betydning."),
    (r"\b(varigt|uudsletteligt) (aftryk|præg)\b", "Oppustet betydning."),
    (r"\bdybt (forankret|rodfæstet)\b", "Oppustet betydning."),
    (r"\b(afspejler|spejler) (en )?(bredere|større|generel)\b", "Oppustet betydning."),
    (r"\b(featured|profiled|cited) in\b.{0,60}\b(outlets|media|publications)\b", "Mediedækning i stedet for indhold."),
    (r"\b(independent|national|regional|international) (media )?coverage\b", "Mediedækning i stedet for indhold."),
    (r"\b(maintains?|has) an? (active|strong) (social media|digital|online) presence\b", "Typisk AI-formulering."),
    (r"\b(stærk|aktiv) tilstedeværelse på (de )?sociale medier\b", "Typisk AI-formulering."),
    (r"\bomtalt i (bl\.a\.|blandt andet|flere|landsdækkende|nationale)\b", "Mediedækning i stedet for indhold."),
]

# Regel 20: overfladisk analyse hængt bag på sætningen
OVERFLADISK = [
    (r",\s+(highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|"
     r"encompassing|enhancing|showcasing|solidifying|reinforcing|demonstrating|illustrating)\b",
     "Analyse hængt bag på sætningen. Slet, eller gør den til en påstand med belæg."),
    (r",\s+hvilket (understreger|fremhæver|afspejler|vidner om|bidrager til|sikrer|styrker|illustrerer|demonstrerer|"
     r"cementerer|skaber|giver)\b",
     "Analyse hængt bag på sætningen. Slet, eller gør den til en påstand med belæg."),
    (r"\bvaluable insights?\b|\bværdifuld(e)? indsigt(er)?\b", "Hvilken indsigt?"),
    (r"\bresonate(s|d)? with\b|\bresonerer (med|hos)\b", "Typisk AI-formulering."),
]

# Regel 21: "er" og "har" frem for omskrivninger
KOPULA = [
    (r"\b(serves|stands|functions|operates) as an?\b", "Skriv »is«."),
    (r"\b(boasts|features|offers) an?\b", "Skriv »has«, hvis det er det der menes."),
    (r"\b(tjener|står) som (en|et)\b", "Skriv »er«."),
    (r"\bbyder på\b", "Skriv »har«."),
    (r"\bfremstår som (en|et)\b", "Skriv »er«, hvis det er det der menes."),
]

# Regel 22: chatbot-rester. Stærke tegn: teksten var skrevet til den der promptede.
CHATBOT = [
    (r"\b(I hope this helps|I hope this is helpful)\b", "Chatbot-rest."),
    (r"(^|\n)\s*(Of course|Certainly|Absolutely|Sure)!", "Chatbot-rest."),
    (r"\byou'?re absolutely right\b", "Chatbot-rest."),
    (r"\bgreat question\b", "Chatbot-rest."),
    (r"\b(would you like (me to|a)|is there anything else|let me know if you('d| would)? (like|want|need))\b", "Chatbot-rest."),
    (r"\bhere is an? (revised|rewritten|polished|draft|version|summary|more detailed)\b", "Chatbot-rest."),
    (r"\bmore detailed breakdown\b", "Chatbot-rest."),
    (r"\b(as an AI|as a large) language model\b", "Chatbot-rest."),
    (r"\b(as of|up to) my (last|latest) (knowledge|training) (update|cutoff)\b", "Chatbot-rest (videnstop)."),
    (r"\bjeg håber (dette|det|det her) (hjælper|kan bruges)\b", "Chatbot-rest."),
    (r"(^|\n)\s*(Selvfølgelig|Absolut|Helt sikkert)!", "Chatbot-rest."),
    (r"\bdu har (helt )?ret\b!", "Chatbot-rest."),
    (r"\bgodt spørgsmål\b", "Chatbot-rest."),
    (r"\b(vil du have at jeg|skal jeg også|lad mig vide hvis)\b", "Chatbot-rest."),
    (r"\bher er (en|et) (omskrevet|revideret|forbedret|kortere|længere|opdateret|bud|forslag|udkast|version)\b",
     "Chatbot-rest."),
    (r"\bsom (en )?(AI|sprogmodel)\b", "Chatbot-rest."),
    (r"\b(pr\.|per|ifølge) min (seneste|sidste) (opdatering|træning)\b", "Chatbot-rest (videnstop)."),
]

# Regel 22 fortsat: kildeforbehold og "korrigerende" forbehold (stærkt tegn fra 2024-26)
KILDEFORBEHOLD = [
    (r"\bwhile specific (details|information) (about .{0,60})?(is|are) (limited|scarce)\b", "Kildeforbehold. Slet."),
    (r"\bnot (widely|extensively|publicly) (available|documented|disclosed|transcribed)\b", "Kildeforbehold. Slet."),
    (r"\bin the (provided|available) (sources|search results|information)\b", "Chatbot-rest."),
    (r"\bbased on (the )?available information\b", "Kildeforbehold."),
    (r"\bshould be (treated|presented|understood|read) as\b.{0,60}\brather than\b", "Korrigerende forbehold."),
    (r"\bdoes not (by itself|on its own) establish\b", "Korrigerende forbehold."),
    (r"\bshould not be confused with\b", "Muligt korrigerende forbehold."),
    (r"\b(baseret på|ud fra) (de )?tilgængelige (oplysninger|kilder|data)\b", "Kildeforbehold."),
    (r"\bikke (offentligt|bredt) (tilgængelig|dokumenteret|beskrevet)e?\b", "Kildeforbehold. Slet."),
    (r"\bi de (angivne|tilgængelige|leverede) kilder\b", "Chatbot-rest."),
    (r"\bbør (ses|læses|behandles|forstås) som\b.{0,60}\b(frem for|snarere end|i stedet for)\b", "Korrigerende forbehold."),
    (r"\bbør ikke forveksles med\b", "Muligt korrigerende forbehold."),
    (r"\bkan ikke i sig selv (fastslå|dokumentere|bevise)\b", "Korrigerende forbehold."),
]

# Regel 22 fortsat: pladsholdere og tekniske artefakter. Altid stærke tegn.
ARTEFAKTER = [
    (r"\[(your|insert|name|date|source|company|describe|add|navn|dato|indsæt|kilde|firma|beskriv|dit|din)\b[^\]]{0,80}\]",
     "Pladsholder der ikke er udfyldt."),
    (r"INSERT_[A-Z_#]+", "Pladsholder der ikke er udfyldt."),
    (r"\b20\d\d-xx-xx\b|\bXX\.XX\.20\d\d\b", "Pladsholderdato."),
    (r"contentReference|oaicite|\bturn\d+(search|news|view|fetch)\d+\b|【\d+[^】]*】|\bciteturn|\bfilecite",
     "Citations-artefakt fra en chatbot."),
    (r"utm_source=(chatgpt\.com|openai|copilot\.com)|referrer=grok\.com", "Link kopieret fra en chatbot."),
    (r"```", "Markdown-kodeblok."),
]

# Regel 23: procesforsikringer (typisk i svar til reviewere og følgebreve)
PROCESFORSIKRING = [
    (r"\bto (enhance|improve|ensure) (the )?(clarity|flow|readability|coherence|consistency|accuracy)\b",
     "Procesforsikring. Sig hvad der konkret er ændret."),
    (r"\b(clarity|readability) and (flow|coherence|conciseness)\b", "Procesforsikring."),
    (r"\bwhile (preserving|retaining|maintaining) (the )?(original|core|key)\b", "Procesforsikring."),
    (r"\b(streamlined|refined|enriched)\b", "Procesforsikring. Hvad blev ændret?"),
    (r"\bwe have carefully (revised|reviewed|considered|addressed)\b", "Procesforsikring. Hvad blev ændret?"),
    (r"\bfor at (sikre|forbedre|øge) (klarhed|læsbarhed|flow|sammenhæng|præcision)\b",
     "Procesforsikring. Sig hvad der konkret er ændret."),
    (r"\b(klarhed|læsbarhed) og (flow|sammenhæng)\b", "Procesforsikring."),
    (r"\bmed (bevarelse|fastholdelse) af (det )?(oprindelige|centrale)\b", "Procesforsikring."),
    (r"\bvi har (omhyggeligt|grundigt|nøje) (gennemgået|revideret|overvejet)\b", "Procesforsikring. Hvad blev ændret?"),
]

# Regel 24: kundeservicetone
KUNDESERVICE = [
    (r"\bI hope (this|my) (message|email|letter) finds you well\b", "Kundeservicetone."),
    (r"\bI am writing to (request|inquire|follow up|express)\b", "Start med ærindet."),
    (r"\bapologi[sz]e for any (inconvenience|confusion)\b", "Kundeservicetone."),
    (r"\bplease (do not|don't) hesitate to\b", "Kundeservicetone."),
    (r"\bjeg håber (denne|min) (mail|besked|henvendelse) finder dig\b", "Kundeservicetone."),
    (r"\bjeg skriver (for at|til dig for at|angående)\b", "Start med ærindet."),
    (r"\b(undskyld|beklager) (for )?(eventuelle|evt\.) (gener|ulemper|misforståelser)\b", "Kundeservicetone."),
    (r"\b(tøv|tøv derfor) ikke med at\b", "Kundeservicetone."),
]

# Regel 26: udfordringer-og-fremtid-formlen
UDFORDRINGER = [
    (r"\bdespite (these|its|their|the) (challenges|limitations|setbacks)\b", "Udfordringer-og-fremtid-formlen."),
    (r"\bdespite (its|their) .{0,60}\bfaces? (several |many |numerous )?challenges\b", "Udfordringer-og-fremtid-formlen."),
    (r"\b(future (outlook|prospects|directions)|challenges and (legacy|opportunities))\b", "Udfordringer-og-fremtid-formlen."),
    (r"\b(trods|på trods af) (disse|de|sine|deres) (udfordringer|begrænsninger)\b", "Udfordringer-og-fremtid-formlen."),
    (r"\bstår (dog )?over for (flere|en række|visse|mange) udfordringer\b", "Udfordringer-og-fremtid-formlen."),
    (r"\bfremtidsudsigter\b", "Udfordringer-og-fremtid-formlen."),
]

# Regel 10 udvidet: flere negative parallelismer
FIGURER += [
    (r"\b(it'?s|it is|this is) not (about )?[^.,;]{1,50}[.,;] (it'?s|it is|this is)\b", "\"It's not X, it's Y\"."),
    (r"\bno [^.,;]{1,25}, no [^.,;]{1,25}, (just|only)\b", "\"No X, no Y, just Z\"."),
    (r"\bdet handler ikke om\b.{1,60}?\bmen om\b", "\"Det handler ikke om X, men om Y\"-figur."),
    (r"\bdet er ikke [^.,;]{1,50}\. det er\b", "\"Det er ikke X. Det er Y\"-figur."),
    (r"\bingen [^.,;]{1,25}, ingen [^.,;]{1,25}, (bare|kun)\b", "\"Ingen X, ingen Y, bare Z\"-figur."),
]

# Hvilke regler der er stærke tegn (sjældne hos mennesker) og ikke bare stil
STAERKE_REGLER = {22}

# Ord der ikke markeres i videnskabelig tekst, fordi de er almindelige fagudtryk der
VIDENSKAB_UNDTAGET |= {"enhance", "enhanced", "enhancing", "enhances", "valuable", "attempted", "highlighted",
                       "emphasizing", "værdifuld", "værdifulde", "anerkendt", "anerkendte", "omhyggelig",
                       "omhyggeligt", "dybdegående", "samspil", "samspillet"}

# Emoji i starten af overskrifter og punkter (regel 14)
EMOJI = r"^\s*(?:[-*•]\s*|#{1,6}\s*)?[\U0001F300-\U0001FAFF☀-➿⭐✅]"

# Regel 1: huller markeret med [NOGET?], fx af skillen fjern-ai-tegn
HULLER = [(r"\[[A-ZÆØÅ ]+\?\]", "Mangler: udfyld før teksten sendes.")]
