---
layout: page
title: My Sample Workflow
permalink: /code-agent/sample-workflow/
nav: false
_styles: >
  .post-header { display: none; }
  pre { white-space: pre-wrap; word-break: break-word; overflow-x: auto; }
---

<h2 class="research-section-header">My Sample Workflow</h2>

<div class="row">
<div class="col-md-8 col-lg-9" markdown="1">

Three modes, depending on the task.

---

## 1. Light Tasks

Single prompt, no back-and-forth.

- Fix a Python graph so the y-axis range starts at 0
- Remove all LaTeX figure titles from a `.tex` file
- Delete all empty lines in a file

**Characteristics:** lightweight · well-defined · specific

---

## 2. Structured but Multi-Step Tasks

For tasks that need planning before any code is written — e.g. building a data cleaning pipeline.

**Step 1 — Dump all requirements to the agent using the Plan skill.** Or draft the plan in a chat interface first, then hand it off to the agent.

The goal is a `plan.md` the agent can execute locally:

```text
You are helping me build a data cleaning pipeline in Python for a panel dataset.
Here is what I need: [list your requirements].
Do not write any code yet. Produce a structured plan as a markdown file called
plan.md. Break the work into numbered steps, flag decisions I need to make, and
note any assumptions.
```

**Step 2 — Review the plan, resolve any open decisions, then tell the agent to execute.**

---

## 3. Unstructured Idea Bouncing

For half-formed hypotheses you want to think through before committing to a structure.

**Example:** "My hypothesis is X. I want to test it with Y. What do you think?"

- **Set the persona first.** One line: who should the AI be? (e.g., "You are an empirical economist specializing in labor markets"). For a local agent, add it to `CLAUDE.md`. Always include **"Do not execute anything"** to keep it in discussion mode.
- **Iterate.** Poke at assumptions, refine the approach. Once things are concrete, you have a plan — go to Section 2.

---

## A Note on Auditing

Be specific. Be suspicious. Push back.

I code badly, and sometimes I cannot audit all the code AI generates. What I do instead:

- Run tests to verify the output behaves as intended
- Ask for the same thing in different wording and compare results
- Paste the code into a separate session — or a different AI — and ask whether it does what you want

**The best way to critique AI output is with another AI.**

</div>
<div class="col-md-4 col-lg-3 d-none d-md-block">
{% include claude-code-toc.html %}
</div>
</div>
