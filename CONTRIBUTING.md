# 🤝 Contributing to Self-Prompting ODQA System

Thank you for your interest in contributing to the Self-Prompting ODQA System! This document provides guidelines and information for contributors.

## 🌟 **Ways to Contribute**

### **1. Code Contributions**
- Bug fixes and improvements
- New features and enhancements
- Performance optimizations
- Documentation updates

### **2. Dataset Contributions**
- Adding new QA pairs to existing topics
- Creating new topic categories
- Improving question quality and diversity
- Fact-checking and validation

### **3. Documentation**
- API documentation
- User guides and tutorials
- Code comments and examples
- Translation to other languages

### **4. Testing**
- Writing unit tests
- Integration testing
- Performance testing
- User acceptance testing

## 🚀 **Getting Started**

### **1. Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/yourusername/self-prompting-odqa.git
cd self-prompting-odqa
```

### **2. Set Up Development Environment**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Frontend setup
cd ../frontend
npm install
```

### **3. Create a Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 **Development Guidelines**

### **Code Style**

#### **Python (Backend)**
- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 88 characters
- Use Black for code formatting

```bash
# Format code
black backend/

# Check style
flake8 backend/

# Type checking
mypy backend/
```

#### **JavaScript/React (Frontend)**
- Use ESLint and Prettier
- Follow React best practices
- Use functional components with hooks
- Consistent naming conventions

```bash
# Format code
npm run format

# Check linting
npm run lint

# Fix linting issues
npm run lint:fix
```

### **Commit Messages**
Use conventional commit format:
```
type(scope): description

Examples:
feat(backend): add new clustering algorithm
fix(frontend): resolve search input validation
docs(readme): update installation instructions
test(api): add unit tests for question processing
```

### **Testing Requirements**

#### **Backend Tests**
```bash
# Run all tests
pytest backend/tests/

# Run with coverage
pytest --cov=backend backend/tests/

# Run specific test file
pytest backend/tests/test_database.py
```

#### **Frontend Tests**
```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- --testNamePattern="SearchComponent"
```

## 📊 **Dataset Contribution Guidelines**

### **Adding New QA Pairs**

1. **Quality Standards**
   - Factually accurate information
   - Specific, non-obvious details
   - Clear, concise questions
   - Detailed explanations

2. **Format Requirements**
```python
QAPair(
    topic='your_topic',
    example='Specific Person/Place/Thing',
    passage='Detailed passage with context and facts...',
    entity='specific detail or fact',
    question='What specific question about the entity?',
    answer='Precise answer',
    explanation='Detailed explanation with context'
)
```

3. **Validation Process**
   - Fact-check all information
   - Ensure uniqueness (no duplicates)
   - Test question-answer accuracy
   - Verify explanation quality

### **Creating New Topics**

1. **Topic Selection Criteria**
   - Broad enough for 45+ QA pairs
   - Factual, verifiable information
   - Educational value
   - Diverse examples available

2. **Implementation Steps**
   - Create topic definition
   - Generate initial QA pairs
   - Test with ODQA system
   - Document topic guidelines

## 🔧 **Technical Contribution Areas**

### **Backend Improvements**
- **Performance**: Optimize database queries, caching
- **Features**: New API endpoints, advanced retrieval
- **Security**: Input validation, rate limiting
- **Monitoring**: Logging, metrics, health checks

### **Frontend Enhancements**
- **UI/UX**: Improved design, accessibility
- **Features**: Advanced search, filtering, visualization
- **Performance**: Code splitting, lazy loading
- **Mobile**: Responsive design improvements

### **Infrastructure**
- **Deployment**: Docker, cloud configurations
- **CI/CD**: GitHub Actions, automated testing
- **Documentation**: API docs, user guides
- **Monitoring**: Error tracking, analytics

## 🧪 **Testing Your Contributions**

### **Before Submitting**
1. **Run all tests**
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

2. **Check code quality**
```bash
# Backend
black backend/ && flake8 backend/

# Frontend
npm run lint && npm run format
```

3. **Test functionality**
```bash
# Start system
python backend/main.py &
npm start --prefix frontend &

# Test API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your test question"}'
```

4. **Verify documentation**
- Update README if needed
- Add docstrings to new functions
- Update API documentation

## 📋 **Pull Request Process**

### **1. Prepare Your PR**
- Ensure all tests pass
- Update documentation
- Add changelog entry
- Rebase on latest main

### **2. PR Description Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### **3. Review Process**
- Automated checks must pass
- Code review by maintainers
- Address feedback promptly
- Squash commits if requested

## 🐛 **Bug Reports**

### **Before Reporting**
1. Check existing issues
2. Reproduce the bug
3. Test on latest version
4. Gather system information

### **Bug Report Template**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.0]
- Node.js: [e.g., 16.14.0]
- Browser: [e.g., Chrome 96.0]

## Additional Context
Screenshots, logs, etc.
```

## 💡 **Feature Requests**

### **Feature Request Template**
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Mockups, examples, etc.
```

## 🏆 **Recognition**

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page
- Special mentions for significant contributions

## 📞 **Getting Help**

### **Communication Channels**
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Email**: Direct contact for sensitive issues

### **Development Questions**
- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions
- Contact maintainers

## 📄 **Code of Conduct**

### **Our Standards**
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### **Unacceptable Behavior**
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Inappropriate conduct

## 🎯 **Development Roadmap**

### **Current Priorities**
1. Expand dataset to 500+ QA pairs
2. Implement advanced clustering algorithms
3. Add multi-language support
4. Improve response time performance

### **Future Goals**
- Real-time collaborative editing
- Advanced analytics dashboard
- Mobile application
- API rate limiting and authentication

---

## 🙏 **Thank You**

Your contributions make this project better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, every contribution is valuable and appreciated!

**Happy Contributing! 🚀**
