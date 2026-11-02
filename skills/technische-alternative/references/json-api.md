# C.M.I. JSON API

Sources: [TA wiki C.M.I. JSON-API](https://wiki.ta.co.at/C.M.I._JSON-API),
[CMI-JSON-API version 8 (PDF, 2025-10-08)](https://www.ta.co.at/download/datei/1751/).

**Read only.** The response is always valid JSON (UTF-8). Authentication is HTTP Basic as a user
with level **Experte** (expert).

## Request

```
GET http://<cmi>/INCLUDE/api.cgi?jsonnode=<node>&jsonparam=<list>[&jsondesignation=1]
```

| Parameter | Meaning |
|---|---|
| `jsonnode` | CAN node, decimal |
| `jsonparam` | comma-separated, e.g. `I,O` or `I1,I2,O3,Sg1`; without a number all values; **max. 16 values per code** |
| `jsondesignation=1` | include designations (API 8+, x2 devices only) |

| Code | Content | Devices |
|---|---|---|
| `I` / `O` | inputs / outputs | UVR1611, x2 |
| `D` | DL inputs | x2 |
| `Sg` `Sd` `St` `Ss` | system values general, date, time, sun | x2 |
| `Sp` | electrical power | CAN-EZ2/EZ3 |
| `Na` / `Nd` | network inputs analog/digital | **UVR1611 only** |
| `M` / `AM` / `AK` | M-Bus / Modbus / KNX | BC2, UVR610 … |
| `La` / `Ld` | logging list analog/digital | x2 |

**The API does not expose CAN inputs of a UVR16x2.** Workaround: add them to the logging list and
read `La`/`Ld`.

## Response

```json
{"Header":{"Version":8,"Device":"87","Timestamp":1793000000},
 "Data":{"Inputs":[{"Number":1,"AD":"A","Value":{"Value":21.4,"Unit":"1"}}]},
 "Status":"OK","Status code":0}
```

- `Timestamp` is UNIX time **with the C.M.I.'s time zone applied** – not plain UTC.
- `RAS` (room sensor mode) only with unit 46: 0 auto, 1 normal, 2 setback, 3 standby.

| Status code | Meaning |
|---|---|
| 0 | OK |
| 1 | NODE ERROR – node not available |
| 2 | FAIL – CAN error or parameter not available for this device |
| 3 | SYNTAX ERROR |
| 4 | **TOO MANY REQUESTS – only one request per minute** |
| 5 | DEVICE NOT SUPPORTED |
| 6 | TOO FEW ARGUMENTS |
| 7 | CAN BUSY |

Whether the limit applies per C.M.I. or per node is not clearly documented – assume per C.M.I. and
put all values of a cycle into **one** request.

## Device IDs (`Device`)

`87` UVR16x2 · `88` RSM610 · `89` CAN-I/O45 · `8B` CAN-EZ2 · `8C` CAN-MTx2 · `8D` CAN-BC2 ·
`8E` UVR65 · `8F` CAN-EZ3 · `91` UVR610 · `92` UVR67 · `80` UVR1611. Not supported, among others:
`8A` the C.M.I. itself, `7F` CoE, `A3` BL-NET.

## API version ↔ C.M.I. firmware

| API | from firmware |
|---|---|
| 1 | 1.25.2 |
| 4 | 1.34.2 |
| 6 | 1.38.1 |
| 7 | 1.42.1 |
| 8 | 1.46.1 |

## Units (`Unit`)

`0` – · `1` °C · `2` W/m² · `3` l/h · `4` s · `5` min · `7` K · `8` % · `10` kW · `11` kWh ·
`12` MWh · `13` V · `14` mA · `15` h · `16` days · `17` imp · `18` kΩ · `19` l · `20` km/h ·
`21` Hz · `22` l/min · `23` bar · `28` m³ · `36` m/s · `38` m³/h · `43` off/on · `44` no/yes ·
`46` °C (RAS) · `50` € · `54` ° · `60` time of day · `63` A · `65` mbar · `67` ppm · `69` W ·
`71` kg · `75` lx · `77` ct/kWh · `78` open/closed.

## Example without a secret in argv

```bash
printf 'user = "%s:%s"\n' "$CMI_USER" "$CMI_PASSWORD" |
  curl -s --config - "http://$CMI_HOST/INCLUDE/api.cgi?jsonnode=1&jsonparam=I,O&jsondesignation=1"
```
