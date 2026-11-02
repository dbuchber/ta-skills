# Worked example: log/pellet boiler, buffer, DHW, solar, two mixed circuits

A real single-family house in Austria (anonymised), renovated: combined log/pellet boiler,
1,500 l stratified buffer, 800 l DHW tank, solar thermal with priority to the DHW tank, a wood
cooking stove with water jacket via return-flow boost, two mixed radiator circuits plus one
direct circuit, weather station. Controller UVR16x2 with C.M.I. and Home Assistant via CoE.
The plan below is the **as-built** state with the lessons learned marked **→**.

## I/O list

| In | Signal | Type | | Out | Signal | Type |
|---|---|---|---|---|---|---|
| 1 | flow circuit 1 | PT1000 | | 1 | pump circuit 1 | relay |
| 2 | flow circuit 2 | PT1000 | | 2 | pump circuit 2 | relay |
| 3 | solar flow | PT1000 | | 3/4 | mixer circuit 1 | relay pair |
| 4 | solar return | PT1000 | | 5 | boiler demand | **potential-free** relay |
| 5 | circulation / stove return | PT1000 | | 6 | solar pump | relay |
| 6–8 | – (reserve) | | | 7 | DHW charging pump | relay |
| 9 | DHW tank (middle) | PT1000 | | 8/9 | mixer circuit 2 | relay pair |
| 10 | buffer bottom | PT1000 | | 10 | solar valve (DHW/buffer) | relay |
| 11 | buffer top | PT1000 | | 11 | – (reserve) | |
| 12 | outdoor | PT1000 | | 12 | return-flow boost pump | analog → switched |
| 13 | collector | KFPT1000 | | 13 | pump circuit 3 | analog → switched |
| 14 | irradiation | GBS01 | | 14 | yard light | analog → switched |
| 15 | wind | impulse (20 Hz input) | | 15–16 | – (reserve) | |
| 16 | rain | RES01 | | | | |
| DL 1 | room sensor living room | RAS+DL | | | | |

Used: 13 of 16 inputs (+1 DL), 13 of 16 outputs.

**→ Lessons**
- **Buffer middle sensor missing.** With only top and bottom, stored energy and "how full" are
  estimates; plan three heights (top/middle/bottom) on any buffer.
- **DHW sensor in the tank middle** as the charging reference means almost the whole tank must
  reach the target – with a "0 K off" differential the pump never stops. Plan a top sensor for
  DHW comfort and use the middle one deliberately.
- **No heat meter on the boiler.** Boiler output had to be derived from storage temperatures.
  An FTS-DL heat meter in the boiler circuit costs ~€130 and makes efficiency measurable.
- **No sensor in the boiler room**, uninsulated pipes: standby losses were large (≈ 940 W at
  80–90 °C buffer) and could only be estimated.
- **Reference room sensor** (DL 1) was faulty for months (~1,660 °C) – plan a plausibility check.
- **Boiler power draw** measured via a smart plug revealed burn/throttle phases; a cheap addition
  where the boiler has no bus.

## Devices and bus

- UVR16x2K, C.M.I. (gateway, logging, CoE to Home Assistant). One CAN segment, two devices, terminations at both ends, 12 V budget well below 6 W.
- **→** The C.M.I. lost its clock after a power outage and its NTP server did not answer: no
  logging for almost two years. Set a working NTP server at commissioning and check it.

## Functions (program V2.x)

Heating circuit 1 and 2 (curve 40 °C at +10 °C / 55 °C at −20 °C, later lowered in 2 K steps),
heat demand (buffer top < 45 °C on / > 80 °C off – with manual firing only an indicator), DHW
charging pump, solar 1 (DHW, priority) and solar 2 (buffer), solar priority, legionella
protection, heat meter solar, comparison for return-flow boost, logic for the circuit release.

**→** The original curve was set before the renovation; after insulation the rooms stayed warm at
30–35 °C flow. Plan curves for the renovated building and keep a reference room sensor to tune
them.

## Regulations touched (Austria, Upper Austria)

Wood boiler acceptance before first operation and recurring inspection (Oö. LuftREnTG), boiler
room (OIB-RL 2, ÖNORM H 5170), DHW hygiene (ÖNORM B 1921), solar (ÖNORM H 7777), filling water
(ÖNORM H 5195-1), electrical connection by an electrician (OVE E 8101). See [austria.md](austria.md).
