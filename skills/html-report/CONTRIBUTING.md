# Contributing to html-report Skill

## Quick Start

1. Clone the repo and install the plugin:
   ```bash
   git clone https://github.com/segmentstream/agent-skills.git
   cd agent-skills
   claude --plugin-dir .
   ```

2. Verify the skill loads:
   ```
   > /skills
   # Should show "html-report" in the list
   ```

3. Test it works:
   ```
   > Generate a channel performance report for Google Ads and Meta
   # Should produce a dark-themed HTML report
   ```

## Development Workflow

### 1. Understand the Architecture

```
skills/html-report/
├── SKILL.md                          # Main skill (loaded by Claude)
├── assets/
│   ├── template.html                 # CSS design system + HTML shell
│   └── logo.svg                      # SegmentStream logo (inline SVG)
├── references/
│   ├── jsx-format.md                 # JSX/Cowork conventions
│   ├── channel-icons.md              # Ad platform SVG icons
│   └── component-gallery.html        # Visual preview (NOT loaded by agents)
├── evals/
│   ├── trigger-eval.json             # Trigger accuracy test set
│   └── quality-scenarios.md          # Output quality test scenarios
└── CONTRIBUTING.md                   # This file
```

**What agents load:** SKILL.md tells the agent to read `assets/template.html` + `assets/logo.svg`. Optionally reads `references/jsx-format.md` or `references/channel-icons.md` based on output format.

**What agents DON'T load:** `component-gallery.html` (large visual reference for humans only).

### 2. Making Changes

**Adding a new component:**
1. Design the CSS in `assets/template.html` (new classes, styles)
2. Document the component pattern in `SKILL.md` (class names, HTML structure, when to use)
3. Optionally add a visual example to the component gallery (for human preview)
4. Add a quality scenario to `evals/quality-scenarios.md`

**Changing colors/typography/tokens:**
1. Update CSS variables in `assets/template.html` `:root` block
2. Update corresponding Tailwind classes in `references/jsx-format.md`
3. Re-test with quality scenarios

**Changing the report frame (topbar/bottombar):**
1. Edit the HTML shell in `assets/template.html`
2. Update `SKILL.md` placeholder documentation

### 3. Testing Your Changes

#### Quick Validation
```bash
python -m scripts.quick_validate skills/html-report/
```

#### Trigger Testing (does the skill activate for the right prompts?)
```bash
python -m scripts.run_eval \
  --eval-set skills/html-report/evals/trigger-eval.json \
  --skill-path skills/html-report/ \
  --runs-per-query 3 \
  --verbose
```

Target: 100% pass rate. If a query fails:
- **False negative** (should trigger but didn't) -- improve SKILL.md description
- **False positive** (shouldn't trigger but did) -- narrow SKILL.md description

#### Quality Testing (does the output match the spec?)

Run each scenario from `evals/quality-scenarios.md`:

```bash
# WITHOUT skill (baseline -- expect poor output)
claude -p "Generate a monthly performance report for Google Ads" --no-skills

# WITH skill (should match acceptance criteria)
claude -p "Generate a monthly performance report for Google Ads"
```

Compare outputs against the acceptance criteria checklist. If the agent:
- Uses wrong colors -- clarify in `assets/template.html` CSS + `SKILL.md`
- Skips components -- make `SKILL.md` more explicit about when to use them
- Uses wrong chart library -- clarify in `SKILL.md` format-specific section

#### Visual Testing

Open generated HTML files in a browser. Check:
- Dark theme renders correctly
- Fonts load (system fonts, no external dependencies)
- Components match the design system
- Print styles work (Cmd+P)

### 4. Two Output Formats

| Format | Environment | Charts | Template |
|--------|------------|--------|----------|
| **HTML** | Claude Code (local files) | Inline SVG or Chart.js CDN | `assets/template.html` |
| **JSX** | Claude.ai / Cowork | Recharts (pre-loaded) | `references/jsx-format.md` |

When editing, update BOTH formats if the change affects shared design tokens (colors, fonts, spacing).

### 5. Key Constraints

- **`template.html` must stay self-contained** -- no external CSS/font imports
- **`SKILL.md` < 15KB** -- agents read this fully; keep it concise
- **`template.html` < 25KB** -- agents read this as CSS reference
- **Channel icons are inline SVG** -- no external image URLs
- **Dark theme only** -- no light mode toggle (keeps CSS simple)
- **System fonts** -- no Google Fonts or CDN font imports

### 6. Submitting Changes

1. Create a branch: `git checkout -b feat/html-report-new-component`
2. Make changes to skill files
3. Run trigger eval + quality scenarios
4. Open PR with:
   - What changed
   - Screenshots of generated reports (before/after)
   - Eval results
