# Repository guide

This repository contains only Irisa Zhou's personal academic website.

## Structure

- `_pages/`: site content
- `_layouts/` and `_includes/`: the shared Jekyll shell
- `assets/css/main.scss`: all site styles
- `assets/js/theme.js`: dark-mode behavior
- `assets/img/`: images used by the retained pages

Do not reintroduce al-folio demo content, unused plugins, or unrelated portfolio features.

## Required checks

After editing, run:

```bash
npx prettier . --write
npx prettier . --check
docker compose run --rm site bundle exec jekyll build
```

Remember, if you are on windows PC and cannot find npx:

```Shell
PS C:\Users\izhou\Documents\IrisaZhou.github.io> where.exe npx
C:\Users\izhou\node-v24.20.0-win-x64\npx
C:\Users\izhou\node-v24.20.0-win-x64\npx.cmd
```

For local preview, run `docker compose up --build` and open [http://localhost:8080](http://localhost:8080).
