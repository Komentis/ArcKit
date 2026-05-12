# techlead (placeholder)

Reserved for the Tech Lead orchestrator plugin — cross-stack feature coordination, BFF contract drafting, sub-agent steering through the Spec Kit flow.

## Expected layout (when populated)

```
plugins/techlead/
  .claude-plugin/plugin.json
  skills/
    tech-lead-orchestrator/SKILL.md
    techlead.specify/SKILL.md
  gemini-extension.json
  gemini-commands/
    tech-lead-orchestrator.toml
    techlead.specify.toml
  README.md
```

Mirror the `archkit` plugin's pattern: Claude wrapper + Gemini wrapper around a single canonical skill body.

## Next steps

Drop your existing tech-lead skill files in here and add an entry to [../../.claude-plugin/marketplace.json](../../.claude-plugin/marketplace.json):

```json
{
  "name": "techlead",
  "source": "./plugins/techlead",
  "description": "Cross-stack feature coordination across UI and Platform."
}
```
