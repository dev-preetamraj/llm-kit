# Publishing llm-kit to PyPI

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [TestPyPI](https://test.pypi.org/) (for testing)
   - [PyPI](https://pypi.org/) (for production)

2. **API Tokens**: Generate API tokens from both sites:
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

3. **Configure Poetry**: Add credentials to Poetry:
   ```bash
   poetry config pypi-token.testpypi <your-testpypi-token>
   poetry config pypi-token.pypi <your-pypi-token>
   ```

## Publishing Steps

### 1. Test on TestPyPI First (Recommended)

```bash
# Build the package
poetry build

# Publish to TestPyPI
poetry publish --repository testpypi

# Test installation
pip install --index-url https://test.pypi.org/simple/ llm-kit
```

### 2. Publish to Production PyPI

Once you've verified the TestPyPI release works:

```bash
# Build the package (if not already built)
poetry build

# Publish to PyPI
poetry publish
```

## Version Management

To update the version before publishing:

```bash
# Update version in pyproject.toml, then:
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.0 -> 0.2.0
poetry version major  # 0.1.0 -> 1.0.0
```

Or manually edit the `version` field in `pyproject.toml`.

## Optional Dependencies

Users can install with optional dependencies:

```bash
pip install llm-kit[gemini]
```

## Post-Publishing

After publishing, verify the package is available:

```bash
pip install llm-kit
```

Check the package page: https://pypi.org/project/llm-kit/

