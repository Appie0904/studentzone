# Contributing to StudentZone

🎓 Thank you for your interest in contributing to StudentZone! We're excited to have you join our community of developers working to connect Dutch students across universities.

## 🤝 How to Contribute

### Types of Contributions

We welcome all types of contributions:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve our docs, README, or code comments
- **🎨 UI/UX Improvements**: Enhance the user interface and experience
- **🧪 Testing**: Write or improve tests
- **🔧 Code**: Fix bugs or implement new features
- **🌍 Translations**: Help with Dutch/English translations
- **📚 Content**: Add educational resources or improve existing ones

### Before You Start

1. **Check existing issues**: Search [GitHub Issues](https://github.com/Appie0904/studentzone/issues) to see if your idea has already been discussed
2. **Join discussions**: Participate in [GitHub Discussions](https://github.com/Appie0904/studentzone/discussions) to share ideas
3. **Read the docs**: Familiarize yourself with the project structure and codebase

## 🚀 Development Setup

### Prerequisites

- Python 3.12 or higher
- Git
- A GitHub account

### Getting Started

1. **Fork the repository**
   ```bash
   # Go to https://github.com/Appie0904/studentzone and click "Fork"
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/studentzone.git
   cd studentzone
   ```

3. **Set up the development environment**
   ```bash
   # Create virtual environment
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up the database
   python manage.py migrate
   
   # Create a superuser (optional)
   python manage.py createsuperuser
   ```

4. **Add the upstream remote**
   ```bash
   git remote add upstream https://github.com/Appie0904/studentzone.git
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- **Django**: Follow [Django coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)
- **JavaScript**: Use consistent indentation (2 spaces) and follow modern ES6+ practices
- **HTML/CSS**: Use semantic HTML and follow Bootstrap conventions

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples:
git commit -m "Add user profile completion feature"
git commit -m "Fix discussion voting bug in community view"
git commit -m "Update README with installation instructions"

# Bad examples:
git commit -m "fix"
git commit -m "stuff"
git commit -m "wip"
```

### Testing

- Write tests for new features
- Ensure all existing tests pass
- Run the test suite before submitting:
  ```bash
  python manage.py test
  ```

### Documentation

- Update documentation for any new features
- Add docstrings to new functions and classes
- Update README.md if needed

## 🔄 Workflow

### Making Changes

1. **Keep your fork updated**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Make your changes**
   - Write your code
   - Add tests
   - Update documentation
   - Test thoroughly

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting a Pull Request

1. **Go to your fork on GitHub**
2. **Click "New Pull Request"**
3. **Select your feature branch**
4. **Fill out the PR template**:
   - Describe what you changed
   - Link any related issues
   - Mention any breaking changes
   - Add screenshots for UI changes

### PR Review Process

1. **Automated checks** will run (tests, linting)
2. **Maintainers** will review your code
3. **Address feedback** if requested
4. **Once approved**, your PR will be merged!

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Try to reproduce the issue
3. Check if it's a configuration issue

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. macOS, Windows, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Python version: [e.g. 3.12.0]
- Django version: [e.g. 5.2.4]

**Additional Context**
Any other context, screenshots, or logs.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
How would you like this feature to work?

**Alternative Solutions**
Any alternative solutions you've considered.

**Additional Context**
Any other context, mockups, or examples.
```

## 🏷️ Issue Labels

We use labels to organize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on

## 🎯 Project Priorities

### High Priority
- User authentication and profiles
- Community creation and management
- Discussion and Q&A system
- Resource sharing functionality

### Medium Priority
- Study partner matching
- Project collaboration tools
- Mobile responsiveness
- Performance optimizations

### Low Priority
- Advanced search features
- Real-time notifications
- API development
- Third-party integrations

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: [support@studentzone.nl](mailto:support@studentzone.nl)

## 🏆 Recognition

Contributors will be recognized in:

- The project README
- Release notes
- GitHub contributors page
- Special badges and mentions

## 📄 License

By contributing to StudentZone, you agree that your contributions will be licensed under the GNU General Public License v3.0.

---

**Thank you for contributing to StudentZone! Together, we're building a better future for Dutch students.** 🎓🇳🇱 