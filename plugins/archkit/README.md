# archkit (plugin)

Architecture intelligence — scan, design, ADR, drift check, deterministic verifier.

## Layout

```
plugins/archkit/
  .claude-plugin/plugin.json   ← Claude Code plugin manifest
  skills/<name>/SKILL.md       ← Claude skills (5 of them)
  gemini-extension.json        ← Gemini CLI extension manifest
  gemini-commands/*.toml       ← Gemini CLI custom commands (mirrors Claude skills)
  README.md
```

Both wrappers reference the same canonical content at the repo root:

```
.archkit/        ← prompts, strategy, templates, commandments
archkit/         ← Python verifier (deterministic backbone)
```

## Install — Claude Code

```
/plugin marketplace add Komentis/ArcKit
/plugin install archkit
```

The five `/arch-*` slash commands become available.

## Install — Gemini CLI

```
gemini extensions install <path-to-this-folder>
```

The same five commands become available as Gemini custom commands.

## Verify

The deterministic verifier is tool-agnostic and runs from the repo root regardless of which agent ran the scan:

```
python -m archkit verify docs/
```

See [../../archkit/README.md](../../archkit/README.md) for the full check list.
