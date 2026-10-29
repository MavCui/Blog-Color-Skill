<p align="center">
  <img src="docs/assets/readme-cover.png" alt="Blog Color — wine-red serif lettering meets a fan of green printed paper folds" width="100%">
</p>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a> · <a href="#install">Install</a> · <a href="#selected-studies">Gallery</a> · <a href="#typography">Typography</a>
</p>

# Blog Color

**Editorial covers for thoughtful writing.**

A Codex skill that turns articles into original landscape cover art through ordinary-object metaphors, Chinese and Latin serif typography, and a disciplined two-ink print language. Designed for Feishu document headers and social article covers, with particular care for writing about AI, products, and ways of working.

One decisive image. A little tension. Enough paper to let it breathe.

## Selected studies

### The Other End

<img src="assets/examples/B-collaboration.png" alt="The Other End — a monumental green pulley and a small oxblood pulley connected by one thread" width="100%">

*Botanical green × oxblood. An unexpected scale relationship makes collaboration visible.*

| The Shape of Context | A Measure of Judgment |
|:---|:---|
| <img src="assets/examples/A-context.png" alt="Blue engraved thread spool with a single terracotta strand and Chinese serif title" width="100%"> | <img src="assets/examples/C-judgment.png" alt="A charcoal sieve catches one red stone, with bold Chinese serif lettering" width="100%"> |
| Cobalt × terracotta · retaining and releasing | Charcoal × signal red · deciding what matters |

These are original model-generated direction studies, not fixed templates. Their lettering is model-rendered, and their native resolutions have not been converted into every target format. The context study is **not** a finished 5:1 Feishu export.

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/MavCui/Blog-Color-Skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/editorial-wide-cover"
```

The repository name is **Blog Color**; the installed skill and invocation name are **`editorial-wide-cover`**. The root [SKILL.md](SKILL.md) is the entry point. If that destination already exists, update the existing installation instead of cloning over it.

The skill is available on your next Codex turn. It uses the built-in image-generation capability when available; the default workflow does not require a separate image API key. Bundled fonts can be loaded directly by a typesetting tool without a system-wide font installation.

Then ask:

```text
Use $editorial-wide-cover to make a Feishu document cover for this article.
Title: 上下文的边界
Use the cobalt–terracotta palette and the preset Chinese/English serifs.
```

## The visual language

| Element | Direction |
|:---|:---|
| **Image** | One ordinary object, or two objects with a meaningful relationship |
| **Composition** | A decisive crop, an unexpected scale, or one concentrated overprint |
| **Type** | Chinese Song/Ming serifs and expressive Latin serifs, with deliberate hierarchy |
| **Color** | Two inks with separate jobs; paper remains visible |
| **Surface** | Etching, screening, plate separation, or restrained photocopy texture |
| **Series** | Consistent ink, type, and spacing; a fresh visual idea for each article |

For an article about context, a thread can carry the idea of retention. For evaluation, a sieve can embody selection. The subject comes from the article's actual relationship—not a recurring stock symbol. Technology topics keep the same art direction; they do not trigger glowing chips, robot heads, or interface panels.

Read the [art direction](references/art-direction.md) for the full working rules.

## Three ink stories

| Palette | Main ink | Accent ink | Paper | Character |
|:---|:---|:---|:---|:---|
| **Cobalt + Terracotta** | `#2148B8` | `#C65F38` | `#FAFAF7` | Clear, warm, observant; the default series |
| **Botanical + Oxblood** | `#008A4B` | `#8F3434` | `#FAFAF7` | Tactile and cultural; relationships and essays |
| **Charcoal + Signal Red** | `#30343A` | `#C83232` | `#E9E9E5` | Direct and critical; evaluation and opinion |

The main ink normally carries about 80% of the printed marks. The accent carries one meaningful event: a connecting point, a retained object, or a selected intersection. The paper is not a third ink.

## Typography

The presets include actual font files, not just a list of font names.

| Preset | Chinese title | English title / subtitle | Use |
|:---|:---|:---|:---|
| **Editorial** | Source Han Serif SC SemiBold | Bodoni Moda Medium | The main publication voice |
| **Literary** | Source Han Serif SC SemiBold | Cormorant Garamond Medium, optionally italic | Reflective and relational writing |
| **Critical** | Source Han Serif SC SemiBold, stronger scale | Bodoni Moda SemiBold | Judgment, evaluation, and argument |

IBM Plex Mono is available for a small, optional issue number. It does not replace the serif title system.

**Two typography workflows:** native generation follows the fonts' visual characteristics; exact typography uses a text-free generated base and real font-file typesetting when the available tools support it. Naming a font in a prompt is not proof that the model loaded that font. Chinese characters and English spelling are checked before delivery.

See the [typography guide](references/typography.md), [font files and licenses](assets/fonts/), and [resource manifest](assets/fonts/manifest.json).

## Made for landscape

| Preset | Target canvas | Core safe area |
|:---|:---|:---|
| **Feishu** | 2000 × 400 · 5:1 | Centered 580 × 240 |
| **Social wide** | 2350 × 1000 · 2.35:1 | Central 76% of width and height |
| **Social 16:9** | 1920 × 1080 | Central 80% width / 76% height |
| **Social 2:1** | 2000 × 1000 | Central 76% of width and height |

The Feishu dimensions follow its [official cover recommendations](https://www.feishu.cn/hc/en-US/articles/990851076781-recommendations-for-covers-in-docs). The other safe areas are this skill's design conventions, not universal platform requirements.

A Feishu header is composed around a compact central information core, with expendable image fragments extending into the wings. A social cover is recomposed to use its additional height. Neither is made by stretching the other.

Image generators can return a different native size or aspect ratio. The workflow reads the actual file, distinguishes a direction study from an upload-ready export, and reports unresolved format limits. See [formats and export checks](references/formats.md).

## Try it

**One article, one image**

```text
Use $editorial-wide-cover for this essay about human–AI collaboration.
Title: 协作的另一端
Botanical green and oxblood. Literary serifs. A 2.35:1 social cover.
```

**The same idea, two compositions**

```text
Use $editorial-wide-cover to make a Feishu header and a 16:9 social cover.
Keep the same metaphor, inks, and typography; recompose for each format.
```

**A coherent series**

```text
Use $editorial-wide-cover for these three articles.
Keep one palette and the editorial serif preset.
Give each article a different object relationship and visual event.
```

**Exact type**

```text
Use $editorial-wide-cover with actual Source Han Serif and Bodoni Moda typesetting.
Generate a text-free artwork first. If exact typesetting is unavailable,
return the clean base and placement specification and tell me what remains.
```

The output includes the image, the prompt actually used, and a small recipe recording the text, palette, typography, target and actual sizes, and review status. The default destination is `output/editorial-wide-cover/<date>/` in the current workspace.

## Inside the skill

```text
SKILL.md                  The generation workflow
agents/openai.yaml        Codex discovery and invocation metadata
references/               Art direction, type, formats, presets, and examples
assets/fonts/             Original font files, OFL texts, and checksums
assets/examples/          Three original generated direction studies
scripts/inspect_cover.py  Read-only PNG/JPEG geometry inspection
scripts/validate_project.py
                          Repository integrity and regression checks
docs/                     README artwork and its generation prompt
```

Run the local checks with Python 3.10 or later; no third-party packages are required:

```bash
python3 scripts/validate_project.py
python3 scripts/inspect_cover.py /path/to/cover.png --preset feishu
```

The inspector checks dimensions, aspect ratio, size, and safe-area coordinates. It does not perform OCR or certify visual quality. Actual images still need to be reviewed.

## Credits & licenses

Created by [MavCui](https://github.com/MavCui). The print grammar was informed by [Yan Liu's mono-color-skill](https://github.com/yanliudesign/mono-color-skill); attribution and the upstream MIT notice are preserved. No upstream reference images or example artworks are bundled.

Skill instructions and code: [MIT](LICENSE). Fonts: their original [SIL Open Font Licenses](assets/fonts/). Original generated project imagery is documented separately in [Asset License](ASSET-LICENSE.md). See [sources](references/sources.md) for provenance and font download records.

---

<p align="center"><em>A little color. A longer look.</em><br><a href="README.zh-CN.md">阅读简体中文版 →</a></p>
