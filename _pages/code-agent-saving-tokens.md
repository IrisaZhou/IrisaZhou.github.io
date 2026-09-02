---
layout: page
title: Saving Tokens in My Process
permalink: /code-agent/saving-tokens/
nav: false
_styles: >
  .post-header { display: none; }
---

<h2 class="research-section-header">Saving Tokens in My Process</h2>

<div class="row">
<div class="col-md-8 col-lg-9" markdown="1">

1. Break tasks down by difficulty and steps. Categorize each part by reasoning effort and model selection.

   1. My experience: always use the latest model. But, for example, for Codex:

      1. Use 5.6 Sol to write prompts, reason back and forth, and do more textual work.
      2. Use 5.6 Luna to write the actual code for execution.
   2. My default level of reasoning effort is set to Medium. I have never encountered a time when it did not get the job done right given clear instructions. In fact, for the couple of times that I thought the task was difficult and selected a higher effort, Codex actually got things done wrong with extremely large token usage.
   3. In my own experience, 5.6 Sol is extremely token-consuming and can get things done right, but most of the time, e.g., using Codex to write an entire script to solve a first-year PhD Macro model, is a complete waste of Sol (hence, tokens).

2. Inside files (at least in VS Code), if I just want to edit a few lines, I always use the Modify function inside (this links to GitHub Copilot). Most institutions have a separate Copilot subscription. This way, small tasks do not burn your Codex tokens.

3. I never write full sentences (which leads to a degradation of my English grammar, I'll have to admit) and difficult words. You never want the model spend tokens trying to (overly) interpret what you meant. 
</div>
<div class="col-md-4 col-lg-3 d-none d-md-block">
{% include claude-code-toc.html %}
</div>
</div>
