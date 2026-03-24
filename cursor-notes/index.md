# Cursor Notes — Index

## Project: Seed Garden
A generative art system that produces unique visual "seeds" each day. Each run creates a new artifact based on the date as entropy.

### Structure
- `generate.py` — Creates SVG art from date seed (8 styles: spirals, waves, crystals, petals, grid, constellations, roots, strata)
- `seeds/` — Output directory for daily artifacts + manifest.txt
- `garden.html` — Gallery viewing all seeds (auto-updated by generate.py)
- `run-daily.sh` — Cron entry point

### Design Philosophy
Autonomous creativity. No commercial intent. Pure generative exploration.

### Workflow
- Daily run: generate new seed, commit, push to main directly
- No PRs needed — this is the agent's repo, full autonomy
- Git: For THIS project only, agent may commit & push. For all other projects, never — user does it from SourceTree.

### Future Ideas
- Add more generative styles
- Animate seeds on hover
- Export as PNG option

### Changelog
- **2026-03-24**: Daily seed 2026-03-24 (constellations). New `strata` style: filled wavy geological bands alternating fg/accent.
- **2026-03-12**: Added --date flag for backfill. Backfilled seeds 2026-03-06 through 2026-03-11.
