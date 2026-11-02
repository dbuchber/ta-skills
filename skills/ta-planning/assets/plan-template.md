# Control plan: <project>

**Status:** <date> · **Planner:** <name> · **Sources checked:** price list <date>, catalogue <year>

## 1. System

- Location: <country / state>
- Heat sources: …
- Storage: buffer <l>, DHW <l / fresh-water station>
- Heating circuits: <n>, radiators / floor, mixed / direct
- Solar: <m²>, consumers, priority
- Extras: …
- Remote access / smart home: …
- Hydraulic scheme: <reference or sketch>

## 2. I/O list

| # | Signal | Type | Location | Cable length | Device / terminal |
|---|---|---|---|---|---|
| In 1 | … | PT1000 | … | … m | UVR16x2 / I1 |
| Out 1 | … | relay / pair / 0–10 V / PWM / potential-free | … | … | … |

Inputs used <n> of <n>, outputs <n> of <n>, reserve <%>.

## 3. Devices

| Device | Why | Node | Supply |
|---|---|---|---|

## 4. Bus

- CAN: nodes, length, bit rate, terminations, 12 V budget <W> of 6 W
- DL: devices and load <%> of 100 %

## 5. Bill of materials

| Article no. | Description | Qty | List price € | Datasheet | Note |
|---|---|---|---|---|---|

Third-party items (pumps, mixer motors, cables, enclosure, surge protection): …

## 6. Functions and starting values

| Function | Task | Inputs/outputs | Starting values | Reason |
|---|---|---|---|---|

## 7. Regulations and funding

| Step | Document | Edition | Who |
|---|---|---|---|

## 8. Commissioning and handover

- [ ] Every sensor plausible, outputs tested in manual mode
- [ ] CAN node list, clock/NTP on the C.M.I., logging running
- [ ] Program `.dat` versioned + text export, passwords handed over separately
- [ ] Acceptance/inspection documents, electrical test report

## Open points

- …
