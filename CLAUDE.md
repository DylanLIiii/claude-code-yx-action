# Introduction

This project aims to build a tool similar to Github Action using the Claude Code SDK, which can perform various operations on code repositories by obtaining information from environment variables and using the Ali YunXiao API. 

- Ali YunXiao is something like Github
- Claude Code SDK is a kind of AI Client

All operations of this tool are performed in the background within the CLI. It can read environment variables.

- 环境变量必须要有
- 组织 ID, 代码库 ID

## Features

- **PR Review**: Automated pull request review using local Git + YunXiao API + Claude Code SDK
  - Analyzes Git diff between branches
  - Posts inline and global comments to YunXiao 
  - Uses Claude Code SDK for intelligent code analysis

# Develop Guide

You should need to use web fetch tool to fetch the content from following URL. 

## Claude Code SDK

- Check How to use Claude Code SDK @docs/CC-SDK-USAGE.md
## Ali YunXiao Usage 
- 服务接入点（domain）: openapi-rdc.aliyuncs.com
- 操作 PR: @docs/yunxiao/PR.md
- 操作 BRANCH: @docs/yunxiao/BRANCH.md

# Environment Variables

Required environment variables for PR review (copy from `.env.example`):

```bash
# Anthropic Claude Code SDK Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here   # Get from https://console.anthropic.com/

# Ali YunXiao API Configuration
ALI_YUNXIAO_TOKEN=pt-0fh3****0fbG_35af****0484  # Personal access token
ALI_YUNXIAO_DOMAIN=openapi-rdc.aliyuncs.com     # API domain (default)
ALI_ORGANIZATION_ID=99d1****71d4                # Your organization ID
ALI_REPOSITORY_ID=2835387                       # Repository ID

# CI Environment (automatically set by most CI/CD systems)
CI_COMMIT_REF_NAME=feature/my-branch            # Current branch name
```

# Usage Examples

## PR Review

Review current branch's PR:
```bash
python -m yx_cc --target-branch master
```

Review specific PR by ID:
```bash
python -m yx_cc --pr-id 123
```

# General Coding Rule 

### Core Principles (in order of priority)

1. **Minimal Change** – Do only what’s needed to satisfy the request.
2. **Preserve Structure** – Don’t rename, refactor, or reorganize unless explicitly told to.
3. **Single Task Focus** – Solve only the stated problem; no unsolicited “improvements.”
4. **Ask When Unsure** – If anything is ambiguous, ask questions instead of guessing.
5. **Rigor is Paramount** – Every choice (algorithm, data structure, pattern, library) must be justified and verifiable. Provide evidence: tests, assertions, analysis, or proofs. Show a clear chain from problem → design → implementation → verification.
6. **Honesty About Completeness** – If a full solution is impossible (missing specs, unclear APIs, etc.), don’t fake completeness. Deliver a defensible partial solution, state what’s missing, why, and next steps.

---

### Coding Guidelines (Python/ML Context)

- Use the project’s existing style and naming patterns. Keep variable names clear but not over-engineered.
- Keep imports and file layout as-is, unless the task explicitly requires changes.

**Avoid unless explicitly requested or strictly necessary for this task:**

- Extra error handling or logging
- Adding type hints where they don’t already exist
- Performance optimizations not asked for
- New configs/classes/abstractions “just in case”

---

### Deliverable Pattern (Recommended)

1. **Clarifications (if needed)**
2. **Plan of Minimal Changes**
3. **Implementation (only what was planned)**
4. **Verification Evidence (tests/checks/analysis)**
5. **Known Limitations & Next Steps (if any)**