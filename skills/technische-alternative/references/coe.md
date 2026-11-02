# CoE – CAN over Ethernet

Sources: [TA wiki CoE](https://wiki.ta.co.at/CAN_over_Ethernet_(CoE)),
[C.M.I. supplementary manual CoE (PDF)](https://www.ta.co.at/download/datei/826/),
[C.M.I. port sharing](https://wiki.ta.co.at/CMI-Portfreigabe).

## What TA documents

- CoE transfers CAN network values (analog, digital) via **UDP** from one C.M.I. to another.
- **UDP 5441 = CoE V1** (2 bytes, ±32,767), **UDP 5442 = CoE V2** (4 bytes), V2 from C.M.I. 1.43.1.
  From 1.43.1 a C.M.I. receives both and sends V2 by default; older receivers need V1.
- Sender: C.M.I. *Einstellungen → Ausgänge → CoE* (settings → outputs → CoE): source, target IP,
  **virtual node**, number of the network output.
- The receiver needs a **static IP**. It gets the virtual node in addition to its own node number –
  that number must not be in use on the receiving CAN bus.
- Analog values travel in **blocks of 4**, digital ones in **2 blocks of 16**. If two sources use
  the same virtual node and block, they reset each other's values to 0/OFF.
- No acknowledge: nobody notices a lost packet.

## Home Assistant as the counterpart

Common choice: the HACS integration **`ta_coe`** with the app "CoE to HTTP server" (third party,
not by TA).

**Controller → HA:** create CAN outputs in TAPPS2 or on the controller, targeting the virtual node
of the integration; on the C.M.I. a CoE output with Home Assistant's IP. In HA they appear as
`sensor.coe_analog_<node>_<nr>` / `binary_sensor.coe_digital_<node>_<nr>`.

- The controller sends only **on change > x**, not before the **blocking time**, at the latest
  after the **interval** (min. 1 min). A value that rarely changes stands still in HA for a long
  time – that is not an outage. For analysis, average time-weighted rather than counting samples.
- Publish set-points (flow set-point, demand set-point) as CAN outputs of their own – they are
  worth more for analysis than any derivation.

**HA → controller:** HA sends UDP to the C.M.I., the C.M.I. puts the values on the CAN bus under a
virtual node, and the controller reads them as a **CAN input** (node = virtual node, number =
network output). Mandatory:

- Set a **timeout** (min. 5 min) and a **value on timeout** – otherwise an HA outage freezes the
  last value forever.
- Feed only **input variables** (e.g. *Offset Vorlaufsolltemp.*, *Raumsolltemperatur*,
  *Externe VL.Solltemp.*); parameters cannot be linked.
- Limit plausibility on the controller (`T.Vorlauf Max` stays dominant).

## Packet format

Not published by TA. Third-party source for V2: Rust crate
[`coe`](https://docs.rs/crate/coe/0.2.1) – 4-byte header (version, length, count), up to 31
payloads of 8 bytes (node, 0-based output index, type, unit ID, int32 LE value). Decimal places
follow from the unit ID.

## C.M.I. ports

Inbound, local: 80 HTTP, 502 Modbus TCP, 5441/5442 CoE. Outbound: 53 DNS, 80 update check,
**123/UDP NTP** (time source WEB), 40001–40003 web portal, mail, online logging. Nothing inbound
from the internet is needed.
