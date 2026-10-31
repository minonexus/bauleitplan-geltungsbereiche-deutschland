"""Eigene Geltungsbereiche gegen diesen Bestand abgleichen — lokal.

Rechnet je Plan dieses Bestands die beste Überlappung (IoU) mit Ihren Plänen
und zählt Ihre Pläne ohne Treffer je Gemeinde bzw. je 10-km-Zelle. Die
Ausgabe enthält keine Ihrer Geometrien.

    python abgleich.py eigene.gpkg --bestand daten/ --aus ergebnis/
    python abgleich.py eigene.gpkg --bestand daten/ --stufe inhalt \
        --gemeinden VG250_GEM.shp --aus ergebnis/

Braucht geopandas >= 0.14 und shapely >= 2.0.

SPDX-License-Identifier: MIT — Copyright (c) 2026 Minonexus GmbH, siehe LICENSE.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd

CRS = "EPSG:25832"
#: Layer mit den Geltungsbereichen; die Datei hat weitere (Teilflächen, Stil)
LAYER = "BP_Plan"

#: Gemessen am Bestand (30.10.2026), Begründung in abgleich/README.md: Bei generalisierter
#: Erfassung (Sachsen-Anhalt) liegen nur 82 % der Paare desselben Plans über 0,9, aber 95 % über
#: 0,7; zwischen 0,8 und 0,9 überlappen sich dagegen kaum verschiedene Pläne (2 %).
IOU_GLEICH = 0.8
IOU_TEILWEISE = 0.3


def lesen_bestand(pfad: Path) -> gpd.GeoDataFrame:
    dateien = sorted(pfad.glob("*.gpkg")) if pfad.is_dir() else [pfad]
    if not dateien:
        raise SystemExit(f"keine GeoPackages unter {pfad}")
    teile = [gpd.read_file(d, layer=LAYER)[["plan_id", "ags", "geometry"]] for d in dateien]
    return gpd.GeoDataFrame(pd.concat(teile, ignore_index=True), crs=teile[0].crs).to_crs(CRS)


def lesen_eigene(pfad: Path, stufe: str | None) -> gpd.GeoDataFrame:
    df = gpd.read_file(pfad)
    if df.crs is None:
        raise SystemExit(f"{pfad}: kein Koordinatensystem angegeben")
    df = df.to_crs(CRS)
    df = df[df.geometry.notna() & ~df.geometry.is_empty].copy()
    df["geometry"] = df.geometry.make_valid()
    df["eigene_nr"] = range(len(df))
    df["eigene_stufe"] = df[stufe].astype(str) if stufe else ""
    return df[["eigene_nr", "eigene_stufe", "geometry"]]


def paare(bestand: gpd.GeoDataFrame, eigene: gpd.GeoDataFrame) -> pd.DataFrame:
    """Alle sich schneidenden Paare mit IoU."""
    links = bestand[["plan_id", "geometry"]].reset_index(drop=True)
    j = gpd.sjoin(links, eigene, predicate="intersects", how="inner")
    a = links.geometry.loc[j.index].reset_index(drop=True)
    b = eigene.geometry.loc[j["index_right"]].reset_index(drop=True)
    schnitt = a.intersection(b, align=False).area.values
    a, b = a.area.values, b.area.values
    vereinigt = a + b - schnitt
    return pd.DataFrame({
        "plan_id": j["plan_id"].values,
        "eigene_nr": j["eigene_nr"].values,
        "eigene_stufe": j["eigene_stufe"].values,
        "iou": (schnitt / vereinigt).round(4),
    })


def klasse(iou: float) -> str:
    if iou >= IOU_GLEICH:
        return "gleich"
    if iou >= IOU_TEILWEISE:
        return "teilweise"
    return "keiner"


def treffer(bestand: gpd.GeoDataFrame, p: pd.DataFrame) -> pd.DataFrame:
    beste = p.sort_values("iou", ascending=False).drop_duplicates("plan_id")
    t = bestand[["plan_id"]].merge(beste, on="plan_id", how="left")
    t["iou"] = t["iou"].fillna(0.0)
    t["klasse"] = t["iou"].map(klasse)
    t.loc[t["klasse"] == "keiner", ["eigene_stufe", "eigene_nr"]] = ["", None]
    t["eigene_nr"] = t["eigene_nr"].astype("Int64")
    return t[["plan_id", "klasse", "iou", "eigene_stufe", "eigene_nr"]]


def ohne_treffer(eigene: gpd.GeoDataFrame, p: pd.DataFrame, gemeinden: Path | None) -> pd.DataFrame:
    """Ihre Pläne, die keinen unserer Pläne mindestens teilweise treffen — nur gezählt."""
    getroffen = set(p.loc[p["iou"] >= IOU_TEILWEISE, "eigene_nr"])
    rest = eigene[~eigene["eigene_nr"].isin(getroffen)].copy()
    rest["flaeche_m2"] = rest.geometry.area
    punkte = rest.copy()
    punkte["geometry"] = rest.geometry.representative_point()

    if gemeinden is not None:
        gem = gpd.read_file(gemeinden).to_crs(CRS)
        spalte = "AGS" if "AGS" in gem.columns else "ags"
        punkte = gpd.sjoin(punkte, gem[[spalte, "geometry"]], predicate="within", how="left")
        punkte["gebiet"] = punkte[spalte].fillna("ausserhalb")
    else:
        # 10-km-Zellen des EEA-Referenzgitters (EPSG:3035), z. B. 10kmE432N312
        laea = punkte.to_crs("EPSG:3035").geometry
        punkte["gebiet"] = [f"10kmE{int(x // 10000)}N{int(y // 10000)}" for x, y in zip(laea.x, laea.y)]

    return (
        punkte.groupby("gebiet")
        .agg(plaene=("eigene_nr", "size"), flaeche_m2=("flaeche_m2", "sum"))
        .reset_index()
        .assign(flaeche_m2=lambda d: d["flaeche_m2"].round(0).astype(int))
        .sort_values("plaene", ascending=False)
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("eigene", type=Path, help="Ihre Geltungsbereiche (GeoPackage, GeoJSON, Shapefile …)")
    ap.add_argument("--bestand", type=Path, required=True, help="Ordner mit unseren GeoPackages oder eine Datei")
    ap.add_argument("--stufe", help="Spalte Ihrer Datei mit der eigenen Inhaltsstufe (wird durchgereicht)")
    ap.add_argument("--gemeinden", type=Path, help="VG250-Gemeinden; ohne: Zählung je 10-km-Zelle")
    ap.add_argument("--aus", type=Path, default=Path("ergebnis"))
    args = ap.parse_args()

    bestand = lesen_bestand(args.bestand)
    eigene = lesen_eigene(args.eigene, args.stufe)
    p = paare(bestand, eigene)

    args.aus.mkdir(parents=True, exist_ok=True)
    t = treffer(bestand, p)
    t.to_csv(args.aus / "treffer.csv", index=False)
    o = ohne_treffer(eigene, p, args.gemeinden)
    o.to_csv(args.aus / "ohne_treffer.csv", index=False)

    zahl = t["klasse"].value_counts()
    print(f"unser Bestand: {len(t)} Pläne — gleich {zahl.get('gleich', 0)}, "
          f"teilweise {zahl.get('teilweise', 0)}, keiner {zahl.get('keiner', 0)}")
    print(f"Ihre Pläne ohne Treffer: {int(o['plaene'].sum())} in {len(o)} Gebieten")
    print(f"geschrieben: {args.aus / 'treffer.csv'}, {args.aus / 'ohne_treffer.csv'}")


if __name__ == "__main__":
    main()
