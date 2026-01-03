# Contributing to llm-kit-pro

First off, thank you for considering contributing to `llm-kit-pro`! It's people like you who make this toolkit better for everyone.

This document provides guidelines and rules for contributing to the project. These are not just rules but best practices to ensure the project remains high-quality, maintainable, and reliable.

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.11+**: The project uses modern Python features.
- **Poetry**: We use Poetry for dependency management and packaging. [Install Poetry](https://python-poetry.org/docs/#installation).

### 2. Local Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/llm-kit-pro.git
   cd llm-kit-pro
   ```
3. Install dependencies:
   ```bash
   poetry install --all-extras
   ```
4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

---

## 🛠 Development Workflow

### 1. Branching Strategy

- Always create a new branch for your work:
  - `feat/description` for new features.
  - `fix/description` for bug fixes.
  - `docs/description` for documentation changes.
  - `refactor/description` for code refactoring.
- Keep your branches up-to-date with the `main` branch.

### 2. Coding Standards

We aim for clean, idiomatic, and type-safe Python code.

- **Type Hints**: All new functions and classes must have complete type hints.
- **Pydantic**: Use Pydantic models for data validation and configuration where appropriate.
- **Formatting**: We use `black` for formatting and `ruff` for linting.
  ```bash
  # Format code
  black .
  # Lint code
  ruff check .
  ```
- **Docstrings**: Use Google-style docstrings for all public modules, classes, and methods.

### 3. Testing Requirements

We maintain high test coverage to ensure stability across multiple LLM providers.

- **New Features**: Must include unit tests and, where applicable, integration tests (using mocks).
- **Bug Fixes**: Should include a regression test that fails without the fix.
- **Running Tests**:
  ```bash
  pytest
  ```
- **Async Testing**: We use `pytest-asyncio`. Ensure your async tests are properly decorated with `@pytest.mark.asyncio`.

### 4. Documentation

- If you add a feature, update the `README.md` and relevant docstrings.
- Documentation is built using Sphinx. To build docs locally:
  ```bash
  cd docs
  make html
  ```

---

## 📤 Submitting a Pull Request

1. **Commit Messages**: Use clear, descriptive commit messages. Follow [Conventional Commits](https://www.conventionalcommits.org/) if possible (e.g., `feat: add Anthropic provider`).
2. **Pull Request Template**:
   - Describe the changes in detail.
   - Explain the motivation (link to an issue if it exists).
   - List any breaking changes.
   - Confirm that tests pass and linting is clean.
3. **Review Process**:
   - At least one maintainer must approve the PR.
   - Address all review comments promptly.
   - Squash commits before merging if requested.

---

## 🐛 Reporting Issues

- Use the GitHub Issue tracker.
- Use a clear and descriptive title.
- Provide a minimal, reproducible example (MRE) for bugs.
- Describe the expected vs. actual behavior.
- Include your environment details (Python version, OS, `llm-kit-pro` version).

---

## ⚖️ Code of Conduct

Be respectful and professional in all interactions. We follow the standard Contributor Covenant Code of Conduct.

---

Thank you for contributing to the future of multi-provider LLM integration!
