# Fjern AI-tegn

Finder og fjerner tegn på AI-skrivning i dansk og engelsk tekst, efter reglerne i [STIL.md](STIL.md).

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

23 fund i 155 ord (14.8 per 100 ord).
```

Se [eksempler/ai_mail.txt](eksempler/ai_mail.txt) (23 fund) og den rensede udgave [eksempler/ai_mail_ren.txt](eksempler/ai_mail_ren.txt) (0 fund).

## Få teksten omskrevet

Åbn repoet i Claude Code og skriv `/fjern-ai-tegn` efterfulgt af teksten eller et filnavn. Skillen ligger i `.claude/skills/fjern-ai-tegn/`.

Den finder ikke på kilder, tal eller anekdoter. Hvor de mangler, skriver den `[KILDE?]` eller spørger dig. I videnskabelig tekst rører den ikke ved forbehold, statistik eller IMRaD-strukturen.

## Hvad scriptet ikke kan

Regel 1, 5, 15 og 16 handler om indhold: er teksten konkret, gentager den sig selv, tager den stilling. Det kræver at man forstår teksten, så det klarer skillen, ikke scriptet.

Scriptet giver falske positive. "Derfor" er tit det rigtige ord, og en treleddet opremsning kan være korrekt. Brug fundene som en liste at gå igennem, ikke som facit.

## Tilføj ord

Mønstrene står i [aitegn/regler.py](aitegn/regler.py), sorteret efter regelnummer. Tilføj en linje i den rigtige liste og kør testene:

```bash
python3 -m unittest
```
