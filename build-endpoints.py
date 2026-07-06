#!/usr/bin/env python3
"""Derive machine endpoints (tokens.css, llms-full.txt token tables) from tokens.json.
Single source of truth: edit tokens.json (or re-export from Figma), then run this.
Usage: python3 build-endpoints.py
"""
import json, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.load(open(ROOT / "tokens.json"))
colls = data["collections"]

def css_name(token):
    return "--" + token.replace("/", "-").replace(" ", "-").lower()

def mode_val(entry, idx):
    v = entry.get("resolved", entry["value"])
    if isinstance(v, list):
        return v[idx]
    return v

def px(v):
    if isinstance(v, (int, float)):
        return f"{v:g}px"
    return str(v)

# ---------- tokens.css ----------
lines = [
    "/* Kiva Ecosystem 2026 — design tokens as CSS custom properties.",
    "   Generated from tokens.json — do not edit by hand. */",
    "",
]
alias_color = colls["Alias - Color"]
themes = alias_color["modes"]

# default theme on :root + foundations
lines.append(":root {")
lines.append("  /* Alias - Color (default theme) */")
for name, entry in alias_color["variables"].items():
    lines.append(f"  {css_name(name)}: {mode_val(entry, 0)};")
lines.append("  /* Global radius */")
for name, entry in colls["Global"]["variables"].items():
    if name.startswith("radius/"):
        lines.append(f"  {css_name(name)}: {px(entry['value'])};")
lines.append("  /* Global spacing scale */")
for name, entry in colls["Global"]["variables"].items():
    if name.startswith("spacing/scale/"):
        lines.append(f"  {css_name(name)}: {px(entry['value'])};")
lines.append("  /* Elevation (x y blur spread / opacity baked into color) */")
lines.append("  --elevation-default: 0 4px 12px rgba(0,0,0,0.08);")
lines.append("  --elevation-hover: 0 4px 16px rgba(0,0,0,0.16);")
lines.append("  --elevation-click-active: 0 4px 12px rgba(0,0,0,0.08);")
lines.append("}")
lines.append("")

# per-theme overrides for alias colors
for i, theme in enumerate(themes):
    if i == 0:
        continue
    lines.append(f'[data-theme="{theme}"] {{')
    for name, entry in alias_color["variables"].items():
        v0, vi = mode_val(entry, 0), mode_val(entry, i)
        if v0 != vi:
            lines.append(f"  {css_name(name)}: {vi};")
    lines.append("}")
    lines.append("")

# component tokens: single-mode collections chain to alias vars where aliased
def var_ref(entry, idx=0):
    v = entry["value"]
    if isinstance(v, list):
        v = v[idx]
    if isinstance(v, str) and v.startswith("{Alias - Color::"):
        return f"var({css_name(v[16:-1])})"
    r = entry.get("resolved")
    if isinstance(r, list):
        r = r[idx]
    if entry["type"] == "FLOAT" and isinstance(r, (int, float)):
        return px(r)
    return str(r)

lines.append("/* Mapped component tokens */")
lines.append(":root {")
for cname in ["Mapped - Forms", "Mapped - Tooltip / Chips / Pills",
              "Mapped - Lightbox / Loading / Carousel / Avatar", "Mapped - Navigation"]:
    lines.append(f"  /* {cname} */")
    for name, entry in colls[cname]["variables"].items():
        if entry["type"] == "STRING":
            lines.append(f'  {css_name(name)}: "{entry.get("resolved", entry["value"])}";')
        else:
            lines.append(f"  {css_name(name)}: {var_ref(entry)};")
lines.append("}")
lines.append("")

# buttons: per-variant blocks
btn = colls["Mapped - Buttons"]
for i, variant in enumerate(btn["modes"]):
    sel = f'[data-button-variant="{variant}"]'
    lines.append(f"{sel} {{")
    for name, entry in btn["variables"].items():
        short = css_name(name.replace("button/", "btn/").replace(" ", "-"))
        lines.append(f"  {short}: {var_ref(entry, i)};")
    lines.append("}")
    lines.append("")

(ROOT / "tokens.css").write_text("\n".join(lines))
print(f"tokens.css written ({len(lines)} lines)")

# ---------- llms token tables (markdown fragment) ----------
md = []
for cname, coll in colls.items():
    md.append(f"### Collection: {cname}")
    md.append("")
    modes = coll["modes"]
    if len(modes) > 1:
        md.append("| token | " + " | ".join(modes) + " |")
        md.append("|" + "---|" * (len(modes) + 1))
        for name, entry in coll["variables"].items():
            vals = [str(mode_val(entry, i)) for i in range(len(modes))]
            md.append(f"| `{name}` | " + " | ".join(vals) + " |")
    else:
        md.append("| token | value | resolves to |")
        md.append("|---|---|---|")
        for name, entry in coll["variables"].items():
            raw = entry["value"] if isinstance(entry["value"], str) else json.dumps(entry["value"])
            md.append(f"| `{name}` | {raw} | {entry.get('resolved', '')} |")
    md.append("")
(ROOT / "_token-tables.md").write_text("\n".join(md))
print(f"_token-tables.md written ({len(md)} lines)")
