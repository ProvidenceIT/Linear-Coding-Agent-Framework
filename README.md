# Autonomous Coding Agent Demo (Linear-Integrated)

A minimal harness demonstrating long-running autonomous coding with the Claude Agent SDK. This demo implements a two-agent pattern (initializer + coding agent) with **Linear as the core project management system** for tracking all work.

## 🚀 **NEW: Optimizations Available**

**Encountering rate limits or security restrictions?** See [OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md) for:
- ⚡ **60-80% fewer API calls** via intelligent caching
- 🔓 **YOLO security mode** (unrestricted commands)
- 🚀 **Parallel agents** (3-5x throughput)
- 📋 **Workflow automation** (Idea → app_spec.txt)

## Key Features

- **Linear Integration**: All work is tracked as Linear issues, not local files
- **Real-time Visibility**: Watch agent progress directly in your Linear workspace
- **Session Handoff**: Agents communicate via Linear comments, not text files
- **Two-Agent Pattern**: Initializer creates Linear project & issues, coding agents implement them
- **Browser Testing**: Puppeteer MCP for UI verification
- **Claude Opus 4.5**: Uses Claude's most capable model by default
- **Intelligent Caching**: Reduces API calls by 60-80% (NEW)
- **Parallel Execution**: Run multiple agents simultaneously (NEW)

## Prerequisites

### 1. Install Claude Code CLI and Python SDK

```bash
# Install Claude Code CLI (latest version required)
npm install -g @anthropic-ai/claude-code

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set Up Authentication

You need two authentication tokens. You can set them using either environment variables or a `.env` file:

#### Option 1: Using .env File (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your tokens:
# CLAUDE_CODE_OAUTH_TOKEN=your-oauth-token-here
# LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
```

**Claude Code OAuth Token:**
- Generate by running: `claude setup-token`
- Add to `.env` file

**Linear API Key:**
- Get from: https://linear.app/YOUR-TEAM/settings/api
- Add to `.env` file

#### Option 2: Using Environment Variables

```bash
# Claude Code OAuth Token
export CLAUDE_CODE_OAUTH_TOKEN='your-oauth-token-here'

# Linear API Key
export LINEAR_API_KEY='lin_api_xxxxxxxxxxxxx'
```

### 3. Verify Installation

```bash
claude --version  # Should be latest version
pip show claude-code-sdk  # Check SDK is installed
```

## Quick Start

### Optimized Version (Recommended)
```bash
# With all optimizations enabled
python autonomous_agent_optimized.py --project-dir ./my_project

# With YOLO mode (unrestricted commands)
python autonomous_agent_optimized.py --project-dir ./my_project --yolo

# Monitor progress in another terminal
python monitor.py ./my_project --watch
```

### Original Version
```bash
python autonomous_agent_demo.py --project-dir ./my_project
```

For testing with limited iterations:
```bash
python autonomous_agent_optimized.py --project-dir ./my_project --max-iterations 3
```

## How It Works

### Linear-Centric Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    LINEAR-INTEGRATED WORKFLOW               │
├─────────────────────────────────────────────────────────────┤
│  app_spec.txt ──► Initializer Agent ──► Linear Issues (50) │
│                                              │               │
│                    ┌─────────────────────────▼──────────┐   │
│                    │        LINEAR WORKSPACE            │   │
│                    │  ┌────────────────────────────┐    │   │
│                    │  │ Issue: Auth - Login flow   │    │   │
│                    │  │ Status: Todo → In Progress │    │   │
│                    │  │ Comments: [session notes]  │    │   │
│                    │  └────────────────────────────┘    │   │
│                    └────────────────────────────────────┘   │
│                                              │               │
│                    Coding Agent queries Linear              │
│                    ├── Search for Todo issues               │
│                    ├── Update status to In Progress         │
│                    ├── Implement & test with Puppeteer      │
│                    ├── Add comment with implementation notes│
│                    └── Update status to Done                │
└─────────────────────────────────────────────────────────────┘
```

### Two-Agent Pattern

1. **Initializer Agent (Session 1):**
   - Reads `app_spec.txt`
   - Lists teams and creates a new Linear project
   - Creates 50 Linear issues with detailed test steps
   - Creates a META issue for session tracking
   - Sets up project structure, `init.sh`, and git

2. **Coding Agent (Sessions 2+):**
   - Queries Linear for highest-priority Todo issue
   - Runs verification tests on previously completed features
   - Claims issue (status → In Progress)
   - Implements the feature
   - Tests via Puppeteer browser automation
   - Adds implementation comment to issue
   - Marks complete (status → Done)
   - Updates META issue with session summary

### Session Handoff via Linear

Instead of local text files, agents communicate through:
- **Issue Comments**: Implementation details, blockers, context
- **META Issue**: Session summaries and handoff notes
- **Issue Status**: Todo / In Progress / Done workflow

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth token (from `claude setup-token`) | Yes |
| `LINEAR_API_KEY` | Linear API key for MCP access | Yes |

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-dir` | Directory for the project | `./autonomous_demo_project` |
| `--max-iterations` | Max agent iterations | Unlimited |
| `--model` | Claude model to use | `claude-opus-4-5-20251101` |

## Project Structure

```
linear-agent-harness/
├── autonomous_agent_demo.py  # Main entry point
├── agent.py                  # Agent session logic
├── client.py                 # Claude SDK + MCP client configuration
├── security.py               # Bash command allowlist and validation
├── progress.py               # Progress tracking utilities
├── prompts.py                # Prompt loading utilities
├── linear_config.py          # Linear configuration constants
├── prompts/
│   ├── app_spec.txt          # Application specification
│   ├── initializer_prompt.md # First session prompt (creates Linear issues)
│   └── coding_prompt.md      # Continuation session prompt (works issues)
└── requirements.txt          # Python dependencies
```

## Generated Project Structure

After running, your project directory will contain:

```
my_project/
├── .linear_project.json      # Linear project state (marker file)
├── app_spec.txt              # Copied specification
├── init.sh                   # Environment setup script
├── .claude_settings.json     # Security settings
└── [application files]       # Generated application code
```

## MCP Servers Used

| Server | Transport | Purpose |
|--------|-----------|---------|
| **Linear** | HTTP (Streamable HTTP) | Project management - issues, status, comments |
| **Puppeteer** | stdio | Browser automation for UI testing |

## Security Model

This demo uses defense-in-depth security (see `security.py` and `client.py`):

1. **OS-level Sandbox:** Bash commands run in an isolated environment
2. **Filesystem Restrictions:** File operations restricted to project directory
3. **Bash Allowlist:** Only specific commands permitted (npm, node, git, etc.)
4. **MCP Permissions:** Tools explicitly allowed in security settings

## Linear Setup

Before running, ensure you have:

1. A Linear workspace with at least one team
2. An API key with read/write permissions (from Settings > API)
3. The agent will automatically detect your team and create a project

The initializer agent will create:
- A new Linear project named after your app
- 50 feature issues based on `app_spec.txt`
- 1 META issue for session tracking and handoff

All subsequent coding agents will work from this Linear project.

## Customization

### Changing the Application

Edit `prompts/app_spec.txt` to specify a different application to build.

### Adjusting Issue Count

Edit `prompts/initializer_prompt.md` and change "50 issues" to your desired count.

### Modifying Allowed Commands

Edit `security.py` to add or remove commands from `ALLOWED_COMMANDS`.

## Troubleshooting

**"CLAUDE_CODE_OAUTH_TOKEN not set"**
Run `claude setup-token` to generate a token, then export it.

**"LINEAR_API_KEY not set"**
Get your API key from `https://linear.app/YOUR-TEAM/settings/api`

**"Appears to hang on first run"**
Normal behavior. The initializer is creating a Linear project and 50 issues with detailed descriptions. Watch for `[Tool: mcp__linear__create_issue]` output.

**"Command blocked by security hook"**
The agent tried to run a disallowed command. Add it to `ALLOWED_COMMANDS` in `security.py` if needed.

**"MCP server connection failed"**
Verify your `LINEAR_API_KEY` is valid and has appropriate permissions. The Linear MCP server uses HTTP transport at `https://mcp.linear.app/mcp`.

## Viewing Progress

Open your Linear workspace to see:
- The project created by the initializer agent
- All 50 issues organized under the project
- Real-time status changes (Todo → In Progress → Done)
- Implementation comments on each issue
- Session summaries on the META issue

## 🚀 Performance Optimizations

### Rate Limiting Issues?
If you're hitting Linear's 1500 req/hr limit, see [OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md) for solutions:

**Quick Fix** (60% fewer API calls):
```bash
cp prompts/coding_prompt_optimized.md prompts/coding_prompt.md
```

**Maximum Performance** (3-5x throughput):
```bash
python parallel_agent.py ./my_project 3
```

### Security Restrictions Blocking Commands?
Enable YOLO mode (unrestricted commands):
```python
from security_yolo import create_yolo_client as create_client
```

See [OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md) for full details.

---

## 📚 Additional Documentation

- **[OPTIMIZATION_GUIDE.md](./OPTIMIZATION_GUIDE.md)** - Comprehensive optimization guide
  - Linear API caching (60-80% reduction)
  - YOLO security modes
  - Parallel agent execution
  - Workflow automation commands

- **Claude Code Commands** (`.claude/commands/`):
  - `/idea-to-spec` - Interactive spec generation
  - `/research-tech-stack` - Technology recommendations
  - `/generate-spec` - Automated spec creation
  - `/optimize-agent` - Configuration optimization

---

## License

MIT License - see [LICENSE](LICENSE) for details.
