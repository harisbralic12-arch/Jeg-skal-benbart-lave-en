"""Kør med: python3 -m unittest"""
import unittest
from pathlib import Path
from aitegn.tjek import tjek

EKS = Path(__file__).parent / "eksempler"


def regler_fundet(tekst, **kw):
    return {f.regel for f in tjek(tekst, **kw)[0]}


class TestTjek(unittest.TestCase):
    def test_eksempelmail_fanger_de_vigtigste(self):
        r = regler_fundet((EKS / "ai_mail.txt").read_text(encoding="utf-8"))
        for regel in (2, 4, 6, 7, 8, 9, 10, 13, 17, 18):
            self.assertIn(regel, r)

    def test_ren_mail_er_ren(self):
        fund, _ = tjek((EKS / "ai_mail_ren.txt").read_text(encoding="utf-8"))
        self.assertEqual(fund, [])

    def test_videnskab_slaar_forbehold_fra(self):
        tekst = "The finding could potentially reflect selection bias."
        self.assertIn(9, regler_fundet(tekst))
        self.assertNotIn(9, regler_fundet(tekst, videnskabelig=True))

    def test_forkortelser(self):
        tekst = "We used optical coherence tomography (OCT). OCT was done twice. AMD was excluded."
        besked = [f.besked for f in tjek(tekst, videnskabelig=True)[0] if f.regel == 0]
        self.assertEqual(len(besked), 1)
        self.assertIn("AMD", besked[0])

    def test_fagterm_central(self):
        self.assertNotIn(6, regler_fundet("Central subfield thickness was 280 µm."))
        self.assertIn(6, regler_fundet("Projektet er centralt for afdelingen."))

    def test_ingen_dobbelt_fund(self):
        fund, _ = tjek("Data tells a story.")
        self.assertEqual(len([f for f in fund if f.regel == 17]), 1)


if __name__ == "__main__":
    unittest.main()
