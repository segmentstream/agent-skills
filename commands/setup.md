---
name: setup
description: Discover SegmentStream projects and configure the plugin for the current workspace. Run this on first use or when adding/switching projects.
argument-hint: "[project name or ID (optional)]"
allowed-tools: ["Read", "Write", "Edit", "mcp__segmentstream__list_active_projects", "mcp__segmentstream__get_project", "mcp__segmentstream__list_conversions", "mcp__segmentstream__list_attribution_models", "mcp__segmentstream__list_data_sources"]
---

Load the `setup` skill for the full project setup flow.

## Instructions

1. Check if `.claude/segmentstream.local.md` exists by reading the file.

2. **If settings exist and an argument was provided**: Search the `projects` array for a case-insensitive match on `name` or `id`. If found, set `activeProjectId` to that project's `id`, write the file, confirm the switch, and stop -- no API calls needed. If not found, proceed to step 3 to discover and add it.

3. **If settings exist and no argument was provided**: Check how many projects are cached.
   - **Single project**: Inform the user it is already configured. Ask whether to reconfigure, add another project, or keep the current settings.
   - **Multiple projects**: Present a numbered list of cached projects. Ask which to make active, or whether to add a new one. If the user picks a cached project, update `activeProjectId` and stop.

4. Call `mcp__segmentstream__list_active_projects()` to discover all accessible projects.

5. Handle the result:
   - **Zero projects**: Stop. Tell the user no projects were found and suggest checking API credentials and MCP connection.
   - **One project**: Present it and ask the user to confirm.
   - **Multiple projects**: If an argument was provided, match it case-insensitively against project names and IDs. If a match is found, confirm with the user. If no match or no argument, present a numbered list and ask the user to choose.

6. Once a project is confirmed, fetch its configuration in parallel:
   - `mcp__segmentstream__get_project(projectId)`
   - `mcp__segmentstream__list_conversions(projectId)`
   - `mcp__segmentstream__list_attribution_models(projectId)`
   - `mcp__segmentstream__list_data_sources(projectId)`

7. Build the project entry and update the `projects` array. If the project ID already exists in the array, **replace** that entry with fresh data (implicit refresh). If it is a new project, **append** it -- preserve other cached projects. Set `activeProjectId` to the newly added project. Preserve any markdown content below the YAML frontmatter. Write the file following the multi-project format defined in the setup skill.

8. Present a summary of what was configured: project name (marked as ACTIVE), currency, timezone, number of attribution models (noting which is default), number of conversions (listing names), and number of data sources (listing platforms). If other projects are cached, list them briefly. Suggest relevant next steps based on the project state.
