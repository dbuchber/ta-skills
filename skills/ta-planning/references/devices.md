# Device selection data

Sources: TA catalogue 2026, price list 2026 (status 15 Oct 2026), manuals (datei IDs in
[catalog.md](catalog.md)), TA wiki. List prices EUR excl. VAT – check the current price list.

## Comparison

| | UVR16x2 | UVR610 | UVR67 | CAN-I/O45 |
|---|---|---|---|---|
| Inputs | 16 | 6 | 6 | 4 |
| Outputs | 16 (11 relay, 5 analog) | 10 (6 relay, 4 analog) | 7 (5 relay, 2 analog) | 5 (3 relay, 2 analog) |
| Relay load | 230 V / 1.5 A each, common fuse 6.3 A | 1.5 A each, 6 A total | 2.5 A ohmic each | 3 A each, fuse 3.15 A |
| Programming | 128 functions | 128 functions (43 types) | >800 fixed programs | **44 functions** |
| Display | 4.3" touch (except -E-NP) | display + knob (except -OD) | display | none |
| Own supply | 100–230 V | 100–230 V | 100–230 V | **from CAN 12 V** (mains only for relays) |
| Extras | CORA-DL, SD, 24 V/12 V out | M-Bus 4 meters or Modbus RTU (-MODB), CORA-F, micro-SD | micro-SD logging | – |
| List price (example) | 01/UVR16X2K €655 | 01/UVR610S €329 | 01/UVR67 €219 | €169 |

## UVR16x2

- **Inputs 1–16:** PT1000, KTY, PT100/500, Ni1000, NTC/PTC, RAS/RASPT, GBS01, RFS, RES01,
  0–3.3 V, resistance, digital. 1–14 impulses ≤ 10 Hz, **15–16 ≤ 20 Hz** (VIG, S0).
  Input 7: 0–10 V; input 8: 0–10 V or 4–20 mA.
- **Outputs:** A1–A4, A6–A11 relays; A5 potential-free changeover; A12–A16 0–10 V (20 mA) or PWM
  10 V/1 kHz, switchable via auxiliary relays; A16 can supply external sensors.
- **Output pairs (3-point mixers):** 1/2, 3/4, 6/7, 8/9, 10/11 without extras; 12/13 and 14/15 with
  auxiliary relays; 1/2 and 6/7 only on the relay version.
- Supply 100–230 V, 3–4.5 W; 12/24 V out **max 6 W total**; DL bus 100 %.
- Limits: 64 fixed values; 64+64 CAN inputs; 32+32 CAN outputs; 32 DL inputs; logging 64+64.
- Variants: -K (wall console), -S (panel/DIN rail), -K-DC/-S-DC (24 V DC), -S-DE (remote display),
  -E-DE / -E-DE-I (PCB with display, -I with 2 current sensors), -E-NP / -E-NP-I (PCB without
  display, operated via another x2, CAN-MTx2 or C.M.I.). Triac version (speed control of old
  pumps) is in the catalogue, not in the 2026 price list.

## UVR610

- Inputs: 6 (input 2 ≤ 20 Hz; 5–6 0–10 V; on -OD 3–6 0–10 V).
- Outputs: A1–A5 relays, A6 potential-free changeover, A7–A10 0–10 V/PWM (or relays via HIREL22).
- 100–230 V, 1–1.9 W; 24 V output shares the 6 W budget. M-Bus (4 meters) or Modbus RTU (-MODB).
- Variants: S, S-OD, S-DC, S-MODB, S-OD-MODB, K, K-OD. -OD is meant as an extension, programmed via
  CAN. No TA-Designer visualisation on the device.
- Up to 16 PMG1 pump-mixer groups via CORA radio (10 via cable) – "9+ heating circuits".

## UVR67 (fixed programs; replaces UVR65)

6 inputs (input 6 ≤ 20 Hz), 7 outputs (A1, A2, A4, A5 relays; A3 changeover; A6/A7 0–10 V/PWM,
100 steps). Full CAN access, DL 100 %, micro-SD. Sensor cable ≤ 50 m at 0.5 mm², load cable ≤ 30 m
at 0.75 mm². Sets with sensor packs: -3/-4 solar, -H/-HU heating circuit, -GT building drying.

## Extensions and interfaces

| Device | Key data | Use |
|---|---|---|
| **CAN-I/O45** | 4 in, 5 out, 44 functions, powered from CAN 12 V | cheap remote I/O |
| **CAN-EZ3** | 3-phase power (KCT current sensors 50/100/400 A, extra), 4 inputs + 2 FTS slots, S0 out, Modbus RTU, CORA, 128 functions | PV surplus, load management, heating rods |
| **CAN-BC2** | 2 isolated CAN sides, DL, M-Bus 4 meters; one add-on: MD-KNX (64/64) or MD-MODB (Modbus RTU 64/64 + 4 meters); 22 functions; 12 V only from feeding side | Modbus/KNX/M-Bus, network separation |
| **CAN-MTx2** | 4.3" touch, room T/RH/dew point/pressure (-CO2: CO₂), 128 functions, no outputs, ≤ 200 mA from CAN | operating panel, room sensor |
| **C.M.I.** | Ethernet gateway: portal/app, Winsol/online logging, e-mail alerts, Modbus TCP, JSON API, CoE; 1.5 W from CAN or 12 V PSU; variants CMI, CMI-NT (with PSU), CMI-S (cabinet, no DL) | remote access, logging, Home Assistant |
| **CAN-RP** | repeater, isolated, no node number, does not pass 12 V | long stubs, segments |
| **DL modules** | AI5-DL (5× 0–10 V in), AO4-DL (4× 0–10 V/PWM out), TDI5-DL (5 PT1000/digital), RM2-DL (2 relays 5 A, no mixer pair) | a few extra signals |

## CORA (TA radio/2-wire)

CORA-DL (cable on DL terminals) and CORA-F (868 MHz). Devices: CORA-HKT radiator thermostat,
AFS216 (14 thermal-actuator outputs), SPP22 socket, PMG1 pump-mixer group (needs a CORA-capable x2
device), heating rods, RAS-CT4. Not a replacement for CAN; not compatible with the old RAS-F/
GBS-F/RCV-DL radio. Minimum firmware for CORA-DL: UVR16x2 1.43, UVR610 1.09, CAN-EZ3 1.08.

## Third-party buses

| Bus | Device |
|---|---|
| Modbus TCP | C.M.I. |
| Modbus RTU | CAN-BC2 + MD-MODB, UVR610-MODB, CAN-EZ3 |
| M-Bus | UVR610 (4), CAN-BC2 (4 + 4) |
| KNX | CAN-BC2 + MD-KNX |
| Home Assistant | C.M.I. via CoE (HACS `ta_coe`) or JSON API (read only, 1 request/min) |

Manufacturer-specific boiler/heat-pump buses are not supported – integrate via 0–10 V/PWM,
Modbus, KNX, SG-Ready or potential-free contacts.

## Discontinued → replacement

UVR1611 → UVR16x2 · RSM610 → UVR610 · UVR65/UVR63 → UVR67 · CAN-I/O35/44 → CAN-I/O45 ·
CAN-MT → CAN-MTx2 · BL-NET/D-LOGG → C.M.I. · CAN-BC → CAN-BC2 · CAN-EZ → CAN-EZ3.
