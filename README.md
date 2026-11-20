# The World in One Day — Friday, 20 November 2026

A make.fun `news-image-20261120` entry: one 1024×1024 newspaper front
page that sums up the world's news of **Friday, 20 November 2026**.

## The front page

**The Hague — the lead.** The International Court of Justice ruled
9–6 that Myanmar committed genocide against the Rohingya in its 2017
campaign in Rakhine — the court's first genocide finding against a
state. Rohingya refugees in Bangladesh cheered the verdict.

**Shenzhen.** Trump, Xi and Putin sat down for the first three-way
summit of the three sitting presidents and issued a four-point peace
declaration, covering nuclear arms control, Iran and the war in
Ukraine.

**New York — markets.** Anthropic's IPO is the biggest listing on
record: priced at $83 a share, up about 17% on its first day, worth
roughly $1.5 trillion. The S&P 500 fell 2% for a fifth straight loss.

**Riyadh.** A Houthi missile hit the capital's tallest tower; Saudi
authorities confirmed damage to a landmark building.

**Also today.** Iran escalated tanker attacks in the Strait of
Hormuz; four nations urged Israel to let aid into flood-hit Gaza;
Cyclone Akvan approached India's Odisha coast, closing schools;
Taiwan's stocks fell 5,248 points over three trading days; and Trump
returned from China for a White House press conference.

## How the image was made

- `compose.py` (Python 3, Pillow) draws the whole page: masthead,
  date strip, headlines, decks, briefs and footer. Every word on the
  page is rendered by this script, so the finished image carries no
  garbled AI text. The script is deterministic — no network, no clock,
  no randomness.
- `assets/` holds four editorial illustrations generated for this
  entry (the ICJ courtroom, the Shenzhen summit table, the IPO trading
  floor, the Riyadh skyline). They contain no text; every word on the
  page comes from `compose.py`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`, byte for byte.

Rebuild the image: `python3 compose.py` — then test the entry
program twice and compare the outputs:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
cmp out1/entry.png out2/entry.png
```
