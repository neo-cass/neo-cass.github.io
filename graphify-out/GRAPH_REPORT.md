# Graph Report - neo-cass.github.io  (2026-11-22)

## Corpus Check
- 12 files · ~6,455 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 2, .ico 1)

## Summary
- 393 nodes · 759 edges · 17 communities (10 shown, 7 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04b096da`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build.py
- _
- T
- st
- deploy
- Y
- d
- b
- photoswipe-lightbox.esm.min.js
- neocass.com
- f
- tt
- A
- Q
- gallery.js
- photoswipe/README.md

## God Nodes (most connected - your core abstractions)
1. `_` - 54 edges
2. `b` - 27 edges
3. `st` - 25 edges
4. `d` - 24 edges
5. `Y` - 24 edges
6. `T` - 20 edges
7. `f` - 15 edges
8. `tt` - 14 edges
9. `A` - 12 edges
10. `x` - 11 edges

## Surprising Connections (you probably didn't know these)
- `r()` --calls--> `o()`  [EXTRACTED]
  public/assets/vendor/photoswipe/photoswipe.esm.min.js → public/assets/vendor/photoswipe/photoswipe.esm.min.js  _Bridges community 7 → community 12_
- `J()` --calls--> `y()`  [EXTRACTED]
  public/assets/vendor/photoswipe/photoswipe.esm.min.js → public/assets/vendor/photoswipe/photoswipe.esm.min.js  _Bridges community 7 → community 1_
- `J()` --calls--> `x`  [EXTRACTED]
  public/assets/vendor/photoswipe/photoswipe.esm.min.js → public/assets/vendor/photoswipe/photoswipe.esm.min.js  _Bridges community 5 → community 1_

## Import Cycles
- None detected.

## Communities (17 total, 7 thin omitted)

### Community 0 - "build.py"
Cohesion: 0.06
Nodes (15): build(), fingerprint(), assert_no_metadata(), circle(), fit_width(), load(), main(), save_webp() (+7 more)

### Community 1 - "_"
Cohesion: 0.06
Nodes (20): _, $, D, G, H, it, j, J() (+12 more)

### Community 2 - "T"
Cohesion: 0.13
Nodes (6): C, h(), M, P(), T, z()

### Community 3 - "st"
Cohesion: 0.09
Nodes (4): e(), E, O, st

### Community 4 - "deploy"
Cohesion: 0.06
Nodes (33): runs-on, steps, concurrency, cancel-in-progress, group, environment, if, needs (+25 more)

### Community 6 - "d"
Cohesion: 0.16
Nodes (3): a, d, r()

### Community 7 - "b"
Cohesion: 0.17
Nodes (3): b, o(), y()

### Community 8 - "photoswipe-lightbox.esm.min.js"
Cohesion: 0.14
Nodes (5): c(), l, p(), u, v

### Community 9 - "neocass.com"
Cohesion: 0.11
Nodes (16): 1. Visual Theme & Atmosphere, 2. Color Palette & Roles, 3. Typography Rules, 4. Component Stylings, 5. Layout Principles, Design System: neocass.com, Analytics (optional), Checks (+8 more)

### Community 10 - "f"
Cohesion: 0.17
Nodes (3): a(), f, k

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_` connect `_` to `T`, `st`, `Y`, `b`, `f`, `tt`, `A`, `Q`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **Should `build.py` be split into smaller, more focused modules?**
  _Cohesion score 0.061683599419448475 - nodes in this community are weakly interconnected._
- **Why does `Y` connect `Y` to `_`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Should `_` be split into smaller, more focused modules?**
  _Cohesion score 0.06475485661424607 - nodes in this community are weakly interconnected._
- **Why does `b` connect `b` to `_`, `st`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Should `T` be split into smaller, more focused modules?**
  _Cohesion score 0.12612612612612611 - nodes in this community are weakly interconnected._
- **Should `st` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._