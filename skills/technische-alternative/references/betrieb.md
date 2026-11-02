# Betrieb: Benutzerebenen, Uhrzeit, Logging, CAN

Quellen: [Benutzerebenen](https://wiki.ta.co.at/Benutzerebenen),
[Datum und Uhrzeit](https://wiki.ta.co.at/Datum_und_Uhrzeit),
[Datenloggen mit Winsol](https://wiki.ta.co.at/Datenloggen_mit_Winsol),
[CAN-Bus](https://wiki.ta.co.at/CAN-Bus), [C.M.I.](https://wiki.ta.co.at/C.M.I.).

## Benutzerebenen der x2-Regler

| Ebene | darf u. a. |
|---|---|
| Anwender | Werte ansehen, freigegebene Fixwerte/Ausgänge, Datum/Uhrzeit, Standort |
| Fachmann (Passwort) | Parameter von Funktionen, Ein-/Ausgängen, CAN/DL; Funktionsdaten und Firmware laden |
| Experte (Passwort) | alles |

- Nach dem Laden von Funktionsdaten und nach jedem Neustart: Anwenderebene.
- 30 min nach einem Login automatisch zurück zur Anwenderebene.
- Passwörter kommen aus den Funktionsdaten. Standardpasswörter **nicht durchprobieren** – den
  Betreiber fragen.
- Das C.M.I. hat ein eigenes HTTP-Login; die JSON-API verlangt dort die Ebene Experte.

## Uhrzeit

- Alle CAN-Geräte übernehmen Datum und Zeit von **Knoten 1**. Das Wiki empfiehlt, das C.M.I.
  zu Knoten 1 zu machen, weil es die Zeit aus dem Netz holt.
- C.M.I.: Zeitquelle *WEB / CAN / DL1 / DL2*, Zeitzone, Sommerzeit, **NTP-Server frei
  eintragbar** (UDP 123 ausgehend).
- Erfahrung: Nach einem Stromausfall verlor das C.M.I. die Zeit, der eingetragene NTP-Server
  (das Gateway) beantwortete kein NTP – das Logging blieb fast zwei Jahre stumm, ohne Meldung.
  Einen öffentlichen Pool oder einen geprüften lokalen Server eintragen und nach jedem
  Stromausfall die Uhr kontrollieren.
- Gangreserve der UVR16x2: etwa 3 Tage.

## Logging

- Am Regler *CAN-Bus → Datenlogging*: bis 64 analoge und 64 digitale Werte. Die Liste gilt für
  das SD-Logging des Reglers und das CAN-Logging per C.M.I.
- Am C.M.I. *Einstellungen → Datenlogging*: Intervall und „Rahmen“ (Quelle = Knoten, Datensatz x2).
- Das C.M.I. schreibt **einmal täglich** vom internen Speicher auf die SD-Karte.
- Winsol kann beim Auslesen Daten am Logger löschen – Einstellung prüfen.
- SD-Logging der UVR: Tagesdateien unter `LOG/<Jahr>`, älteste werden bei < 50 MB frei gelöscht.

## CAN-Bus

- Knoten 1–62, Standardrate 50 kbit/s (max. 1 000 m), eine Strangleitung, Abschluss an beiden
  Enden, höchstens 6 W an der 12-V-Ader.
- CAN-Eingänge: Timeout mindestens 5 min, danach „Netzwerkfehler“ – Ersatzwert bewusst wählen.
- CAN-Ausgänge senden bei Änderung > x, frühestens nach Blockierzeit (≥ 1 s), spätestens nach
  Intervall (≥ 1 min).
