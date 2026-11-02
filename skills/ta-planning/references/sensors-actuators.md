# Sensors, actuators and accessories

Sources: TA catalogue 2026, sensor datasheet (datei 1127), UVR16x2/UVR67 manuals, TA wiki.

## Temperature sensors

**PT1000 (class B) is TA's standard.** KTY is the old standard, still sold for existing systems –
do not mix types without setting each input accordingly.

| Sensor | Location | Range |
|---|---|---|
| KFPT1000 | collector (silicone cable, junction box with surge protection) | −50…240 °C, briefly 260 °C |
| KEPT1000 | boiler | 0…160 °C, briefly 180 °C |
| BFPT1000 | storage tank, DHW, flow (6×20 mm) | 0…90 °C, briefly 100 °C |
| BFPT1000 4×35 / 5×60 | high temperature / ball valve KH for heat metering | up to 240 °C |
| MSP60/130 | ultra-fast: MSP130 fresh-water/DHW, MSP60 heat metering | – |
| AUSPT | outdoor (north side, no sun, no exhaust air) | −30…50 °C |
| THEL | thermocouple type K up to 600 °C (flue gas) via UMV5-DL | – |

**Immersion sleeves (TH):** inner Ø 6 mm, ½" thread, lengths 40/60/90/140/200/300 mm, brass or
stainless (e.g. 01/TH140). Buffer tanks: one sleeve per measuring height, long enough to reach
the water, not the insulation. Contact sensors on pipes only with heat-conducting paste and
insulation over the sensor.

**Cables:** 0.5 mm² up to 50 m (≈ +1 K error with PT1000), more cross-section for longer runs.
Never in the same cable as mains; ≥ 5 cm apart if unshielded.

## Room sensors

| Sensor | Connection | Notes |
|---|---|---|
| RASPT | analog input | temperature, ±4 K knob, mode switch (encoded as offset) |
| RAS+DL | DL bus (20 %, 10 % with 12 V) | temperature, humidity, dew point, mode, ±4 K |
| RAS-CT4 | CORA, 230 V or 12 V | 4" touch, up to 3 functions of the parent controller |
| CAN-MTx2 | CAN | panel with room T/RH/pressure (CO₂ variant) |

A room sensor in a reference room is cheap and makes heating-curve tuning measurable; it is also
needed for room influence.

## Flow, energy, pressure, weather

- **FTS-DL** (vortex, DL 25 %): FTS2-32 (DN10), 4-50 (DN15), 5-85 (DN20), 9-150 (DN25), 14-240
  (DN32, x2 only); −40…125 °C; flow + temperature, optional second PT1000 and pressure sensor.
  **Not for fresh-water stations** – the DL bus is too slow.
- **VIG** impeller impulse sensors, 0.5 l/impulse, potential-free; needs ≥ 20 cm straight pipe.
  Use the 20 Hz inputs (UVR16x2 15–16, UVR610 2, UVR67 6).
- Heat-meter sets: WMZ-SET (FTS + 2 ball valves + fast sensor), EZ4-50/EZ5-85 for CAN-EZ3.
- Pressure: PRS0-6DL (0–6 bar, DL 13 %), DPS23-DL differential pressure.
- Weather: GBS01 irradiation (analog), RES01 rain, WIS01 wind (impulse).
- Flow switches: STS01DC (controller input), STS03AC (230 V, for high-efficiency pumps).

## Pumps

- **High-efficiency pumps:** speed via **0–10 V or PWM** analog outputs (10 V, 1 kHz). Configure
  the output **scaling**: "solar mode" 0–100 % or inverse "heating mode" 100–0 %, with min/max from
  the pump datasheet. TA has **no library of pump profiles** – whether a pump takes PWM, and which
  profile, comes from the pump manufacturer. Accessories: UPM3 signal cable, APC (0–10 V → PWM),
  PFSC (isolated PWM/0–10 V).
- **Old asynchronous pumps:** triac outputs (UVR16x2 triac version) – check availability.
- Switching only: relay output (UVR16x2/UVR610 1.5 A per relay) – compare with the pump's rated
  and inrush current from its datasheet; use a contactor or HIREL-PF where in doubt.

## Mixers and relays

- TA sells no mixer motors (except PMG1). Third-party 3-point motors on an **output pair**;
  0–10 V actuators on an analog output.
- Auxiliary relays: HIREL22 (2 relays from 2 analog outputs, optionally potential-free),
  HIREL-230V (UVR16x2K console), HIREL-PF (potential-free, 230 V/3 A), RM2-DL (2 relays via DL, 5 A,
  **cannot drive a mixer pair**).
- **Boiler demand:** use a **potential-free** contact (A5 on the UVR16x2, A6 on the UVR610, A3 on
  the UVR67, or HIREL-PF) – never put controller mains onto a boiler's demand input.

## Sensor packs

GP1PT–GP4PT, EP1PT (GP3PT fits the UVR16x2 "factory setting" example, GP4PT the UVR610).
UVR67 sets include matching sensors.
