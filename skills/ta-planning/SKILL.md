---
name: ta-planning
description: Planning heating, hot-water and solar control systems with Technische Alternative (TA) products – for homeowners planning their own system and for installers. Use when someone wants to choose a TA controller (UVR16x2, UVR610, UVR67, CAN-I/O45, CAN-EZ3, CAN-BC2, CAN-MTx2, C.M.I.), count inputs and outputs, pick sensors, immersion sleeves, flow sensors, room sensors or auxiliary relays, design the CAN or DL bus, write a bill of materials with article numbers and list prices, find the right datasheet or manual on ta.co.at, pick a program from the TA program library, or check which Austrian standards, OIB guidelines, state law and funding conditions apply. Also use for German requests like "welchen Regler brauche ich", "Stückliste UVR", "Fühler planen", "Heizungsregelung planen", "Kesseltausch Förderung Regelung". For operating or analysing an existing TA installation use the skill technische-alternative instead.
---

# Planning with Technische Alternative

The output of a planning session is a **plan someone can order and wire from**: an I/O list,
the chosen devices with reasons, a bus plan, a bill of materials with article numbers and links,
a function plan with starting values, and the checklist of applicable regulations. Template:
[assets/plan-template.md](assets/plan-template.md). Worked example:
[references/example-plan.md](references/example-plan.md).

Two audiences, one method:

- **Homeowner:** explain choices in plain words, flag every point where a licensed installer or
  electrician is required (Austria: installation for funding, mains connection, acceptance of the
  firing system), and keep the plan honest about uncertainty.
- **Installer:** be terse, give article numbers, terminal-level I/O and bus figures; skip basics.

Ask early which one you are talking to, and which country/state the system is in.

## Live data, not memory

Product data, prices and document versions change. This skill holds **how to find** them and the
figures as of **November 2026**; check before quoting:

- Product pages, datasheets, manuals, price list, program library: [references/catalog.md](references/catalog.md)
  – including the soft-404 trap on ta.co.at and how to find stable `datei/<id>` links.
- TA wiki for function details: `https://wiki.ta.co.at/index.php?title=<Page>&action=raw`.
- Prices: the current price list (list prices, EUR excl. VAT). Installer discounts (price groups)
  are not public – say so instead of guessing.

## Method

### 1. Capture the system

Ask for or derive: heat sources (log/pellet boiler, heat pump, gas, district heating, wood stove
with water jacket, electric rod), storage (buffer volume, DHW tank or fresh-water station),
heating circuits (number, radiators or floor heating, mixed or direct), solar thermal (fields,
consumers), DHW circulation, extras (return-flow boost, pool, cooling, ventilation, PV surplus),
existing sensors and wiring, remote access wishes (app, Home Assistant, logging), and whether a
hydraulic scheme exists. Without a hydraulic scheme there is no reliable plan – sketch one
first or ask for it.

### 2. I/O list – the foundation

One row per signal: name, type (temperature PT1000, 0–10 V, impulse, digital, DL value), location,
cable length; outputs with type (relay switching, relay pair for 3-point mixer, 0–10 V/PWM for a
high-efficiency pump, potential-free contact for a boiler demand), load. Count, then add **≥ 20 %
reserve** – systems grow (a second circuit, a heat meter, a sensor that should have been there).
Measurements worth adding from the start: buffer top/middle/bottom, DHW tank, every flow
temperature, outdoor, collector; flow/heat meters where energy matters; room sensors where curves
need tuning. Room temperature at a reference room makes heating-curve tuning possible later.

### 3. Choose devices

[references/devices.md](references/devices.md) has inputs, outputs, loads, function limits and
typical uses. Rules of thumb:

- Fixed standard scheme, ≤ 6 inputs / 7 outputs, no programming wanted → **UVR67** (program
  number from its list).
- Everything else → **UVR16x2** (16/16) as the central controller; **UVR610** (6/10) for small
  systems or as a second controller; **CAN-I/O45** (4/5, max 44 functions, no own supply) as a
  cheap extension; DL modules (AI5-DL, AO4-DL, TDI5-DL, RM2-DL) for a few extra signals.
- **C.M.I.** whenever remote access, logging history, Home Assistant (CoE), Modbus TCP or loading
  programs from a PC is wanted – for most systems that means always.
- Bus converters only for real needs: CAN-BC2 for Modbus RTU/KNX/M-Bus or galvanic separation,
  CAN-RP for long stubs, CAN-EZ3 for electrical energy (PV surplus, heating rods).

### 4. Bus plan

[references/bus-design.md](references/bus-design.md): node numbers (defaults collide – renumber),
line topology and termination, length vs. bit rate, **6 W budget on the CAN 12 V**, DL bus load
(sum ≤ 100 % per master), cable types and separation from mains.

### 5. Sensors, actuators, accessories

[references/sensors-actuators.md](references/sensors-actuators.md): PT1000 as standard, sensor type
per location and temperature range, immersion sleeves and lengths, flow sensors (FTS-DL vs. VIG),
pump control via PWM/0–10 V and output scaling, auxiliary relays, mixer motors (third party).

### 6. Bill of materials

Table: article number, description, quantity, list price, datasheet link (`datei/<id>`), source
date. Mark items that appear in the catalogue but not in the price list as "verify with TA".
Separate TA items from third-party items (pumps, mixer motors, cables, enclosure, surge
protection).

### 7. Function plan and starting values

Start from the **x2 program library** or a programming example if one matches the hydraulics
([catalog.md](references/catalog.md)); otherwise list the TA functions per task (heating circuit,
heat demand, charging pump, solar + priority, legionella, comparison/logic, heat meter). Give
starting values with reasons, e.g. heating curve for radiators after renovation lower than for
an old house; demand set-point tied to the circuit's *Anforderungssolltemp.* rather than a fixed
value; legionella release only from a heat source that starts by itself. Details of each function:
skill **technische-alternative**, `references/functions.md`.

### 8. Regulations, commissioning, handover

- Regulations and funding: [references/austria.md](references/austria.md) (Austria, example state
  Upper Austria). For other countries, say that the checklist is missing and list what to look
  for (building law, firing-system acceptance, standards for hydraulics/DHW/solar/electrical,
  funding conditions).
- Commissioning: sensor plausibility (every sensor reads sensibly), output test in manual mode,
  CAN node list, clock/NTP on the C.M.I., logging running, program export (`.txt`) and versioned
  `.dat` handed over, passwords handed over separately.

## Boundaries

- No legal or safety sign-off: hydraulic safety equipment (expansion, safety valve, thermal
  discharge safety on solid-fuel boilers) is the installer's design responsibility; the plan
  points to the standard, it does not replace it.
- Do not summarise standard contents; cite number, edition and scope.
- Prices are list prices at the stated date; never present them as an offer.
