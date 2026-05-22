---
layout: page
title: Getting Started
permalink: /code-agent/getting-started/
nav: false
_styles: >
  .post-header { display: none; }
---

<h2 class="research-section-header">Getting Started</h2>

<div class="row">
<div class="col-md-8 col-lg-9" markdown="1">

The best starting point is a chat-based AI interface: [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com). I list these three because they are the ones I have used extensively — but I imagine any comparable tool would work just as well. You do not need a code agent right away; getting comfortable with conversational AI first goes a long way.

That said, there are three things I would not use AI without:

1. **VS Code or Cursor** — a proper code editor makes it much easier to review what the agent is actually doing to your files.
2. **Basic familiarity with GitHub** — version control is not optional; learn the basics [here](/teaching/git-and-terminal/). It is your safety net.
3. **A local folder that is fully Git-backed** — only ever point the agent at a folder that is tracked by a repository. Never give it access to anything you have not committed.

<div class="alert alert-danger" role="alert" markdown="1">
<strong style="color: darkred;">AI can and will make mistakes. To fully maximize its capacity, sometimes we need to allow it to make a lot of changes. 99% of these changes are desirable — but 1% can be disastrous. If you are not willing to back up your work with GitHub, I would not use a code agent at all.</strong>
</div>

## Setting up Claude Code on Mac (terminal)

**Prerequisites:** [Homebrew](https://brew.sh) and Node.js. If you do not have Node.js yet:

```bash
brew install node
```

**Step 1 — Install Claude Code:**

```bash
npm install -g @anthropic-ai/claude-code
```

**Step 2 — Navigate to your project folder:**

```bash
cd /path/to/your/project
```

**Step 3 — Start the agent:**

```bash
claude
```

On first run it will open a browser window to authenticate with your Anthropic account. Once done, you are in an interactive session inside your project folder. Type your instruction in plain English and press Enter.

## Understanding the basics in under three minutes

_Coming soon._

</div>
<div class="col-md-4 col-lg-3 d-none d-md-block">
{% include claude-code-toc.html %}
</div>
</div>
