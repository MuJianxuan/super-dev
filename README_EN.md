# Super Dev

<div align="center">


# God-Tier AI Development Team
### Top-Tier AI Development Team

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-2024%20informational)](https://github.com/psf/black)
[![Type Checks](https://img.shields.io/badge/type%20checks-mypy-success)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-59%20passing-brightgreen)](tests/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)](.github/workflows/ci.yml)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://code.claude.com)
[![PyPI](https://img.shields.io/badge/PyPI-1.0.0-orange)](https://pypi.org/project/super-dev/)

English | [简体中文](README.md)

[Features](#-features) • [Quick Start](#-quick-start) • [Command Reference](#-command-reference) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## What is Super Dev?

**Super Dev** is a commercial-grade AI-assisted development tool focused on **Spec-Driven Development (SDD)**. It starts from a one-sentence requirement and automatically generates complete project documentation, specifications, CI/CD configurations, and database migration scripts.

```
Idea → Docs → Spec → Review → AI Implementation → Deployment
```

### Core Value

| Capability | Description |
|:---|:-----|
| **Spec-Driven Development** | OpenSpec-like workflow, align on specs before coding |
| **8-Stage Pipeline** | Docs → Spec → Red Team → Quality Gate → Code Review → AI Prompt → CI/CD → Migration |
| **10 Expert System** | PM/Architect/UI/UX/Security/Code/DBA/QA/DevOps/RCA collaboration |
| **Knowledge Injection** | 6 business domains + 4 platforms expertise auto-injected |
| **Quality Gate** | 80+ score standard ensuring commercial-grade deliverables |
| **Ready to Use** | CLI tool, one-command generation of complete project assets |

---

## Features

### 1. Complete Development Pipeline

Super Dev provides an 8-stage automated pipeline from idea to deployment:

```
┌──────────────────────────────────────────────────────────────┐
│                    Super Dev Complete Pipeline                │
├──────────────────────────────────────────────────────────────┤
│  Stage 1  │  Generate Docs (PRD + Architecture + UI/UX)      │
│  Stage 2  │  Create Spec (OpenSpec style)                    │
│  Stage 3  │  Red Team Review (Security + Performance + Arch)  │
│  Stage 4  │  Quality Gate (Auto-scoring 80+ to pass)         │
│  Stage 5  │  Code Review Guide                               │
│  Stage 6  │  AI Prompt Generation                            │
│  Stage 7  │  CI/CD Config (5 platforms)                      │
│  Stage 8  │  Database Migration Scripts (6 ORMs)             │
└──────────────────────────────────────────────────────────────┘
```

### 2. CLI Tools

```bash
# ===== Core Commands =====
super-dev pipeline "Feature description"  # Run complete 8-stage pipeline
super-dev create "Feature description"    # One-click project (Docs + Spec + AI Prompt)
super-dev spec <subcommand>              # Spec-Driven Development management

# ===== Project Management =====
super-dev init <name>                    # Initialize new project
super-dev analyze [path]                 # Analyze existing project structure
super-dev config <cmd>                   # Configuration management

# ===== Expert System =====
super-dev expert --list                   # List all available experts
super-dev expert PM "prompt"             # Call Product Manager expert
super-dev expert ARCHITECT               # Call Architect expert

# ===== Quality & Deployment =====
super-dev quality --type all             # Run quality checks
super-dev deploy --cicd github           # Generate CI/CD configuration
super-dev preview -o output.html         # Generate UI prototype

# ===== Workflow =====
super-dev workflow                        # Run interactive workflow
```

### 3. Spec-Driven Development (SDD)

Super Dev includes an OpenSpec-like spec-driven development workflow:

```
┌────────────────────┐
│ Draft Change       │
│ Proposal           │
└────────┬───────────┘
         │ share intent with your AI
         ▼
┌────────────────────┐
│ Review & Align     │
│ (edit specs/tasks) │◀──── feedback loop ──────┐
└────────┬───────────┘                          │
         │ approved plan                        │
         ▼                                      │
┌────────────────────┐                          │
│ Implement Tasks    │──────────────────────────┘
│ (AI writes code)   │
└────────┬───────────┘
         │ ship the change
         ▼
┌────────────────────┐
│ Archive & Update   │
│ Specs (source)     │
└────────────────────┘
```

**Directory Structure:**
```
.super-dev/
├── specs/          # Current specs (single source of truth)
│   └── auth/
│       └── spec.md
├── changes/        # Proposed changes
│   └── add-2fa/
│       ├── proposal.md
│       ├── tasks.md
│       ├── design.md
│       └── specs/
│           └── auth/
│               └── spec.md  # Delta (ADDED/MODIFIED/REMOVED)
└── archive/        # Archived changes
```

### 4. Expert Team

| Expert | Expertise | Use Cases |
|:---|:-----|:---------|
| **PM** | Requirements analysis, PRD writing, user stories | Product planning, feature definition |
| **ARCHITECT** | System design, tech selection, architecture docs | Architecture design, tech decisions |
| **UI** | Visual design, design specs, component libraries | Interface design, visual specs |
| **UX** | Interaction design, user experience, information architecture | Interaction flows, user experience |
| **SECURITY** | Security review, vulnerability detection, threat modeling | Security review, penetration testing |
| **CODE** | Code implementation, best practices, code review | Code implementation, code review |
| **DBA** | Database design, SQL optimization, data modeling | Database design, performance optimization |
| **QA** | Quality assurance, testing strategy, automated testing | Test planning, quality assurance |
| **DEVOPS** | Deployment, CI/CD, containerization, monitoring | Deployment configuration, pipelines |
| **RCA** | Root cause analysis, incident post-mortems, improvement suggestions | Incident analysis, post-mortem review |

### 5. Knowledge Base

#### Business Domains
- **FinTech** (fintech) - Payments, lending, wealth management, insurance
- **E-commerce** (ecommerce) - B2C/B2B/C2C, cross-border, social commerce
- **Medical** (medical) - Medical informatics, health management
- **Social Media** (social) - Feed, instant messaging, content moderation
- **IoT** (iot) - Device management, MQTT/CoAP, edge computing
- **Education** (education) - Live classroom, question bank, learning analytics
- **Authentication** (auth) - JWT, OAuth2, RBAC
- **Content Management** (content) - CMS, content recommendation, search

#### Technology Platforms
- **Web** - React/Vue/Angular + Node/Python/Go
- **Mobile** - React Native/Flutter
- **WeChat** - WeChat Mini Programs
- **Desktop** - Electron/Tauri

### 6. Supported Tech Stack

#### Frontend Frameworks
- React, Vue, Angular, Svelte

#### Backend Frameworks
- Node.js, Python, Go, Java

#### Database ORMs
- Prisma, TypeORM, Sequelize, SQLAlchemy, Django, Mongoose

#### CI/CD Platforms
- GitHub Actions, GitLab CI, Jenkins, Azure DevOps, Bitbucket Pipelines

---

## Quick Start

### Installation

```bash
# Install with pip
pip install super-dev

# Or install from source
git clone https://github.com/shangyankeji/super-dev.git
cd super-dev
pip install -e .
```

### Requirements

- Python 3.10+
- Modern terminal (with ANSI color support)

### Core Usage: From Idea to Deployment

#### Method 1: Complete Pipeline (Recommended)

```bash
# One sentence → Complete project assets (8 stages)
super-dev pipeline "User Authentication System" \
  --platform web \
  --frontend react \
  --backend node \
  --cicd github \
  --quality-threshold 80
```

**Auto-generates:**
```
output/
├── User Authentication System-prd.md         # PRD document
├── User Authentication System-architecture.md # Architecture design
├── User Authentication System-uiux.md         # UI/UX design
├── User Authentication System-redteam.md      # Red team review
├── User Authentication System-quality-gate.md # Quality gate report
├── User Authentication System-code-review.md  # Code review guide
├── User Authentication System-ai-prompt.md    # AI prompts
└── ...
.super-dev/changes/User Authentication System/
├── proposal.md                                # Change proposal
├── tasks.md                                   # Task checklist
└── specs/                                     # Spec definitions
.github/workflows/
├── ci.yml                                     # CI configuration
└── cd.yml                                     # CD configuration
prisma/
├── schema.prisma                              # Database schema
└── migrations/                                # Migration scripts
```

#### Method 2: One-Click Project Creation

```bash
# Generate docs + Spec + AI prompts
super-dev create "User Authentication System" \
  --platform web \
  --frontend react \
  --backend node \
  --domain auth
```

#### Method 3: Step-by-Step Creation

```bash
# 1. Initialize project
super-dev init todo-app \
  --platform web \
  --frontend react \
  --backend node

# 2. Edit configuration
vim super-dev.yaml

# 3. Run workflow
super-dev workflow
```

### Claude Code Skill Integration

```bash
# Install to Claude Code
./install.sh

# Use in Claude Code
Just tell Claude: "Help me analyze this project with Super Dev"
```

---

## Command Reference

### pipeline - Complete Pipeline

```bash
super-dev pipeline "Feature description" [options]

Options:
  -p, --platform {web,mobile,wechat,desktop}
                        Target platform (default: web)
  -f, --frontend {react,vue,angular,svelte,none}
                        Frontend framework (default: react)
  -b, --backend {node,python,go,java,none}
                        Backend framework (default: node)
  -d, --domain {fintech,ecommerce,medical,social,iot,education,auth,content}
                        Business domain
  --name NAME           Project name (auto-generated from description)
  --cicd {github,gitlab,jenkins,azure,bitbucket}
                        CI/CD platform (default: github)
  --skip-redteam        Skip red team review
  --quality-threshold N Quality gate threshold (default: 80)

Examples:
  super-dev pipeline "E-commerce shopping cart"
  super-dev pipeline "User login" --platform wechat --cicd gitlab
```

### create - One-Click Project Creation

```bash
super-dev create "Feature description" [options]

Options:
  -p, --platform       Target platform
  -f, --frontend       Frontend framework
  -b, --backend        Backend framework
  -d, --domain         Business domain
  --name NAME          Project name
  --skip-docs          Skip doc generation, create Spec only
```

### spec - Spec Management

```bash
# Initialize SDD directory structure
super-dev spec init

# List all changes
super-dev spec list

# Show change details
super-dev spec show <change-id>

# Create change proposal
super-dev spec propose <change-id> --title "Title" --description "Description"

# Add requirement
super-dev spec add-req <change-id> <component> <requirement-id> "Requirement description"

# Validate spec format
super-dev spec validate              # Validate all changes
super-dev spec validate <change-id>  # Validate single change
super-dev spec validate -v           # Show verbose output

# Interactive dashboard
super-dev spec view                  # Show dashboard of all specs and changes

# Archive change
super-dev spec archive <change-id>
```

### expert - Call Expert

```bash
# List all available experts
super-dev expert --list

# Call specific expert
super-dev expert PM "Help me write an e-commerce platform PRD"
super-dev expert ARCHITECT "Design high-concurrency architecture"
super-dev expert SECURITY "Review security approach"
```

### Other Commands

```bash
# Initialize project
super-dev init <name> [options]

# Analyze existing project
super-dev analyze [path] [options]

# Quality check
super-dev quality --type {prd,architecture,ui,ux,code,all}

# Generate deployment config
super-dev deploy --docker --cicd {github,gitlab,jenkins,azure,bitbucket}

# Generate UI prototype
super-dev preview -o output.html

# Run interactive workflow
super-dev workflow [--phase ...]

# Configuration management
super-dev config {get,set,list} [key] [value]
```

---

## Examples

### Example 1: User Authentication System

```bash
super-dev pipeline "User Authentication System" \
  --platform web \
  --frontend react \
  --backend node \
  --cicd github
```

### Example 2: E-commerce Platform

```bash
super-dev pipeline "E-commerce Shopping Cart" \
  --platform web \
  --frontend vue \
  --backend python \
  --domain ecommerce \
  --cicd gitlab
```

### Example 3: WeChat Mini Program

```bash
super-dev create "Food Ordering Mini Program" \
  --platform wechat \
  --domain auth
```

### Example 4: Spec-Driven Development

```bash
# 1. Initialize SDD
super-dev spec init

# 2. Create change proposal
super-dev spec propose add-user-auth \
  --title "Add User Authentication" \
  --description "Implement JWT-based user authentication"

# 3. Add requirement
super-dev spec add-req add-user-auth auth user-registration \
  "The system SHALL allow user registration with email and password"

# 4. Show change
super-dev spec show add-user-auth

# 5. Archive when complete
super-dev spec archive add-user-auth
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## Contact

- **GitHub**: https://github.com/shangyankeji/super-dev
- **Issues**: https://github.com/shangyankeji/super-dev/issues
- **Email**: 11964948@qq.com

---

<div align="center">

**If this project helps you, please give it a Star!**

Made with passion by [Excellent](https://github.com/shangyankeji)

</div>
