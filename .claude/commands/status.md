---
description: Show the status of all agents and their worktrees
---

# Agent Status

Display the current status of all agent worktrees and branches.

## Usage

```
/status
```

## What this command shows

1. List of all worktrees and their branches
2. Current git status for each worktree
3. Recent commits on each branch
4. Which agents have completed their tasks

## Example Output

```
Agent Worktrees Status:
- Agent1 (camera-capture): 3 commits, last: "feat: implement camera initialization"
- Agent2 (hand-detection): 2 commits, last: "feat: add MediaPipe integration"
- Agent3 (joint-measurement): Not started
- Agent4 (data-sender): In progress
- Agent5 (main-controller): Waiting for dependencies
```
