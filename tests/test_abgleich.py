"""Abgleichskript an erfundenen Flächen — Werte von Hand nachgerechnet."""

import csv
import subprocess
import sys
from pathlib import Path

import geopandas as gpd
from shapely.geometry import box

SKRIPT = Path(__file__).resolve().parents[1] / "abgleich" / "abgleich.py"


def _lesen(pfad: Path) -> list[dict]:
    with open(pfad, newline="") as f:
        return list(csv.DictReader(f))


def test_abgleich(tmp_path: Path) -> None:
    (tmp_path / "daten").mkdir()
    gpd.GeoDataFrame(
        {"plan_id": ["BP-XX-1", "BP-XX-2", "BP-XX-3"], "ags": ["1", "1", "2"]},
        geometry=[box(600000, 5700000, 600100, 5700100), box(601000, 5700000, 601100, 5700100),
                  box(602000, 5700000, 602100, 5700100)],
        crs="EPSG:25832",
    ).to_file(tmp_path / "daten" / "xx.gpkg", layer="BP_Plan")
    # wie in der Ausgabe: weitere Layer vor und nach BP_Plan
    for layer in ("BP_BaugebietsTeilFlaeche", "A_zuerst"):
        gpd.GeoDataFrame({"plan_id": []}, geometry=[], crs="EPSG:25832").to_file(
            tmp_path / "daten" / "xx.gpkg", layer=layer
        )
    # Partner in WGS84: der Umweg darf die IoU nicht verfälschen
    gpd.GeoDataFrame(
        {"inhalt": ["xplanung", "scan", "pdf"]},
        geometry=[box(600002, 5700000, 600100, 5700100),   # 9.800 / 10.000
                  box(601050, 5700000, 601150, 5700100),   # 5.000 / 15.000
                  box(605000, 5705000, 605100, 5705100)],  # kein Gegenstück
        crs="EPSG:25832",
    ).to_crs("EPSG:4326").to_file(tmp_path / "eigene.geojson")
    gpd.GeoDataFrame(
        {"AGS": ["09162000"]}, geometry=[box(604000, 5704000, 606000, 5706000)], crs="EPSG:25832"
    ).to_file(tmp_path / "gem.gpkg")

    subprocess.run(
        [sys.executable, str(SKRIPT), str(tmp_path / "eigene.geojson"), "--bestand", str(tmp_path / "daten"),
         "--stufe", "inhalt", "--gemeinden", str(tmp_path / "gem.gpkg"), "--aus", str(tmp_path / "erg")],
        check=True,
    )

    treffer = {r["plan_id"]: r for r in _lesen(tmp_path / "erg" / "treffer.csv")}
    assert (treffer["BP-XX-1"]["klasse"], float(treffer["BP-XX-1"]["iou"])) == ("gleich", 0.98)
    assert treffer["BP-XX-1"]["eigene_stufe"] == "xplanung"
    assert (treffer["BP-XX-2"]["klasse"], float(treffer["BP-XX-2"]["iou"])) == ("teilweise", 0.3333)
    assert treffer["BP-XX-3"]["klasse"] == "keiner"

    ohne = _lesen(tmp_path / "erg" / "ohne_treffer.csv")
    assert ohne == [{"gebiet": "09162000", "plaene": "1", "flaeche_m2": "10000"}]
