---
name: setup
description: This skill should be used when the user asks to "set up project", "configure segmentstream", "which project", "connect to segmentstream", "initialize", "first time setup", "refresh configuration", "reconfigure", or when no `.claude/segmentstream.local.md` settings file exists. Use this skill proactively at the start of a session if no settings file exists. Provides project discovery, configuration caching, and settings management.
user-invocable: true
argument-hint: "[project name or ID (optional)]"
---

# Project Setup

Discover SegmentStream projects accessible to the current API key and cache their configuration locally. The cached settings file eliminates repeated API calls for project metadata and gives every subsequent skill instant access to project IDs, conversion definitions, attribution models, and data source inventories.

## When to Trigger

Activate this skill in any of the following situations:

- **First conversation** -- `.claude/segmentstream.local.md` does not exist in the workspace.
- **Explicit request** -- the user asks to set up, configure, initialize, or connect to SegmentStream.
- **Command invocation** -- the user runs `/segmentstream:setup` or `/segmentstream:refresh`.
- **Stale configuration** -- another skill detects that cached IDs no longer resolve (e.g., a conversion ID returns 404).

## Setup Flow

### Step 0 -- Verify MCP connectivity

Before anything else, confirm the SegmentStream MCP tools are reachable. Use `ToolSearch` with query `"segmentstream"` to check whether any `mcp__segmentstream__*` tools appear.

**If tools are found:** proceed to Step 1.

**If no tools are found:** the MCP server is not connected — the user likely hasn't completed OAuth authentication. Do the following:
1. Tell the user the SegmentStream connector needs to be connected before setup can proceed.
2. Call `mcp__mcp-registry__search_mcp_registry(keywords: ["segmentstream"])` to discover the connector's `directoryUuid`.
3. Call `mcp__mcp-registry__suggest_connectors(uuids: [<directoryUuid>])` to present the Connect button.
4. Stop here. Do not proceed to Step 1 until the user confirms they have connected and authenticated.

### Step 1 -- Check for existing settings

Read `.claude/segmentstream.local.md` in the workspace root. If the file exists and contains valid YAML frontmatter with an `activeProjectId` and `projects` array, one or more projects are already configured. Proceed to Step 2. If the file does not exist, proceed to Step 3 (discovery).

### Step 2 -- Handle existing settings

Check whether the requested project is already cached:

- **Argument provided** (project name or ID): Search the `projects` array for a case-insensitive match on `name` or `id`. If found, set `activeProjectId` to that project's `id` and stop -- no API calls needed, just switch. If not found, proceed to Step 3 to discover and add it.
- **No argument + single cached project**: Inform the user the project is already configured. Ask whether to reconfigure, add another project, or keep the current settings.
- **No argument + multiple cached projects**: Present the cached projects as a numbered list. Ask which one to make active, or whether to add a new one. If the user picks a cached project, update `activeProjectId` and stop.

### Step 3 -- Discover available projects

```
mcp__segmentstream__list_active_projects()
```

This returns all projects the API key has access to. Handle three cases:

| Result | Action |
|--------|--------|
| **Zero projects** | Stop. Guide the user: check that `SEGMENTSTREAM_MCP_URL` is set, the API key is valid, and the account has at least one active project. Suggest running `/mcp` to verify the MCP connection. |
| **One project** | Present the project name and ID. Ask the user to confirm this is the intended project before proceeding. |
| **Multiple projects** | Present a numbered list of projects (name + ID). Ask the user to choose one. If the user ran `/segmentstream:setup <name>`, attempt a case-insensitive match on the project name or ID and confirm. |

### Step 4 -- Fetch project configuration

Once a project is selected, fetch its full configuration in parallel:

```
mcp__segmentstream__get_project(projectId)
mcp__segmentstream__list_conversions(projectId)
mcp__segmentstream__list_attribution_models(projectId)
mcp__segmentstream__list_data_sources(projectId)
```

Extract the following from responses:

- **Project**: `id`, `name`, `defaultCurrency`, `timezone`
- **Conversions**: `id`, `name`, `type` for each conversion
- **Attribution models**: `id`, `name`, `isDefault` for each model
- **Data sources**: `id`, `name`, `type` for each connected source

### Step 5 -- Write the settings file

Build the project entry and update the `projects` array. If the selected project ID already exists in the array, **replace** that entry with the fresh data (this acts as an implicit refresh). If it is a new project, **append** it to the existing array -- do not replace other cached projects. Set `activeProjectId` to the newly added or updated project. Preserve any markdown content below the YAML frontmatter (user notes).

```yaml
---
activeProjectId: "abc123"
projects:
  - id: "abc123"
    name: "My Company"
    defaultCurrency: "USD"
    timezone: "Europe/Berlin"
    attributionModels:
      - id: "model-1"
        name: "ML Attribution"
        isDefault: true
      - id: "model-2"
        name: "First Click"
        isDefault: false
    conversions:
      - id: "conv-1"
        name: "Purchase"
        type: "transaction"
      - id: "conv-2"
        name: "Lead"
        type: "lead"
    dataSources:
      - id: "ds-1"
        name: "Google Ads"
        type: "google_ads"
      - id: "ds-2"
        name: "Meta Ads"
        type: "facebook"
    defaults:
      conversionId: "conv-1"
      attributionModelId: "model-1"
    cachedAt: "2026-03-12T10:00:00Z"
  - id: "def456"
    name: "Another Company"
    defaultCurrency: "EUR"
    timezone: "Europe/London"
    attributionModels: []
    conversions: []
    dataSources: []
    cachedAt: "2026-03-12T10:00:00Z"
---

# Project Notes

Any user-specific notes about this project configuration.
```

**File location**: `.claude/segmentstream.local.md` is gitignored by default (the `.gitignore` in this plugin includes `.claude/*.local.md`). This keeps credentials-adjacent data out of version control.

**YAML rules**:
- Quote all string values.
- Use ISO 8601 for `cachedAt` (per project).
- List items use consistent indentation (2 spaces).
- Keep `attributionModels` sorted with the default model first.
- Keep `conversions` sorted alphabetically by name.

### Step 6 -- Confirm completion

After writing the file, present a summary to the user:

```
Project configured: My Company (abc123) [ACTIVE]
  Currency: USD | Timezone: Europe/Berlin
  Attribution models: 2 (default: ML Attribution)
  Conversions: 5 (Purchase, Lead, Signup, ...)
  Data sources: 3 (Google Ads, Meta Ads, Microsoft Ads)
  Cached at: 2026-03-12T10:00:00Z
```

If other projects are also cached, list them briefly:

```
Other cached projects:
  - Another Company (def456)
```

Suggest next steps based on what was discovered:
- If conversions exist: "Try asking about your campaign performance or ROAS."
- If no conversions yet: "No conversions are configured yet. Set up conversions in SegmentStream before querying attribution data."
- If data sources are connected: "Your data sources are active -- reports should have data."
- If no data sources: "No data sources found. Connect ad platforms in SegmentStream to start ingesting cost data."

## Switching Projects

When multiple projects are cached, the user can switch the active project without re-fetching data. If the user says "switch to Company B" or similar:

1. Search the `projects` array for a case-insensitive match on `name` or `id`.
2. If found, update `activeProjectId` to the matched project's `id` and write the file.
3. Confirm the switch: "Switched active project to Company B (def456)."
4. If not found, suggest running `/segmentstream:setup Company B` to add and configure it.

## Refresh Flow

The refresh flow re-fetches project configuration without re-running discovery. Use when conversions, attribution models, or data sources have changed in SegmentStream.

1. Read `.claude/segmentstream.local.md` and extract `activeProjectId` and the `projects` array from the YAML frontmatter.
2. If no settings file exists, stop and direct the user to run `/segmentstream:setup` first.
3. Determine which project to refresh:
   - If an argument is provided (project name or ID), find the matching project in the `projects` array. If not found, stop and tell the user.
   - If no argument, refresh the active project (the one matching `activeProjectId`).
4. Preserve any markdown content below the YAML frontmatter (user notes).
5. Re-fetch all four endpoints (same as Step 4 above) using the target project's `id`.
6. Replace that project's entry in the `projects` array with the fresh data. Update its `cachedAt` to the current timestamp. Leave all other cached projects untouched.
7. Write the updated file, appending the preserved markdown notes after the frontmatter closing `---`.
8. Compare old and new configurations for the refreshed project. Report changes explicitly:
   - New conversions or attribution models added
   - Removed conversions or data sources
   - Name changes or type changes
   - If nothing changed, say so

## Error Handling

| Error | Response |
|-------|----------|
| SegmentStream MCP tools not found via ToolSearch | The MCP connector is not authenticated. Use `search_mcp_registry` + `suggest_connectors` to guide the user through connecting (see Step 0). Do not attempt any `mcp__segmentstream__*` calls until tools are confirmed available. |
| MCP connection failure (timeout, auth error) | Guide the user to check `SEGMENTSTREAM_MCP_URL` and API credentials. Suggest running `/mcp` to verify the server connection. |
| `list_active_projects` returns empty | The API key may lack project access. Ask the user to verify permissions in SegmentStream settings. |
| `get_project` returns 404 | The cached project ID is stale. Remove the project from the `projects` array and re-run setup. If it was the only project, delete the settings file and start fresh. |
| Partial fetch failure (e.g., conversions OK but data sources fail) | Write what succeeded, note the failure in the summary, and suggest retrying with `/segmentstream:refresh`. |

## Settings File as Context

Other skills read `.claude/segmentstream.local.md` to avoid redundant API calls. The file serves as a lightweight project context that loads instantly at conversation start. Skills should:

- Read the settings file and use `activeProjectId` to find the current project in the `projects` array.
- Use the active project's cached data (conversions, attribution models, data sources) for all operations.
- Fall back to API calls only if the file is missing or the active project's `cachedAt` timestamp is older than 7 days.
- Never modify the settings file directly -- always route through this setup skill or the refresh command.

## Related Commands

- `/segmentstream:setup` -- full discovery and configuration flow
- `/segmentstream:refresh` -- update cached configuration without re-selecting the project
