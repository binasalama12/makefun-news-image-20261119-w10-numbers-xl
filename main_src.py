#!/usr/bin/env python3
"""By The Numbers XL edition - news-image-20261119, round 3 (wallet w10).

The entry is entry.png: one dense front page for Thursday 19 November
2026 that leads with the day in figures - the $81.3bn IPO, 15.9m GTA VI
pre-orders, 200,000 people in Cyclone Akvan's evacuation zone - above
the stories themselves. This file is the readable source of the
entrypoint: it verifies the page is a well-formed PNG, prints the
masthead line and the numbered index of all 39 stories on the page
(3 leads, 12 pictured panels, 24 briefs), and copies the page into the
MAKEFUN_OUTPUT_DIR directory (default /output).

Standard library only.
"""
import hashlib
import os
import shutil
import struct
import sys

MASTHEAD = "THE DAY IN WORLD NEWS - Thursday 19 November 2026 - By The Numbers XL"

# The index of the page: (number, kind, label, headline) per story.
# LEAD = top story, PIC = pictured panel, BRIEF = one-line brief.
PAGE_INDEX = [
    (1, "LEAD", "SHENZHEN - SUMMIT", "Trump, Xi and Putin hold first three-way summit"),
    (2, "LEAD", "WORLDWIDE - GAMES", "GTA VI arrives after a 13-year wait"),
    (3, "LEAD", "NASDAQ - MARKETS", "Anthropic debuts in the biggest IPO on record"),
    (4, "PIC", "THE HAGUE - LAW", "World Court rules on Myanmar's Rohingya case"),
    (5, "PIC", "ODISHA - STORM", "Akvan bears down as 200,000 flee the coast"),
    (6, "PIC", "ANTALYA - CLIMATE", "COP31 enters its final 48 hours"),
    (7, "PIC", "KERCH - WAR", "Crimean Bridge hit a third time in a week"),
    (8, "PIC", "SEOUL - EDUCATION", "Half a million sit Korea's Suneung"),
    (9, "PIC", "FLORIDA - WEATHER", "Flooded Florida braces for still more rain"),
    (10, "PIC", "SHENZHEN - TRADE", "APEC leaders adopt the Shenzhen Declaration"),
    (11, "PIC", "JAZAN - GULF", "Saudi Arabia says danger has passed in three cities"),
    (12, "PIC", "KYIV - WAR", "Left off the agenda, Ukraine watches Shenzhen"),
    (13, "PIC", "NEW YORK - ART", "Van Gogh sells for a record $190.4m"),
    (14, "PIC", "SPACE - SCIENCE", "Voyager 1, one light-day out - NASA briefs the world"),
    (15, "PIC", "GAZA - WAR", "Israeli tanks cross Gaza's Yellow Line"),
    (16, "BRIEF", "BRUSSELS", "EU proposes a \u20ac45bn loan for Ukraine"),
    (17, "BRIEF", "WASHINGTON", "US and Venezuela sign a military cooperation agreement"),
    (18, "BRIEF", "PYONGYANG", "IAEA: North Korea has expanded uranium enrichment at Yongbyon"),
    (19, "BRIEF", "JERUSALEM", "Herzog taps ex-army chief Eisenkot to form a government"),
    (20, "BRIEF", "TEHRAN", "Trump says Iran is exploring chemical and biological weapons"),
    (21, "BRIEF", "KUWAIT CITY", "Kuwait repels its first Iranian attack in two months"),
    (22, "BRIEF", "RIYADH", "Debris from an intercepted Houthi rocket damages the PIF tower"),
    (23, "BRIEF", "GAZA", "Australia, Canada, Italy and UK demand unrestricted aid access"),
    (24, "BRIEF", "KINSHASA", "Ebola cases in DR Congo pass 11,000 in the widening outbreak"),
    (25, "BRIEF", "GENEVA", "Record 589 million children now live in conflict zones"),
    (26, "BRIEF", "NAIROBI", "Kenya's drought deepens the milk shortage; prices climb"),
    (27, "BRIEF", "PARIS", "France sees a fourth weekend of cost-of-living protests"),
    (28, "BRIEF", "TOKYO", "Dozens of Japanese firms issue breach notices after KARTE hack"),
    (29, "BRIEF", "WASHINGTON", "Ransomware group N0n claims data from 59 firms, incl. JPMorgan"),
    (30, "BRIEF", "MIAMI", "US court convicts Haitian pastor over the 2021 Moise assassination"),
    (31, "BRIEF", "WASHINGTON", "Trump makes a third Supreme Court bid on Venezuelan protections"),
    (32, "BRIEF", "CAPE CANAVERAL", "NASA sets coverage for the Northrop Grumman CRS-25 launch"),
    (33, "BRIEF", "MENLO PARK", "Google upgrades Gemini Tasks with calling, booking and payment"),
    (34, "BRIEF", "WELLINGTON", "India and New Zealand open their First Test in Wellington"),
    (35, "BRIEF", "SPORT", "Sindhu returns to the badminton world top five"),
    (36, "BRIEF", "MOGADISHU", "Somalia's constitutional reforms spark federal tensions"),
    (37, "BRIEF", "WASHINGTON", "NSA outage disrupts Middle East intelligence links"),
    (38, "BRIEF", "ANTALYA", "Vanuatu urges reform of climate talks as COP31 ends"),
    (39, "BRIEF", "DELHI", "Delhi-NCR schools reopen as GRAP Stage-III curbs are lifted"),
]

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Return (width, height) from the IHDR chunk of the PNG at path."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png does not start with a PNG signature")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png is missing its IHDR chunk")
    return struct.unpack(">II", head[16:24])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    page = os.path.join(here, "entry.png")
    try:
        width, height = png_dimensions(page)
    except (OSError, ValueError) as exc:
        print(f"entry.png rejected: {exc}")
        return 1
    print(MASTHEAD)
    print(f"Front page: {width}x{height} PNG, {len(PAGE_INDEX)} stories indexed below.")
    for number, kind, label, headline in PAGE_INDEX:
        print(f"{number:>2}. [{kind}] {label} - {headline}")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    shutil.copyfile(page, target)
    with open(page, "rb") as fh:
        blob = fh.read()
    digest = hashlib.sha256(blob).hexdigest()
    print(f"{len(PAGE_INDEX)} stories - copied the page to {target}")
    print(f"Page fingerprint: {len(blob)} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
