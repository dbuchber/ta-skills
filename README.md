# ta-skills

Claude-Skills für Heizungsregelungen von **Technische Alternative** (UVR16x2, UVR610, RSM610,
CAN-I/O45, CAN-MTx2, C.M.I.) und ihre Anbindung an Home Assistant.

*Claude skills for Technische Alternative heating controllers (UVR16x2, C.M.I.) – JSON API, CoE,
TAPPS2, menu access via the C.M.I., and analysis recipes. The skill itself is in English;
this README is German.*

## Skills

| Skill | Inhalt |
|---|---|
| [`technische-alternative`](skills/technische-alternative/SKILL.md) | Lesen über JSON-API und CoE, Ändern über C.M.I.-Menü und TAPPS2, Funktionen und Parameter, Betrieb (Benutzerebenen, Uhrzeit, Logging), Auswertungen |

```
skills/technische-alternative/
├── SKILL.md                 Einstieg, Arbeitsweise, Fallstricke
├── references/
│   ├── json-api.md          C.M.I. JSON-API: Parameter, Statuscodes, Einheiten
│   ├── coe.md               CAN over Ethernet, Home Assistant in beide Richtungen
│   ├── cmi-menu.md          UVR-Menü über das C.M.I. lesen und ändern (beobachtetes Protokoll)
│   ├── tapps2.md            Funktionsdaten ändern, versionieren, übertragen
│   ├── functions.md         Heizkreis, Anforderung, Ladepumpe, Solar, Legionellen, WMZ …
│   ├── operation.md         Benutzerebenen, Uhrzeit/NTP, Logging, CAN
│   └── analysis.md          Speicherinhalt, Bedarfsmodell, Heizkurve, Kesselphasen, Verluste
└── scripts/
    └── cmi_menu.py          Menüseiten lesen, Werte mit Prüfung und Rücklesung setzen
```

## Installation

Den Ordner `skills/technische-alternative` nach `~/.claude/skills/` kopieren oder verlinken.

## Sprache und Quellen

Der Skill ist auf Englisch geschrieben; Parameternamen stehen so, wie TA sie am Gerät zeigt
(deutsch). Primärquelle ist das [TA-Wiki](https://wiki.ta.co.at) – der Skill verweist darauf und
weist Claude an, Details dort nachzuschlagen; bei Widerspruch gilt das Wiki.

## Grundsätze

- Erst lesen, dann ändern; jede Schreibaktion zurücklesen; der Betreiber gibt jede Änderung frei.
- Zugangsdaten nur über Umgebungsvariablen oder stdin, nie in Kommandozeilen oder Dateien.
- Was aus der offiziellen TA-Dokumentation stammt, ist verlinkt. Was nur am Gerät beobachtet
  wurde (das Menü-Protokoll des C.M.I.), ist als solches gekennzeichnet und kann sich mit der
  Firmware ändern.

Kein offizielles Produkt von Technische Alternative RT GmbH. Markennamen gehören ihren Inhabern.

## Lizenz

MIT
