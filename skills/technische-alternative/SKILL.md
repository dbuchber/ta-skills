---
name: technische-alternative
description: Working with heating controllers from Technische Alternative (TA) – UVR16x2, UVR610, RSM610, CAN-I/O45, CAN-MTx2, C.M.I. – and their integration with Home Assistant. Use for anything around TA controllers – reading values via the C.M.I. JSON API, CoE (CAN over Ethernet) to and from Home Assistant, changing and transferring function data with TAPPS2, setting parameters through the C.M.I. menu (heating curve, heat demand, solar, charging pump, legionella protection), user levels, data logging/Winsol, clock/NTP, reading and analysing program exports and measurements (buffer tank, heating curve, boiler demand). Also use when only "UVR", "C.M.I.", "CMI", "TAPPS", "CoE", "Heizkurve", "ta_coe" or "Technische Alternative" is mentioned, or when measurements of a wood/pellet/solar heating system with a TA controller are to be analysed – including German requests.
---

# Technische Alternative (UVR16x2 & C.M.I.)

A TA controller runs a heating system that freezes, overheats or breeds legionella when it goes
wrong. So more than elsewhere: **read first, change second, read back every change, and let the
operator approve each write individually.** The guides below keep read and write paths apart.

TA's user interface is German. Parameter names are quoted as they appear on the device
(`T.Vorlauf +10°C`, `Diff. Ein`, `Anforderung Heizung`); translations follow in brackets where
helpful.

## The family in three sentences

Controllers (UVR16x2, UVR610, formerly RSM610) and modules (CAN-I/O45, CAN-MTx2) share a CAN bus,
each device with its own node number 1–62. The **C.M.I.** is the Ethernet gateway: web interface,
JSON API (read only), CoE (UDP, values between CAN networks and to third-party systems), data
logging to SD. Programming is done in **TAPPS2** (drawing `.tdw`, function data `.dat`),
transferred via the C.M.I. or SD card.

## Sources

The skill summarises; the **TA wiki is the primary source** and is more current.

- **Wiki:** https://wiki.ta.co.at – one page per device and per function. For targeted lookups,
  fetch the wikitext: `https://wiki.ta.co.at/index.php?title=<Page_title>&action=raw`
  (e.g. `Heizkreisregelung_(Funktion)`, `C.M.I._JSON-API`, `CAN_over_Ethernet_(CoE)`). This was
  reliable where rendered pages were not.
- **Manuals (PDF):** `https://www.ta.co.at/download/datei/<id>` – IDs are linked in the reference
  files (JSON API, CoE, UVR16x2 programming, TAPPS2, C.M.I.).
- **C.M.I. online help** (`help.ta.co.at`) sits behind a bot challenge. Do not try to bypass it;
  ask the user to open the page if its content is needed.
- **If this skill and the wiki disagree, the wiki wins** – then check firmware versions (C.M.I.
  *Status*, controller *Version*), since behaviour changes with firmware.

## Clarify first

1. **Which node numbers?** C.M.I. web interface → *CAN-Bus*. Defaults: UVR16x2 = 1,
   UVR610/RSM610/CAN-I/O45 = 32, CAN-MTx2 = 50, C.M.I. = 56 – often different in real systems.
2. **Which firmware?** The JSON API version depends on the C.M.I. firmware
   ([references/json-api.md](references/json-api.md)).
3. **Is there a program export?** TAPPS2 *Datei → Exportieren → Dokumentation* (`.txt`). It is the
   best source for functions, parameters and signal chains – far better than clicking through the
   menu. Encoding ISO-8859-1 with CRLF: `iconv -f latin1 -t utf-8 | tr -d '\r'`.
4. **Who lights the fire?** With manually fired log boilers the controller's demand output
   ("Anforderung") starts nothing – it is only an indicator. That changes how every boiler
   function should be judged.

## Ways to the device – reading

| Path | For | Limits |
|---|---|---|
| **JSON API** `/INCLUDE/api.cgi` | inputs, outputs, DL bus, system values, logging list | **one request per minute**, needs expert login, no CAN/network inputs of x2 devices → [json-api.md](references/json-api.md) |
| **CoE → Home Assistant** (e.g. HACS `ta_coe`) | live values the controller sends as CAN outputs to a virtual node | sent only on change > x or after an interval; values may be minutes old → [coe.md](references/coe.md) |
| **C.M.I. menu** (remote display of the controller) | everything the display shows, including parameters | weak web server, user levels → [cmi-menu.md](references/cmi-menu.md) |
| **Data logging** (C.M.I. → SD, Winsol) | history at minute resolution | only with a valid clock; list defined on the controller → [operation.md](references/operation.md) |
| **Program export** (`.txt`) | parameters, links, sensor corrections | only as current as the last transfer; values changed on the device are missing |

## Changing – the order

1. **Write down target and way back:** parameter, old value, new value, how to revert.
2. **Get the operator's approval** for exactly these values.
3. **Small trial steps directly on the controller** (display or C.M.I. menu): effective at once,
   reversible at once, no restart. For heating curves: 2 K per step, observe for a week.
4. **Read back every write** and compare with the expected value. On mismatch or timeout,
   **stop** – do not retry blindly.
5. **Prove the effect** on an output variable (e.g. flow set temperature via CoE or menu).
6. **Make it permanent in TAPPS2** (new version `_V<x>.dat`, text export, change note);
   otherwise the next transfer overwrites the trial values → [tapps2.md](references/tapps2.md).

Script for steps 3–4 via the C.M.I. menu: [scripts/cmi_menu.py](scripts/cmi_menu.py) (`page`/`get`
read; `set` writes only with `--write` and checks old value and read-back).

## Functions and typical adjustments

Parameters (fixed values) and input variables (linkable) are different: **parameters cannot be fed
from outside.** To inject values from Home Assistant you need an input variable – such as
*Offset Vorlaufsolltemp.* (flow set-point offset) on the heating circuit. Heating circuit, heat
demand, charging pump, solar, solar priority, legionella, comparison, logic, heat meter:
[references/functions.md](references/functions.md).

## Analysis

Recipes with formulas and pitfalls – stored energy in kWh, usable heat, standby losses, heating
curve vs. room temperature, demand signal vs. actual firing, throttled phases of the boiler from
its power draw, sensor plausibility: [references/analysis.md](references/analysis.md).

## Pitfalls that already cost time

- **Overloaded C.M.I. web server:** a handful of menu requests in quick succession made the C.M.I.
  unreachable for 5 to 20 minutes (packet loss, HTTP timeouts) while CoE kept running. Batch
  requests, keep ≥ 10 s between them, wait after a timeout instead of retrying.
- **Clock:** the C.M.I. loses its time on power loss; without a reachable NTP server it has no time
  source and **logging stays silent without any error** (seen: almost two years). Point NTP at a
  server that really answers; node 1 sets the time for the CAN bus.
- **Implausible sensors** go unnoticed in Home Assistant: a DL room sensor reported ~1,660 °C for
  months and thereby blocked an automation requiring "room < 20 °C". Check value ranges.
- **Sensor correction** lives in the program (`Sensorkorrektur: +10,0 K`) – a fixed offset that is
  right at one operating point only. Look it up in the export before comparing measurements.
- **Set temperature = 5 °C** on a flow set-point means "pump off / shut-off condition active", not
  a fault.
- **Querying non-existent CAN nodes** on the C.M.I. costs ~20 s timeout each.
- **`Freigabe Heizkreis` = OFF also disables frost protection.**

## Safety rules

- Never put credentials on a command line (`argv`) or in repository files; pass them via
  environment variables from a keychain, or via `curl --config -` on stdin.
- The expert credentials required by the JSON API are the same that can change everything in the
  web interface – a "read-only" script effectively has write access. Restrict read scripts to
  `api.cgi` and `devpagex.cgi`.
- Never without an explicit request: loading function data, firmware, total reset, restart,
  deleting files or logs, resetting meters, manual mode of outputs.
- Do not try default passwords – ask for the password.
- When done, discard the menu session (delete the cookie); the controller falls back to the user
  level after 30 minutes anyway.
