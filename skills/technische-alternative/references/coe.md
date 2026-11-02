# CoE – CAN over Ethernet

Quellen: [TA-Wiki CoE](https://wiki.ta.co.at/CAN_over_Ethernet_(CoE)),
[CMI-Zusatzanleitung CoE (PDF)](https://www.ta.co.at/download/datei/826/),
[CMI-Portfreigabe](https://wiki.ta.co.at/CMI-Portfreigabe).

## Was TA dokumentiert

- CoE überträgt CAN-Netzwerkwerte (analog, digital) per **UDP** von einem C.M.I. zu einem anderen.
- **UDP 5441 = CoE V1** (2 Byte, ±32 767), **UDP 5442 = CoE V2** (4 Byte), V2 ab C.M.I. 1.43.1.
  Ab 1.43.1 empfängt ein C.M.I. beide, sendet standardmäßig V2. Ältere Empfänger brauchen V1.
- Sender: C.M.I. *Einstellungen → Ausgänge → CoE*: Quelle, Ziel-IP, **virtueller Knoten**,
  Nummer des Netzwerkausgangs.
- Empfänger braucht eine **feste IP**. Er bekommt den virtuellen Knoten zusätzlich zur eigenen
  Knotennummer – die Nummer darf im Empfänger-CAN nicht belegt sein.
- Analoge Werte gehen in **Blöcken zu 4**, digitale in **2 Blöcken zu 16**. Senden zwei Quellen
  über denselben virtuellen Knoten in denselben Block, setzen sie sich gegenseitig auf 0/AUS.
- Kein Acknowledge: Was verloren geht, merkt niemand.

## Home Assistant als Gegenstelle

Gängig ist die HACS-Integration **`ta_coe`** mit dem App „CoE to HTTP server“ (Drittanbieter,
nicht von TA).

**UVR → HA:** In TAPPS2 bzw. am Regler CAN-Ausgänge anlegen, Ziel ist der virtuelle Knoten der
Integration; am C.M.I. CoE-Ausgang mit der IP von HA. In HA erscheinen sie als
`sensor.coe_analog_<knoten>_<nr>` / `binary_sensor.coe_digital_<knoten>_<nr>`.

- Die UVR sendet nur **bei Änderung > x**, frühestens nach **Blockierzeit**, spätestens nach
  **Intervall** (min. 1 min). Ein Sensor, der sich selten ändert, steht in HA lange still – das
  ist kein Ausfall. Für Auswertungen zeitgewichtet mitteln, nicht Stichproben zählen.
- Sollwerte (Vorlaufsoll, Anforderungssoll) als eigene CAN-Ausgänge freigeben – sie sind für
  Auswertungen wertvoller als jede Ableitung.

**HA → UVR:** HA schickt UDP an das C.M.I., das C.M.I. stellt die Werte unter einem virtuellen
Knoten auf den CAN-Bus, die UVR liest sie als **CAN-Eingang** (Knoten = virtueller Knoten,
Nummer = Netzwerkausgang). Pflicht dabei:

- **Timeout** (min. 5 min) und **Wert bei Timeout** setzen – sonst bleibt bei einem HA-Ausfall
  der letzte Wert ewig stehen.
- Nur in **Eingangsvariablen** einspeisen (z. B. *Offset Vorlaufsolltemp.*,
  *Raumsolltemperatur*, *Externe VL.Solltemp.*); Parameter lassen sich nicht verknüpfen.
- Plausibilität am Regler begrenzen (T.Vorlauf Max bleibt dominant).

## Paketformat

Offiziell nicht veröffentlicht. Drittquelle für V2: Rust-Crate
[`coe`](https://docs.rs/crate/coe/0.2.1) – 4-Byte-Kopf (Version, Länge, Anzahl), bis 31
Nutzlasten à 8 Byte (Knoten, Ausgangsindex 0-basiert, Typ, Unit-ID, Wert int32 LE). Dezimalstellen
ergeben sich aus der Unit-ID.

## Ports des C.M.I.

Eingehend lokal: 80 HTTP, 502 Modbus TCP, 5441/5442 CoE. Ausgehend: 53 DNS, 80 Update-Prüfung,
**123/UDP NTP** (Zeitquelle WEB), 40001–40003 Webportal, Mail, Online-Logging. Eingehend aus dem
Internet wird nichts gebraucht.
