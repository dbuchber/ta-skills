<div align="center">

# 🔥 ta-skills

**Claude-Skills für Heizungsregelungen von Technische Alternative**

Planen · in Betrieb nehmen · betreiben · auswerten — UVR16x2, UVR610, UVR67, C.M.I. und Home Assistant

![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-D97757?style=flat-square)
![Technische Alternative](https://img.shields.io/badge/TA-UVR16x2_·_C.M.I.-2E7D32?style=flat-square)
![Home Assistant](https://img.shields.io/badge/Home_Assistant-CoE-41BDF5?style=flat-square&logo=homeassistant&logoColor=white)
![Stand](https://img.shields.io/badge/Stand-November_2026-555?style=flat-square)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-blue?style=flat-square)

</div>

---

## Worum es geht

Eine TA-Regelung ist frei programmierbar und deshalb mächtig – und genauso leicht falsch geplant,
falsch parametriert oder unbemerkt kaputt. Diese Skills geben Claude das Wissen und die
Arbeitsweise, um dabei zu helfen: **für Eigentümer, die ihre eigene Anlage verstehen und
verbessern wollen, und für Installateure, die eine neue planen.**

| | Skill | Wofür |
|:-:|---|---|
| 📐 | [**`ta-planning`**](skills/ta-planning/SKILL.md) | Neue oder umgebaute Anlage planen: E/A-Liste, Geräteauswahl, Busplan, Stückliste mit Artikelnummern und Datenblättern, Funktionsplan, Normen und Förderung in Österreich |
| 🔧 | [**`technische-alternative`**](skills/technische-alternative/SKILL.md) | Bestehende Anlage betreiben: Werte lesen (JSON-API, CoE), Parameter sicher ändern (C.M.I.-Menü, TAPPS2), Funktionen verstehen, Messdaten auswerten |

## So greifen die Teile ineinander

```mermaid
flowchart LR
    subgraph P["📐 ta-planning"]
        direction TB
        P1[Anlage erfassen] --> P2[E/A-Liste]
        P2 --> P3[Geräte & Bus]
        P3 --> P4[Stückliste]
        P4 --> P5[Funktionsplan]
        P5 --> P6[Normen & Förderung]
    end

    subgraph T["🔧 technische-alternative"]
        direction TB
        T1[Lesen] --> T2[Ändern mit Rücklesung]
        T2 --> T3[Auswerten]
        T3 -. Erkenntnisse .-> T2
    end

    P6 ==>|Inbetriebnahme| T1
    T3 -. Erfahrungen aus dem Betrieb .-> P1

    TA[("🌐 ta.co.at<br/>Katalog · Preisliste<br/>Datenblätter · Wiki")] -.-> P
    TA -.-> T
```

## Der Weg zur Anlage

Woher Claude seine Werte bekommt und wo es eingreifen kann:

```mermaid
flowchart LR
    C(["🤖 Claude"])

    subgraph LAN["Netzwerk"]
        CMI["C.M.I.<br/>Gateway"]
        HA["Home Assistant<br/>ta_coe"]
    end

    subgraph CAN["CAN-Bus"]
        UVR["UVR16x2<br/>Regler"]
        IO["CAN-I/O45<br/>UVR610 …"]
    end

    subgraph FELD["Anlage"]
        S["Fühler<br/>PT1000 · FTS-DL · RAS+DL"]
        A["Pumpen · Mischer<br/>Kesselanforderung"]
    end

    C -- "JSON-API<br/>lesen, 1×/min" --> CMI
    C -- "Menü<br/>lesen · ändern mit Freigabe" --> CMI
    C -- "Verlauf & Auswertung" --> HA
    CMI <-- "CoE (UDP)" --> HA
    CMI <--> UVR
    UVR <--> IO
    S --> UVR
    UVR --> A
```

## Was drin ist

<details>
<summary><b>📐 ta-planning</b> – Planung in acht Schritten</summary>

```
skills/ta-planning/
├── SKILL.md                 Planungsablauf, Zielgruppen, Grenzen
├── assets/plan-template.md  Vorlage für den Planungsbericht
└── references/
    ├── catalog.md           Produktseiten, Katalog, Preisliste, Datenblatt-IDs, Programmbibliothek
    ├── devices.md           Regler und Module im Vergleich, Grenzen, Schnittstellen
    ├── sensors-actuators.md Fühler, Tauchhülsen, Durchfluss, Pumpen, Mischer, Hilfsrelais
    ├── bus-design.md        CAN- und DL-Bus: Topologie, Länge, 12-V-Budget, Buslast
    ├── austria.md           Normen, OIB-Richtlinien, Landesrecht OÖ, Förderung 2026
    └── example-plan.md      Durchgerechnetes Beispiel mit Erfahrungen aus dem Betrieb
```

</details>

<details>
<summary><b>🔧 technische-alternative</b> – Betrieb und Auswertung</summary>

```
skills/technische-alternative/
├── SKILL.md                 Arbeitsweise, Wege zum Gerät, Fallstricke, Sicherheitsregeln
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

</details>

## Installation

```bash
git clone https://github.com/dbuchber/ta-skills.git
ln -s "$PWD/ta-skills/skills/ta-planning"            ~/.claude/skills/ta-planning
ln -s "$PWD/ta-skills/skills/technische-alternative" ~/.claude/skills/technische-alternative
```

Danach erkennt Claude Code die Skills von selbst – etwa bei *„Welchen Regler brauche ich für zwei
Heizkreise und Solar?“* oder *„Senk die Heizkurve um 2 K und prüf, ob es wirkt.“*

## Beispiele

| Frage | Skill |
|---|---|
| „Ich tausche meinen Ölkessel gegen Pellets – welche TA-Regelung, welche Fühler, was kostet das, welche Förderung gibt es?“ | 📐 |
| „Mach mir eine Stückliste für Puffer, Boiler, Solar und drei Heizkreise mit Datenblatt-Links.“ | 📐 |
| „Wie viel Energie steckt gerade im Puffer, und reicht sie bis morgen?“ | 🔧 |
| „Warum kommt die Kesselanforderung bei Frost zu spät?“ | 🔧 |
| „Bring die Vorlauf-Sollwerte der UVR als Sensoren nach Home Assistant.“ | 🔧 |

## Grundsätze

> [!IMPORTANT]
> **Erst lesen, dann ändern.** Jede Schreibaktion am Regler braucht die Freigabe des Betreibers,
> wird zurückgelesen und an einer Ausgangsgröße nachgewiesen.

- 🔐 **Zugangsdaten** nur über Umgebungsvariablen oder stdin – nie in Kommandozeilen oder Dateien.
- 📚 **Quellen:** Das [TA-Wiki](https://wiki.ta.co.at) ist Primärquelle; der Skill verweist darauf
  und schlägt Details dort nach. Was nur am Gerät beobachtet wurde (das Menüprotokoll des C.M.I.),
  ist als solches gekennzeichnet.
- 📅 **Stand November 2026:** Preise, Normausgaben und Förderbedingungen ändern sich – vor
  Verwendung prüfen.
- ⚖️ **Keine Rechtsberatung.** Verantwortung für Planung und Ausführung trägt der befugte
  Fachbetrieb.

## Sprache

Die Skills sind auf **Englisch** geschrieben, damit Claude sie in jeder Sprache nutzt;
Parameternamen stehen so, wie TA sie am Gerät zeigt (deutsch). Fragen auf Deutsch funktionieren.

---

<sub>Kein offizielles Produkt der Technische Alternative RT GmbH. Markennamen gehören ihren Inhabern. · Lizenz: MIT</sub>
