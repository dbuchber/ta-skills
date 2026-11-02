# C.M.I. JSON-API

Quellen: [TA-Wiki C.M.I. JSON-API](https://wiki.ta.co.at/C.M.I._JSON-API),
[CMI-JSON-API Version 8 (PDF, 2025-10-08)](https://www.ta.co.at/download/datei/1751/).

**Nur lesend.** Antwort ist immer gültiges JSON (UTF-8). Authentifizierung per HTTP-Basic als
Benutzer der Ebene **Experte**.

## Aufruf

```
GET http://<cmi>/INCLUDE/api.cgi?jsonnode=<knoten>&jsonparam=<liste>[&jsondesignation=1]
```

| Parameter | Bedeutung |
|---|---|
| `jsonnode` | CAN-Knoten, dezimal |
| `jsonparam` | kommagetrennt, z. B. `I,O` oder `I1,I2,O3,Sg1`; ohne Nummer alle; **max. 16 Werte je Kürzel** |
| `jsondesignation=1` | liefert Bezeichnungen mit (ab API 8, nur x2-Geräte) |

| Kürzel | Inhalt | Geräte |
|---|---|---|
| `I` / `O` | Eingänge / Ausgänge | UVR1611, x2 |
| `D` | DL-Eingänge | x2 |
| `Sg` `Sd` `St` `Ss` | Systemwerte allgemein, Datum, Zeit, Sonne | x2 |
| `Sp` | elektrische Leistung | CAN-EZ2/EZ3 |
| `Na` / `Nd` | Netzwerkeingänge analog/digital | **nur UVR1611** |
| `M` / `AM` / `AK` | M-Bus / Modbus / KNX | BC2, UVR610 … |
| `La` / `Ld` | Logging-Liste analog/digital | x2 |

**CAN-Eingänge einer UVR16x2 gibt es in der API nicht.** Umweg: in die Logging-Liste aufnehmen
und über `La`/`Ld` lesen.

## Antwort

```json
{"Header":{"Version":8,"Device":"87","Timestamp":1793000000},
 "Data":{"Inputs":[{"Number":1,"AD":"A","Value":{"Value":21.4,"Unit":"1"}}]},
 "Status":"OK","Status code":0}
```

- `Timestamp` ist UNIX-Zeit **mit eingerechneter Zeitzone** des C.M.I., also kein reines UTC.
- `RAS` (Raumfühler-Betriebsart) nur bei Unit 46: 0 Auto, 1 Normal, 2 Abgesenkt, 3 Standby.

| Status code | Bedeutung |
|---|---|
| 0 | OK |
| 1 | NODE ERROR – Knoten nicht verfügbar |
| 2 | FAIL – CAN-Fehler oder Parameter für das Gerät nicht verfügbar |
| 3 | SYNTAX ERROR |
| 4 | **TOO MANY REQUESTS – nur eine Anfrage pro Minute** |
| 5 | DEVICE NOT SUPPORTED |
| 6 | TOO FEW ARGUMENTS |
| 7 | CAN BUSY |

Ob das Limit je C.M.I. oder je Knoten gilt, ist nicht eindeutig dokumentiert – je C.M.I.
annehmen und alle Werte eines Zyklus in **eine** Anfrage packen.

## Geräte-IDs (`Device`)

`87` UVR16x2 · `88` RSM610 · `89` CAN-I/O45 · `8B` CAN-EZ2 · `8C` CAN-MTx2 · `8D` CAN-BC2 ·
`8E` UVR65 · `8F` CAN-EZ3 · `91` UVR610 · `92` UVR67 · `80` UVR1611. Nicht unterstützt u. a.
`8A` C.M.I. selbst, `7F` CoE, `A3` BL-NET.

## API-Version ↔ C.M.I.-Firmware

| API | ab Firmware |
|---|---|
| 1 | 1.25.2 |
| 4 | 1.34.2 |
| 6 | 1.38.1 |
| 7 | 1.42.1 |
| 8 | 1.46.1 |

## Einheiten (`Unit`)

`0` – · `1` °C · `2` W/m² · `3` l/h · `4` s · `5` min · `7` K · `8` % · `10` kW · `11` kWh ·
`12` MWh · `13` V · `14` mA · `15` h · `16` Tage · `17` Imp · `18` kΩ · `19` l · `20` km/h ·
`21` Hz · `22` l/min · `23` bar · `28` m³ · `36` m/s · `38` m³/h · `43` Aus/Ein · `44` Nein/Ja ·
`46` °C (RAS) · `50` € · `54` ° · `60` Uhrzeit · `63` A · `65` mbar · `67` ppm · `69` W ·
`71` kg · `75` lx · `77` ct/kWh · `78` offen/geschlossen.

## Beispiel ohne Geheimnis in argv

```bash
printf 'user = "%s:%s"\n' "$CMI_USER" "$CMI_PASSWORD" |
  curl -s --config - "http://$CMI_HOST/INCLUDE/api.cgi?jsonnode=1&jsonparam=I,O&jsondesignation=1"
```
