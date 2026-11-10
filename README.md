# Geltungsbereiche der Bauleitpläne in Deutschland

**Nur Geometrien.** Dieses Repo enthält die räumlichen Geltungsbereiche
geltender Bebauungspläne (§ 9 Abs. 7 BauGB): wo ein Bebauungsplan gilt.
Es enthält **keine Planinhalte, keine amtlichen Datensätze und keine
Dokumente** — keinen Namen, keine Nummer, keine Festsetzungen, keine Links.

Herausgeber: Minonexus GmbH · Lizenz unseres Anteils: CC BY 4.0, Geometrien
nach der Lizenz ihrer Quelle (siehe [Lizenz](#lizenz)) · Stand: siehe
[`manifest.json`](manifest.json)

Mehr bei Minonexus:
[Bebauungspläne — Datenquellen, Abdeckung und Ausblick](https://minonexus.com/minonexus/bebauungsplaene) ·
[Welche Bebauungspläne kennt Minonexus? (tagesaktuell)](https://minonexus.com/performance/bebauungsplaene)

## Hintergrund

**Bauleitpläne sind in Deutschland verstreut.** Jede Gemeinde stellt ihre Pläne
selbst auf; veröffentlicht werden sie von Gemeinde, Kreis, Land oder einem
Dienstleister, in vielen Formaten und unter vielen Lizenzen. Woher unsere Pläne
stammen, was ein Treffer bedeutet und welche Rolle XPlanung spielt, beschreibt
der Artikel [Bebauungspläne bei Minonexus](https://minonexus.com/minonexus/bebauungsplaene).

**Was dieses Repo bietet.** Wir veröffentlichen als Open Content die Gebiete, in
denen nach unserer Kenntnis ein Bauleitplan gilt. Das hilft schon bei einer
Grundfrage: Richtet sich ein Vorhaben auf einem Grundstück nach den
Festsetzungen eines Bebauungsplans (§ 30 BauGB), oder muss es sich in die
Umgebung einfügen (§ 34 BauGB, im Außenbereich § 35 BauGB)?

**Kein Treffer ist keine gesicherte Aussage.** Liegt ein Grundstück in keiner
unserer Flächen, kann trotzdem ein Plan gelten, den wir noch nicht kennen.
Melden Sie solche Pläne gern als [Issue](#mitmachen).

**Warum keine Planinhalte.** Festsetzungen, Dokumente und die übrigen Angaben
zu den Plänen veröffentlichen wir hier aus zwei Gründen nicht:

- **Die Lizenzlage ist uneinheitlich und oft unklar.** Manche Quellen nennen
  keine Lizenz, andere erlauben keine Weitergabe, einzelne Gemeinden verlangen
  eine ausdrückliche Freigabe.
- **Ganz offen: In den Inhalten steckt unsere Arbeit.** Quellen finden, Pläne
  zusammenführen und Festsetzungen auswerten kostet viel Aufwand, und daraus ist
  ein Wettbewerbsvorteil entstanden.

**Austausch mit Partnern.** Quellen und Planinhalte tauschen wir gern mit
Partnern aus, auf Gegenseitigkeit und wenn beide Seiten davon profitieren.
Partner bekommen dasselbe Schema mit befüllten Spalten, soweit die Lizenz der
Quelle es erlaubt. Was wir haben, zeigen die Spalten [`stufe`, `dokument` und
`festsetzungen`](#bp_plan-befüllte-spalten), und `partnerlieferung` sagt je Plan,
ob wir Daten weitergeben dürfen oder nur auf die Quelle verweisen. Die
[Abdeckung](#abdeckung) und der [Abgleich](#abgleich) mit Ihrem eigenen Bestand
zeigen, wo wir noch Daten von Ihnen brauchen könnten. Kontakt:
**markus@minonexus.com**.

## Abdeckung

Wie viel unser Bestand abdeckt — je Land Pläne, Gemeinden mit Plan, Gebäude
und Einwohner im Plan, XPlanung und Festsetzungen —, steht tagesaktuell unter
**[minonexus.com/performance/bebauungsplaene](https://minonexus.com/performance/bebauungsplaene)**.
Die Seite wird jede Nacht neu gerechnet; dieses Repo wird wöchentlich
aktualisiert (`aktualisiert` in [`manifest.json`](manifest.json)). Eine
eigene Tabelle hier liefe ihr hinterher.

Zum Stand der Dateien je Gemeinde:
[`abdeckung/gemeinden.csv`](abdeckung/gemeinden.csv) — Pläne, Planfläche,
XPlanung X2/X1, mit Dokument und mit Festsetzungen, dazu Gebäude und Einwohner
der Gemeinde und davon im Plan (Gebäude: amtliche 3D-Gebäudemodelle,
Einwohner: Zensus 2022). Ein Plan zählt zur Gemeinde, in der er überwiegend
liegt; überlappende Pläne zählen ihre Fläche mehrfach.

Die Zahlen beschreiben **die Abdeckung unseres Bestands**, nicht den Stand der
Gemeinden. Fehlt bei uns ein Plan, heißt das nicht, dass die Gemeinde ihn
nicht veröffentlicht — vielleicht nur über einen Weg, den wir noch nicht
kennen. Hinweise darauf sind willkommen (siehe [Mitmachen](#mitmachen)).

## Download

Die Daten liegen unter `https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/`, je
Land ein GeoPackage (`<land>.gpkg.zip`, EPSG:25832). Die Geltungsbereiche stehen im Layer
`BP_Plan`, eine Fläche je Plan; zwei weitere Layer sind leer (siehe [Daten](#daten)). Alle 16 zusammen sind 263 MB. Eine Anmeldung braucht es nicht. Prüfsummen und Stand
je Land stehen in [`manifest.json`](manifest.json).

### Ein Land laden

1. Das Land in der Liste unten suchen und die Datei anklicken, z. B. `hh.gpkg.zip` für Hamburg.
2. Die ZIP-Datei entpacken.
3. Das GeoPackage in QGIS ziehen oder über *Layer → Layer hinzufügen → Vektorlayer* öffnen.
   QGIS lädt alle drei Layer. Nur `BP_Plan` hat Inhalt. `BP_BaugebietsTeilFlaeche` und
   `BP_UeberbaubareGrundstuecksFlaeche` sind in dieser Ausgabe **absichtlich leer**: Sie
   sind für Planinhalte angelegt, die wir hier nicht veröffentlichen (siehe [Daten](#daten)).
   Damit sie nicht nach Daten aussehen, sind sie grau gestrichelt gestylt. Sie lassen sich
   entfernen, oder man wählt beim Öffnen nur `BP_Plan`.

Ein Stil ist in der Datei: Umringe nach `stufe` eingefärbt, ab 1:10.000 mit `plan_id`
beschriftet. Die Farbe sagt, **in welcher Form die Verwaltung den Plan bereitstellt** — nichts
über seine Qualität oder Gültigkeit. Ausführlich im
[Artikel](https://minonexus.com/minonexus/bebauungsplaene#in-welcher-form-ein-plan-vorliegt).

| Farbe | Stufe | Kurz |
|---|---|---|
| dunkelgrün | `X2` – XPlanung vollvektoriell | Planinhalte als Objekte: Baugebiete, Baufenster, Maße |
| hellgrün | `X1` – XPlanung mit Rasterplan | Geltungsbereich und Plandaten strukturiert, Planinhalte nicht als Objekte |
| blau | `N` – XPlanung-nah | kein XPlanung-Dienst, aber Attribute mit XPlanung-Codes |
| orange | `V` – sonstiger Vektor | Umring aus einem anderen Dienst der Verwaltung, etwa einem WFS oder Geoportal |

<details>
<summary><b>Alle 16 Länder</b> (Größe zum Stand vom 2026-11-10)</summary>

| Land | Datei | Flächen | Größe |
|---|---|---:|---:|
| Baden-Württemberg | [`bw.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/bw.gpkg.zip) | 73.062 | 55 MB |
| Bayern | [`by.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/by.gpkg.zip) | 100.139 | 52 MB |
| Berlin | [`be.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/be.gpkg.zip) | 2.852 | 2 MB |
| Brandenburg | [`bb.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/bb.gpkg.zip) | 7.891 | 5 MB |
| Bremen | [`hb.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/hb.gpkg.zip) | 1.791 | 4 MB |
| Hamburg | [`hh.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/hh.gpkg.zip) | 3.048 | 4 MB |
| Hessen | [`he.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/he.gpkg.zip) | 24.901 | 17 MB |
| Mecklenburg-Vorpommern | [`mv.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/mv.gpkg.zip) | 9.299 | 6 MB |
| Niedersachsen | [`ni.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/ni.gpkg.zip) | 44.377 | 23 MB |
| Nordrhein-Westfalen | [`nw.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/nw.gpkg.zip) | 74.903 | 56 MB |
| Rheinland-Pfalz | [`rp.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/rp.gpkg.zip) | 17.078 | 11 MB |
| Saarland | [`sl.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/sl.gpkg.zip) | 3.003 | 2 MB |
| Sachsen | [`sn.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/sn.gpkg.zip) | 9.187 | 7 MB |
| Sachsen-Anhalt | [`st.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/st.gpkg.zip) | 8.250 | 6 MB |
| Schleswig-Holstein | [`sh.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/sh.gpkg.zip) | 12.717 | 7 MB |
| Thüringen | [`th.gpkg.zip`](https://data.minonexus.com/bauleitplan-geltungsbereiche-deutschland/th.gpkg.zip) | 6.355 | 4 MB |

</details>

## Daten

Das Schema folgt **XPlanung 6.1**, flach wie das XPlanSyn-Schema der
XPlanung-Dienste: je Klasse ein Layer, Attribute mit ihren XPlanung-Namen,
Codes mit Text daneben. Dasselbe Schema nutzen wir im Austausch mit Partnern.
Hier sind nur die Spalten befüllt, die den Geltungsbereich beschreiben. Die
übrigen sind angelegt und leer, damit sichtbar ist, was es zu einem Plan geben
kann. Die Datei ist **kein XPlanGML** und erfüllt keinen Standard der
XLeitstelle. Sie ist eine dokumentierte Abbildung darauf
([XPlanung 6.1](https://xleitstelle.de/xplanung/releases-xplanung?fid=2275),
[Objektartenkatalog](https://xleitstelle.de/releases/objektartenkatalog_6_1)).

| Layer | Inhalt |
|---|---|
| `BP_Plan` | eine Fläche je Plan: der Geltungsbereich (`raeumlicherGeltungsbereich`) |
| `BP_BaugebietsTeilFlaeche` | angelegt, **ohne Zeilen**. Im Austausch mit Partnern: die Baugebiete eines Plans mit Art der Nutzung, GRZ, GFZ, Zahl der Vollgeschosse, Bauweise, Dachform und Höhen |
| `BP_UeberbaubareGrundstuecksFlaeche` | angelegt, ohne Zeilen. Im Austausch: die Baufenster, also die überbaubaren Grundstücksflächen |

**Warum leere Layer?** Sie zeigen, was es zu einem Plan geben kann, und halten
das Schema gleich: Partner bekommen dieselbe Datei mit befüllten Layern, soweit
die Lizenz der Quelle es erlaubt. Wer die öffentliche Fassung kennt, kennt damit
auch das Austauschformat. Leer heißt hier **nicht veröffentlicht**, nicht „nicht
vorhanden“. Ob wir zu einem Plan Festsetzungen führen, steht in `BP_Plan` in der
Spalte `festsetzungen`.

### `BP_Plan`: befüllte Spalten

| Feld | Bedeutung |
|---|---|
| `plan_id` | Kennung des Plans, z. B. `BP-ST-276092`. **Stabil:** wird nie wiederverwendet und verschwindet nie ohne Eintrag in [`nachfolger.csv`](nachfolger.csv). Das Land im Präfix ist Lesehilfe, eindeutig ist die Zahl |
| `maskierung` | `oeffentlich`: Die Spalten des Datensatzes (unten) sind in dieser Ausgabe leer |
| `ags` | Amtlicher Gemeindeschlüssel der Gemeinde, in der der größte Teil des Plans liegt — **von uns bestimmt** (VG250), nicht `XP_Gemeinde.ags` des Plans |
| `land` | Bundesland der Gemeinde, Kürzel wie in `XP_Bundeslaender` — kann vom Land im Präfix der `plan_id` abweichen, wenn ein Dienst über die Landesgrenze reicht |
| `geometrie` | `amtlich`: Umring aus einem Dienst der Verwaltung |
| `stufe` | In welcher Form die Verwaltung den Plan bereitstellt: `X2` XPlanung vollvektoriell · `X1` XPlanung mit Rasterplan · `N` XPlanung-nah · `V` sonstiger Vektor (siehe [Ein Land laden](#ein-land-laden)). Unsere Einteilung, kein XPlanung-Attribut |
| `xpVersion` | XPlanung-Version der Quelle, z. B. `6.0`; leer ohne XPlanung |
| `dokument` | ob wir die Planurkunde oder den Textteil führen: `ja` · `nein` |
| `festsetzungen` | welche Festsetzungen wir maschinenlesbar führen — **nur die Namen, keine Werte**, Abbildung unten |
| `quelle` | Schlüssel in [`quellen.json`](quellen.json) |
| `lizenz` | Lizenz der Geometrie, Kennung wie in `quellen.json` |
| `bearbeitung_erlaubt` | `false` bei CC BY-ND: die Fläche nur unverändert weitergeben |
| `rechtsstand_angenommen` | `true`: Die Quelle nennt keinen Rechtsstand; wir nehmen an, dass der veröffentlichte Plan in Kraft ist. `false`: Die Quelle führt ihn als in Kraft |
| `einschraenkung` | leer, oder was die Quelle an der Nutzung einschränkt: ihr Vermerk (`genehmigung`, `lizenz_unklar`, …) oder ihre Lizenz. Der Geltungsbereich steht dann als amtliches Werk hier (siehe [Lizenz](#lizenz)) |
| `partnerlieferung` | was ein Kooperationspartner zu diesem Plan bekäme: `daten` — die Spalten des Datensatzes, soweit vorhanden · `nur_verweis` — aus Lizenzgründen keine Daten, nur der Link zur Quelle |
| `geom_hash` | Prüfsumme der Geometrie, s. u. |
| `stand` | Stand des Landes, in dem sich die Fläche zuletzt geändert hat |
| `hinweis` | „Nur Geltungsbereich, keine Planinhalte. Maßgeblich ist die ausgefertigte Satzung.“ — bei `einschraenkung` und `nur_verweis` mit einem Satz dazu |

### `BP_Plan`: leere Spalten

`name`, `nummer`, `planArt`, `planArtWert`, `rechtsstand`, `rechtsstandWert`,
`inkrafttretensDatum`, `xpAgs`, `gemeinde`,
`externeReferenz`, `gmlId`, `herkunft`, `quelleUrl`, `lizenz_attribute`. Leer
heißt hier **nicht veröffentlicht**, nicht „nicht vorhanden“. Platzhalter gibt
es keine: Ein leeres Feld behauptet nichts.

Mit Kooperationspartnern tauschen wir dieselbe Datei mit befüllten Spalten
aus — je Plan nach der Lizenz seiner Quelle. Was ein Partner zu einem Plan
bekäme, sagt schon hier `partnerlieferung`.

### Kennzeichen `festsetzungen` und XPlanung

| Kennzeichen | XPlanung 6.1 (`BP_BaugebietsTeilFlaeche` bzw. `BP_UeberbaubareGrundstuecksFlaeche`) |
|---|---|
| `grz` | `GRZ`, `GRZmin`, `GRZmax`, `GR` |
| `gfz` | `GFZ`, `GFZmin`, `GFZmax`, `GF` |
| `z` | `Z`, `Zmin`, `Zmax`, `Zzwingend` |
| `bauweise` | `bauweise` |
| `hoehe` | `hoehenangabe` (Trauf-, First-, Gebäudehöhe) |
| `dachform` | `dachgestaltung` |
| `baugebiet` | `besondereArtDerBaulNutzung` |
| `baufenster` | die Klasse `BP_UeberbaubareGrundstuecksFlaeche` |

**Nur geltende Pläne.** Pläne im Verfahren, aufgehobene und entfallene Pläne
sind nicht enthalten. Entfällt ein Plan, steht er in der Änderungsliste des
nächsten Stands und in `nachfolger.csv`.

**Auch Satzungen.** Ein Teil der Flächen sind keine Bebauungspläne im engeren
Sinn, sondern Innen- und Außenbereichssatzungen (§ 34 Abs. 4, § 35 Abs. 6
BauGB) oder örtliche Bauvorschriften, soweit die Quelle sie im selben Bestand
führt. Für ein Grundstück sind sie ebenso maßgeblich.

**„Geltend" ist nicht immer amtlich belegt.** Nennt die Quelle keinen
Rechtsstand, nehmen wir an, dass ein veröffentlichter Plan in Kraft ist.
Welche Pläne das sind, sagt die Spalte `rechtsstand_angenommen`.

**Ein Umring je Plan.** Liegt ein Plan in mehreren Quellen vor, nehmen wir den
Umring einer Quelle, in dieser Reihenfolge: XPlanung, Original-Vektor eines
Kreis-, Stadt- oder Landesdienstes, XPlanung-nahe Ableitung. Umringe
verschiedener Quellen werden **nicht** vereinigt.

### `geom_hash`

Die ersten 16 Hex-Zeichen von SHA-256 über die Geometrie als WKB, so wie sie
im GeoPackage steht (2D, Little Endian):

```python
import hashlib
geom_hash = hashlib.sha256(geometry.wkb).hexdigest()[:16]
```

Gleicher Hash heißt: dieselbe Geometrie, Byte für Byte. Damit lässt sich
zwischen zwei Ständen sehen, welche Umringe sich geändert haben, ohne sie zu
verschneiden. Für den Vergleich mit **eigenen** Daten taugt er nicht — schon
eine Umprojektion ändert ihn. Dafür gibt es das [Abgleichskript](#abgleich).

### Stände und Nachfolger

Jedes Land hat eigene Stände (1, 2, 3 …); [`manifest.json`](manifest.json)
nennt je Stand neu, geändert und entfallen. Ausgegeben wird wöchentlich. Ein
Land ohne Änderung behält in der Regel seinen Stand und seine Datei; ändern
wir das Format der Dateien, bekommen alle Länder einen neuen Stand, auch wenn
sich keine Fläche bewegt hat.

[`nachfolger.csv`](nachfolger.csv): `alt_id`, `neu_id`, `grund`
(`zusammengelegt` · `geteilt` · `entfallen`), `stand`. Wer eine
alte `plan_id` gespeichert hat, findet hier, was daraus geworden ist.

## Abgleich

Wer selbst Geltungsbereiche führt, kann mit
[`abgleich/abgleich.py`](abgleich/) seinen Bestand gegen unseren rechnen —
**lokal, ohne etwas hochzuladen**. Ergebnis sind zwei Tabellen ohne
Geometrie: welche unserer Pläne bei Ihnen vorkommen, und wie viele Ihrer Pläne
je Gemeinde bei uns fehlen. Anleitung: [`abgleich/README.md`](abgleich/README.md).

Möchten Sie über das Ergebnis mit uns sprechen — etwa über Planinhalte zu den
Plänen, die beide führen —, schreiben Sie an **markus@minonexus.com**.

## Mitmachen

- **Umring falsch?** Ein Issue mit `plan_id` und woraus der Fehler folgt.
- **Plan fehlt?** Ein Issue mit Gemeinde und, wenn bekannt, wo der Plan
  veröffentlicht ist.

Mehr in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Lizenz

- **Unser Anteil** — Zusammenstellung, `plan_id`, Gemeindezuordnung,
  Kennzeichen (`stufe`, `dokument`, `festsetzungen`, `rechtsstand_angenommen`),
  Abdeckung:
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de),
  Namensnennung „Minonexus GmbH, bauleitplan-geltungsbereiche-deutschland".
- **Das Abgleichskript** ([`abgleich/`](abgleich/)) steht unter der
  [MIT-Lizenz](abgleich/LICENSE).
- **Die Geometrien** stehen unter der Lizenz ihrer Quelle (Feld `lizenz`).
  Die Quellenvermerke für den gesamten Bestand stehen gesammelt in
  [`QUELLEN.md`](QUELLEN.md) und maschinenlesbar in
  [`quellen.json`](quellen.json); jede Fläche verweist über `quelle` auf
  ihren Eintrag. Wer einen Teil des Bestands weitergibt, gibt die Einträge der
  enthaltenen Quellen mit.
- **Geändert:** Sachdaten entfernt; die Geometrien auf 2D reduziert, nach
  EPSG:25832 umprojiziert, wo sie ungültig waren technisch gültig gemacht, und
  die Punktfolge normalisiert. Inhaltlich bearbeitet — verschnitten, geglättet,
  korrigiert oder vereinigt — ist keine Fläche, auch keine mit
  `bearbeitung_erlaubt = false`.
- **`amtliches-werk`**: Geltungsbereiche, die eine Satzung festsetzt, sind
  nach unserer Auffassung als amtliches Werk nach § 5 UrhG frei; Quellenvermerk mit der Gemeinde als
  Herausgeber. So stehen auch Geltungsbereiche aus Quellen hier, deren
  Lizenzangabe unklar ist oder deren Bedingungen die Nutzung einschränken —
  vermerkt in `einschraenkung` und in [`QUELLEN.md`](QUELLEN.md). Die Daten
  dieser Pläne geben wir nicht weiter, auch nicht an Partner.

Keine Gewähr für Vollständigkeit und Richtigkeit. Maßgeblich ist allein die
ausgefertigte Satzung der Gemeinde.
