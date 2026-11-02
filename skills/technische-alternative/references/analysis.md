# Analysing TA systems

Recipes from analysing a system with a log/pellet boiler, stratified buffer tank, hot-water tank,
solar thermal and two mixed heating circuits (data from Home Assistant/InfluxDB, hourly means, two
heating seasons). The numbers are examples; adapt volumes and limits to your system.

## Data sources

- **CoE sensors in HA** arrive irregularly (only on change). Bring them onto a fixed grid before
  calculating (minutes: `resample().max().ffill(limit=…)`, hours: mean with limited
  interpolation). Binary states as share of the hour, not as samples.
- **C.M.I. logging** (SD, Winsol) is the densest source – as long as the clock is right.
- **Time zones:** timestamps floored in local time fail at the autumn DST change
  (`AmbiguousTimeError`); compute in UTC, convert only for display.

## Stored energy

```
E [kWh] = c · V · T   with c = 1.163 Wh/(l·K)
buffer  = 1.163 · V_buffer · (T_top + T_bottom)/2
DHW     = 1.163 · V_dhw · T_middle
```

**Usable** is only what lies above the temperature the consumers still need, e.g. buffer above
35 °C mean, hot water above 45 °C. Every extra degree of headroom adds `1.163 · V` Wh – about
1.7 kWh for 1,500 l.

**Daily draw** = sum of the hourly decreases of the content (increases are heat sources).

## Demand model vs. outdoor temperature

Fit daily draw against daily mean outdoor temperature (heating days only, e.g. < 12 °C) linearly.
Lessons:

- After a renovation (insulation) use **only the days after it**.
- Below 0 °C the draw did not rise further (sun on clear frosty days, thermal mass) – clamp the
  outdoor temperature: `a + b · (20 − max(T, 0))`.
- Base load (hot water + losses) from non-heating days.
- Daily scatter of ±10 kWh is normal; round recommendations to quarter loads.

## Heating curve vs. room temperature

Room temperature against actual flow temperature, split into outdoor temperature classes, only
hours with the pump running. If rooms stay warm at low flow temperature, the curve is too high.
Rooms above the boiler room or next to warm risers are not valid evidence.
Actual flow persistently below set while the buffer is hot → check mixer/hydraulics, not the curve.

## Demand signal vs. firing

For every firing start, record the demand state and the buffer top temperature. Many firings
without demand at a warm buffer mean: refuelled too early. Compare the buffer top at demand-on
with the flow set-point in frost: if it is lower, the demand comes too late.

## Boiler phases from its power draw

A smart plug on the boiler reveals its phases even without a bus connection:

| Power (example) | Phase |
|---|---|
| ~2 W | standby |
| 25–37 W after fan operation | throttled/ember: buffer full, fire waiting |
| 40–55 W | fan, full burn |
| > 100 W | ignition/feeding |

Segment: power > 15 W, bridge gaps < 45 min, burns ≥ 1 h. Throttled phases typically start at a
buffer top of ~80 °C. A high share of throttled burn time means more wood was loaded than the
buffer could take – poor burnout, hot buffer, higher losses.

## Standby losses

Select hours without pump, boiler and solar, plot the hourly decrease of stored energy against
buffer temperature. Example: ~300 W at 50–60 °C, ~940 W at 80–90 °C. This includes tank
insulation, pipes and thermosiphon circulation; uninsulated pipes in the boiler room drive it.
An overcharged buffer thus costs ~10 kWh/day extra.

## Plausibility

- Check value ranges per sensor (one room sensor reported 1,660 °C for months).
- Take sensor corrections from the program export into account.
- Anemometers on analog inputs produce outliers: hourly means, hard limits.
