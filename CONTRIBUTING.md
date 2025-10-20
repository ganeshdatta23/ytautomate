# Contributing to YouTube Automation System

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/ganeshdatta23/yt-automation.git
cd yt-automation
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where possible
- Write clear commit messages

## Testing

Before submitting:

```bash
python test_system.py
python main.py --mode single --no-upload
```

## Questions?

Open an issue or discussion for any questions!

Thank you for contributing! 🚀
