"""Find tegn på AI-skrevet tekst.

Brug:
    python3 -m aitegn.tjek min_tekst.txt
    python3 -m aitegn.tjek manuskript.docx --videnskabelig
    pbpaste | python3 -m aitegn.tjek -
    python3 -m aitegn.tjek tekst.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path

from . import regler

# Regler der er sat ud af kraft i videnskabelig tekst (se STIL.md)
SLAAET_FRA_I_VIDENSKAB = {9, 11, 12, 15, 16}
# Regel 21 ("serves as a control") og kildeforbehold er normalt sprog i manuskripter
SLAAET_FRA_I_VIDENSKAB_EKSTRA = {21}

FLAGS = re.IGNORECASE | re.UNICODE


@dataclass
class Fund:
    regel: int
    linje: int
    tekst: str
    besked: str


def laes_fil(sti: str) -> str:
    if sti == "-":
        return sys.stdin.read()
    p = Path(sti)
    if p.suffix.lower() == ".docx":
        return laes_docx(p)
    return p.read_text(encoding="utf-8")


def laes_docx(p: Path) -> str:
    """Træk tekst ud af en .docx uden eksterne pakker. Ét afsnit per blok."""
    with zipfile.ZipFile(p) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    afsnit = []
    for para in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.DOTALL):
        dele = re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>|<w:(tab|br)/>", para, flags=re.DOTALL)
        tekst = "".join(t if t else (" " if kind == "tab" else "\n") for t, kind in dele)
        tekst = (tekst.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                 .replace("&quot;", '"').replace("&apos;", "'"))
        afsnit.append(tekst)
    return "\n\n".join(a for a in afsnit if a.strip())


def linjenummer(tekst: str, pos: int) -> int:
    return tekst.count("\n", 0, pos) + 1


def uddrag(tekst: str, start: int, slut: int, kontekst: int = 25) -> str:
    a = max(0, start - kontekst)
    b = min(len(tekst), slut + kontekst)
    s = tekst[a:b].replace("\n", " ")
    return ("…" if a > 0 else "") + s + ("…" if b < len(tekst) else "")


def find_afsnit(tekst: str) -> list[tuple[int, str]]:
    """Returnér (startposition, afsnitstekst) for hvert afsnit adskilt af tom linje."""
    res = []
    for m in re.finditer(r"(?:[^\n]|\n(?!\s*\n))+", tekst):
        if m.group().strip():
            res.append((m.start(), m.group()))
    return res


def find_saetninger(afsnit: str) -> list[tuple[int, str]]:
    res = []
    for m in re.finditer(r"[^.!?\n]+(?:[.!?]+|$)", afsnit):
        s = m.group().strip()
        if len(s.split()) >= 2:
            res.append((m.start() + len(m.group()) - len(m.group().lstrip()), s))
    return res


def ord_antal(s: str) -> int:
    return len(re.findall(r"\w+", s))


def tjek(tekst: str, videnskabelig: bool = False, markdown_i_docx: bool = False) -> tuple[list[Fund], dict]:
    fund: list[Fund] = []

    brugt: dict[int, list[tuple[int, int]]] = {}

    def tilfoej(regel: int, start: int, slut: int, besked: str):
        if videnskabelig and (regel in SLAAET_FRA_I_VIDENSKAB or regel in SLAAET_FRA_I_VIDENSKAB_EKSTRA):
            return
        if slut > start:
            if any(start < b and a < slut for a, b in brugt.get(regel, [])):
                return  # samme sted er allerede markeret under samme regel
            brugt.setdefault(regel, []).append((start, slut))
        fund.append(Fund(regel, linjenummer(tekst, start), uddrag(tekst, start, slut), besked))

    def kør_liste(regel: int, liste):
        for mønster, besked in liste:
            for m in re.finditer(mønster, tekst, FLAGS):
                tilfoej(regel, m.start(), m.end(), besked)

    kør_liste(1, regler.HULLER)
    kør_liste(2, regler.VAGE_KILDER)
    kør_liste(3, regler.PROCES)
    kør_liste(4, regler.META)
    for mønster, erstatning in regler.OPPUSTEDE_ORD:
        for m in re.finditer(mønster, tekst, FLAGS):
            if videnskabelig and m.group().lower() in regler.VIDENSKAB_UNDTAGET:
                continue
            tilfoej(6, m.start(), m.end(), f"»{m.group()}« → {erstatning}")
    for mønster, erstatning in regler.FORMELLE_ORD:
        for m in re.finditer(mønster, tekst, FLAGS):
            tilfoej(7, m.start(), m.end(), f"»{m.group()}« → {erstatning}")
    kør_liste(9, regler.FORBEHOLD)
    kør_liste(10, regler.FIGURER)
    kør_liste(17, regler.BESJAELING)
    kør_liste(19, regler.BETYDNING)
    kør_liste(20, regler.OVERFLADISK)
    kør_liste(21, regler.KOPULA)
    kør_liste(22, regler.CHATBOT)
    kør_liste(22, regler.ARTEFAKTER)
    if not videnskabelig:
        kør_liste(22, regler.KILDEFORBEHOLD)
    kør_liste(23, regler.PROCESFORSIKRING)
    kør_liste(24, regler.KUNDESERVICE)
    kør_liste(26, regler.UDFORDRINGER)

    afsnit = find_afsnit(tekst)
    alle_saetninger: list[int] = []

    # Regel 8: overgangsord i sætningsstart
    overgang_re = re.compile(r"^(" + "|".join(regler.OVERGANGSORD) + r")\b", FLAGS)
    afsnit_med_overgang = 0
    for a_start, a in afsnit:
        saetninger = find_saetninger(a)
        alle_saetninger.extend(ord_antal(s) for _, s in saetninger)
        første = True
        for s_start, s in saetninger:
            m = overgang_re.match(s)
            if m:
                tilfoej(8, a_start + s_start, a_start + s_start + len(m.group()),
                        f"Sætningen starter med »{m.group()}«. Kan den undværes?")
                if første:
                    afsnit_med_overgang += 1
            første = False

    # Regel 11: ens sætningslængder
    stats = {"ord": ord_antal(tekst), "saetninger": len(alle_saetninger), "afsnit": len(afsnit)}
    if len(alle_saetninger) >= 6:
        snit = statistics.mean(alle_saetninger)
        cv = statistics.pstdev(alle_saetninger) / snit if snit else 0
        stats["saetningslaengde_snit"] = round(snit, 1)
        stats["saetningslaengde_variation"] = round(cv, 2)
        if cv < 0.35:
            tilfoej(11, 0, 0, f"Sætningerne er næsten lige lange (snit {snit:.0f} ord, "
                               f"variation {cv:.2f}). Bland korte og lange.")
        # Nyere modeller holder sætninger mellem 8 og 20 ord (Wikipedia, 2026)
        andel = sum(8 <= n <= 20 for n in alle_saetninger) / len(alle_saetninger)
        stats["andel_8_til_20_ord"] = round(andel, 2)
        if len(alle_saetninger) >= 8 and andel >= 0.85:
            tilfoej(11, 0, 0, f"{andel:.0%} af sætningerne er mellem 8 og 20 ord. "
                               "Det er typisk for nyere AI-modeller. Skriv nogle meget korte og nogle lange.")
        # Lange stræk af ens sætninger
        stræk = 1
        for x, y in zip(alle_saetninger, alle_saetninger[1:]):
            stræk = stræk + 1 if abs(x - y) <= 3 else 1
            if stræk == 5:
                tilfoej(11, 0, 0, "Fem sætninger i træk med næsten samme længde.")
    if len(afsnit) >= 4:
        længder = [ord_antal(a) for _, a in afsnit if not re.match(r"\s*([-*•#]|\d+\.)", a)]
        if len(længder) >= 4:
            snit = statistics.mean(længder)
            cv = statistics.pstdev(længder) / snit if snit else 0
            if cv < 0.25:
                tilfoej(11, 0, 0, f"Afsnittene er næsten lige lange (variation {cv:.2f}).")

    # Regel 12: treleddede opremsninger
    tre_led = list(re.finditer(r"\b[\w-]+(?: [\w-]+){0,2}, [\w-]+(?: [\w-]+){0,2},? (?:og|eller|and|or) [\w-]+",
                               tekst, FLAGS))
    stats["tre_led"] = len(tre_led)
    if len(tre_led) >= 3:
        for m in tre_led:
            tilfoej(12, m.start(), m.end(), "Tre led i opremsningen. Er det tredje led nødvendigt?")

    # Regel 13: tankestreger
    for m in re.finditer(regler.LANG_TANKESTREG, tekst):
        tilfoej(13, m.start(), m.end(), "Lang tankestreg. Brug komma, kolon eller parentes.")
    kort = [m for m in re.finditer(re.escape(regler.KORT_TANKESTREG_MELLEMRUM), tekst)]
    if len(kort) >= 2:
        for m in kort:
            tilfoej(13, m.start(), m.end(), "Tankestreg. Duer komma, kolon eller parentes?")

    # Regel 14: formatering
    fed = re.findall(r"\*\*[^*]+\*\*|__[^_]+__", tekst)
    linjer = [l for l in tekst.splitlines() if l.strip()]
    punkter = [l for l in linjer if re.match(r"\s*([-*•]|\d+[.)])\s", l)]
    overskrifter = [l for l in linjer if re.match(r"\s*#{1,6}\s", l)]
    stats.update(fed=len(fed), punktlinjer=len(punkter), overskrifter=len(overskrifter))
    if len(fed) >= 3:
        tilfoej(14, 0, 0, f"{len(fed)} steder med fed skrift. Hjælper de læsningen?")
    if linjer and len(punkter) / len(linjer) > 0.4 and len(punkter) >= 4:
        tilfoej(14, 0, 0, f"{len(punkter)} af {len(linjer)} linjer er punkter. Ville prosa være bedre?")
    if punkter:
        pl = [ord_antal(p) for p in punkter]
        if len(pl) >= 4 and statistics.mean(pl) and statistics.pstdev(pl) / statistics.mean(pl) < 0.25:
            tilfoej(14, 0, 0, "Alle punkter fylder næsten lige meget.")
    for m in re.finditer(regler.EMOJI, tekst, re.MULTILINE):
        tilfoej(14, m.start(), m.end(), "Emoji i starten af en overskrift eller et punkt.")
    for m in re.finditer(r"^\s*(?:[-*•]|\d+[.)])\s+(\*\*|__)[^*_\n]{1,40}:?(\*\*|__):?", tekst, re.MULTILINE):
        tilfoej(14, m.start(), m.end(), "Punkt med fed overskrift (\"inline header\"). Typisk AI-liste.")
    for m in re.finditer(r"^\s*#{1,6}\s+(.+)$", tekst, re.MULTILINE):
        småord = {"and", "or", "the", "of", "in", "for", "to", "a", "an", "on", "with", "at", "by"}
        ordene = [o for o in re.findall(r"[A-Za-z]+", m.group(1)) if o.lower() not in småord]
        if len(ordene) >= 3 and all(o[0].isupper() for o in ordene):
            tilfoej(14, m.start(), m.end(), "Overskrift i Title Case. Skriv kun første ord med stort.")
    if markdown_i_docx:
        tilfoej(22, 0, 0, "Word-dokumentet indeholder Markdown (** eller #). Teksten er kopieret fra en chatbot.")
    if overskrifter and stats["ord"] < 400:
        tilfoej(14, 0, 0, f"{len(overskrifter)} overskrifter i en tekst på {stats['ord']} ord.")

    # Regel 18: opmuntrende slutning
    # Hilsner som "Bedste hilsner" tæller ikke som sidste afsnit
    indholdsafsnit = [(s, a) for s, a in afsnit if ord_antal(a) >= 8]
    if indholdsafsnit:
        sidste_start, sidste = indholdsafsnit[-1]
        for mønster in regler.OPMUNTRING:
            for m in re.finditer(mønster, sidste, FLAGS):
                tilfoej(18, sidste_start + m.start(), sidste_start + m.end(),
                        "Opmuntrende slutning. Slut hvor indholdet slutter.")

    # Videnskabelig: forkortelser skal skrives ud første gang
    if videnskabelig:
        set_ = set()
        for m in re.finditer(r"\b([A-ZÆØÅ][A-ZÆØÅ0-9-]*[A-ZÆØÅ0-9])s?\b", tekst):
            ab = m.group(1)
            if ab in set_ or re.fullmatch(r"[IVXLCDM]+", ab):
                continue
            set_.add(ab)
            # Defineret = står i parentes, evt. med præfiks som "(anti-VEGF)"
            før = tekst[max(0, m.start() - 15):m.start()]
            efter = tekst[m.end():m.end() + 1]
            if not (re.search(r"\([\w-]*$", før) and efter in (")", ",", ";")):
                tilfoej(0, m.start(), m.end(),
                        f"»{ab}« bruges uden at være skrevet helt ud først.")

    fund.sort(key=lambda f: (f.linje, f.regel))
    stats["fund"] = len(fund)
    stats["staerke_fund"] = sum(f.regel in regler.STAERKE_REGLER for f in fund)
    stats["fund_per_100_ord"] = round(100 * len(fund) / stats["ord"], 1) if stats["ord"] else 0
    return fund, stats


REGELNAVNE = {
    0: "Forkortelse",
    1: "Hul",
    2: "Kilde",
    3: "Proces",
    4: "Meta",
    6: "Oppustet ord",
    7: "Formelt ord",
    8: "Overgangsord",
    9: "Forbehold",
    10: "AI-figur",
    11: "Rytme",
    12: "Skabelon",
    13: "Tankestreg",
    14: "Formatering",
    17: "Besjæling",
    18: "Slutning",
    19: "Oppustet betydning",
    20: "Overfladisk analyse",
    21: "Omskrevet 'er'",
    22: "Chatbot-rest",
    23: "Procesforsikring",
    24: "Kundeservice",
    26: "Formel",
}


def udskriv(fund: list[Fund], stats: dict, farve: bool) -> str:
    gul = "\033[33m" if farve else ""
    grå = "\033[90m" if farve else ""
    fed = "\033[1m" if farve else ""
    nul = "\033[0m" if farve else ""
    ud = []
    for f in fund:
        sted = f"linje {f.linje}" if f.tekst else "hele teksten"
        navn = REGELNAVNE.get(f.regel, "")
        nr = f"regel {f.regel}" if f.regel else "videnskab"
        ud.append(f"{gul}{sted:>12}{nul}  {fed}{navn}{nul} {grå}({nr}){nul}: {f.besked}")
        if f.tekst and f.tekst.strip():
            ud.append(f"{'':>14}{grå}{f.tekst.strip()}{nul}")
    ud.append("")
    ud.append(f"{fed}{stats['fund']} fund i {stats['ord']} ord "
              f"({stats['fund_per_100_ord']} per 100 ord).{nul}")
    if stats.get("staerke_fund"):
        ud.append(f"{gul}{stats['staerke_fund']} stærke tegn (regel 22): rester af en chatbot-samtale. "
                  f"Dem skriver mennesker næsten aldrig.{nul}")
    if "saetningslaengde_snit" in stats:
        ud.append(f"Sætninger: {stats['saetninger']}, snitlængde {stats['saetningslaengde_snit']} ord, "
                  f"variation {stats['saetningslaengde_variation']} (under 0,35 er monotont).")
    return "\n".join(ud)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Find tegn på AI-skrevet tekst.")
    p.add_argument("fil", help="tekstfil (.txt, .md, .docx) eller - for stdin")
    p.add_argument("-v", "--videnskabelig", action="store_true",
                   help="videnskabelig tekst: slår regel 9, 11, 12, 15, 16 fra og tjekker forkortelser")
    p.add_argument("--json", action="store_true", help="output som JSON")
    a = p.parse_args(argv)

    tekst = laes_fil(a.fil)
    md_docx = a.fil.lower().endswith(".docx") and bool(re.search(r"\*\*\S|^#{1,6} ", tekst, re.MULTILINE))
    fund, stats = tjek(tekst, a.videnskabelig, md_docx)
    if a.json:
        print(json.dumps({"stats": stats, "fund": [asdict(f) for f in fund]}, ensure_ascii=False, indent=2))
    else:
        print(udskriv(fund, stats, sys.stdout.isatty()))
    return 1 if fund else 0


if __name__ == "__main__":
    sys.exit(main())
