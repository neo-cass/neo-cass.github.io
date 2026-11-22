# Design System: neocass.com
**Project ID:** n/a (hand-built site, not a Stitch project)

The source of truth for how the site looks. `public/assets/css/style.css` implements it;
change this file first when the design changes.

## 1. Visual Theme & Atmosphere

**Plain, quiet and text-first, like a well-kept README.** One narrow column of monospace
text on a flat greyscale background, with the photos as the only colour. Nothing moves, glows or floats. The page is meant
to be read in under a minute: who this is, what they have published, where to find the CV.

The plainness is deliberate. Engineers and hiring managers read heavy styling as a template;
a bare page puts the work (a CERN thesis, a poster, a talk) first and signals that someone
chose every element. Restraint is the personality: decoration is never added to fill space.

- **Density:** Compact but not cramped. Clear gaps between sections, tight rows within
  them; white space only where it separates groups, never as filler.
- **Mood:** Utilitarian, calm, confident. Closer to a man page than to a portfolio.

## 2. Color Palette & Roles

Greyscale only for text and lines. No accent colour: links are told apart by their
underline, not by hue.

| Role | Light | Dark | Used for |
|---|---|---|---|
| **Page** | Paper White (#ffffff) | Near-Black (#111111) | The single background for everything, including the footer. |
| **Ink** | Soft Charcoal (#222222) | Pale Ash (#e4e4e4) | Name, link text, body copy. |
| **Muted** | Neutral Grey (#767676) | Mid Grey (#8f8f8f) | Role line, section headings, years, descriptions, footer, brackets around links. Both pass WCAG AA (4.5:1 and 5.9:1). |
| **Underline** | Silver (#bbbbbb) | Graphite (#555555) | Resting underline under links; it turns Ink on hover. |
| **Rule** | Whisper Grey (#e5e5e5) | Deep Grey (#2a2a2a) | Hairlines under section headings and above the footer. |
| **Field edge** | Steel Grey (#8a8a8a) | Slate (#6a6a6a) | Contact-form field borders (3:1 against the page). |

Light and dark follow the visitor's system setting. Only the colour tokens change between
them; nothing else.

Photos (the portrait and the gallery) are shown in **full colour**: they are the only
colour on the page, so they stand out against the greyscale text.

## 3. Typography Rules

- **One typeface: Inconsolata**, self-hosted from `public/assets/fonts/inconsolata/` (one
  34 KB variable file, Latin subset, SIL Open Font License in `OFL.txt`). It is preloaded,
  shown with `font-display: swap`, and falls back to the system monospace font. Nothing is
  loaded from Google or any other font service. It was chosen so the page looks the same on
  every device (the old system-font stack showed SF Mono, Menlo or Consolas depending on
  the browser) and for its calm, slightly narrow, humanist shapes.
- **Body:** 17px (1.0625rem), line height 1.5. Inconsolata has a small x-height, so 17px
  reads like 15px in most monospace fonts. Every size is in rem so it follows the reader's
  browser setting.
- **Name (h1):** the same size as the body, bold. Hierarchy comes from weight and position,
  not from big type.
- **Section headings (h2):** body size, regular weight, Muted, sentence case
  ("Publications", "Presentations", "CV", "Photos").
- **Descriptions and footer:** 15px (0.9375rem), Muted, sentence case with proper nouns capitalised
  ("Master’s thesis · University of Bath & CERN").
- **Separators:** a middle dot with spaces ( · ) between facts in a description.
- **Naming:** the document is always called **CV**, never "résumé". Profile links use each
  service's own capitalisation: CV, GitHub, LinkedIn, ORCID.

## 4. Component Stylings

* **Links:** Ink text with a thin Silver underline (a 1px bottom border) that darkens to Ink
  on hover. No colour change, no animation.
* **Profile links:** a single wrapping row under the name, each wrapped in Muted square
  brackets: `[CV] [GitHub] [LinkedIn] [ORCID]`. Hover underlines the word itself.
* **Portrait:** a small 64px square, full colour, sharp corners, beside the name and role.
* **Sections:** a Muted heading sitting on a full-width Rule hairline. No boxes or cards.
* **Entries:** a two-column row. The left column (6 characters wide) holds the year, or a
  short label such as "PDF", in Muted. The right column holds the title as a link with the
  description underneath. On phones the label stacks above the title.
* **Photos:** a grid of four full-colour thumbnails cropped to 3:4 (two per row on phones),
  sharp corners, small even gaps. A click opens the full image in a lightbox.
* **Inputs/Forms:** square-cornered fields with a 1px Field-edge border on the page colour;
  the border turns Ink on focus. Labels are Muted, above each field. The button is a
  square-cornered Ink outline that fills with Ink on hover.
* **Focus:** a 2px Ink outline, offset 2px, on every interactive element.
* **Never used:** rounded corners, pills, cards, shadows, gradients, glow, emoji as icons,
  icon fonts, accent colours, entrance or scroll animations.

## 6. AI-look review

Checked on 22 Nov 2026 with the `unslop-ui` audit (its scanner plus a manual pass over the
nine common "looks AI-generated" patterns). Result: clean, scanner score 0. No
Tailwind/shadcn defaults, no purple or indigo, no gradients, no gratuitous motion, no
rounded corners, no glow, no emoji icons, no centred hero with feature cards. The only
item it raised, the generic system font, was resolved by switching to Inconsolata. Re-run
the audit after any visual redesign and keep this section up to date.

## 5. Layout Principles

- **One left-aligned column**, at most 76 characters wide (about 645px), centred on the page, with a 16px
  gutter on each side so nothing touches the screen edge on phones.
- **Top to bottom:** header (portrait, name, role, profile links), Publications,
  Presentations, CV, Photos, then the contact form when it is enabled, then the footer.
  There is no navigation bar; the page is short enough to scroll.
- **Spacing system: an 8-point grid with a 4px half-step** (the scale used by Material
  Design and most product design systems), applied with the **Gestalt law of proximity**:
  things that belong together sit closer than things that do not, so the gaps alone show
  the structure without extra boxes or lines.

  | Token | Size | Used for |
  |---|---|---|
  | `--space-2xs` | 4px | Heading text to its hairline; form label to field |
  | `--space-xs` | 8px | Between photo thumbnails; button and field padding |
  | `--space-sm` | 12px | Name block to profile links; hairline to first entry; between entries; between form fields; footer hairline to text |
  | `--space-md` | 16px | Portrait to name; horizontal button padding |
  | `--space-lg` | 32px | Above each section heading; before the footer; below the footer; top of page on phones |
  | `--space-xl` | 48px | Top of page on desktop |

  The proximity order, from closest to furthest: a title and its description (no gap, just
  line height) < one entry and the next (12px) < a heading and its content (16px including
  the hairline) < one section and the next (32px). Each step is clearly larger than the one
  before, so the eye groups correctly. Don't add a gap that breaks that order.
- **Footer:** "© year Neo Cass" in Muted under a hairline that spans the text column.
- **Breakpoint:** a single one at 480px, where entry rows stack and photos go two across.
