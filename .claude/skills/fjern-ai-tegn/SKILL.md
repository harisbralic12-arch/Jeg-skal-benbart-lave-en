---
name: fjern-ai-tegn
description: Omskriv en tekst så tegnene på AI-skrivning forsvinder, efter reglerne i STIL.md. Brug når brugeren beder om at fjerne AI-tegn, "gøre teksten mindre AI-agtig", rense en tekst, eller skriver /fjern-ai-tegn. Virker på mails, opslag, notater, ansøgninger og videnskabelig tekst (abstracts, manuskripter, svar til reviewere).
---

# Fjern AI-tegn

Reglerne står i `STIL.md` i roden af repoet. Læs filen før du går i gang. Den er facit; denne skill beskriver kun fremgangsmåden.

## 1. Find teksten og genren

Teksten kommer enten som en fil (`.txt`, `.md`, `.docx`) eller indsat i beskeden. Ligger den i beskeden, så gem den i scratchpad-mappen som `.txt`.

Afgør om teksten er videnskabelig: manuskript, abstract, protokol, fondsansøgning eller svar til reviewere. Er du i tvivl, så spørg. Genren bestemmer hvilke regler der gælder.

## 2. Kør tjekket

```bash
python3 -m aitegn.tjek <fil>              # almindelig tekst
python3 -m aitegn.tjek <fil> --videnskabelig
```

Kør fra repoets rod. Scriptet finder de mekaniske tegn (ord, figurer, tankestreger, monoton rytme, forkortelser). Det ser ikke regel 1, 5, 15 og 16, som kræver at man forstår indholdet. Dem tjekker du selv.

Scriptet giver falske positive. "Derfor" kan være det rigtige ord, og "central" kan være en fagterm. Vurdér hvert fund.

## 3. Omskriv

- Ret kun det reglerne kræver. Bevar forfatterens pointer, tal, navne og rækkefølge.
- Find ikke på fakta, kilder, tal eller anekdoter. Peger regel 2 på en kilde uden navn, så slet påstanden eller skriv `[KILDE?]`. Mangler der personlig erfaring (regel 16), så spørg brugeren.
- Erstat ikke ét AI-ord med et andet. "Vigtig" i stedet for "central" hjælper ikke, hvis sætningen kan klare sig uden.
- Skriv på tekstens eget sprog.

### Videnskabelig tekst

- Forbehold bliver stående. "Associated with", "may", "suggests" må ikke blive til "leads to", "is" eller "shows".
- IMRaD og ensartede metodesætninger bliver stående.
- Ingen personlig holdning, undtagen i fortolkningen i diskussionen.
- Forkortelser skrives ud første gang: "optical coherence tomography (OCT)".
- Ændr ikke på tal, statistik, p-værdier eller konfidensintervaller.
- Er en påstand stærkere end data bærer, så skriv det til brugeren i stedet for at skrive den om i stilhed. Det er indhold, ikke sprog.

## 4. Tjek igen

Kør scriptet på den omskrevne tekst og ret det der stadig er tilbage, hvis det er et rigtigt fund.

## 5. Svar

Giv brugeren:

1. Den omskrevne tekst, klar til at kopiere.
2. En kort liste over de vigtigste ændringer (højst 6 punkter). Ikke hver eneste ordudskiftning.
3. Spørgsmål om det du ikke kunne løse selv: manglende kilder, manglende anekdote, påstande der rækker ud over data.
4. Antal fund før og efter fra scriptet, på én linje.

Hvis teksten lå i en fil og brugeren beder om det, så gem den nye version ved siden af med `_ren` i navnet. For `.docx` gemmes resultatet som `.txt` eller `.md`, medmindre brugeren beder om Word.
