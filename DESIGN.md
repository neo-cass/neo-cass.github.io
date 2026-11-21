# Design System: neocass.com
**Project ID:** n/a (hand-built site, not a Stitch project)

The source of truth for how the site looks. `public/assets/css/style.css` implements it;
change this file first when the design changes.

## 1. Visual Theme & Atmosphere

**Plain, quiet and text-first, like a well-kept README.** One narrow column of monospace
text on a flat background, greyscale only. Nothing moves, glows or floats. The page is meant
to be read in under a minute: who this is, what they have published, where to find the CV.

The plainness is deliberate. Engineers and hiring managers read heavy styling as a template;
a bare page puts the work (a CERN thesis, a poster, a talk) first and signals that someone
chose every element. Restraint is the personality: decoration is never added to fill space.

- **Density:** Airy vertically, compact horizontally. Generous gaps between sections, tight
  rows within them.
- **Mood:** Utilitarian, calm, confident. Closer to a man page than to a portfolio.

## 2. Color Palette & Roles

Greyscale only. No accent colour: links are told apart by their underline, not by hue.

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

Photos are shown in **greyscale** so they sit inside the palette, and come back to full
colour on hover or keyboard focus.

## 3. Typography Rules

- **One typeface: the visitor's own monospace font** (SF Mono on Apple devices, Consolas on
  Windows, Liberation Mono or similar on Linux). No web fonts are downloaded, ever.
- **Body:** 15px (0.9375rem), line height 1.6. Every size is in rem so it follows the
  reader's browser setting.
- **Name (h1):** the same size as the body, bold. Hierarchy comes from weight and position,
  not from big type.
- **Section headings (h2):** body size, regular weight, Muted, sentence case
  ("Publications", "Presentations", "CV", "Photos").
- **Descriptions and footer:** 14px, Muted, sentence case with proper nouns capitalised
  ("Master’s thesis · University of Bath & CERN").
- **Separators:** a middle dot with spaces ( · ) between facts in a description.
- **Naming:** the document is always called **CV**, never "résumé". Profile links use each
  service's own capitalisation: CV, GitHub, LinkedIn, ORCID.

## 4. Component Stylings

* **Links:** Ink text with a thin Silver underline (a 1px bottom border) that darkens to Ink
  on hover. No colour change, no animation.
* **Profile links:** a single wrapping row under the name, each wrapped in Muted square
  brackets: `[CV] [GitHub] [LinkedIn] [ORCID]`. Hover underlines the word itself.
* **Portrait:** a small 64px square, greyscale, sharp corners, beside the name and role.
* **Sections:** a Muted heading sitting on a full-width Rule hairline. No boxes or cards.
* **Entries:** a two-column row. The left column (6 characters wide) holds the year, or a
  short label such as "PDF", in Muted. The right column holds the title as a link with the
  description underneath. On phones the label stacks above the title.
* **Photos:** a grid of four thumbnails cropped to 3:4 (two per row on phones), sharp
  corners, small even gaps. A click opens the full image in a lightbox.
* **Inputs/Forms:** square-cornered fields with a 1px Field-edge border on the page colour;
  the border turns Ink on focus. Labels are Muted, above each field. The button is a
  square-cornered Ink outline that fills with Ink on hover.
* **Focus:** a 2px Ink outline, offset 2px, on every interactive element.
* **Never used:** rounded corners, pills, cards, shadows, gradients, glow, emoji as icons,
  icon fonts, accent colours, entrance or scroll animations.

## 5. Layout Principles

- **One left-aligned column**, at most 72 characters wide, centred on the page, with a 16px
  gutter on each side so nothing touches the screen edge on phones.
- **Top to bottom:** header (portrait, name, role, profile links), Publications,
  Presentations, CV, Photos, then the contact form when it is enabled, then the footer.
  There is no navigation bar; the page is short enough to scroll.
- **Spacing rhythm:** 64px above the header (40px on phones), 48px above each section
  heading, 16px between entries, 64px before the footer.
- **Footer:** "© year Neo Cass" in Muted under a hairline that spans the text column.
- **Breakpoint:** a single one at 480px, where entry rows stack and photos go two across.
