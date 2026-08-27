# Irisa Zhou

Personal academic website for Irisa Zhou, an economist and Ph.D. candidate at the University of Toronto.

## Local development

```bash
docker compose up --build
```

Open <http://localhost:8080>.

## Checks

```bash
npm ci
npx prettier . --check
docker compose run --rm site bundle exec jekyll build
```
