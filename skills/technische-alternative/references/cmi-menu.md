# C.M.I. menu: operating the controller from the browser

The C.M.I. renders the menu of every x2 node as a web page – the same pages as on the display.
Parameters can be read and, after logging in as *Fachmann* (specialist) or *Experte* (expert),
changed.

> **Observed, not documented.** The addresses below were taken from the web interface of a
> C.M.I. with firmware 1.48.1 connected to a UVR16x2 (November 2026). TA does not describe this
> protocol, and other firmware may differ. Before every write, read the page and check that
> designation and old value match.

## Addresses

All addresses are hex strings; the first two characters are the CAN node (`0F` = 15).

| Purpose | Request |
|---|---|
| Node list | `GET /can_knoten.cgi?node=<n>` → link `menupagex.cgi?nodex2=<KK>005800` |
| Load a page | `GET /INCLUDE/devpagex.cgi?pagex2=<address>` (HTML fragment) |
| Main menu | `<KK>005800` – contains e.g. functions `<kk>055800`, inputs `<kk>025800`, fixed values `<kk>035800` |
| Function *n* | `<kk><ff>5c07` with `ff` = n − 1 (hex); tabs `…5c01`, `…5c03`, `…5c05`, `…5c07`, `…5c0a` |
| Sub-page | e.g. heating curve of a heating circuit `<kk><ff>5c11` |
| Value dialog | `GET /INCLUDE/changerx2.cgi?sadrx2=<value-address>` → hidden field `changeadrx2`, min/max, current value |
| **Write** | `GET /INCLUDE/change.cgi?changeadrx2=<changeadr>&changetox2=<value>` (decimal point, e.g. `38.0`) |
| Login level | `GET /INCLUDE/devpagexUser.cgi?changeuserx2=<kk>0157ff<password>` (Fachmann) or `<kk>0257ff` (Experte) |

- Values appear in the HTML as `<div class="VALUE_B">Designation</div><div class="VALUE_C" adresse="…">Value</div>`.
- The login response starts with the level (`1`, `2`) followed by a hex token; the browser stores
  it as cookie **`canremote<node>`**. Without it, parameter pages show only the level selector.
- The C.M.I.'s own HTTP Basic login applies in addition.
- The controller returns to the user level 30 minutes after login.

## One change, step by step

1. Read the page, check designation and old value.
2. Read the value dialog: `changeadrx2`, allowed range, current value.
3. Write only if the current value equals the expected one.
4. Wait 5–10 s, read the dialog again, compare the new value.
5. Check the effect on an output variable (e.g. flow set temperature via CoE).
6. Discard the cookie.

[`scripts/cmi_menu.py`](../scripts/cmi_menu.py) does exactly this.

## Robustness

The C.M.I. web server is weak. Observed: after five to ten requests within a minute the C.M.I.
was unreachable twice, for **5 and 20 minutes**; CoE and control kept running. Therefore:

- ≥ 10 s between requests, one change at a time.
- After a timeout do not retry; wait with a simple reachability probe (`GET /`, a 401 answer is
  enough) until it answers again, then **read** the state before writing on – the last write may
  have arrived.
- Non-existent nodes cost ~20 s per request.
