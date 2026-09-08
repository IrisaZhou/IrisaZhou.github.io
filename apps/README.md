# Read-only marimo notebooks

GitHub Actions exports every Python notebook under `apps/` as a read-only
WebAssembly app. The source path determines the public URL:

```text
apps/<section>/<notebook>.py
  -> /assets/marimo/<section>/<notebook>/
```

Keep notebook dependencies in the inline script metadata at the top of each
notebook. Put data and other local assets in a `public/` directory beside the
notebook, and access them with `mo.notebook_location()`.

Do not commit generated `html-wasm` output. The deployment workflow creates it
inside `_site` after Jekyll builds the main website.
