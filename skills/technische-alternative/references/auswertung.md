# Auswertungen an TA-Anlagen

Rezepte aus der Analyse einer Anlage mit Scheitholz-/Pelletkessel, Schichtpuffer,
Warmwasserspeicher, Solarthermie und zwei Mischerkreisen (Daten aus Home Assistant/InfluxDB,
Stundenmittel, zwei Heizperioden). Die Zahlen sind Beispiele; Volumen und Grenzen an die
eigene Anlage anpassen.

## Datenquellen

- **CoE-Sensoren in HA** liegen ungleichmäßig vor (nur bei Änderung). Vor jeder Rechnung auf ein
  festes Raster bringen (Minuten: `resample().max().ffill(limit=…)`, Stunden: Mittel mit
  begrenzter Interpolation). Binäre Zustände als Stundenanteil, nicht als Stichprobe.
- **C.M.I.-Logging** (SD, Winsol) ist die dichteste Quelle – aber nur, solange die Uhr stimmt.
- **Zeitzonen:** auf Lokalzeit gerundete Zeitstempel scheitern an der Herbst-Umstellung
  (`AmbiguousTimeError`); in UTC rechnen, erst zur Anzeige umwandeln.

## Speicherinhalt

```
E [kWh] = c · V · T   mit c = 1,163 Wh/(l·K)
Puffer  = 1,163 · V_puffer · (T_oben + T_unten)/2
Boiler  = 1,163 · V_boiler · T_mitte
```

**Nutzbar** ist nur, was über der Temperatur liegt, die die Verbraucher noch brauchen, z. B.
Puffer über 35 °C im Mittel, Warmwasser über 45 °C. Jedes Grad mehr Spielraum unten bringt
`1,163 · V` Wh – bei 1 500 l rund 1,7 kWh.

**Entnahme pro Tag** = Summe der stündlichen Abnahmen des Inhalts (Zunahmen sind Erzeuger).

## Bedarfsmodell gegen Außentemperatur

Tagesentnahme gegen Tagesmittel außen (nur Heiztage, z. B. < 12 °C) linear anpassen.
Erfahrungen:

- Nach einer Sanierung (Dämmung) **nur Tage danach** verwenden.
- Unter 0 °C stieg die Entnahme nicht weiter (Sonne an klaren Frosttagen, Speichermasse) –
  Außentemperatur unten kappen: `a + b · (20 − max(T, 0))`.
- Grundlast (Warmwasser + Verluste) aus den Nicht-Heiztagen.
- Tagesstreuung ±10 kWh ist normal; für eine Empfehlung auf Viertel-Füllungen runden.

## Heizkurve gegen Raumtemperatur

Raumtemperatur gegen Vorlauf-Ist, getrennt nach Außentemperatur-Klassen, nur Stunden mit
laufender Pumpe. Bleibt der Raum bei niedrigem Vorlauf warm, ist die Kurve zu hoch. Räume über
dem Heizraum oder an warmen Steigleitungen sind als Beleg untauglich.
Vorlauf-Ist dauerhaft unter Soll bei gleichzeitig warmem Puffer → Mischer/Hydraulik prüfen,
nicht die Kurve.

## Anforderung gegen Anheizen

Für jeden Brennbeginn den Zustand der Anforderung und Puffer oben festhalten. Viele Brände ohne
Anforderung bei warmem Puffer heißen: zu früh nachgelegt. Puffer oben beim Einschalten der
Anforderung gegen den Vorlauf-Soll bei Frost halten: liegt er darunter, kommt sie zu spät.

## Kesselphasen aus der Stromaufnahme

Ein Smart-Plug am Kessel zeigt die Betriebsphasen, auch ohne Busanbindung:

| Leistung (Beispiel) | Phase |
|---|---|
| ~2 W | Bereitschaft |
| 25–37 W nach Gebläsebetrieb | Drosselung/Glut: Puffer voll, Feuer wartet |
| 40–55 W | Gebläse, Vollbrand |
| > 100 W | Zündung/Förderung |

Segmentieren: Leistung > 15 W, Lücken < 45 min überbrücken, Brände ≥ 1 h. Drosselphasen beginnen
typisch bei Puffer oben ~80 °C. Ein hoher Anteil gedrosselter Brennzeit heißt: mehr Holz
aufgelegt, als der Puffer aufnehmen konnte – schlechter Ausbrand, heißer Puffer, höhere Verluste.

## Stillstandsverluste

Stunden ohne Pumpe, Kessel und Solar auswählen, Abnahme des Speicherinhalts je Stunde gegen
Puffertemperatur auftragen. Beispiel: ~300 W bei 50–60 °C, ~940 W bei 80–90 °C. Enthält
Speicherdämmung, Rohre und Schwerkraftzirkulation; ungedämmte Rohre im Heizraum treiben den
Wert. Ein überladener Puffer kostet so ~10 kWh/Tag zusätzlich.

## Plausibilität

- Wertebereiche je Fühler prüfen (ein Raumfühler meldete monatelang 1 660 °C).
- Sensorkorrekturen aus dem Programmexport berücksichtigen.
- Windmesser über Analogeingang liefern Ausreißer: Stundenmittel, harte Grenzen.
