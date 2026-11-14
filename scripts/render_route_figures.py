#!/usr/bin/env python3
"""Rebuild the public SVG route and elevation figures from index.html's embedded NASA/JPL waypoints."""
from __future__ import annotations

import ast
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "index.html"
OUT = ROOT / "assets"
ORIGIN_LON = 77.4509
ORIGIN_LAT = 18.4446
APP_RADIUS_KM = 59.15
TARGET_SOLS = [13, 648, 940, 1219, 1250, 1299, 1354]
STOP_NAMES = ["Base", "Delta front", "Margin Unit", "Cheyava Falls", "Serpentine Rapids", "Pico Turquino", "Witch Hazel Hill"]


def read_waypoints() -> list[list[float]]:
    source = APP.read_text(encoding="utf-8")
    match = re.search(r"const WP=(\[.*?\]);\s*\nconst EMB=", source, re.S)
    if not match:
        raise ValueError("Could not locate embedded WP array in index.html")
    points = ast.literal_eval(match.group(1))
    if len(points) != 698:
        raise ValueError(f"Expected 698 embedded waypoints, found {len(points)}")
    return points


def xy(point: list[float]) -> tuple[float, float]:
    _, lon, lat, *_ = point
    x = (lon - ORIGIN_LON) * APP_RADIUS_KM * math.cos(math.radians(lat))
    y = (lat - ORIGIN_LAT) * APP_RADIUS_KM
    return x, y


def anchors(points: list[list[float]]) -> list[tuple[int, list[float]]]:
    indices = [min(range(len(points)), key=lambda i: abs(points[i][0] - sol)) for sol in TARGET_SOLS]
    return [(i, points[i]) for i in indices]


def route_svg(points: list[list[float]], stops: list[tuple[int, list[float]]]) -> str:
    subset = points[:stops[-1][0] + 1]
    coords = [xy(p) for p in subset]
    stop_coords = [xy(p) for _, p in stops]
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    xmin, xmax = min(xs) - 1.8, max(xs) + 1.8
    ymin, ymax = min(ys) - 1.8, max(ys) + 1.8
    W, H = 1100, 670
    left, top, plot_w, plot_h = 65, 75, 680, 455

    def sx(x: float) -> float:
        return left + (x - xmin) / (xmax - xmin) * plot_w

    def sy(y: float) -> float:
        return top + (ymax - y) / (ymax - ymin) * plot_h

    rover_path = " ".join(("M" if i == 0 else "L") + f"{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(coords))
    human_path = " ".join(("M" if i == 0 else "L") + f"{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(stop_coords))
    grid = []
    for i in range(6):
        x = left + i * plot_w / 5
        y = top + i * plot_h / 5
        grid.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top+plot_h}" class="grid"/>')
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" class="grid"/>')
    marks = []
    for i, (x, y) in enumerate(stop_coords):
        px, py = sx(x), sy(y)
        marks.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="11" class="anchor"/><text x="{px:.1f}" y="{py+5:.1f}" text-anchor="middle" class="number">{i+1}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Perseverance traverse and straight anchor connections at Jezero</title>
<desc id="desc">Plan-view plot generated from NASA/JPL Mars 2020 waypoint longitude and latitude fields. Cyan is the rover waypoint traverse. Orange connects the seven selected waypoint anchors by straight segments. This is not a terrain basemap or a human-safe route.</desc>
<style>text{{font-family:Arial,sans-serif}}.title{{font-size:27px;font-weight:700;fill:#eef3f6}}.sub{{font-size:15px;fill:#aebcc7}}.grid{{stroke:#344859;stroke-width:1;opacity:.75}}.rover{{fill:none;stroke:#65c9d1;stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}.straight{{fill:none;stroke:#ff9a5b;stroke-width:4;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:10 7}}.anchor{{fill:#ff9a5b;stroke:#1a222a;stroke-width:2}}.number{{font-size:13px;font-weight:800;fill:#111820}}.label{{font-size:15px;font-weight:700;fill:#eef3f6}}.legend{{font-size:15px;fill:#dce5eb}}.axis{{font-size:13px;fill:#aebcc7}}</style>
<rect width="100%" height="100%" fill="#0e1821" rx="18"/>
<text x="75" y="32" class="title">Jezero · Perseverance traverse</text>
<text x="75" y="60" class="sub">NASA/JPL M20 waypoints · plan view relative to the landing-site origin · km</text>
{''.join(grid)}
<path d="{rover_path}" class="rover"/>
<path d="{human_path}" class="straight"/>
{''.join(marks)}
<rect x="780" y="75" width="275" height="455" rx="12" fill="#14232e" stroke="#344859"/>
<text x="805" y="110" class="label">Selected waypoint anchors</text>
{''.join(f'<circle cx="800" cy="{150+i*48}" r="10" class="anchor"/><text x="800" y="{154+i*48}" text-anchor="middle" class="number">{i+1}</text><text x="820" y="{155+i*48}" class="legend">{html.escape(name)}</text>' for i,name in enumerate(STOP_NAMES))}
<line x1="65" y1="585" x2="108" y2="585" class="rover"/><text x="122" y="591" class="legend">Perseverance waypoint traverse</text>
<line x1="420" y1="585" x2="463" y2="585" class="straight"/><text x="477" y="591" class="legend">Straight connections between selected anchors</text>
<text x="65" y="635" class="sub">Sols: 13, 648, 933 (nearest to 940), 1219, 1250, 1299, 1354.</text>
<text x="1035" y="635" text-anchor="end" class="sub">Illustrative plan view · no DEM</text>
</svg>'''


def profile_svg(points: list[list[float]], stops: list[tuple[int, list[float]]]) -> str:
    end = stops[-1][0]
    subset = points[:end + 1]
    W, H = 1100, 500
    left, top, plot_w, plot_h = 105, 95, 900, 285
    xvals = [p[4] / 1000 for p in subset]
    zvals = [p[3] for p in subset]
    xmin, xmax = min(xvals), max(xvals)
    ymin, ymax = min(zvals) - 40, max(zvals) + 40

    def sx(x: float) -> float:
        return left + (x - xmin) / (xmax - xmin) * plot_w

    def sy(y: float) -> float:
        return top + (ymax - y) / (ymax - ymin) * plot_h

    path = " ".join(("M" if i == 0 else "L") + f"{sx(x):.1f},{sy(z):.1f}" for i, (x, z) in enumerate(zip(xvals, zvals)))
    grid, labels = [], []
    for k in range(5):
        yv = ymin + k * (ymax - ymin) / 4
        py = sy(yv)
        grid.append(f'<line x1="{left}" y1="{py:.1f}" x2="{left+plot_w}" y2="{py:.1f}" class="grid"/>')
        labels.append(f'<text x="{left-12}" y="{py+5:.1f}" text-anchor="end" class="axis">{yv:.0f}</text>')
    for i, (idx, p) in enumerate(stops):
        px, py = sx(p[4] / 1000), sy(p[3])
        labels.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" class="anchor"/><text x="{px+10:.1f}" y="{py-12:.1f}" class="label">{i+1}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Perseverance waypoint elevation profile</title>
<desc id="desc">Elevation along the Perseverance odometer track from Sol 13 through the waypoint nearest Sol 1354. All waypoints are plotted; selected science-stop anchors are numbered.</desc>
<style>text{{font-family:Arial,sans-serif}}.title{{font-size:27px;font-weight:700;fill:#eef3f6}}.sub{{font-size:15px;fill:#aebcc7}}.grid{{stroke:#344859;stroke-width:1;opacity:.75}}.profile{{fill:none;stroke:#65c9d1;stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}.anchor{{fill:#ff9a5b;stroke:#1a222a;stroke-width:2}}.label{{font-size:15px;font-weight:700;fill:#fff}}.axis{{font-size:14px;fill:#aebcc7}}</style>
<rect width="100%" height="100%" fill="#0e1821" rx="18"/>
<text x="75" y="34" class="title">Perseverance · waypoint elevation profile</text>
<text x="75" y="62" class="sub">NASA/JPL M20 waypoint elevation field plotted against rover odometer</text>
{''.join(grid)}{''.join(labels)}<path d="{path}" class="profile"/>
<text x="555" y="430" text-anchor="middle" class="axis">Rover odometer from Sol 13 (km)</text>
<text x="28" y="242" text-anchor="middle" class="axis" transform="rotate(-90 28 242)">Waypoint elevation field (m)</text>
<text x="90" y="475" class="sub">Selected anchors end at Sol 1354: {p[4]/1000:.1f} km odometer · waypoint fields, not a human walking profile.</text>
</svg>'''


def main() -> None:
    points = read_waypoints()
    stops = anchors(points)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "jezero-route-overview.svg").write_text(route_svg(points, stops), encoding="utf-8")
    (OUT / "perseverance-elevation-profile.svg").write_text(profile_svg(points, stops), encoding="utf-8")
    print(f"Rendered route and elevation SVGs from {len(points)} NASA/JPL waypoints.")
    print("Anchor Sols actually selected:", ", ".join(str(p[1][0]) for p in stops))


if __name__ == "__main__":
    main()