---
layout: page
title: Getting Started with Code Agents for Economists
permalink: /teaching/code-agents/
nav: false
_styles: >
  .post-header { display: none; }
---

<h2 class="research-section-header">Getting Started with Code Agents for Junior Economists</h2>

This page is a personal guide to using AI code agents as a junior economist — not from the perspective of a seasoned researcher with deep domain expertise, but from someone learning both economics and AI tooling at the same time. My goal is to share what actually works (and what doesn't) when integrating code agents into an economics research workflow, based on my own hands-on experience. If you're early in your PhD and want to use AI to get more done without yet having a strong command of the literature or a highly specialized skill set, this is for you. A note upfront: all of the content here is produced from my own input with the help of code agents.

Two resources that have helped me a great deal are [Claude Blattman](https://claudeblattman.com/) and the [claude-howto](https://github.com/luongnv89/claude-howto) guide on GitHub. Both are written primarily with Claude in mind, but in practice I have found they translate very naturally to Copilot, Cursor, and Codex as well — the underlying ideas carry across tools. That said, my personal experience has been that working with Claude Code (Claude's terminal-based agent) and GPT via Codex is noticeably better than using Copilot. Copilot is genuinely useful, especially because the student plan is free, and that access was invaluable when I hit my usage limits on Claude and GPT — so I do not want to dismiss it. But as a day-to-day research companion, the former two have worked much better for me.

<div class="alert alert-info" role="alert" markdown="1">

**My background when I share this:**

- Primarily Mac user, but sometimes use Windows for large dataset handling
- Finishing my PhD in Economics
- Claude Pro plan
- GitHub Copilot — Student Free Version
- Cursor Pro plan

</div>

**On this page:**

1. [Setting up the environment](#setting-up-the-environment)
2. [Understanding the basics in under three minutes](#understanding-the-basics-in-under-three-minutes)
3. [What works](#what-works)
4. [What doesn't work](#what-doesnt-work)
5. [Useful tools and additions that complement code agents](#useful-tools-and-additions-that-complement-code-agents)
6. [A typical example of my research flow](#a-typical-example-of-my-research-flow)

---

## Setting up the environment

The best starting point is a chat-based AI interface: [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com). I list these three because they are the ones I have used extensively — but I imagine any comparable tool would work just as well. You do not need a code agent right away; getting comfortable with conversational AI first goes a long way.

That said, there are three things I would not use AI without:

1. **VS Code or Cursor** — a proper code editor makes it much easier to review what the agent is actually doing to your files.
2. **Basic familiarity with GitHub** — version control is not optional; learn the basics [here](/teaching/git-and-terminal/). It is your safety net.
3. **A local folder that is fully Git-backed** — only ever point the agent at a folder that is tracked by a repository. Never give it access to anything you have not committed.

<div class="alert alert-danger" role="alert" markdown="1">
<strong style="color: darkred;">AI can and will make mistakes. To fully maximize its capacity, sometimes we need to allow it to make a lot of changes. 99% of these changes are desirable — but 1% can be disastrous. If you are not willing to back up your work with GitHub, I would not use a code agent at all.</strong>
</div>

#### Setting up Claude Code on Mac (terminal)

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

## What works

_Coming soon._

## What doesn't work

_Coming soon._

## Useful tools and additions that complement code agents

_Coming soon._

## A typical example of my research flow

_Coming soon._
