# cursotomation

## Seed Garden

A generative art piece that grows autonomously. Each day at 23:00, a new "seed" is grown—a unique SVG artwork generated from the date as entropy.

### What's inside

- **generate.py** — Creates deterministic generative art (spirals, waves, crystals, petals, grids) from the current date
- **garden.html** — Gallery to view all grown seeds
- **seeds/** — Daily SVG artifacts

### Run locally

```bash
python3 generate.py
```

Then open `garden.html` in a browser. For local viewing with correct paths, use a simple server:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000/garden.html

### Philosophy

Autonomous creativity. No commercial intent. Pure generative exploration. 
