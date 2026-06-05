---
layout: page
title: File & Folder Setup
permalink: /code-agent/file-setup/
nav: false
_styles: >
  .post-header { display: none; }
---

<h2 class="research-section-header">File & Folder Setup</h2>

<div class="row">
<div class="col-md-8 col-lg-9" markdown="1">

My setup has two parts: a local project folder tracked by GitHub, and a data folder in Dropbox linked into that project via a symlink. The agent only ever touches the Git-backed folder — data stays in Dropbox and is never committed.

---

## 1. Clone an existing GitHub repo locally

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

If you want it in a specific location:

```bash
git clone https://github.com/your-username/your-repo.git ~/Projects/your-repo
```

### Set your Git identity (first time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Drop `--global` to set it only for the current repo.

---

## 2. Create a symlink to your Dropbox data folder

The symlink lives inside your project folder but points to wherever your data actually is.

```bash
ln -s ~/Dropbox/your-data-folder ~/Projects/your-repo/data
```

`data` now appears inside your project but Git ignores it entirely — see Step 3.

---

## 3. Set up `.gitignore`

Download the template below and save it as `.gitignore` in your repo root. It covers symlinked data folders, macOS and Windows system files, LaTeX auxiliary files, and Python virtual environments.

<a href="/assets/downloads/sample-gitignore.txt" download=".gitignore" class="btn btn-sm btn-outline-secondary">Download .gitignore template</a>

Or generate it manually:

```bash
curl -o .gitignore https://irisazhou.github.io/assets/downloads/sample-gitignore.txt
```

What it ignores:

- `data/`, `auxiliary/` — symlinked or local folders you never want committed
- `.DS_Store`, `._*`, `Thumbs.db`, `Desktop.ini` — OS clutter
- `*.aux`, `*.log`, `*.bbl`, `*.synctex.gz`, … — LaTeX build artifacts
- `__pycache__/`, `venv/`, `.venv/`, `.ipynb_checkpoints/` — Python environments and notebooks

---

## The result

```
your-repo/
├── code/
├── output/
├── data -> ~/Dropbox/your-data-folder   ← symlink, not tracked
└── .gitignore
```

The agent sees `data/` as a normal folder. Git ignores it entirely.

</div>
<div class="col-md-4 col-lg-3 d-none d-md-block">
{% include claude-code-toc.html %}
</div>
</div>
