---
name: refresh
description: Re-fetch and update the cached SegmentStream project configuration. Use when conversions, attribution models, or data sources have changed.
argument-hint: "[project name or ID (optional — defaults to active project)]"
allowed-tools: ["Read", "Write", "Edit", "mcp__segmentstream__get_project", "mcp__segmentstream__list_conversions", "mcp__segmentstream__list_attribution_models", "mcp__segmentstream__list_data_sources"]
---

Load the `setup` skill and follow the refresh flow.

## Instructions

1. Read `.claude/segmentstream.local.md` to extract `activeProjectId`, the `projects` array, and all existing configuration from the YAML frontmatter. Also capture any markdown content below the closing `---` of the frontmatter (user notes) -- this must be preserved.

2. If the settings file does not exist, stop and tell the user: "No project is configured yet. Run `/segmentstream:setup` to discover and configure a project first."

3. Determine which project to refresh:
   - If an argument was provided (project name or ID), search the `projects` array for a case-insensitive match. If not found, stop and tell the user that project is not cached -- suggest running `/segmentstream:setup <name>` to add it.
   - If no argument, use the active project (the entry matching `activeProjectId`).

4. Using the target project's `id`, re-fetch all project configuration in parallel:
   - `mcp__segmentstream__get_project(projectId)`
   - `mcp__segmentstream__list_conversions(projectId)`
   - `mcp__segmentstream__list_attribution_models(projectId)`
   - `mcp__segmentstream__list_data_sources(projectId)`

5. If `get_project` returns a 404 or error, the project may have been deleted or the ID is stale. Tell the user and suggest running `/segmentstream:setup` to select a new project.

6. Replace the target project's entry in the `projects` array with the fresh data. Update its `cachedAt` to the current ISO 8601 timestamp. Leave all other cached projects untouched. Write the updated file, appending the preserved markdown notes after the closing `---`.

7. Compare the old configuration (from step 1) with the new configuration (from step 4) for the refreshed project. Report a diff summary to the user:
   - New conversions added (list names)
   - Conversions removed (list names)
   - New attribution models added
   - Attribution models removed
   - New data sources connected (list names and platforms)
   - Data sources removed
   - Default attribution model changed
   - Currency or timezone changed
   - If nothing changed, say "Configuration is up to date -- no changes detected."

8. Show the refreshed project name and the updated `cachedAt` timestamp to confirm the refresh completed.
