#!/usr/bin/env python3
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
    style = rng.choice(["spirals", "waves", "crystals", "petals", "grid", "constellations", "roots", "ink", "moss"])
    
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

    elif style == "ink":
        n_blots = rng.randint(4, 9)
        for _ in range(n_blots):
            cx = rng.uniform(60, w - 60)
            cy = rng.uniform(60, h - 60)
            r_base = 25 + rng.random() * 45
            pts = []
            n_ctrl = rng.randint(6, 12)
            for i in range(n_ctrl):
                angle = i * 6.28 / n_ctrl + rng.random() * 0.5
                r = r_base * (0.6 + rng.random() * 0.8)
                x = cx + r * (1 if rng.random() > 0.3 else -1) * (0.5 + rng.random())
                y = cy + r * 0.7 * (1 if rng.random() > 0.4 else -1)
                pts.append(f"{x},{y}")
            if len(pts) >= 3:
                paths.append("M " + " L ".join(pts) + " Z")

    elif style == "moss":
        n_clusters = rng.randint(5, 12)
        for _ in range(n_clusters):
            cx = rng.uniform(30, w - 30)
            cy = rng.uniform(30, h - 30)
            n_dots = rng.randint(8, 25)
            spread = 15 + rng.random() * 35
            for _ in range(n_dots):
                dx = rng.gauss(0, spread)
                dy = rng.gauss(0, spread * 0.8)
                x = cx + dx
                y = cy + dy
                if 5 < x < w - 5 and 5 < y < h - 5:
                    r = rng.uniform(0.8, 3.5)
                    paths.append(f"M {x+r},{y} m -{r},0 a {r},{r} 0 1,1 {r*2},0 a {r},{r} 0 1,1 -{r*2},0")
    
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
    
    if style == "ink":
        svg_parts = [f'<path d="{p}" fill="{fg}" fill-opacity="{rng.uniform(0.15, 0.5)}" stroke="none"/>' for p in paths]
    elif style == "moss":
        svg_parts = [f'<path d="{p}" fill="{fg}" fill-opacity="{rng.uniform(0.4, 0.9)}" stroke="none"/>' for p in paths]
    else:
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
    openers = ["Today the", "A", "Perhaps", "Between", "Within", "Through", "Beyond"]
    middles = ["pattern", "shape", "trace", "echo", "shadow", "whisper", "drift"]
    closers = ["finds its form.", "emerges.", "lingers.", "unfolds.", "settles.", "remembers."]
    return f"{rng.choice(openers)} {rng.choice(middles)} {rng.choice(closers)}"


def _backfill_dreams(entries):
    result = []
    for e in entries:
        if not e.strip():
            continue
        parts = e.split("|")
        if len(parts) >= 5:
            result.append(e)
        else:
            date_str = parts[0]
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                seed = date_seed(dt)
                dream = generate_dream(seed)
                dream_flat = dream.replace("\n", " | ")
                result.append(f"{e}|{dream_flat}")
            except ValueError:
                result.append(e)
    return result


def generate_dream(seed):
    rng = random.Random(seed + 2)
    lines = [
        ("The wind", "carries no name."),
        ("A stone", "holds the light."),
        ("Between sleep", "and waking."),
        ("The river", "forgets the source."),
        ("Dust settles", "on old glass."),
        ("A bird", "crosses the frame."),
        ("The moon", "writes in silver."),
        ("Nothing moves", "but the shadow."),
        ("The garden", "dreams of rain."),
        ("Time folds", "into itself."),
    ]
    a, b = rng.choice(lines)
    return f"{a}\n{b}"


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
    dream = generate_dream(seed)
    thought_path = Path("seeds") / (dt.strftime("%Y-%m-%d") + ".txt")
    thought_path.write_text(thought)
    manifest_path = Path("seeds") / "manifest.txt"
    entries = manifest_path.read_text().splitlines() if manifest_path.exists() else []
    dream_flat = dream.replace("\n", " | ")
    entry = f"{dt.strftime('%Y-%m-%d')}|{style}|{filename}|{thought}|{dream_flat}"
    entries = [e for e in entries if filename not in e]
    entries.append(entry)
    entries.sort(key=lambda e: e.split("|")[0], reverse=True)
    entries = _backfill_dreams(entries)
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
