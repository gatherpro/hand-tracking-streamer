---
description: Create a new git worktree for an agent to work on a specific issue
---

# Spawn Agent Worktree

Create a new git worktree for an agent to work on their assigned module.

## Usage

```
/spawn <agent_number>
```

## Parameters

- `agent_number`: The agent number (1-5)
  - 1: Camera Capture Module
  - 2: Hand Detection Module
  - 3: Joint Measurement Module
  - 4: Data Sender Module
  - 5: Main Controller Module

## What this command does

1. Creates a new feature branch for the specified agent
2. Makes an initial commit on that branch
3. Pushes the branch to remote
4. Creates a git worktree in the parent directory
5. Creates a TODO.md file in the worktree with agent-specific tasks

## Example

```
/spawn 1
```

This will:
- Create branch: `feature/camera-capture`
- Create worktree: `../agent1-worktree`
- Setup TODO.md for Agent1

## After spawning

The agent should:
1. Navigate to their worktree: `cd ../agent{N}-worktree`
2. Read `AGENTS.md` to understand their role
3. Check `TODO.md` for specific tasks
4. Start implementing their module
