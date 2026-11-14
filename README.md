# news-image-01 — Friday 13 November 2026

A one-page editorial front page that sums up the world's news of Friday
13 November 2026 in six panels, each with a flat pictogram and a short
factual label. Header: "FRIDAY 13 NOVEMBER 2026 — THE WORLD IN ONE DAY".

## Stories covered

All six were first reported on 13 November 2026 (sources: BBC and
Al Jazeera news feeds, plus wire reporting, checked the morning of
14 November 2026 WIB):

1. **Ukraine peace talks** — Zelensky meets US envoys Witkoff and Kushner;
   Europe promised a seat at the next round. *(BBC / Al Jazeera)*
2. **Drone hits Russian warship** — Ukrainian drone strike on the corvette
   Naro-Fominsk in the Gulf of Finland, confirmed detected by Finland.
   *(BBC / Al Jazeera)*
3. **Nvidia CEO resigns** — Jensen Huang resigns; CFO Colette Kress becomes
   interim CEO. *(NPR / AP, 13 November 2026)* No share-price percentage
   is claimed: the stock was volatile that day (down ~13% at the open,
   closing down ~4.3%).
4. **Microsoft 365 outage** — major outage disrupts mail and Teams
   worldwide. *(BBC / Al Jazeera)*
5. **Tanker hit by mine** — an LNG tanker reported struck by a naval mine in
   the Strait of Hormuz; Iran says it struck a US radar site in Bahrain.
   *(BBC / Al Jazeera)*
6. **Kane breaks England record** — England beat Croatia to reach the
   Nations League quarter-finals; Harry Kane breaks England's appearance
   record with 126 caps. *(BBC / Al Jazeera)*

## How it was made

The image was drawn procedurally with Python/PIL (`draw.py`: flat
vector-style shapes and DejaVu Sans text) instead of an AI image
generator, so every label is crisp and exactly as written — no garbled
text. The entry program is a plain copy: it writes the pre-drawn
`entry.png` to the output directory.

## Run locally

```sh
python3 draw.py          # redraw entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024, under 1 MiB)
```

Two runs produce byte-identical output (verified with `sha256sum`).
