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

    def test_ren_mail_har_kun_huller(self):
        fund, _ = tjek((EKS / "ai_mail_ren.txt").read_text(encoding="utf-8"))
        self.assertEqual({f.regel for f in fund}, {1})

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


    # Tegn fra Wikipedia:Signs of AI writing
    def test_chatbot_rester_er_staerke(self):
        tekst = "Here is a revised version of your text. I hope this helps! See utm_source=chatgpt.com"
        fund, stats = tjek(tekst)
        self.assertEqual(stats["staerke_fund"], 3)

    def test_overfladisk_analyse(self):
        self.assertIn(20, regler_fundet("The clinic opened in 1989, highlighting its role in the region."))
        self.assertIn(20, regler_fundet("Klinikken åbnede i 1989, hvilket understreger dens betydning."))

    def test_oppustet_betydning(self):
        self.assertIn(19, regler_fundet("It stands as a testament to the team."))
        self.assertIn(19, regler_fundet("Åbningen markerede et vendepunkt for afdelingen."))

    def test_kopula_ikke_i_videnskab(self):
        tekst = "The fellow eye served as a control. The clinic serves as a hub."
        self.assertIn(21, regler_fundet(tekst))
        self.assertNotIn(21, regler_fundet(tekst, videnskabelig=True))

    def test_procesforsikring_i_reviewersvar(self):
        tekst = "We have carefully revised the discussion to improve clarity and flow."
        self.assertIn(23, regler_fundet(tekst, videnskabelig=True))

    def test_kundeservice(self):
        self.assertIn(24, regler_fundet("Jeg håber denne mail finder dig vel."))

    def test_otte_til_tyve_ord(self):
        s = "Patienten blev undersøgt i klinikken den første dag af lægen. "
        _, stats = tjek(s * 10)
        self.assertEqual(stats["andel_8_til_20_ord"], 1.0)


if __name__ == "__main__":
    unittest.main()
