# Website Migration Plan

## Goal
Migrate the current website setup in `legacy/` into the new al-folio theme, with a clean academic layout similar in spirit to https://ziqingyan.com/.

## Current Decisions
- Site should be set up as a personal site root for now.
- Final custom domain can be added later.
- Initial live tabs: About/Home, Research, Teaching, Misc.
- Priority is a fast go-live with core pages first; polish can come later.
- Visual target: close, minimalist match to the reference site.
- Use placeholders for images and missing assets for now.

## What Will Be Migrated
- About/Home content from the legacy HTML export.
- Research content, including working papers and work in progress.
- Teaching page content.
- A new Misc. tab in the top navigation.
- Existing PDFs and images will be linked when available, otherwise placeholders will be used.

## What I Need From You
- Profile photo for the home page, or confirmation that a placeholder should be used temporarily.
- Final display name and site title.
- Email address and any social links to show.
- Paper/PDF links or filenames for each research item.
- Teaching content you want live now, if any.
- The actual content you want on the Misc. page.
- Later, the custom domain and DNS details when you are ready to switch.

## Execution Steps
1. Update site-wide configuration in `_config.yml` for the personal-site root setup.
2. Rewrite the homepage in `_pages/about.md` to match the target structure and tone.
3. Create or update a Research page and map legacy research content into al-folio sections.
4. Add a new `_pages/misc.md` page and expose it in the top navigation.
5. Keep Teaching available as a top tab with a minimal first pass.
6. Link placeholders for assets that are not yet provided.
7. Validate the build locally after each major change.
8. Finalize the custom domain switch once the content is in place.

## Notes
- The legacy HTML files are the source of truth for content recovery.
- The repository already has al-folio page templates and nav support, so the work is mostly content/configuration rather than theme surgery.
- I will keep the first pass lightweight so the site can go live sooner, then refine appearance and content density afterward.
