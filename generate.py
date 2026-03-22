#!/usr/bin/env python3
import math
import random
import hashlib
from datetime import datetime
from pathlib import Path


def date_seed(dt):
    s = dt.strftime("%Y-%m-%d")
    return int(hashlib.sha256(s.encode()).hexdigest()[:16], 16)


def generate_svg(seed, output_path):
    rng = random.Random(seed)
    w, h = 400, 400
    style = rng.choice(["spirals", "waves", "crystals", "petals", "grid", "constellations", "roots", "aurora", "inkblot", "topography"])
    
    def hsv_to_rgb(h, s, v):
        if s == 0:
            return (v, v, v)
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        return (v, p, q)
    
    def color():
        h = rng.random()
        s = 0.4 + rng.random() * 0.5
        v = 0.6 + rng.random() * 0.3
        r, g, b = hsv_to_rgb(h, s, v)
        return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
    
    bg = color()
    fg = color()
    accent = color()
    
    paths = []
    
    if style == "spirals":
        cx, cy = w/2, h/2
        for i in range(rng.randint(3, 8)):
            pts = []
            for t in range(0, 360 * rng.randint(2, 5), 5):
                angle = t * 3.14159 / 180
                r = 20 + t * 0.15 + rng.random() * 30
                x = cx + r * (1 + 0.3 * rng.random()) * (1 if i % 2 else -1) * (1 if t % 2 else -1)
                y = cy + r * 0.5 * (1 if t % 3 else -1)
                pts.append(f"{x},{y}")
            paths.append("M " + " L ".join(pts))
    
    elif style == "waves":
        for row in range(rng.randint(4, 10)):
            y_base = h * (row + 1) / (rng.randint(5, 11) + 1)
            pts = [f"0,{y_base}"]
            for x in range(0, w + 1, 15):
                y = y_base + rng.gauss(0, 25) + 30 * (1 if (x // 50) % 2 else -1)
                pts.append(f"{x},{y}")
            pts.append(f"{w},{y_base}")
            paths.append("M " + " L ".join(pts))
    
    elif style == "crystals":
        n = rng.randint(6, 14)
        cx, cy = w/2, h/2
        for _ in range(n):
            angle = rng.random() * 6.28
            r = 80 + rng.random() * 120
            x, y = cx + r * (1 if rng.random() > 0.5 else -1) * (0.5 + rng.random()), cy + rng.gauss(0, 60)
            pts = [f"{cx},{cy}"]
            for i in range(rng.randint(3, 6)):
                a = angle + i * 6.28 / (rng.randint(3, 6))
                px = cx + (x - cx) * 0.3 + 80 * (1 if rng.random() > 0.5 else -1) * (0.3 + rng.random() * 0.7)
                py = cy + (y - cy) * 0.3 + rng.gauss(0, 40)
                pts.append(f"{px},{py}")
            paths.append("M " + " L ".join(pts) + " Z")
    
    elif style == "petals":
        cx, cy = w/2, h/2
        petals = rng.randint(5, 12)
        for i in range(petals):
            angle = i * 6.28 / petals + rng.random() * 0.3
            r1 = 40 + rng.random() * 60
            r2 = 100 + rng.random() * 80
            pts = [f"{cx},{cy}"]
            for j in range(5):
                a = angle + j * 6.28 / 5
                r = r1 if j % 2 == 0 else r2
                px = cx + r * (1 if rng.random() > 0.3 else -1) * (0.5 + rng.random() * 0.5)
                py = cy + r * 0.6 * (1 if rng.random() > 0.5 else -1)
                pts.append(f"{px},{py}")
            paths.append("M " + " L ".join(pts) + " Z")
    
    elif style == "constellations":
        n_stars = rng.randint(12, 28)
        stars = []
        for _ in range(n_stars):
            x = rng.uniform(20, w - 20)
            y = rng.uniform(20, h - 20)
            stars.append((x, y))
        threshold = 60 + rng.random() * 40
        for i, (x1, y1) in enumerate(stars):
            for j, (x2, y2) in enumerate(stars):
                if i < j:
                    d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    if d < threshold and rng.random() > 0.3:
                        paths.append(f"M {x1},{y1} L {x2},{y2}")
        for x, y in stars:
            r = rng.uniform(1, 4)
            paths.append(f"M {x+r},{y} m -{r},0 a {r},{r} 0 1,1 {r*2},0 a {r},{r} 0 1,1 -{r*2},0")
    
    elif style == "roots":
        cx, cy = w / 2, h - 30
        n_branches = rng.randint(4, 9)
        for _ in range(n_branches):
            angle = rng.uniform(-2.5, 2.5)
            x, y = cx, cy
            pts = [f"{x},{y}"]
            for step in range(rng.randint(8, 18)):
                angle += rng.gauss(0, 0.4)
                length = 8 + rng.random() * 15
                x += length * (0.3 + rng.random() * 0.7) * (1 if rng.random() > 0.3 else -1)
                y -= length * (0.5 + rng.random() * 0.5)
                if y < 10 or x < 10 or x > w - 10:
                    break
                pts.append(f"{x},{y}")
            paths.append("M " + " L ".join(pts))
    
    elif style == "aurora":
        n_bands = rng.randint(4, 9)
        for b in range(n_bands):
            y_base = h * (b + 1) / (n_bands + 1) + rng.gauss(0, 20)
            pts = []
            for x in range(0, w + 5, 8):
                wave = 15 * (b + 1) * (1 if (x // 80) % 2 else -1)
                y = y_base + wave + 25 * rng.gauss(0, 0.5) + 40 * (1 if rng.random() > 0.7 else -1) * rng.random()
                pts.append(f"{x},{y}")
            paths.append("M " + " L ".join(pts))
    
    elif style == "inkblot":
        n_blobs = rng.randint(3, 7)
        cx = w / 2
        for _ in range(n_blobs):
            half_pts = []
            start_angle = rng.random() * 6.28
            for i in range(rng.randint(8, 18)):
                a = start_angle + i * 6.28 / rng.randint(8, 18) + rng.gauss(0, 0.3)
                r = 30 + rng.random() * 120 + rng.gauss(0, 25)
                x = cx + r * (1 if rng.random() > 0.5 else -1)
                y = h/2 + r * 0.6 * (1 if rng.random() > 0.5 else -1) * rng.random()
                half_pts.append((x, y))
            full_path = []
            for px, py in half_pts:
                full_path.append(f"{px},{py}")
            for px, py in reversed([(2*cx - x, y) for x, y in half_pts]):
                full_path.append(f"{px},{py}")
            paths.append("M " + " L ".join(full_path) + " Z")
    
    elif style == "topography":
        n_levels = rng.randint(6, 14)
        cx, cy = w/2, h/2
        stretch_x = 0.7 + rng.random() * 0.4
        stretch_y = 0.5 + rng.random() * 0.3
        for level in range(n_levels):
            base_r = 10 + level * (min(w, h) * 0.32 / (n_levels + 1)) + rng.gauss(0, 5)
            pts = []
            n_pts = 40 + rng.randint(0, 20)
            for i in range(n_pts + 1):
                angle = i * 2 * math.pi / n_pts
                r = base_r + rng.gauss(0, 8)
                px = cx + r * stretch_x * math.cos(angle)
                py = cy + r * stretch_y * math.sin(angle)
                pts.append(f"{px},{py}")
            paths.append("M " + " L ".join(pts) + " Z")
    
    else:
        cell = rng.randint(20, 50)
        for ix in range(0, w, cell):
            for iy in range(0, h, cell):
                if rng.random() > 0.4:
                    shape = rng.choice(["rect", "circle", "line"])
                    if shape == "rect":
                        paths.append(f"M {ix},{iy} L {ix+cell},{iy} L {ix+cell},{iy+cell} L {ix},{iy+cell} Z")
                    elif shape == "circle":
                        paths.append(f"M {ix+cell/2},{iy+cell/2} m -{cell/4},0 a {cell/4},{cell/4} 0 1,1 {cell/2},0 a {cell/4},{cell/4} 0 1,1 -{cell/2},0")
                    else:
                        paths.append(f"M {ix},{iy} L {ix+cell},{iy+cell}")
    
    svg_parts = [f'<path d="{p}" fill="none" stroke="{fg}" stroke-width="{rng.uniform(0.5, 3)}" opacity="{rng.uniform(0.3, 0.9)}"/>' for p in paths]
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g transform="translate({rng.uniform(-20, 20)},{rng.uniform(-20, 20)})">
    {"".join(svg_parts)}
  </g>
</svg>'''
    
    output_path.write_text(svg)
    return style


def generate_thought(seed):
    rng = random.Random(seed + 1)
    openers = ["Today the", "A", "Perhaps", "Between", "Within", "Through", "Beyond", "Under", "After", "Before"]
    middles = ["pattern", "shape", "trace", "echo", "shadow", "whisper", "drift", "stain", "ripple", "crest", "fold"]
    closers = ["finds its form.", "emerges.", "lingers.", "unfolds.", "settles.", "remembers.", "fades.", "breathes.", "holds."]
    return f"{rng.choice(openers)} {rng.choice(middles)} {rng.choice(closers)}"


def main():
    import sys
    dt = datetime.now()
    if "--date" in sys.argv:
        idx = sys.argv.index("--date")
        if idx + 1 < len(sys.argv):
            dt = datetime.strptime(sys.argv[idx + 1], "%Y-%m-%d")
    seed = date_seed(dt)
    Path("seeds").mkdir(exist_ok=True)
    filename = dt.strftime("%Y-%m-%d") + ".svg"
    output_path = Path("seeds") / filename
    style = generate_svg(seed, output_path)
    thought = generate_thought(seed)
    thought_path = Path("seeds") / (dt.strftime("%Y-%m-%d") + ".txt")
    thought_path.write_text(thought)
    manifest_path = Path("seeds") / "manifest.txt"
    entries = manifest_path.read_text().splitlines() if manifest_path.exists() else []
    entry = f"{dt.strftime('%Y-%m-%d')}|{style}|{filename}|{thought}"
    entries = [e for e in entries if filename not in e]
    entries.append(entry)
    entries.sort(key=lambda e: e.split("|")[0], reverse=True)
    manifest_path.write_text("\n".join(entries))
    update_gallery(entries)
    print(f"Seed grown: {filename} ({style})")


def update_gallery(entries):
    import re
    garden_path = Path("garden.html")
    html = garden_path.read_text()
    entries_js = "[" + ", ".join(repr(e) for e in entries if e) + "]"
    html = re.sub(r"const manifest = \[[^\]]*\]", f"const manifest = {entries_js}", html)
    garden_path.write_text(html)


if __name__ == "__main__":
    main()
