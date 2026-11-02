# C.M.I.-Menü: die UVR im Browser bedienen

Das C.M.I. zeigt das Menü jedes x2-Knotens als Webseite – dieselben Seiten wie am Display.
Damit lassen sich Parameter lesen und, nach Login als Fachmann oder Experte, ändern.

> **Beobachtet, nicht dokumentiert.** Die Adressen unten stammen aus der Weboberfläche eines
> C.M.I. mit Firmware 1.48.1 an einer UVR16x2 (November 2026). TA beschreibt dieses Protokoll
> nicht; mit anderer Firmware kann es abweichen. Vor jeder Schreibaktion die Seite lesen und
> prüfen, dass Bezeichnung und alter Wert stimmen.

## Adressen

Alle Adressen sind Hex-Strings; die ersten zwei Zeichen sind der CAN-Knoten (`0F` = 15).

| Zweck | Aufruf |
|---|---|
| Knotenliste | `GET /can_knoten.cgi?node=<n>` → Link `menupagex.cgi?nodex2=<KK>005800` |
| Seite laden | `GET /INCLUDE/devpagex.cgi?pagex2=<adresse>` (HTML-Fragment) |
| Hauptmenü | `<KK>005800` – darin u. a. Funktionen `<kk>055800`, Eingänge `<kk>025800`, Fixwerte `<kk>035800` |
| Funktion *n* | `<kk><ff>5c07` mit `ff` = n − 1 (hex); Reiter `…5c01`, `…5c03`, `…5c05`, `…5c07`, `…5c0a` |
| Unterseite | z. B. Heizkurve eines Heizkreises `<kk><ff>5c11` |
| Wert-Dialog | `GET /INCLUDE/changerx2.cgi?sadrx2=<wert-adresse>` → verstecktes Feld `changeadrx2`, Min/Max, aktueller Wert |
| **Schreiben** | `GET /INCLUDE/change.cgi?changeadrx2=<changeadr>&changetox2=<wert>` (Dezimalpunkt, z. B. `38.0`) |
| Login Ebene | `GET /INCLUDE/devpagexUser.cgi?changeuserx2=<kk>0157ff<passwort>` (Fachmann) bzw. `<kk>0257ff` (Experte) |

- Werte stehen im HTML als `<div class="VALUE_B">Bezeichnung</div><div class="VALUE_C" adresse="…">Wert</div>`.
- Die Login-Antwort beginnt mit der Ebene (`1`, `2`) und einem Hex-Token; der Browser legt sie
  als Cookie **`canremote<knoten>`** ab. Ohne dieses Cookie zeigen Parameterseiten nur die
  Ebenenauswahl.
- Zusätzlich gilt das HTTP-Basic-Login des C.M.I. selbst.
- Die UVR kehrt 30 min nach dem Login in die Anwenderebene zurück.

## Ablauf einer Änderung

1. Seite lesen, Bezeichnung und alten Wert prüfen.
2. Wert-Dialog lesen: `changeadrx2`, erlaubter Bereich, aktueller Wert.
3. Nur wenn der aktuelle Wert dem erwarteten entspricht: schreiben.
4. 5–10 s warten, Dialog erneut lesen, neuen Wert vergleichen.
5. Wirkung an einer Ausgangsvariablen prüfen (z. B. Vorlaufsolltemperatur per CoE).
6. Cookie verwerfen.

[`scripts/cmi_menu.py`](../scripts/cmi_menu.py) macht genau das.

## Belastbarkeit

Der Webserver des C.M.I. ist schwach. Beobachtet: Nach fünf bis zehn Abrufen innerhalb einer
Minute war das C.M.I. zweimal **5 bzw. 20 Minuten** nicht erreichbar; CoE und Regelung liefen
weiter. Deshalb:

- ≥ 10 s zwischen Abrufen, eine Änderung nach der anderen.
- Bei Timeout nicht wiederholen, sondern mit einer einfachen Erreichbarkeitsprobe (`GET /`,
  Antwort 401 genügt) warten, bis es wieder antwortet; dann den Stand **lesen**, bevor
  weitergeschrieben wird – die letzte Schreibaktion kann angekommen sein.
- Nicht vorhandene Knoten kosten ~20 s je Abruf.
