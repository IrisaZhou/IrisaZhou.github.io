---
layout: page
title: What Works vs. What Doesn't Work
permalink: /code-agent/what-works/
nav: false
_styles: >
  .post-header { display: none; }
---

<h2 class="research-section-header">What Works vs. What Doesn't Work</h2>

<div class="row">
<div class="col-md-8 col-lg-9" markdown="1">

## Do's

1. Use sequence words:

- "Do this, then that"
- Use numbered list: 1, 2, 3

The key is to directly tell the AI where the task boundaries are.

2. At the start of each session, explicitly ask it to read `CLAUDE.md`, `CODEX.md`, or `AGENTS.md`.
   <small class="text-muted">Although it says it will automatically read, my experience is that sometimes it randomly stops reading it.</small>

3. Read the "state" your code agent tells you.

- check what it says it is doing
- interrupt early if it goes off in a weird direction
- reduce error cost and token use

## Don'ts

This is the hiccups that eat up your tokens.

1. Access issues.
   <small class="text-muted">It may try again and again and burn tokens while blocked by access restrictions, by restrictions you set yourself, or by some boundary. The solution is not full access; it is to specify in `Claude.md` or `agents.md` not to retry so many times.</small>

2. Missing plugins.
   <small class="text-muted">It may keep trying different ways to work around the missing plugin before asking whether you want to install it.</small>

</div>
<div class="col-md-4 col-lg-3 d-none d-md-block">
{% include claude-code-toc.html %}
</div>
</div>
