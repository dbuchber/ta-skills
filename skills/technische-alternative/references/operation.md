# Operation: user levels, clock, logging, CAN

Sources: [user levels](https://wiki.ta.co.at/Benutzerebenen),
[date and time](https://wiki.ta.co.at/Datum_und_Uhrzeit),
[data logging with Winsol](https://wiki.ta.co.at/Datenloggen_mit_Winsol),
[CAN bus](https://wiki.ta.co.at/CAN-Bus), [C.M.I.](https://wiki.ta.co.at/C.M.I.).

## User levels of x2 controllers

| Level | may, among others |
|---|---|
| Anwender (user) | view values, released fixed values/outputs, date/time, location |
| Fachmann (specialist, password) | parameters of functions, inputs/outputs, CAN/DL; load function data and firmware |
| Experte (expert, password) | everything |

- After loading function data and after every restart: user level.
- 30 minutes after a login the controller returns to the user level.
- Passwords come from the function data. **Do not try default passwords** – ask the operator.
- The C.M.I. has its own HTTP login; the JSON API requires the expert level there.

## Clock

- All CAN devices take date and time from **node 1**. The wiki recommends making the C.M.I.
  node 1, since it gets the time from the network.
- C.M.I.: time source *WEB / CAN / DL1 / DL2*, time zone, DST, **NTP server freely configurable**
  (UDP 123 outbound).
- Experience: after a power outage the C.M.I. lost its time and the configured NTP server (the
  router) did not answer NTP – logging stayed silent for almost two years without any message.
  Use a public pool or a verified local server, and check the clock after every power outage.
- Power reserve of the UVR16x2 clock: about 3 days.

## Logging

- On the controller *CAN-Bus → Datenlogging*: up to 64 analog and 64 digital values. The list
  applies to the controller's SD logging and to CAN logging via the C.M.I.
- On the C.M.I. *Einstellungen → Datenlogging*: interval and "frame" (source = node, data set x2).
- The C.M.I. writes from internal memory to the SD card **once a day**.
- Winsol can delete data on the logger when reading – check the setting.
- Controller SD logging: daily files under `LOG/<year>`, the oldest are deleted when < 50 MB free.

## CAN bus

- Nodes 1–62, default rate 50 kbit/s (max. 1,000 m), a single line, terminated at both ends,
  max. 6 W on the 12 V wire.
- CAN inputs: timeout at least 5 min, then "network error" – choose the substitute value
  deliberately.
- CAN outputs send on change > x, not before the blocking time (≥ 1 s), at the latest after the
  interval (≥ 1 min).
