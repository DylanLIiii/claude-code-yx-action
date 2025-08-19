# YX-CC: AI-Powered Code Review Tool

A sophisticated automated code review tool that integrates multiple AI providers (Claude Code SDK and OpenAI API) with Ali YunXiao API to provide intelligent, multi-stage code analysis and review capabilities.

## 🌟 Features

### 🔍 Intelligent PR Review
- **Multi-Stage Analysis**: Three-phase review process (Summary → Analysis → Comments)
- **Multiple AI Providers**: Supports both Claude Code SDK and OpenAI API for flexible AI-powered analysis
- **Smart Caching**: Automatically reuses existing review results to avoid redundant processing
- **Flexible Modes**: Selective review phases (summary, analysis, comments) with configurable modes

### 🚀 Advanced Capabilities
- **Real-time Progress Tracking**: Live updates on review progress with timing metrics
- **Inline Comments**: Precise line-level comments with severity levels (MUST_FIX, SHOULD_FIX, SUGGESTION)
- **PR Description Updates**: Automatically updates PR descriptions with generated summaries
- **Multi-Source Diff**: Prioritizes YunXiao API, falls back to local Git commands
- **JSON Export**: Exports complete review results for audit and analysis

### 🛠️ Technical Excellence
- **Async Processing**: Fully asynchronous for optimal performance
- **Robust Error Handling**: Comprehensive error handling with detailed logging
- **Environment Flexible**: Supports multiple environment variable sources
- **Backward Compatible**: Supports both new JSON and legacy comment formats

## 📦 Installation

### Prerequisites
- Python 3.12+
- Ali YunXiao account with API access
- AI Provider access:
  - **Claude Code SDK**: Anthropic Claude API access, or
  - **OpenAI API**: OpenAI API key with compatible models

### Quick Setup

1. **Clone and install**:
```bash
git clone <repository-url>
cd yx-cc
uv sync
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Verify installation**:
```bash
uv run python -m yx_cc --help
```

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file in your project root or home directory (`~/.yx-cc.env`):

```bash
# AI Provider Configuration (choose one)
# Option 1: Claude Code SDK
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Option 2: OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o  # or any compatible model
OPENAI_BASE_URL=https://api.openai.com/v1  # optional, for custom endpoints

# Ali YunXiao API Configuration
ALI_YUNXIAO_TOKEN=pt-0fh3****0fbG_35af****0484
ALI_YUNXIAO_DOMAIN=openapi-rdc.aliyuncs.com
ALI_ORGANIZATION_ID=your_organization_id_here
ALI_REPOSITORY_ID=your_repository_id_here

# CI/CD Environment (auto-detected in most CI systems)
CI_COMMIT_REF_NAME=feature/your-branch-name
```

### Environment Variable Sources

The tool automatically loads environment variables from:
1. `.env` in current directory
2. `~/.yx-cc.env` in home directory
3. System environment variables

## 🚀 Usage

### Basic PR Review

Review current branch against target branch:
```bash
# Review current branch vs master (all phases)
uv run python -m yx_cc --target-branch master

# Review specific phases only
uv run python -m yx_cc --target-branch master --modes summary analysis

# Force regenerate all phases
uv run python -m yx_cc --target-branch master --force-regenerate
```

### Review Specific PR

```bash
# Review PR by local ID
uv run python -m yx_cc --pr-id 123

# Review specific PR with selective modes
uv run python -m yx_cc --pr-id 123 --modes comments
```

### Available Review Modes

- `summary`: Generate PR summary and update description
- `analysis`: Perform in-depth code quality analysis
- `comments`: Generate line-level code review comments

### Command Line Options

```bash
usage: yx-cc [-h] [--target-branch TARGET_BRANCH] [--pr-id PR_ID]
             [--modes {summary,analysis,comments} [{summary,analysis,comments} ...]]
             [--force-regenerate]

YX-CC PR Review Tool

options:
  -h, --help            show this help message and exit
  --target-branch TARGET_BRANCH
                        Target branch to compare against (default: master)
  --pr-id PR_ID         Specific PR local ID to review
  --modes {summary,analysis,comments} [{summary,analysis,comments} ...]
                        Review modes to run (default: all phases)
  --force-regenerate    Force regeneration of phases even if existing results found
```

## 📊 Review Process

### Phase 1: Summary Generation
- Analyzes Git diff between branches
- Generates comprehensive PR summary
- Updates PR description automatically
- Output: Structured summary with key insights

### Phase 2: Change Analysis  
- Performs deep code quality analysis
- Identifies potential issues and improvements
- Considers security, performance, and maintainability
- Output: Detailed analysis report with recommendations

### Phase 3: Comment Generation
- Generates precise line-level comments
- Categorizes by severity (MUST_FIX, SHOULD_FIX, SUGGESTION)
- Provides specific improvement suggestions
- Output: Inline comments posted directly to PR

## 🏗️ Project Architecture

```
yx-cc/
├── src/yx_cc/
│   ├── core/
│   │   ├── pr_reviewer.py      # Main review orchestrator
│   │   ├── prompt_reader.py    # System prompt management
│   │   ├── output_formatter.py # Result formatting
│   │   └── utils.py           # Utility functions
│   ├── integrations/
│   │   ├── ali_yunxiao.py     # YunXiao API client
│   │   ├── claude_code_runner.py # Claude Code SDK integration
│   │   ├── openai_runner.py   # OpenAI API integration
│   │   └── git_handler.py     # Git operations
│   └── main.py               # CLI entry point
├── config/system_prompts/     # Review prompt templates
└── docs/                     # Documentation
```

## 🔧 Development

### Setup Development Environment
```bash
# Install development dependencies
uv sync --dev

# Run the tool
uv run python -m yx_cc --target-branch master
```

### Code Quality Standards
- **KISS Principle**: Simple, intuitive design
- **YAGNI**: Implement only what's needed now
- **SOLID Principles**: Single responsibility, open/closed, etc.
- **DRY**: Avoid code duplication
- **Async First**: Fully asynchronous for performance

### Testing
```bash
# Run tests (when implemented)
uv run pytest

# Run with coverage
uv run pytest --cov=yx_cc
```

## 📚 API Documentation

### AI Providers

#### Claude Code SDK
- [Official Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk#python-specific-best-practices)
- Python SDK for AI-powered code analysis
- Advanced tool capabilities and context management

#### OpenAI API
- [Official Documentation](https://platform.openai.com/docs/api-reference)
- Direct API integration with OpenAI models
- Supports custom base URLs for compatible endpoints (e.g., Azure OpenAI)

### Ali YunXiao API
- [Official Documentation](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup/)
- Repository management and PR operations

## 🐛 Troubleshooting

### Common Issues

**JSON Parsing Error: "Expecting value: line 3 column 1 (char 4)"**
- This indicates the YunXiao API returned non-JSON response
- Check API credentials and network connectivity
- Verify ALI_YUNXIAO_TOKEN and organization/repository IDs

**Authentication Issues**
- Verify all required environment variables are set
- For Claude Code SDK: Check ANTHROPIC_API_KEY validity
- For OpenAI API: Verify OPENAI_API_KEY and OPENAI_MODEL configuration
- Check Ali YunXiao token validity and permissions
- Ensure organization and repository IDs are correct

**Git Integration Issues**
- Verify Git repository is properly initialized
- Check branch names and permissions
- Ensure CI_COMMIT_REF_NAME is set in CI environments

### Debug Mode
Enable detailed logging by setting log level in your environment:
```bash
export LOGURU_LEVEL=DEBUG
uv run python -m yx_cc --target-branch master
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the coding standards
4. Add tests if applicable
5. Submit a pull request with detailed description

### Development Guidelines
- Follow existing code style and patterns
- Add comprehensive error handling
- Include detailed logging for debugging
- Update documentation as needed

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- [Claude Code SDK](https://docs.anthropic.com/en/docs/claude-code/sdk) for advanced AI-powered code analysis
- [OpenAI API](https://platform.openai.com/docs/api-reference) for flexible AI model integration
- [Ali YunXiao](https://help.aliyun.com/zh/yunxiao/) for repository management API
- [Loguru](https://github.com/Delgan/loguru) for elegant logging
- [UV](https://github.com/astral-sh/uv) for fast Python package management

---

**Built with ❤️ by Heng Li using Claude Code**