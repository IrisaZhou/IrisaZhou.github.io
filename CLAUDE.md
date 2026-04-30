# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Site Is

Academic personal website for Irisa Zhou (PhD candidate, Economics, University of Toronto). Built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Hosted at `https://irisazhou.github.io`.

The site has four navigation tabs: **Home**, **Research**, **Teaching**, **Misc.**

Legacy HTML exports of the original Google Sites pages are in `legacy/` and serve as the content source of truth.

## Local Development

Docker is required (no local Ruby/Python setup):

```bash
docker compose pull && docker compose up   # start dev server at http://localhost:8080
docker compose up --build                  # rebuild after dependency changes
docker compose down                        # stop and free port 8080
```

Without Docker (requires Ruby + ImageMagick installed locally):

```bash
bundle install
bundle exec jekyll serve --port 4000
```

## Before Committing

```bash
npm install --save-dev prettier @shopify/prettier-plugin-liquid
npx prettier . --write
```

The CI `prettier.yml` workflow will fail PRs that are not formatted.

## Key Files for Content Editing

| What to change | File |
|---|---|
| Bio, intro, homepage research section | `_pages/about.md` |
| Research tab content | `_pages/research.md` |
| Teaching tab content | `_pages/teaching.md` |
| Misc tab content | `_pages/misc.md` |
| Bibliography (unused in nav, but powers search) | `_bibliography/papers.bib` |
| Site-wide settings (name, url, analytics) | `_config.yml` |
| Social links (email, GitHub, LinkedIn) | `_data/socials.yml` |
| Profile photo | `assets/img/Irisa_crop.jpeg` |

## Navigation Order

Pages appear in the navbar when `nav: true` is set in their frontmatter. Order is controlled by `nav_order`. Current order:

- Home (`/`) — `about.md`, always first
- Research (`nav_order: 2`) — `_pages/research.md`
- Teaching (`nav_order: 3`) — `_pages/teaching.md`
- Misc. (`nav_order: 4`) — `_pages/misc.md`

All other pages (`publications`, `projects`, `blog`, `cv`, `books`, `repositories`, `profiles`) are hidden (`nav: false`).

## Scholar / Bibliography Config

`_config.yml` sets `scholar.last_name: [Zhou]` to highlight Irisa's name in bibliography entries. The `_bibliography/papers.bib` file contains her papers. The `/publications/` page is hidden from nav but is indexed by site search.

## Architecture Notes

- `_layouts/about.liquid` controls the homepage layout. To add sections (announcements, latest posts, selected papers) enable them in `about.md` frontmatter.
- `_includes/` contains reusable Liquid components (news, courses, selected papers, social links, etc.).
- `_data/socials.yml` drives the social icons rendered at the bottom of the homepage via `{% social_links %}`.
- The `_teachings/` collection is wired up but currently empty — add `.md` files there (with `layout: course`) to populate the Teaching page.
- ImageMagick is required for the build (handles responsive WebP image generation). It is pre-installed in the Docker image.

## Common Pitfalls

- Special characters in `_config.yml` values must be quoted: `title: "My: Site"`.
- `url` and `baseurl` in `_config.yml` must be consistent — for a user page (`username.github.io`) set `baseurl:` to empty.
- The CI deploy workflow (`deploy.yml`) pushes the built site to `gh-pages` branch. GitHub Pages source must be set to that branch in repo Settings → Pages.
- Do not set `toc_enabled` in `_config.yml` — it is not a valid al-folio key and will break the build.
