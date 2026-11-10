# Fjern AI-tegn

Finder og fjerner tegn på AI-skrivning i dansk og engelsk tekst, efter reglerne i [STIL.md](STIL.md). Regel 19 til 26 og en stor del af ordlisterne kommer fra [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), læst november 2026.

Værktøjet har to dele. Et Python-script markerer de mekaniske tegn: ordvalg, faste figurer, tankestreger, monoton sætningsrytme og forkortelser der ikke er skrevet ud. En Claude Code-skill omskriver teksten og bruger scriptet til at tjekke før og efter.

## Tjek en tekst

Kræver kun Python 3.9 eller nyere. Ingen pakker at installere.

```bash
python3 -m aitegn.tjek min_mail.txt
python3 -m aitegn.tjek manuskript.docx --videnskabelig
python3 -m aitegn.tjek tekst.md --json
pbpaste | python3 -m aitegn.tjek -          # macOS: tjek det du har kopieret
```

Med `--videnskabelig` slås regel 9, 11, 12, 15 og 16 fra, ord som "central" og "robust" må gerne stå, og forkortelser der ikke er skrevet ud første gang bliver markeret.

Eksempel på output:

```
     linje 5  Kilde (regel 2): Hvilke studier? Navngiv kilden eller fjern påstanden.
              …l rolle for afdelingen.  Studier viser at kunstig intelligens k…
     linje 7  Besjæling (regel 17): Data fortæller ikke noget. Sig hvad tallene er.
              …angfoldig patientgruppe. Data fortæller en klar historie om hvor…

24 fund i 155 ord (15.5 per 100 ord).
```

Fund under regel 22 tæller som stærke tegn: "Her er en revideret version", ikke udfyldte pladsholdere, citations-rester som `oaicite` og links med `utm_source=chatgpt.com`. Mennesker skriver dem næsten aldrig. Resten er stiltegn, og ét af dem betyder ikke noget alene. Det er når de hober sig op, at teksten lyder som AI.

Eksempler:

- [eksempler/ai_mail.txt](eksempler/ai_mail.txt): dansk mail, 24 fund. Den rensede udgave [eksempler/ai_mail_ren.txt](eksempler/ai_mail_ren.txt) har kun to huller markeret med `[…?]`, som skal udfyldes.
- [eksempler/chatbot_svar.txt](eksempler/chatbot_svar.txt): engelsk følgebrev kopieret direkte fra en chatbot, 31 fund, heraf 4 stærke.
- [eksempler/abstract.txt](eksempler/abstract.txt): abstract, tjekket med `--videnskabelig`.

## Få teksten omskrevet

Åbn repoet i Claude Code og skriv `/fjern-ai-tegn` efterfulgt af teksten eller et filnavn. Skillen ligger i `.claude/skills/fjern-ai-tegn/`.

Den finder ikke på kilder, tal eller anekdoter. Hvor de mangler, skriver den `[KILDE?]` eller spørger dig. I videnskabelig tekst rører den ikke ved forbehold, statistik eller IMRaD-strukturen.

## Hvad scriptet ikke kan

Regel 1, 5, 15, 16 og 25 handler om indhold: er teksten konkret, gentager den sig selv, tager den stilling. Det kræver at man forstår teksten, så det klarer skillen, ikke scriptet.

Wikipedia advarer selv mod at stole på detektorer, og mod at tro man selv kan se forskel: i et studie fra 2025 ramte mennesker uden erfaring med sprogmodeller ikke bedre end tilfældigt. Scriptet siger ikke om en tekst er skrevet af AI. Det peger på formuleringer der lyder sådan.

Scriptet giver falske positive. "Derfor" er tit det rigtige ord, og en treleddet opremsning kan være korrekt. Brug fundene som en liste at gå igennem, ikke som facit.

## Tilføj ord

Mønstrene står i [aitegn/regler.py](aitegn/regler.py), sorteret efter regelnummer. Tilføj en linje i den rigtige liste og kør testene:

```bash
python3 -m unittest
```
