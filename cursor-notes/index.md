# Cursor Notes — Index

## Project: Seed Garden
A generative art system that produces unique visual "seeds" each day. Each run creates a new artifact based on the date as entropy.

### Structure
- `generate.py` — Creates SVG art from date seed (10 styles: spirals, waves, crystals, petals, grid, constellations, roots, aurora, inkblot, topography)
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
- Export as PNG option
- Seasonal or lunar influence on style choice

### Changelog
- **2026-03-22**: Added aurora, inkblot, topography styles. Expanded thought generator. Hover animations on gallery cards (scale, glow, image brightness). Backfilled 2026-03-13 through 2026-03-22.
- **2026-03-12**: Added --date flag for backfill. Backfilled seeds 2026-03-06 through 2026-03-11.
