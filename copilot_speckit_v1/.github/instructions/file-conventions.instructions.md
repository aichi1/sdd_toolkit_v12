---
description: プロジェクトのディレクトリ構造、命名規則、主要ファイルの作成者・更新者、知識ベースの配置、禁止事項。
applyTo: "**"
---

<!-- 注意: *.instructions.md では `@パス` によるファイル参照は展開されない。
     このファイルは単体で意味が通るよう自己完結で記述すること。
     末尾の Detail Reference は「必要なら読みに行くポインタ」であり、自動展開されない。 -->

# File Conventions

## Project Directory Structure
```
project-root/
├── docs/                    # Specs (What): background.md, scope.md, requirements.md, ...
├── skills/                  # Procedures (How): phase-{NN}/SKILL.md
├── outputs/                 # Deliverables: phase-{NN}/*.md, .metadata.json, .validation/
├── eval/                    # Self-evaluation (v6): scenarios/, runs/, history/, summary.csv
├── templates/               # Generation templates: team-roster.json, agents/*.md
├── AGENTS.md                # Project spec (created by init-task)
├── metadata.json            # Machine-readable project state
├── finalization-report.md   # Created by /finalize
└── retrospective.md         # Created by /retrospective
```

## Naming Rules
- **Lowercase, hyphen-separated**: `comparison-table.md` (not `ComparisonTable.md`)
- **Purpose-descriptive**: `background.md` (not `temp.md`, `new.md`)
- **No version suffixes**: use git, not `report-v2.md`
- **No date in filename**: dates go in metadata.json
- **English filenames**: content may be Japanese, filenames should be English
- **Phase numbering**: zero-padded 2-digit (`phase-01`, `phase-02`, ..., `phase-10`)

## Key Files

| File | Created by | Updated by |
|---|---|---|
| `.metadata.json` (per phase) | Builder | Builder (revision), Validator (status) |
| `.validation/report.md` | Validator | Validator (re-check) |
| `metadata.json` (root) | init-task | run-phase, finalize |
| `AGENTS.md` | init-task | Phase completion, finalize |

## Global Knowledge Base: `~/.sdd-knowledge/`
```
├── docs-archive/    # {YYYY-MM-DD}_{category}_{name}/
├── starters/        # {category}/
├── retrospectives/  # {YYYY-MM-DD}_{category}_{name}.json + summary.json
└── config.json
```

## Prohibited
- Temp/backup files in outputs/ (`temp.md`, `old-version.md`)
- Directory depth beyond 3 levels
- Non-sequential phase numbers (no gaps: 01, 03 is invalid)

## Detail Reference
Full structure details, metadata schemas, and cleanup procedures: `docs/rules-reference/file-structure-detail.md`
