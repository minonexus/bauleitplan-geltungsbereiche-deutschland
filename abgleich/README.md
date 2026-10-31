# Abgleich mit eigenen Geltungsbereichen

`abgleich.py` vergleicht Ihre Geltungsbereiche mit diesem Bestand. Es läuft
**auf Ihrem Rechner**, lädt nichts hoch und schreibt keine Ihrer Geometrien in
die Ausgabe.

```bash
pip install "geopandas>=0.14" "shapely>=2.0"
python abgleich.py eigene.gpkg --bestand pfad/zu/unseren/gpkg/ --aus ergebnis/
```

| Option | |
|---|---|
| `--stufe SPALTE` | Spalte Ihrer Datei mit einer eigenen Inhaltsangabe (etwa „XPlanung", „Scan mit GRZ"). Sie wird je Treffer durchgereicht |
| `--gemeinden VG250_GEM.shp` | zählt Ihre Pläne ohne Treffer je Gemeinde ([VG250 des BKG](https://gdz.bkg.bund.de)). Ohne die Option je 10-km-Zelle des EEA-Referenzgitters |

## Was gerechnet wird

Für jedes Paar aus unserem und Ihrem Plan, das sich schneidet, die **IoU**:
Schnittfläche geteilt durch Vereinigungsfläche. 1 heißt deckungsgleich, 0
heißt keine Überlappung. Der Vergleich über Flächen ist nötig, weil zwei
Häuser denselben Plan fast nie mit denselben Koordinaten führen — andere
Quelle, andere Projektion, andere Genauigkeit. `geom_hash` hilft dabei nicht.

| Klasse | IoU | Lesart |
|---|---|---|
| `gleich` | ≥ 0,8 | derselbe Geltungsbereich, anders erfasst |
| `teilweise` | ≥ 0,3 | Überlappung: generalisiert erfasst, Änderungsplan oder andere Abgrenzung |
| `keiner` | < 0,3 | bei Ihnen nicht vorhanden |

**Woher die Schwellen kommen.** Gemessen an unserem Bestand (Oktober 2026).
Wo wir denselben Plan aus zwei Quellen führen (21.940 Paare), decken sich
91 % mit IoU ≥ 0,95. Das zählt allerdings nur Paare, die wir überhaupt
zusammengeführt haben, und das tun wir meist erst ab 0,9. Sachsen-Anhalt
zeigt, was darunter liegt: Dort ist eine Quelle generalisiert, wir führen ab
0,5 zusammen, und von den Paaren liegen nur 82 % über 0,9, aber 95 % über 0,7.
Umgekehrt überlappt kaum ein Plan einen *anderen* Plan zu 0,8 bis 0,9 (2 % der
Pläne, Stichprobe von 38.184). Ab 0,8 ist `gleich` also verlässlich; darunter
ist `teilweise` mehrdeutig.

**`gleich` heißt gleicher Geltungsbereich, nicht unbedingt derselbe Plan.**
Änderungspläne gelten oft für genau die Fläche des Ursprungsplans: Bei 11 %
unserer Pläne gibt es einen anderen, der mit IoU ≥ 0,99 deckungsgleich ist,
fast immer eine Änderung. Einer Ihrer Pläne kann deshalb bei mehreren unserer
`plan_id` als `gleich` erscheinen. Welcher es ist, klärt erst der Planinhalt.

## Ausgabe

**`treffer.csv`** — je unserer `plan_id`:

| Spalte | |
|---|---|
| `plan_id` | unser Plan |
| `klasse` | `gleich`, `teilweise`, `keiner` |
| `iou` | beste Überlappung mit einem Ihrer Pläne |
| `eigene_stufe` | Ihre Angabe aus `--stufe` für diesen Treffer |
| `eigene_nr` | Zeile Ihrer Datei (ab 0) für diesen Treffer — für Sie, zum Zurückfinden; vor dem Weitergeben streichen, wenn Sie mögen |

**`ohne_treffer.csv`** — Ihre Pläne, die keinen unserer mindestens teilweise
treffen, nur gezählt:

| Spalte | |
|---|---|
| `gebiet` | AGS der Gemeinde bzw. 10-km-Zelle |
| `plaene` | Anzahl |
| `flaeche_m2` | Fläche zusammen |

Zusammen zeigen beide Tabellen, wo Sie zu unseren Plänen mehr Inhalt führen
und wo Sie Pläne haben, die uns fehlen. Wenn Sie darüber sprechen möchten,
genügen diese beiden Dateien: [Kontakt im README](../README.md#abgleich).

## Lizenz

Das Skript steht unter der [MIT-Lizenz](LICENSE).
