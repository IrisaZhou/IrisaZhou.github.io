---
layout: page
title: Git & Terminal Basics
permalink: /teaching/git-and-terminal/
nav: false
_styles: >
  .post-header { display: none; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
  th, td { padding: 0.5rem 0.75rem; border: 1px solid #dee2e6; vertical-align: top; }
  th { background-color: #f8f9fa; font-weight: 600; }
---

## Git & Terminal Basics

A quick reference for the two tools you need before using any code agent. You do not need to memorize these — bookmark this page and come back when you need it.

---

## 1. Basic Git commands

Git tracks changes to your files over time. Every project you work on with a code agent should be inside a Git repository.

| Command                   | What it does                                      | Example                                     |
| ------------------------- | ------------------------------------------------- | ------------------------------------------- |
| `git init`                | Initialize a new repository in the current folder | `git init`                                  |
| `git clone <url>`         | Download a remote repository to your machine      | `git clone https://github.com/you/repo.git` |
| `git status`              | Show which files have been changed or staged      | `git status`                                |
| `git add <file>`          | Stage a file to be included in the next commit    | `git add analysis.do`                       |
| `git add .`               | Stage all changed files at once                   | `git add .`                                 |
| `git commit -m "message"` | Save a snapshot of your staged changes            | `git commit -m "add baseline table"`        |
| `git push`                | Upload your commits to the remote (e.g. GitHub)   | `git push`                                  |
| `git pull`                | Download and merge the latest changes from remote | `git pull`                                  |
| `git log`                 | Show the commit history                           | `git log`                                   |
| `git diff`                | Show unstaged changes line by line                | `git diff`                                  |
| `git branch`              | List all branches                                 | `git branch`                                |
| `git checkout -b <name>`  | Create and switch to a new branch                 | `git checkout -b new-feature`               |
| `git checkout <branch>`   | Switch to an existing branch                      | `git checkout main`                         |
| `git merge <branch>`      | Merge another branch into the current one         | `git merge new-feature`                     |

**Minimal workflow for everyday use:**

```bash
git add .
git commit -m "describe what you changed"
git push
```

---

## 2. Basic terminal commands

These are Mac/Linux (zsh/bash) commands. The terminal is where you run code agents, install tools, and navigate your file system.

| Command           | What it does                                       | Example                           |
| ----------------- | -------------------------------------------------- | --------------------------------- |
| `pwd`             | Print the current directory path                   | `pwd`                             |
| `ls`              | List files in the current directory                | `ls`                              |
| `ls -la`          | List all files including hidden ones, with details | `ls -la`                          |
| `cd <path>`       | Change directory                                   | `cd Documents/my-project`         |
| `cd ..`           | Go up one directory level                          | `cd ..`                           |
| `mkdir <name>`    | Create a new folder                                | `mkdir data`                      |
| `touch <file>`    | Create a new empty file                            | `touch notes.txt`                 |
| `cp <src> <dest>` | Copy a file                                        | `cp table1.tex table1_backup.tex` |
| `mv <src> <dest>` | Move or rename a file                              | `mv draft.do final.do`            |
| `cat <file>`      | Print the contents of a file                       | `cat config.yml`                  |
| `open <path>`     | Open a file or folder in Finder                    | `open .`                          |
| `which <tool>`    | Show where a command is installed                  | `which python`                    |
| `echo <text>`     | Print text to the terminal                         | `echo "hello"`                    |
| `clear`           | Clear the terminal screen                          | `clear`                           |

---

<div class="alert alert-danger" role="alert" markdown="1">

### `rm` — Read this before using it

```bash
rm <file>        # delete a file
rm -r <folder>   # delete a folder and everything inside it
```

**`rm` permanently deletes files. There is no Trash. There is no undo.**

Unlike deleting a file in Finder (which sends it to the Trash), `rm` removes the file immediately and irrecoverably from your disk. Running `rm -r` on the wrong folder can wipe out hours or weeks of work in under a second.

**Rules I follow:**

- Never run `rm` unless I am 100% certain what I am deleting.
- Never run `rm -rf` (the `-f` flag forces deletion without any confirmation prompt) unless I have verified the path character by character.
- Always make sure the folder is Git-backed before letting a code agent anywhere near it — agents can and do issue `rm` commands.

If you are not sure, use `mv` to move the file to a temporary folder instead of deleting it. That way you can recover it.

</div>

---

← [Back to Getting Started with Code Agents for Junior Economists](/code-agent/getting-started/)
