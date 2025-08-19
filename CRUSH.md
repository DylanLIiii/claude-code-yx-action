# Build & Development Commands

## Core Commands
- `python -m yx_cc --target-branch master` - Run PR review for current branch
- `python -m yx_cc --pr-id 123` - Review specific PR by ID
- `uv sync` - Install dependencies
- `uv run python -m yx_cc ...` - Run with uv

## Code Style Guidelines

### Python Conventions
- Use existing patterns and naming conventions from the codebase
- Follow async/await patterns for API calls
- Use loguru for logging with appropriate levels (debug, info, warning, error)
- Type hints are used sparingly - follow existing minimal approach
- Exception handling should be specific and include logging

### Imports & Structure
- Group imports: standard library, third-party, local modules
- Use relative imports for internal modules (`from .core import ...`)
- Async functions should be named with `async_` prefix when needed
- Class names use PascalCase, methods and functions use snake_case

### Error Handling
- Always log exceptions with context using loguru
- Use try/catch blocks for external API calls
- Raise ValueError for configuration/missing environment issues
- Include meaningful error messages for debugging

### API Integration Patterns
- Use environment variables for configuration (ALI_YUNXIAO_TOKEN, etc.)
- Timeout all HTTP requests (30s default)
- Log request/response details at debug level
- Handle JSON parsing errors gracefully

### Testing & Verification
- No test framework currently configured
- Manual testing via CLI commands with real PR data
- JSON responses are dumped to ./tmp/ for inspection