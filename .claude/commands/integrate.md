---
description: Integrate completed agent work into main branch
---

# Integrate Agent Work

Merge completed agent work from feature branches into the main branch.

## Usage

```
/integrate <agent_number>
```

Or integrate all completed agents:

```
/integrate all
```

## Parameters

- `agent_number`: The agent number (1-5) or "all"

## What this command does

1. Checks if the agent's tests are passing
2. Reviews the changes
3. Creates or updates a pull request
4. If approved, merges the PR into main
5. Updates other agents' branches if needed

## Prerequisites

Before integrating, ensure:
- [ ] All tests pass
- [ ] Code is reviewed
- [ ] Documentation is complete
- [ ] No conflicts with main branch

## Example

```
/integrate 1
```

This will integrate Agent1's camera capture module into main.
