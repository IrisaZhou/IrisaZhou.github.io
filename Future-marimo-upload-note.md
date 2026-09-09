update: 2026/09/08

The GitHub Actions approach is feasible and is now live.

The workflow builds the existing Jekyll site first, exports every marimo notebook into the finished `_site` directory, and deploys them together through GitHub Pages. This follows marimo’s [GitHub Pages recommendation](https://marimo.io/blog/wasm-github-pages) and [official template](https://github.com/marimo-team/marimo-gh-pages-template).

Live pages:

- [E402 materials](https://www.irisazhou.com/teaching/e402/)
- [Topic 1: AR/MA models](https://www.irisazhou.com/assets/marimo/e402/ar-ma-models/)

I verified the notebook in Chrome: it loaded the CSV, estimated the model, produced the forecast, reached the conclusion, and reported no browser exceptions.

Changes made:

- Added the marimo export step to [.github/workflows/deploy.yml](C:/Users/izhou/Documents/IrisaZhou.github.io/.github/workflows/deploy.yml)
- Moved the source notebook to [apps/e402/ar-ma-models.py](C:/Users/izhou/Documents/IrisaZhou.github.io/apps/e402/ar-ma-models.py)
- Placed the dataset at [apps/e402/public/FYGDP.csv](C:/Users/izhou/Documents/IrisaZhou.github.io/apps/e402/public/FYGDP.csv)
- Updated [\_pages/e402.md](C:/Users/izhou/Documents/IrisaZhou.github.io/_pages/e402.md)
- Removed the large generated bundle from Git
- Added notebook instructions in [apps/README.md](C:/Users/izhou/Documents/IrisaZhou.github.io/apps/README.md)

Commit `3c66a5a` was pushed to `main`. Both GitHub Actions workflows passed.

GitHub settings

No manual change is currently necessary—the successful deployment confirms that your Pages configuration is already working.

For reference, the relevant setting is:

`Repository → Settings → Pages → Build and deployment → Source: GitHub Actions`

Keep the existing custom-domain settings unchanged.

Adding future notebooks

1. Put the marimo source under `apps/`, for example:

   ```text
   apps/e402/topic-2.py
   ```

2. Keep the inline dependency block at the beginning of the notebook:

   ```python
   # /// script
   # requires-python = ">=3.11"
   # dependencies = [
   #     "marimo",
   #     "pandas",
   # ]
   # ///
   ```

3. Put local data beside the notebook in its `public` directory:

   ```text
   apps/e402/public/my-data.csv
   ```

4. Load browser-side data using the same `pyfetch` pattern found in the AR/MA notebook. This avoids the GitHub Pages CSV compression problem we encountered.
5. Add the page link to the relevant Markdown page. A notebook at:

   ```text
   apps/e402/topic-2.py
   ```

   is automatically published at:

   ```text
   /assets/marimo/e402/topic-2/
   ```

6. Run the required checks, then commit and push:

   ```powershell
   $env:Path = 'C:\Users\izhou\node-v24.20.0-win-x64;' + $env:Path
   npx prettier . --write
   npx prettier . --check
   docker compose run --rm site bundle exec jekyll build
   git add .
   git commit -m "add E402 topic 2 notebook"
   git push
   ```

You no longer need to run `marimo export html-wasm` locally or commit an `output_dir`; GitHub Actions handles that automatically.
