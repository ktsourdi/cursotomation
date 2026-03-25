# cursotomation

## Seed Garden

A generative art piece that grows autonomously. Each day at 23:00, a new "seed" is grown—a unique SVG artwork generated from the date as entropy.

### What's inside

- **generate.py** — Creates deterministic generative art (spirals, waves, crystals, petals, grid, constellations, roots, orbits) from the current date
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

### Deploy live (Vercel)

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Import this repo — Vercel will auto-detect it as a static site
3. Deploy — every push to `main` will auto-deploy

The garden will be live at `your-project.vercel.app`. No build step needed.

### Philosophy

Autonomous creativity. No commercial intent. Pure generative exploration. 
