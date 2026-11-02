# Funktionen der x2-Regler

Quellen: TA-Wiki-Seiten je Funktion (Links unten); Grundsätze aus „TAPPS2 Funktionsmodule“.

## Grundsätze

- **Eingangsvariablen** haben eine Quelle (Benutzer, Eingang, Ausgang, Funktion, Fixwert,
  Systemwert, DL-Bus, CAN analog/digital). **Parameter** sind feste Werte – nicht verknüpfbar.
  Was dynamisch werden soll, muss die Funktion als Eingangsvariable anbieten.
- **Diff. Ein / Diff. Aus werden zur Solltemperatur addiert** und dürfen negativ sein.
  Soll 60 °C, Diff. Ein −15 K, Diff. Aus +20 K heißt: ein unter 45 °C, aus über 80 °C.
- Funktionsgrößen intern in kleinster Einheit: 100,0 % ergibt als „dimensionslos“ 1000.

## Heizkreisregelung — [Wiki](https://wiki.ta.co.at/Heizkreisregelung_(Funktion))

**Heizkurve „Temperatur“:** zwei Stützpunkte `T.Vorlauf +10°C` und `T.Vorlauf -20°C` plus fester
Bezugspunkt 20 °C außen = 20 °C Vorlauf; der Verlauf ist **gekrümmt, nicht linear**. „Steilheit“
ist die Normkurve. Berechnet für 20 °C Raumsoll, für andere Sollwerte parallel verschoben.

| Parameter | Wirkung |
|---|---|
| `Niveau` | Parallelverschiebung (Parameter, nicht verknüpfbar) |
| `T.Vorlauf Max` / `Min` | Grenzen; Min gilt außer im Standby |
| `T.Vorlauf Min Normal` | Untergrenze nur im Normalbetrieb – **muss beim Absenken der Kurve mit**, sonst greift sie an milden Tagen |
| `Raumeinfluss` | 0–90 %, braucht einen Raumfühler |
| `Einschaltüberhöhung` | 0–20 %, wirkt nach Pumpenstillstand, voll nach 10 h |

**Von außen beeinflussbar** (Eingangsvariablen): *Offset Vorlaufsolltemp.*,
*Offset Raumsolltemp.*, *Raumsolltemperatur*, *Heizen mit externer VL.Solltemp.* +
*Externe VL.Solltemp.* – z. B. per CoE aus Home Assistant.

**Abschaltbedingungen der Pumpe:** Raum Ist > Soll (Normal/Absenk), **T.Vorlauf Soll < Min**
(Werkseinstellung, häufigste), T.Vorlauf Ist > Max, T.Außen-Mittel > Max. Bei aktiver
Abschaltung: Pumpe aus, Vorlaufsoll = **5 °C**.

**Achtung:** *Freigabe Heizkreis = AUS* → **kein Frostschutz**. Den *Externen Schalter* nie mit
einem Temperaturfühler verknüpfen (kann den Regler beschädigen).

Ausgangsvariablen u. a.: Vorlaufsolltemperatur, Effektive Raumsolltemperatur, Pumpe, Mischer,
Betriebsart (1 Normal, 2 Abgesenkt, 3 Standby, 4 Frostschutz, 11 Externe VL-Soll …),
**Anforderungssolltemp.** (für die Anforderung Heizung).

## Anforderung Heizung — [Wiki](https://wiki.ta.co.at/Anforderung_Heizung_(Funktion))

- Ein bei *Soll Anforderung + Diff. Ein* am Fühler T.Anf, aus bei *Soll Abschaltung + Diff. Aus*
  am Fühler T.Aus (ohne T.Aus beide an T.Anf).
- *Solltemperatur Anforderung* kann die **Anforderungssolltemp. des Heizkreises** sein – dann
  wandert die Schwelle mit der Heizkurve. Mit festem Soll (z. B. 60 °C, Diff. Ein −15 K) kommt
  die Anforderung bei Frost leicht zu spät: Fällt der Puffer oben unter 45 °C, verlangt der
  Heizkreis womöglich schon 48–50 °C.
- `Sockeltemperatur T.Anf. Min`, `T.Erz. Max` (schaltet auch während der Mindestlaufzeit ab),
  `Mindestlaufzeit Erzeuger`, *Einmal Laden*, Ökobetrieb (Unterdeckung).
- **Bei Hand-/Scheitholzfeuerung startet der Ausgang nichts** – er ist nur eine Anzeige.

## Ladepumpe — [Wiki](https://wiki.ta.co.at/Ladepumpenfunktion)

Ein, wenn T.Zub > T.Zub.Min, T.Zub um Diff. über T.Ref und T.Ref < T.Ref.Max. Mindest- und
Maximaltemperatur sind Eingangsvariablen. Regel: bei T.Zub.Min Diff. Ein > Diff. Aus, bei
T.Ref.Max Diff. Ein < Diff. Aus. Sitzt der Referenzfühler in der **Speichermitte**, muss fast der
ganze Speicher die Zieltemperatur erreichen – mit „Aus 0 K“ schaltet die Pumpe dann nie ab.

## Solarregelung / Solarvorrang — [Wiki](https://wiki.ta.co.at/Solarregelung_(Funktion)), [Vorrang](https://wiki.ta.co.at/Solarvorrang_(Funktion))

Solar: Kollektor zwischen Min und Max, Differenz Kollektor–Referenz, Referenz < Max.
Vorrang: absolut (erst wenn der Vorrangspeicher voll ist) oder relativ (Vorrangtimer mit
Stillstand, Spüldauer, Laufzeit, Wartezeit). Läuft die Solarpumpe nachts, gibt sie
Speicherwärme über den Kollektor ab – an der Nacht-Laufzeit leicht zu erkennen.

## Legionellenschutz — [Wiki](https://wiki.ta.co.at/Legionellenschutzfunktion)

Startet, wenn die Solltemperatur innerhalb der Intervallzeit nicht für die Haltezeit erreicht
wurde. Hängt die Freigabe an einem Erzeuger, der nicht von selbst startet (Holz), scheitert
die Funktion still – sie läuft, kommt aber nie ans Ziel.

## Vergleich / Logik — [Vergleich](https://wiki.ta.co.at/Vergleichsfunktion), [Logik](https://wiki.ta.co.at/Logikfunktion)

Vergleich: A > (B + Diff.), Wert A nicht als Benutzerwert. Logik: Oder, Und, Flip-Flop
(Löschen dominant), XOR; unbenutzte Eingänge auf „unbenutzt“.

## Wärmemengenzähler — [Wiki](https://wiki.ta.co.at/Wärmemengenzähler_(Funktion))

Vorlauf, Rücklauf, Durchfluss (auch fest), Wärmekapazität. Ohne Kalibrierung bei 10 K Spreizung
bis ±21 % Fehler, mit ±4,5 %. Zählerstände werden **nur stündlich** gespeichert. *Zähler
löschen* und die Eingangsvariable *Zählerrücksetzung* löschen **alle** Perioden.
