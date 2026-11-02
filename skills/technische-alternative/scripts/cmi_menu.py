#!/usr/bin/env python3
"""Read and (carefully) change UVR16x2 menu values through the C.M.I. web interface.

Observed protocol, C.M.I. firmware 1.48.1 - see references/cmi-menue.md. Python stdlib only.

Credentials come from the environment, never from argv:
  CMI_HOST       host or IP of the C.M.I.
  CMI_USER       C.M.I. web login
  CMI_PASSWORD   C.M.I. web password
  UVR_PASSWORD   Fachmann/Experte password of the controller (only for parameter pages / set)

Usage:
  cmi_menu.py page <node> <page-addr> [--login experte|fachmann]   # page text with value addresses
  cmi_menu.py get  <node> <value-addr> [--login …]                 # change dialog: range, current value
  cmi_menu.py set  <node> <value-addr> --expect 40.0 --to 38.0 [--login …] [--write]

`set` without --write is a dry run. With --write it checks the current value against --expect,
writes, waits, reads back and exits 1 on any mismatch. The C.M.I. web server is weak: requests are
spaced by PAUSE seconds; after a timeout, read the state before writing again.
"""
import argparse
import base64
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PAUSE = 10          # seconds between requests; faster pacing made the C.M.I. drop off for minutes
TIMEOUT = 25
LEVEL = {"fachmann": "0157ff", "experte": "0257ff"}


class Cmi:
    def __init__(self, node):
        try:
            self.host = os.environ["CMI_HOST"]
            auth = f'{os.environ["CMI_USER"]}:{os.environ["CMI_PASSWORD"]}'
        except KeyError as e:
            sys.exit(f"missing environment variable {e}")
        self.auth = "Basic " + base64.b64encode(auth.encode()).decode()
        self.node = f"{int(node):02x}"
        self.cookie = None
        self.last = 0.0

    def get(self, path):
        wait = self.last + PAUSE - time.time()
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(f"http://{self.host}{path}", headers={"Authorization": self.auth})
        if self.cookie:
            req.add_header("Cookie", f"canremote{int(self.node, 16)}={self.cookie}")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", "replace")
        finally:
            self.last = time.time()

    def login(self, level):
        pw = os.environ.get("UVR_PASSWORD")
        if not pw:
            sys.exit("UVR_PASSWORD not set")
        r = self.get(f"/INCLUDE/devpagexUser.cgi?changeuserx2={self.node}{LEVEL[level]}"
                     + urllib.parse.quote(pw, safe=""))
        if not r[:1].isdigit() or r[0] == "0" or int(r[1:].strip() or "0", 16) == 0:
            sys.exit("login failed")
        self.cookie = r.strip()
        print(f"login ok ({level})", file=sys.stderr)

    def page(self, addr):
        t = self.get(f"/INCLUDE/devpagex.cgi?pagex2={addr}")
        t = re.sub(r'<div class="VALUE_C" adresse="([0-9a-fA-F]+)">', r" = [\1] ", t)
        t = re.sub(r'<[^>]*fadresse="([0-9a-fA-F]+)"[^>]*>', r"\n[\1] ", t)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        return "\n".join(re.sub(r"\s+", " ", l).strip() for l in t.split("\n") if l.strip())

    def dialog(self, addr):
        t = self.get(f"/INCLUDE/changerx2.cgi?sadrx2={addr}")
        cadr = re.search(r'value="([0-9A-F]+)" name="changeadrx2"', t)
        inp = re.search(r'<input[^>]*name="changetox2"[^>]*>', t)
        if not cadr or not inp:
            return None
        attr = dict(re.findall(r'(\w+)="([^"]*)"', inp.group(0)))
        return {"changeadr": cadr.group(1), "value": attr.get("value"),
                "min": attr.get("min"), "max": attr.get("max")}

    def write(self, changeadr, value):
        self.get(f"/INCLUDE/change.cgi?changeadrx2={changeadr}&changetox2={urllib.parse.quote(value)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["page", "get", "set"])
    ap.add_argument("node", help="CAN node of the controller, decimal")
    ap.add_argument("addr", help="page address (page) or value address (get/set), hex")
    ap.add_argument("--login", choices=list(LEVEL))
    ap.add_argument("--expect", help="set: value that must be current before writing")
    ap.add_argument("--to", help="set: new value, decimal point")
    ap.add_argument("--write", action="store_true", help="set: actually write (default: dry run)")
    a = ap.parse_args()

    c = Cmi(a.node)
    try:
        if a.login:
            c.login(a.login)
        if a.cmd == "page":
            print(c.page(a.addr))
            return
        d = c.dialog(a.addr)
        if d is None:
            sys.exit("no change dialog - wrong address or insufficient level (use --login)")
        print(f"current {d['value']}  range {d['min']}..{d['max']}  changeadr {d['changeadr']}")
        if a.cmd == "get":
            return
        if a.expect is None or a.to is None:
            sys.exit("set needs --expect and --to")
        if float(d["value"]) != float(a.expect):
            sys.exit(f"STOP: expected {a.expect}, found {d['value']}")
        if not float(d["min"]) <= float(a.to) <= float(d["max"]):
            sys.exit(f"STOP: {a.to} outside {d['min']}..{d['max']}")
        if not a.write:
            print(f"dry run: would set {d['value']} -> {a.to}")
            return
        c.write(d["changeadr"], a.to)
        back = c.dialog(a.addr)
        got = back and back["value"]
        print(f"{time.strftime('%H:%M:%S')} {d['value']} -> {a.to}, read back {got}")
        if got is None or float(got) != float(a.to):
            sys.exit("STOP: read-back mismatch - check the page before retrying")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"C.M.I. not answering ({e}). Wait until GET / answers, then READ before writing again.")


if __name__ == "__main__":
    main()
