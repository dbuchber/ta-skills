---
name: technische-alternative
description: Arbeiten mit Regelungen von Technische Alternative (TA) – UVR16x2, UVR610, RSM610, CAN-I/O45, CAN-MTx2, C.M.I. – und ihrer Anbindung an Home Assistant. Verwenden bei allem rund um TA-Heizungsregler: Werte lesen über die C.M.I. JSON-API, CoE (CAN over Ethernet) von und zu Home Assistant, Funktionsdaten mit TAPPS2 ändern und übertragen, Parameter im C.M.I.-Menü setzen (Heizkurve, Anforderung, Solar, Ladepumpe, Legionellenschutz), Benutzerebenen, Datenlogging/Winsol, Uhrzeit/NTP, Programmexporte lesen und auswerten (Puffer, Heizkurve, Kesselanforderung). Auch verwenden, wenn nur „UVR“, „C.M.I.“, „CMI“, „TAPPS“, „CoE“, „Heizkurve am Regler“ oder „ta_coe“ fällt, oder wenn Messwerte einer Holz-/Pellet-/Solaranlage mit TA-Regler analysiert werden sollen.
---

# Technische Alternative (UVR16x2 & C.M.I.)

Ein TA-Regler steuert eine Heizung, die bei Fehlern friert, überhitzt oder Legionellen züchtet.
Deshalb gilt hier mehr als sonst: **erst lesen, dann ändern, jede Änderung zurücklesen, und der
Betreiber gibt jede Schreibaktion einzeln frei.** Die Anleitungen unten trennen lesende und
schreibende Wege ausdrücklich.

## Die Familie in drei Sätzen

Regler (UVR16x2, UVR610, früher RSM610) und Module (CAN-I/O45, CAN-MTx2) hängen an einem
CAN-Bus, jedes Gerät mit eigener Knotennummer 1–62. Das **C.M.I.** ist das Ethernet-Gateway
dazu: Weboberfläche, JSON-API (nur lesen), CoE (UDP, Werte zwischen CAN-Netzen und zu
Fremdsystemen), Datenlogging auf SD. Programmiert wird mit **TAPPS2** (Zeichnung `.tdw`,
Funktionsdaten `.dat`), übertragen über C.M.I. oder SD-Karte.

## Zuerst klären

1. **Welche Knotennummern?** C.M.I.-Weboberfläche → *CAN-Bus*. Standard: UVR16x2 = 1,
   UVR610/RSM610/CAN-I/O45 = 32, CAN-MTx2 = 50, C.M.I. = 56 – in Bestandsanlagen oft anders.
2. **Welche Firmware?** C.M.I. *Status*; UVR *Version*. JSON-API-Version hängt an der
   C.M.I.-Firmware ([references/json-api.md](references/json-api.md)).
3. **Gibt es einen Programmexport?** TAPPS2 *Datei → Exportieren → Dokumentation* (`.txt`). Er
   ist die beste Quelle für Funktionen, Parameter und Signalketten – weit besser als das Menü
   abzuklicken. Kodierung ISO-8859-1 mit CRLF: `iconv -f latin1 -t utf-8 | tr -d '\r'`.
4. **Wer feuert?** Bei Scheitholz- oder Handbetrieb startet die „Anforderung“ nichts – sie ist
   dann nur eine Anzeige. Das ändert die Bewertung jeder Kesselfunktion.

## Wege zum Gerät – lesend

| Weg | Wofür | Grenze |
|---|---|---|
| **JSON-API** `/INCLUDE/api.cgi` | Eingänge, Ausgänge, DL-Bus, Systemwerte, Logging-Liste | **1 Anfrage pro Minute**, verlangt Experten-Login, keine CAN-/Netzwerkeingänge von x2-Geräten → [json-api.md](references/json-api.md) |
| **CoE → Home Assistant** (z. B. HACS `ta_coe`) | laufende Werte, die die UVR als CAN-Ausgang an einen virtuellen Knoten sendet | sendet nur bei Änderung > x oder nach Intervall; Werte können Minuten alt sein → [coe.md](references/coe.md) |
| **C.M.I.-Menü** (Fernbedienung der UVR im Browser) | alles, was das Display zeigt, inkl. Parameter | schwacher Webserver, Login-Ebenen → [cmi-menue.md](references/cmi-menue.md) |
| **Datenlogging** (C.M.I. → SD, Winsol) | Historie in Minutenauflösung | nur mit gültiger Uhrzeit, Liste am Regler festgelegt → [betrieb.md](references/betrieb.md) |
| **Programmexport** (`.txt`) | Parameter, Verknüpfungen, Sensorkorrekturen | nur so aktuell wie die letzte Übertragung; am Gerät geänderte Werte fehlen |

## Ändern – Reihenfolge

1. **Ziel und Rückweg aufschreiben**: Parameter, alter Wert, neuer Wert, wie zurück.
2. **Freigabe** des Betreibers für genau diese Werte einholen.
3. **Kleine Probeschritte direkt am Regler** (Display oder C.M.I.-Menü): sofort wirksam, sofort
   umkehrbar, kein Neustart. Für Kurven: 2 K je Schritt, eine Woche beobachten.
4. **Jede Schreibaktion zurücklesen** und gegen den erwarteten Wert prüfen. Bei Abweichung oder
   Zeitüberschreitung **anhalten** – nicht blind wiederholen.
5. **Wirkung belegen**: Ausgangsvariable (z. B. Vorlaufsolltemperatur) über CoE oder Menü.
6. **Endgültig in TAPPS2 festschreiben** (neue Fassung `_V<x>.dat`, Textexport, Änderungsprotokoll),
   sonst überschreibt die nächste Übertragung die Probewerte → [tapps2.md](references/tapps2.md).

Skript für Schritt 3–4 über das C.M.I.-Menü: [scripts/cmi_menu.py](scripts/cmi_menu.py)
(`read` liest, `set` schreibt nur mit `--write` und prüft alten Wert und Rücklesung).

## Funktionen und typische Stellschrauben

Parameter (feste Werte) und Eingangsvariablen (verknüpfbar) sind verschieden: **Parameter lassen
sich nicht von außen speisen.** Wer Werte aus Home Assistant einspielen will, braucht eine
Eingangsvariable – etwa *Offset Vorlaufsolltemp.* am Heizkreis. Details zu Heizkreis,
Anforderung Heizung, Ladepumpe, Solar, Solarvorrang, Legionellenschutz, Vergleich, Logik,
Wärmemengenzähler: [references/funktionen.md](references/funktionen.md).

## Auswerten

Rezepte mit Formeln und Fallstricken – Speicherinhalt in kWh, nutzbare Wärme, Stillstandsverluste,
Heizkurve gegen Raumtemperatur, Anforderung gegen tatsächliches Anheizen, Abkühl-/Drosselphasen
des Kessels aus der Stromaufnahme, Sensor-Plausibilität: [references/auswertung.md](references/auswertung.md).

## Fallstricke, die schon Zeit gekostet haben

- **C.M.I.-Webserver überlastet:** Wenige Menüabrufe kurz hintereinander, und das C.M.I. war
  5 bis 20 Minuten nicht erreichbar (Ping mit Verlust, HTTP-Timeout) – CoE lief dabei weiter.
  Abrufe bündeln, ≥ 10 s Abstand, nach einem Timeout warten statt nachfeuern.
- **Uhr:** Das C.M.I. verliert bei Stromausfall die Zeit; ohne erreichbaren NTP-Server fehlt
  ihm die Zeitquelle, und das **Logging bleibt stumm, ohne Fehlermeldung** (gesehen: fast zwei
  Jahre). NTP auf einen Server setzen, der wirklich antwortet; Knoten 1 gibt die Zeit im CAN vor.
- **Unplausible Fühler** fallen in HA nicht auf: Ein DL-Raumfühler meldete monatelang ~1 660 °C
  und sperrte damit eine Automation, die „Raum < 20 °C“ verlangte. Wertebereiche prüfen.
- **Sensorkorrektur** steht im Programm (`Sensorkorrektur: +10,0 K`) – ein fester Offset, der
  nur an einem Betriebspunkt stimmt. Im Export nachsehen, bevor man Messwerte vergleicht.
- **Soll = 5 °C** bei einer Vorlaufsolltemperatur heißt „Pumpe aus / Abschaltbedingung aktiv“,
  kein Defekt.
- **Nicht vorhandene CAN-Knoten** im C.M.I. abzufragen kostet je ~20 s Timeout.
- **Freigabe Heizkreis = AUS schaltet auch den Frostschutz ab.**

## Sicherheitsregeln

- Zugangsdaten nie in Kommandozeilen (`argv`), nie in Dateien im Repo; über Umgebungsvariablen
  aus einem Schlüsselbund oder `curl --config -` auf stdin.
- Die Experten-Zugangsdaten der JSON-API sind dieselben, die in der Weboberfläche alles ändern
  dürfen – ein „lesendes“ Skript hat faktisch Schreibrechte. Lesende Skripte daher auf
  `api.cgi` und `devpagex.cgi` beschränken.
- Nie ohne ausdrücklichen Auftrag: Funktionsdaten laden, Firmware, Totalreset, Neustart,
  Datei löschen, Logging löschen, Zählerstände zurücksetzen, Handbetrieb von Ausgängen.
- Standardpasswörter nicht ausprobieren – nach dem Passwort fragen.
- Nach Abschluss die Menüsitzung verwerfen (Cookie löschen); die UVR fällt nach 30 min ohnehin
  in die Anwenderebene zurück.
