# CAN and DL bus design

Sources: TA wiki CAN-Bus, DL-Bus; UVR16x2 mounting manual (datei 1263); device manuals.

## CAN bus

- **Line topology only.** Terminate first and last device ("term"), all others "open". Stubs up
  to ~10 m are tolerated; longer → CAN-RP repeater or CAN-BC2 segment.
- **Max 62 devices**, node numbers 1–62, all at the same bit rate (default 50 kbit/s).

| Bit rate | Max total length |
|---|---|
| 5 kbit/s | 10 km |
| 10 | 5 km |
| 20 | 2.5 km |
| **50 (default)** | **1 km** |
| 125 | 400 m |
| 250 | 200 m |
| 500 | 100 m |

- **Cable:** 2×2 twisted pair, shielded, ≥ 0.5 mm², ≤ 60 pF/m, 120 Ω (e.g. "Unitronic Bus CAN
  2×2×0.5"); twist CAN-H with CAN-L and +12 V with GND. Tolerated without guarantee: KNX
  J-Y(St)Y 2×2×0.8 ≤ 250 m, CAT5 ≤ 150 m with few nodes. Change cable type only behind a repeater.
  Multi-building runs: follow the wiki's shielding/earthing rules, surge protection CAN-ÜS/ÜS2.
- **12 V budget:** load on the CAN 12 V (plus the 24 V output) **≤ 6 W per supplying
  controller**. TA's rules of thumb disagree (2 or 3 powered devices) – add up watts and fit a
  12 V power supply (10/NETZTEIL-12V) when in doubt. CAN-I/O45 and CAN-MTx2 (≤ 200 mA) draw from
  the bus; the C.M.I. ~1.5 W.
- **Node numbers:** factory defaults collide (UVR16x2 1, UVR610/I-O45 32, EZ3 40, BC2 48,
  MTx2 50, C.M.I. 56, UVR67 12) – plan a numbering scheme. **Node 1 sets the date/time for the
  whole bus**; making the C.M.I. node 1 (it syncs via NTP) is TA's recommendation.
- CAN inputs need a timeout (≥ 5 min) and a deliberate value on timeout.

## DL bus

- 2 wires (DL + GND), star or chain. Any cable ≥ 0.75 mm² up to 30 m; shielded up to 100 m. Keep
  ≥ 20 cm from mains trays; never in the same cable as CAN.
- **Each master provides 100 % load.** Sum the loads:

| Device | DL load |
|---|---|
| FTS-DL | 25 % (30 % with pressure sensor) |
| RAS+DL | 20 % (10 % with 12 V) |
| TDI5-DL | 30 % |
| ISE-DL | 30 % |
| PRS0-6DL | 13 % |
| AI5-DL | 11 % |
| GDS-DL, UMV5-DL, LDIM5-DL, power controllers | 10 % |
| RFS-DL (humidity) | 6 % |
| AO4-DL, NME5-DL | 5 % (need 12 V) |
| DPS23-DL | 39 % (15 % if S1–S3 unused) |

- Each value is selected by device address (DIP switches) and **index**; CORA-DL replaces this
  with the device's CORA ID but the load still counts.
- DL is slow: fine for temperatures, humidity, flow for heat metering; not for fresh-water
  stations or switching lights.

## Checklist

- [ ] Node plan written, defaults changed, node 1 decided
- [ ] Bus length vs. bit rate, terminations at both ends only
- [ ] 12 V budget ≤ 6 W per supplying device, PSU where needed
- [ ] DL load ≤ 100 % per master
- [ ] Cable types and routing separate from mains
