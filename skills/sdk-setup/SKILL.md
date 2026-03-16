---
name: sdk-setup
description: "Prepare and customize the SegmentStream SDK tracking snippet for a client website. Use when the user asks to 'prepare tracking code', 'install SDK', 'generate snippet', 'set up tracking', 'configure SDK modules', 'SDK installation', or any request about adding SegmentStream tracking to a website. Guides through module selection, installation method, and conversion tracking setup."
---

# SDK Setup

Prepare a customized SegmentStream SDK tracking snippet for installation on a client website. The SDK has configurable modules controlled via `window.segmentstream_sdk_settings` -- this skill walks through each module with the user before generating the final snippet.

## Critical Rule

**Never hardcode the SDK snippet template, module names, or default values in this skill.** The base snippet and configurable modules must always be fetched from docs at runtime because the documentation may be updated.

## Docs URL

```
https://docs.segmentstream.com/project-configuration/sdk
```

Fetch this page via `WebFetch` at the start of every tracking code preparation session. Parse the page to extract:
1. The base SDK snippet (the `<script>` block)
2. The list of `window.segmentstream_sdk_settings` parameters, their descriptions, and default values

## Workflow

### Step 1 -- Resolve project

Look up the project using `list_active_projects()`. If the project is already cached in `.claude/segmentstream.local.md`, use the cached `activeProjectId`. The project ID is needed for the snippet.

### Step 2 -- Fetch current SDK docs

```
WebFetch("https://docs.segmentstream.com/project-configuration/sdk")
```

Parse the response to extract:
- The base `<script>` snippet with the `apiKey` placeholder
- All `window.segmentstream_sdk_settings` parameters, including:
  - Parameter name
  - Description / what it controls
  - Default value (enabled or disabled)

If the fetch fails, inform the user and suggest they provide the docs content manually.

### Step 3 -- Ask about installation method

Present two options:
1. **Direct HTML** -- paste the snippet into the `<head>` section of every page
2. **Google Tag Manager (GTM)** -- add as a Custom HTML tag

This affects the output format (GTM requires wrapping in a Custom HTML tag with specific trigger configuration).

### Step 4 -- Ask about conversion tracking

Ask whether the user needs conversion tracking (e-commerce or custom events). If yes, note that conversion tracking code will be appended after the base snippet. Fetch conversion tracking details from the same docs page.

### Step 5 -- Walk through each SDK module

For **each** configurable parameter found in Step 2, ask the user whether to enable or disable it. Present:
- The parameter name
- What it does (from docs)
- The default value
- A recommendation if appropriate (e.g., bot tracking and non-idle tracking are usually unnecessary for most clients)

Ask about modules **one group at a time** (not all at once) to avoid overwhelming the user. Group logically (e.g., data collection modules, storage modules, behavioral modules).

**Do not assume defaults.** The user must explicitly confirm each module choice. This prevents the process violation where all modules are enabled by default and the user has to manually disable unwanted ones.

### Step 6 -- Generate the customized snippet

Assemble the final snippet:
1. Start with the base `<script>` block from docs, inserting the project's API key
2. Add `window.segmentstream_sdk_settings` with only the parameters the user chose to change from defaults
3. If conversion tracking was requested, append the conversion tracking code
4. If GTM was selected, wrap in GTM Custom HTML tag format

Present the complete snippet to the user for review.

### Step 7 -- Save the artifact

Save the finalized snippet to:
```
.artifacts/<client-name>/sdk-tracking-snippet.html
```

If the client name is not known, ask the user. Include a comment header in the file with:
- Client name
- Project ID
- Date generated
- Modules enabled/disabled

## Output Format

The saved artifact should be a complete, copy-pasteable HTML file:

```html
<!--
  SegmentStream SDK Tracking Snippet
  Client: <client-name>
  Project ID: <project-id>
  Generated: <date>
  Modules: <summary of enabled/disabled>
-->

<!-- SDK settings (customized) -->
<script>
  window.segmentstream_sdk_settings = {
    // only non-default settings listed here
  };
</script>

<!-- SegmentStream SDK -->
<script>
  // base snippet from docs with API key
</script>
```

## Error Handling

| Error | Response |
|-------|----------|
| Docs fetch fails | Inform user. Ask them to provide the SDK docs content or try again later. |
| No active project found | Direct user to run `/segmentstream:setup` first. |
| User unsure about a module | Explain what the module does in plain language. If still unsure, suggest keeping the default. |
