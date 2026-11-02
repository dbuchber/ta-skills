# TAPPS2: changing and transferring function data

Sources: [TA wiki TAPPS2](https://wiki.ta.co.at/TAPPS2),
[Programming with TAPPS2](https://wiki.ta.co.at/Programmieren_mit_TAPPS2),
[Function data](https://wiki.ta.co.at/Funktionsdaten),
[UVR16x2 programming, general notes (PDF)](https://www.ta.co.at/download/datei/1260),
[TAPPS2 manual (PDF)](https://www.ta.co.at/download/datei/1579/).

## Files

| File | What | Read by |
|---|---|---|
| `.tdw` | TAPPS2 drawing with layout and comments | TAPPS2 only |
| `.dat` | function data | the controller |
| `.txt` | documentation (*Datei → Exportieren → Dokumentation*) | humans and diff |
| `.x2d` | function overview (TA-Designer) | controller display |

A `.dat` can be imported but loses its layout – keep the `.tdw`. TAPPS2 refuses to export when
the program has errors (e.g. a duplicate CAN input).

## Keeping versions

One `.dat` per program version (`Plant_V2.1.dat`, `Plant_V2.2.dat`), next to it the text export and
a short change note (date, author, what and why). The text export is the only diffable form;
keep it in Git.

## Changing a program

1. **Back up the device state.** On the controller *Datenverwaltung → Speichern…* (to SD) or via
   C.M.I. *Datenverwaltung* (data administration): download the node's function data. This also
   captures values changed on the device since the last transfer.
2. Open the last transferred `.tdw`/`.dat` and **save it as a new version right away**.
3. Carry over values tried out on the device – whatever is not in TAPPS2 is gone after transfer.
4. Check: simulator (x2-Simulator ≥ 1.38) and diff the text export against the previous version.
5. *Datei → Exportieren → Funktionsdaten*.
6. Transfer: C.M.I. *Datenverwaltung* (upload file, send to node) or SD card on the controller.
   The Fachmann/Experte password **of the target device** is required.
7. Answer the prompts: meter readings of outputs and functions, heat meter calibration values,
   CORA pairing, CAN node number – after a program change usually **retain**.
8. Afterwards: version/file name on the device, `CHANGE.LOG` on the SD card, function status,
   set-points.

## What loading does

- The controller first writes **`_Backup.dat`** with the old state to the SD card.
- All parameters and fixed values come from the new `.dat`; the only exceptions are the meters,
  calibration values and pairings asked about.
- Afterwards the controller is at the **user level**, and the passwords from the `.dat` apply.
- Every change on the controller is logged with a timestamp in `CHANGE.LOG` on the SD card.
- **Total reset** erases the whole program (node number and bus rate stay). Restoring factory
  firmware (hold reset while powering on until the beep ends) triggers it as well.

## Firmware

Free at ta.co.at/download/firmware. UVR16x2, UVR610, CAN-MTx2, C.M.I. via SD card, other devices
via CAN. Read the "please read before download" notes – intermediate versions are sometimes
required. **C.M.I. reset button:** short until the LEDs run = factory reset; held until the end of
the LED chase = firmware update from SD.
