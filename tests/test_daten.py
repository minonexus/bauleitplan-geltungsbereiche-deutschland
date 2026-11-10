"""Die Dateien im Repo, so wie die Ausgabe sie schreibt: vollständig, untereinander stimmig, öffentlich.

Geprüft wird nur, was ohne die GeoPackages geht. Die liegen bis zum Merge nicht öffentlich; dass die
veröffentlichten Dateien zu `manifest.json` passen, prüft die Ausgabe selbst (sha256, Größe).
Nur Standardbibliothek, damit dieser Teil auch ohne geopandas läuft.
"""

import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LAENDER = {"BB", "BE", "BW", "BY", "HB", "HE", "HH", "MV", "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH"}
#: die ersten beiden Stellen des AGS
AGS_LAND = {
    "01": "SH", "02": "HH", "03": "NI", "04": "HB", "05": "NW", "06": "HE", "07": "RP", "08": "BW",
    "09": "BY", "10": "SL", "11": "BE", "12": "BB", "13": "MV", "14": "SN", "15": "ST", "16": "TH",
}
PLAN_ID = re.compile(r"BP-[A-Z]{2}-\d+")


def _json(name: str):
    return json.loads((REPO / name).read_text(encoding="utf-8"))


def _csv(name: str) -> list[dict]:
    with open(REPO / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def manifest() -> dict:
    return _json("manifest.json")


@pytest.fixture(scope="module")
def quellen() -> list[dict]:
    return _json("quellen.json")


def test_manifest_ist_die_oeffentliche_fassung(manifest):
    """Eine Partnerlieferung trägt Sachdaten und gehört nie hierher."""
    assert manifest["schema"]["maskierung"] == "oeffentlich"
    assert manifest["lizenz"] == "CC-BY-4.0"
    assert manifest["crs"] == "EPSG:25832"
    assert manifest["namensnennung"].strip()
    assert manifest["schema"]["layer"][0] == "BP_Plan"


def test_manifest_je_land(manifest):
    laender = manifest["laender"]
    assert laender and set(laender) <= LAENDER
    aktualisiert = date.fromisoformat(manifest["aktualisiert"])
    for land, e in laender.items():
        assert e["datei"] == f"{land.lower()}.gpkg.zip", land
        assert re.fullmatch(r"[0-9a-f]{64}", e["sha256"]), land
        assert e["bytes"] > 0, land
        assert isinstance(e["stand"], int) and e["stand"] >= 1, land
        assert date.fromisoformat(e["datum"]) <= aktualisiert, land
        for feld in ("flaechen", "gelesen", "neu", "geaendert", "entfallen", "eingeschraenkt", "nur_verweis"):
            assert isinstance(e[feld], int) and e[feld] >= 0, (land, feld)
        # gelesen: auch Pläne ohne Gemeinde, die nicht ausgegeben werden
        assert e["flaechen"] <= e["gelesen"], land
        assert sum(e["stufe"].values()) == e["flaechen"], land


def test_quellen(quellen, manifest):
    schluessel = [q["schluessel"] for q in quellen]
    assert len(schluessel) == len(set(schluessel)), "Schlüssel doppelt"
    for q in quellen:
        assert q["land"] in LAENDER, q["schluessel"]
        assert q["plaene"] > 0, q["schluessel"]
        assert q["lizenz"], q["schluessel"]
        assert q["bereitsteller"], q["schluessel"]
        assert isinstance(q["bearbeitung_erlaubt"], bool), q["schluessel"]
    # Jede ausgegebene Fläche gehört zu genau einer Quelle
    je_land = Counter()
    for q in quellen:
        je_land[q["land"]] += q["plaene"]
    assert dict(je_land) == {land: e["flaechen"] for land, e in manifest["laender"].items() if e["flaechen"]}


def test_jede_quelle_mit_vermerk(quellen):
    """Die Lizenzen verlangen den Quellenvermerk: keine Quelle ohne Zeile in QUELLEN.md."""
    md = (REPO / "QUELLEN.md").read_text(encoding="utf-8")
    fehlt = [q["schluessel"] for q in quellen if f"`{q['schluessel']}`" not in md]
    assert not fehlt, f"nicht in QUELLEN.md: {fehlt[:10]}"


def test_nachfolger(manifest):
    zeilen = _csv("nachfolger.csv")
    assert zeilen and list(zeilen[0]) == ["alt_id", "neu_id", "grund", "stand"]
    hoechster = max(e["stand"] for e in manifest["laender"].values())
    # eine alte ID darf mehrere Nachfolger haben (geteilt), dieselbe Zeile steht nur einmal da
    assert len({tuple(z.values()) for z in zeilen}) == len(zeilen), "Zeile doppelt"
    for z in zeilen:
        assert PLAN_ID.fullmatch(z["alt_id"]), z
        assert 1 <= int(z["stand"]) <= hoechster, z
        if z["neu_id"]:
            assert PLAN_ID.fullmatch(z["neu_id"]), z
            assert z["grund"] and z["grund"] != "entfallen", z
        else:
            assert z["grund"] == "entfallen", z


def test_abdeckung(manifest):
    zeilen = _csv("abdeckung/gemeinden.csv")
    assert list(zeilen[0]) == [
        "ags", "gemeinde", "land", "plaene", "planflaeche_km2", "xplanung_x2", "xplanung_x1", "mit_dokument",
        "mit_festsetzungen", "gebaeude", "gebaeude_im_plan", "einwohner", "einwohner_im_plan",
    ]
    ags = [z["ags"] for z in zeilen]
    assert len(ags) == len(set(ags)), "AGS doppelt"
    for z in zeilen:
        assert re.fullmatch(r"\d{8}", z["ags"]), z
        assert z["land"] == AGS_LAND[z["ags"][:2]], z
        assert z["gemeinde"], z
        assert float(z["planflaeche_km2"]) >= 0, z
        for teil in ("xplanung_x2", "xplanung_x1", "mit_dokument", "mit_festsetzungen"):
            assert 0 <= int(z[teil]) <= int(z["plaene"]), (z["ags"], teil)
        for teil, ganz in (("gebaeude_im_plan", "gebaeude"), ("einwohner_im_plan", "einwohner")):
            if z[ganz]:
                assert 0 <= int(z[teil] or 0) <= int(z[ganz]), (z["ags"], teil)
    assert {z["land"] for z in zeilen} <= set(manifest["laender"])
