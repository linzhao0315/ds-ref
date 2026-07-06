# Kiva Ecosystem 2026 — Design System

The canonical token reference for the Kiva product platform.

A single-file, self-contained reference for typography, colors, spacing, layout grid, radius, elevation, border, buttons, and the Mapped component layer (forms, tooltip, chips and pills, loading, carousel, lightbox, navigation and footer, avatar). Built to serve both human designers and AI agents working on Kiva product surfaces.

## Machine endpoints (for AI tools and build pipelines)

One source of truth, three renditions. Point AI tools at these URLs instead of the HTML:

| Endpoint | What it is |
|---|---|
| [`llms.txt`](https://linzhao0315.github.io/ds-ref/llms.txt) | Index + core rules — the entry point for agents (llmstxt.org convention) |
| [`llms-full.txt`](https://linzhao0315.github.io/ds-ref/llms-full.txt) | Complete flat markdown: rules, component specifications, full token tables |
| [`tokens.json`](https://linzhao0315.github.io/ds-ref/tokens.json) | Full variable library export: Global primitives, Alias semantic layer (5 theme modes), Mapped component layer. Aliases preserved as `{Collection::token}` references |
| [`tokens.css`](https://linzhao0315.github.io/ds-ref/tokens.css) | The same tokens as CSS custom properties; themes via `[data-theme]`, button variants via `[data-button-variant]` |

`tokens.css` and the token tables in `llms-full.txt` are generated from `tokens.json` by `build-endpoints.py` — edit `tokens.json` (or re-export from Figma), run the script, commit all four.

## Live reference

[**linzhao0315.github.io/ds-ref**](https://linzhao0315.github.io/ds-ref/)

## Source of truth

All values are resolved from:

- The Figma variable library (`Alias - *` collections)
- The `@kiva/kv-tokens` package
- Effect-style specifications maintained in the Kiva design system Figma file

## Authorship

| Role | |
|---|---|
| Authored by | **Lin Zhao** |
| Editorial authority | **Lin Zhao** · **Biju Baek** |

The named editorial authorities hold the right to interpret, clarify, and approve changes to this reference. Questions on intent or scope should be directed to them.

## How to use

- Open `index.html` in any modern browser. No build step, no dependencies.
- Click any token color to copy its hex value.
- Hover any token row to read its usage notes.
- Click **Copy as prompt** on any panel to get a paste-ready context block for AI tools.
- Click **Export tokens** to download the full token set as JSON, CSS variables, Tailwind config, or AI prompt bundle.
- Press `/` to focus search · arrow keys to navigate panels.

## Typefaces

The reference is rendered in the two Kiva typefaces:

- **Dovetail MVB** (`fonts/44829.otf` — Regular 400, `fonts/44831.otf` — Medium 500). Used for Display, Headline 1, Headline 2, and Blockquote.
- **Kiva Post Grotesk** (`fonts/KivaPostGrot-*.otf` — 8 weight/style files: Light, Light Italic, Book, Book Italic, Medium, Medium Italic, Bold, Bold Italic). Used for Subheadline, Title, Base, Button, Label, Caption, Upper, Small.

These typefaces are part of the Kiva visual identity and are subject to their own licensing terms. Use outside this reference requires permission from the editorial authority listed above.

## License

See `LICENSE` for terms.

---

© 2026 Kiva. All rights reserved.
