# Finding products, documents and prices on ta.co.at

Checked 2 November 2026.

## Site structure

- German product pages: `https://www.ta.co.at/<category>/<product-slug>`. Categories:
  `/standardregler`, `/cora`, `/x2-frei-programmierbare-regler`, `/x2-bedienung-schnittstellen`,
  `/x2-energiemanagement`, `/erweiterungsmodule`, `/sensoren`, `/zubehoer`, `/pumpengruppen`,
  `/auslauftypen` (discontinued).
- English pages: `/en/<category-en>/<slug-en>` – slugs are **not** translations of the German
  ones; scrape the English category page instead of guessing.
- **Soft 404:** ta.co.at answers **HTTP 200 for non-existent paths**. A 200 does not prove a
  product exists – only trust URLs taken from category pages.

## Catalogue and price list

| Document | URL | Note |
|---|---|---|
| Catalogue 2026 DE | https://www.ta.co.at/fileadmin/Downloads/Katalog/deutsch/Katalog_2026_DE_web.pdf | ~43 pages, I/O, scope of delivery, article numbers, **no prices** |
| Catalogue 2026 EN | …/Katalog/englisch/Katalog_2026_EN_web.pdf | |
| Price list 2026 DE | https://www.ta.co.at/download/datei/18130 | "gültig ab 01.03.2026", "Stand 15.10.2026", EUR excl. VAT |
| Price list 2026 EN | https://www.ta.co.at/download/datei/18134 | |

- Article numbers look like `01/UVR16X2K`; prefixes `01/`, `10/`, `13/`, `02/` (promotions),
  `03/` – meaning not documented.
- Column **PG** (price group 1/2/3): conditions differ by group; discounts are not public.
- Where catalogue and price list differ (e.g. UVR16x2 triac version, FRISTAR3 in the catalogue
  only), the newer price list is more current – mark such items "verify with TA".
- A new year's price list gets a new `datei` ID – find it via the download page.

## Manuals and datasheets

- Pattern `https://www.ta.co.at/download/datei/<id>` → the PDF itself (versioned file name in the
  header). **Document IDs stay stable across revisions**; firmware and software IDs change with
  every version. Old links like `/download/datei/24292445-manual-uvr65/` are dead – use the
  plain numeric ID.
- Finding an ID: (a) the product page lists its documents as
  `data-label="<title>" href="/download/datei/<id>"`; (b) https://www.ta.co.at/download/dokumente
  lists all ~770 documents on one large page (client-side filter only). One ID per language.

| Product | German documents (datei ID) |
|---|---|
| UVR16x2 | general 1260, mounting relay 1263, mounting triac 1262, operation 635, -E-DE/NP 625, -DC 2474, TAPPS2 functions 1261 |
| UVR610 | programming & operation 3499, mounting 3276, functions 3275, -OD 4620, -MODB 4621, -OD-MODB 8030, UVR610K 8107, -DC 4622 |
| UVR67 | all chapters 2827, beginners' guide 4247 (UVR65, discontinued: 2429) |
| CAN-I/O45 | general 483, mounting & operation 491, functions 484 |
| CAN-EZ3 | mounting & general 3455, current sensors 4623 |
| CAN-BC2 | manual 1667, MD-MODB 1669, MD-KNX 1672 |
| CAN-MTx2 | manual 458, -ST mounting 8569 |
| C.M.I. | quick guide 497, online manual PDF 804, CoE 826, JSON API 1751, CMI-S 13546 |
| CAN-RP | 2828 |
| FTS-DL | 1610 (FTS14-240DL 1223, via CORA-DL 9761) |
| Temperature sensors | datasheet 1127 |
| RASPT | 1112 · RAS-CT4 17958 |
| HIREL22 / -230V / -PF | 1184 / 1208 / 1196 |
| AO4-DL | 2120 · PRS0-6DL 1322 |
| TAPPS2 | manual 1579 |

## Planning aids from TA

- **x2 program library** – https://www.ta.co.at/download/x2-programmbibliothek: 27 complete
  programs (function data + visualisation) filterable by heating circuits (2–5), boilers (0–2),
  solar, district heating, DHW via tank or fresh-water module. They fit only if the hydraulics
  match – TA advises against heavy modification.
- **Programming examples** – https://www.ta.co.at/download/x2-programmierbeispiele: ~75
  examples, e.g. heating circuit with burner demand and DHW pump (datei 2991), with RAS+DL (2976),
  two CAN devices (2979), solar with PWM pump (2988), solar with two consumers (2982), boiler
  cascade with/without buffer (2996/2997), hygienic DHW with circulation (2998), heat metering
  (3002), 3 circuits with PMG1 (18107), PV surplus (14237, 14714, 18037).
- **TA-Designer templates** – https://www.ta.co.at/download/ta-designer-vorlagen.
- **TAPPS2** (free, Windows) with a hydraulic drawing layer; **x2-Simulator** for testing.
- **UVR67 programs:** >800 fixed programs, e.g. 0 simple solar, 16 storage charging from boiler,
  32 burner demand, 96 buffer and DHW from solid-fuel boiler, 800 heating circuit with up to two
  heat sources, 816 return-flow boost, 832 solid-fuel boiler + buffer + circuit + auxiliary
  demand – full list in manual 2827.
- **TA programming service** (only for installers buying directly from TA), seminars, webinars.

Not available from TA: a UVR16x2-vs-UVR610 comparison, an I/O-counting sheet, a general
scheme catalogue beyond the program library. x2 devices ship **without** a factory program
(exception: ATON).
