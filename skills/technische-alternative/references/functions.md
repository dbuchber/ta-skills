# Functions of the x2 controllers

Sources: TA wiki page per function (links below); principles from "TAPPS2 Funktionsmodule".
German names are those shown on the device.

## Principles

- **Input variables** have a source (user, input, output, function, fixed value, system value,
  DL bus, CAN analog/digital). **Parameters** are fixed values – not linkable. Whatever should
  become dynamic must be offered by the function as an input variable.
- **`Diff. Ein` / `Diff. Aus` (on/off differential) are added to the set temperature** and may be
  negative. Set 60 °C, Diff. Ein −15 K, Diff. Aus +20 K means: on below 45 °C, off above 80 °C.
- Function values internally use the smallest unit: 100.0 % taken as "dimensionless" becomes 1000.

## Heating circuit (`Heizkreisregelung`) — [wiki](https://wiki.ta.co.at/Heizkreisregelung_(Funktion))

**Curve type "Temperatur":** two points `T.Vorlauf +10°C` and `T.Vorlauf -20°C` (flow temperature
at +10 / −20 °C outside) plus a fixed reference 20 °C outside = 20 °C flow; the curve is
**bent, not linear**. "Steilheit" is the standard slope curve. Computed for a 20 °C room set-point
and shifted in parallel for other set-points.

| Parameter | Effect |
|---|---|
| `Niveau` | parallel shift (parameter, not linkable) |
| `T.Vorlauf Max` / `Min` | limits; Min applies except in standby |
| `T.Vorlauf Min Normal` | lower limit in normal mode only – **lower it together with the curve**, otherwise it dominates on mild days |
| `Raumeinfluss` | room influence 0–90 %, needs a room sensor |
| `Einschaltüberhöhung` | start-up boost 0–20 %, after pump standstill, full after 10 h |

**Can be influenced from outside** (input variables): *Offset Vorlaufsolltemp.*,
*Offset Raumsolltemp.*, *Raumsolltemperatur*, *Heizen mit externer VL.Solltemp.* +
*Externe VL.Solltemp.* – e.g. via CoE from Home Assistant.

**Pump shut-off conditions:** room actual > set (normal/setback), **flow set < Min** (factory
default, the most common), flow actual > Max, outdoor average > Max. When a shut-off is active:
pump off, flow set-point = **5 °C**.

**Warning:** `Freigabe Heizkreis` = OFF → **no frost protection**. Never link the *Externer
Schalter* (external switch) to a temperature sensor (can damage the controller).

Output variables include flow set temperature, effective room set temperature, pump, mixer,
operating mode (1 normal, 2 setback, 3 standby, 4 frost protection, 11 external flow set …) and
**Anforderungssolltemp.** (demand set-point, for the heat demand function).

## Heat demand (`Anforderung Heizung`) — [wiki](https://wiki.ta.co.at/Anforderung_Heizung_(Funktion))

- On at *set demand + Diff. Ein* at sensor T.Anf, off at *set shut-off + Diff. Aus* at sensor
  T.Aus (without T.Aus both at T.Anf).
- *Solltemperatur Anforderung* can be the heating circuit's **Anforderungssolltemp.** – then the
  threshold follows the heating curve. With a fixed set-point (e.g. 60 °C, Diff. Ein −15 K) the
  demand comes slightly late in frost: when the buffer top drops below 45 °C, the circuit may
  already ask for 48–50 °C.
- `Sockeltemperatur T.Anf. Min`, `T.Erz. Max` (also cuts off during minimum runtime),
  `Mindestlaufzeit Erzeuger`, *Einmal Laden* (charge once), eco mode (under-supply).
- **With manual/log firing the output starts nothing** – it is just an indicator.

## Charging pump (`Ladepumpe`) — [wiki](https://wiki.ta.co.at/Ladepumpenfunktion)

On when T.Zub (source) > T.Zub.Min, T.Zub is a differential above T.Ref and T.Ref < T.Ref.Max.
Minimum and maximum are input variables. Rule: for T.Zub.Min Diff. Ein > Diff. Aus, for T.Ref.Max
Diff. Ein < Diff. Aus. If the reference sensor sits **mid-tank**, almost the whole tank must
reach the target – with "Aus 0 K" the pump then never stops.

## Solar / solar priority — [solar](https://wiki.ta.co.at/Solarregelung_(Funktion)), [priority](https://wiki.ta.co.at/Solarvorrang_(Funktion))

Solar: collector between Min and Max, collector–reference differential, reference < Max.
Priority: absolute (next tank only when the priority tank is full) or relative (priority timer
with standstill, flush time, runtime, wait time). A solar pump running at night dumps stored heat
through the collector – easy to spot from night-time runtime.

## Legionella protection — [wiki](https://wiki.ta.co.at/Legionellenschutzfunktion)

Starts if the set temperature was not held for the hold time within the interval. If its release
depends on a heat source that does not start by itself (wood), the function fails silently – it
runs but never reaches its target.

## Comparison / logic — [comparison](https://wiki.ta.co.at/Vergleichsfunktion), [logic](https://wiki.ta.co.at/Logikfunktion)

Comparison: A > (B + diff), value A cannot be a user value. Logic: OR, AND, flip-flop (reset
dominant), XOR; set unused inputs to "unbenutzt".

## Heat meter (`Wärmemengenzähler`) — [wiki](https://wiki.ta.co.at/Wärmemengenzähler_(Funktion))

Flow, return, volume flow (also fixed), heat capacity. Without calibration up to ±21 % error at
10 K spread, with calibration ±4.5 %. Meter readings are saved **only hourly**. *Zähler löschen*
and the input variable *Zählerrücksetzung* clear **all** periods.
