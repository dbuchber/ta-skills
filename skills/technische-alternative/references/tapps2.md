# TAPPS2: Funktionsdaten ändern und übertragen

Quellen: [TA-Wiki TAPPS2](https://wiki.ta.co.at/TAPPS2),
[Programmieren mit TAPPS2](https://wiki.ta.co.at/Programmieren_mit_TAPPS2),
[Funktionsdaten](https://wiki.ta.co.at/Funktionsdaten),
[UVR16x2 Programmierung, Allgemeine Hinweise (PDF)](https://www.ta.co.at/download/datei/1260).

## Dateien

| Datei | Was | Wer liest sie |
|---|---|---|
| `.tdw` | TAPPS2-Zeichnung mit Anordnung und Kommentaren | nur TAPPS2 |
| `.dat` | Funktionsdaten | der Regler |
| `.txt` | Dokumentation (*Datei → Exportieren → Dokumentation*) | Menschen und Diff |
| `.x2d` | Funktionsübersicht (TA-Designer) | Regler-Display |

Eine `.dat` lässt sich importieren, verliert dabei aber die Anordnung – deshalb die `.tdw`
aufbewahren. TAPPS2 verweigert den Export bei Programmierfehlern (z. B. doppelter CAN-Eingang).

## Fassungen führen

Je Programmstand eine eigene `.dat` (`Anlage_V2.1.dat`, `Anlage_V2.2.dat`), daneben der
Textexport und ein kurzes Änderungsprotokoll (Datum, Autor, was und warum). Der Textexport ist
die einzige diff-bare Form; in Git versionieren.

## Ablauf einer Programmänderung

1. **Stand vom Gerät sichern.** Am Regler *Datenverwaltung → Speichern…* (auf SD) oder über das
   C.M.I. *Datenverwaltung* die Funktionsdaten des Knotens herunterladen. So sind auch Werte
   gesichert, die seit der letzten Übertragung am Gerät geändert wurden.
2. Die zuletzt übertragene `.tdw`/`.dat` öffnen, **sofort unter neuer Fassung speichern**.
3. Am Gerät erprobte Werte übernehmen – was nicht in TAPPS2 steht, ist nach der Übertragung weg.
4. Prüfen: Simulator (x2-Simulator ≥ 1.38) und Textexport gegen die Vorfassung diffen.
5. *Datei → Exportieren → Funktionsdaten*.
6. Übertragen: C.M.I. *Datenverwaltung* (Datei hochladen, an Knoten senden) oder SD-Karte am
   Regler. Verlangt wird das Fachmann-/Experten-Passwort **des Zielgeräts**.
7. Abfragen beantworten: Zählerstände der Ausgänge und Funktionen, Kalibrierwerte WMZ,
   CORA-Pairing, CAN-Knotennummer – nach einer Programmänderung in der Regel **Beibehalten**.
8. Nachher: Version/Dateiname am Gerät, `CHANGE.LOG` auf der SD, Funktionsstatus, Sollwerte.

## Was beim Laden passiert

- Der Regler legt vorher **`_Backup.dat`** mit dem alten Stand auf die SD-Karte.
- Alle Parameter und Fixwerte kommen aus der neuen `.dat`; Ausnahmen sind nur die abgefragten
  Zähler, Kalibrierwerte und Pairings.
- Danach steht der Regler in der **Anwenderebene**, es gelten die Passwörter aus der `.dat`.
- Jede Änderung am Regler landet mit Zeitstempel in `CHANGE.LOG` auf der SD-Karte.
- **Totalreset** löscht die gesamte Programmierung (Knoten und Busrate bleiben). Firmware-
  Werkszustand (Reset-Taste beim Einschalten bis Ende des Pfeiftons) löst ihn ebenfalls aus.

## Firmware

Kostenlos unter ta.co.at/download/firmware. UVR16x2, UVR610, CAN-MTx2, C.M.I. per SD-Karte,
andere Geräte über CAN. „Bitte vor dem Download lesen“ beachten – manchmal sind
Zwischenversionen nötig.
**C.M.I.-Reset-Taster:** kurz bis die LEDs laufen = Werksreset; bis zum Ende des Lauflichts
gehalten = Firmware-Update von SD.
