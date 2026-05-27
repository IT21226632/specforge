SpecForge

AI-assisted software delivery pipeline that transforms structured feature specifications into implementation plans, generated code, automated tests, validation artifacts, and deployment evidence using deterministic quality controls and human approval workflows.

--------------------

Features

AI-generated implementation planning
AI-assisted code generation
Automated test generation
Deterministic quality gates
Security scanning
Human approval checkpoints
Audit artifact generation
Dependency auto-detection
GitHub Actions CI pipeline
Streamlit observability dashboard

--------------------

Architecture Overview

SpecForge follows a staged AI-assisted delivery pipeline:

Feature Spec
     ↓
Validation Stage
     ↓
Implementation Planning
     ↓
Human Approval Checkpoint
     ↓
Code Generation
     ↓
Test Generation
     ↓
Dependency Detection
     ↓
Quality Gates
     ↓
Deployment Evidence


--------------------

Design Decisions

1. AI-Assisted Planning

Large Language Models are used to generate:

implementation plans
code changes
automated tests

This accelerates software delivery while preserving human oversight.

2. Deterministic Quality Controls

All generated artifacts pass through automated validation:

Ruff (linting)
MyPy (type checking)
Pytest (testing)
Bandit (security scanning)

This ensures outputs are validated independently from the AI model.

3. Human Governance Workflow

SpecForge introduces mandatory approval checkpoints

--------------------

Tech Stack

Python 3.11
FastAPI
Streamlit
Google Gemini API
Ruff
MyPy
Pytest
Bandit
GitHub Actions

--------------------

Project Structure

specforge/
│
├── README.md (specforge/README.md)
├── .gitignore (specforge/.gitignore)
├── requirements.txt (specforge/requirements.txt)
├── .github/
│ └── workflows/
│ └── specforge.yml (specforge/.github/workflows/specforge.yml)
│
├── specs/
│ └── example_feature.yaml (specforge/specs/example_feature.yaml)
│
├── gate_signals/
│ └── implementation_plan.request (specforge/gate_signals/implementation_plan.request)
│
├── tests/
│ └── test_intake.py (specforge/tests/test_intake.py)
│
├── dashboard/
│ └── app.py (specforge/dashboard/app.py)
│
├── pipeline/
│ ├── __init__.py (specforge/pipeline/init.py)
│ ├── main.py (specforge/pipeline/main.py)
│ ├── models.py (specforge/pipeline/models.py)
│ ├── util.py (specforge/pipeline/util.py)
│ ├── prompts/
│ │ ├── planner.txt (specforge/pipeline/prompts/planner.txt)
│ │ ├── codegen.txt (specforge/pipeline/prompts/codegen.txt)
│ │ └── testgen.txt (specforge/pipeline/prompts/testgen.txt)
│ └── stages/
│ ├── __init__.py (specforge/pipeline/stages/init.py)
│ ├── intake.py (specforge/pipeline/stages/intake.py)
│ ├── planner.py (specforge/pipeline/stages/planner.py)
│ ├── approval.py (specforge/pipeline/stages/approval.py)
│ ├── codegen.py (specforge/pipeline/stages/codegen.py)
│ ├── testgen.py (specforge/pipeline/stages/testgen.py)
│ ├── dependency_manager.py (specforge/pipeline/stages/dependency_manager.py)
│ ├── quality.py (specforge/pipeline/stages/quality.py)
│ ├── package_initializer.py (specforge/pipeline/stages/package_initializer.py)
│ └── sandbox.py (specforge/pipeline/stages/sandbox.py)
│
├── pipeline/audit/
│ ├── __init__.py (specforge/pipeline/audit/init.py)
│ └── logger.py (specforge/pipeline/audit/logger.py)
│
└── sandbox/
├── __init__.py (specforge/sandbox/init.py)
└── generated/
├── __init__.py (specforge/sandbox/generated/init.py)
├── generated_api.py (specforge/sandbox/generated/generated_api.py)
└── tests/
├── __init__.py (specforge/sandbox/generated/tests/init.py)
└── test_generated_api.py

--------------------

Setup Instructions

1. Clone Repository

git clone https://github.com/IT21226632/specforge.git

2. Create Virtual Environment

python -m venv venv

Windows - venv\Scripts\activate
mac/Linux - source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create .env file

5. Running the Pipeline

vscode teeminal
python -m pipeline.main specs/example_feature.yaml

dashboard
streamlit run dashboard/app.py

-----------------

Example Feature Specification

feature:
  name: User Login
  objective: Allow users to securely log into the system

acceptance_criteria:
  - User can login with valid credentials
  - Invalid passwords are rejected

------------------

Example End-to-End Flow

Validate specification
Generate implementation plan
Human approval
Generate code
Generate tests
Install dependencies
Run quality checks
Generate deployment evidence

-------------------

Generated Artifacts

SpecForge automatically stores:

specifications
generated plans
approvals
generated code
generated tests
quality reports
deployment evidence

-------------------

Quality Gates

ruff
mypy
pytest
bandit

-------------------

GitHub Actions

Continuous Integration is configured using GitHub Actions.

Pipeline runs automatically on:

push
pull request

-------------------

Observability Dashboard

A lightweight Streamlit dashboard provides:

live pipeline logs
interactive approvals
terminal monitoring
execution visibility

-------------------

Trade-Offs

Strengths

Rapid prototyping
Human-supervised AI workflow
Deterministic validation
Transparent audit trail

Limitations

Generated code quality depends on prompt quality
Recovery loops are not yet automated
Dependency detection currently uses static mapping
No containerized runtime in current version

-------------------

Future Improvements

Self-healing regeneration loops
Multi-agent orchestration
Docker containerization
Prompt versioning
Semantic dependency resolution
Deployment automation
Advanced observability metrics
Evaluation benchmarking
