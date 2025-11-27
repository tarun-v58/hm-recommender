# Contributing to H&M Recommender

Thank you for your interest in contributing! Please follow these guidelines to help us maintain code quality.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hm-recommender.git
   cd hm-recommender
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python init_db.py
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Code Style Guidelines

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Max line length: 100 characters
- Use 4 spaces for indentation

```python
def get_recommendations(user_id: int, top_k: int = 50) -> List[Product]:
    """
    Generate personalized recommendations for a user.
    
    Args:
        user_id: The user's ID
        top_k: Number of recommendations to return
        
    Returns:
        List of recommended Product objects
    """
    # Implementation here
```

### TypeScript/React (Frontend)

- Use TypeScript strict mode
- Use functional components with hooks
- Follow component naming: PascalCase
- Use descriptive variable names
- Add JSDoc comments for complex logic

```typescript
interface ProductProps {
  id: number;
  name: string;
  price: number;
}

const ProductCard: React.FC<ProductProps> = ({ id, name, price }) => {
  // Component implementation
};
```

## Git Commit Messages

Use clear, descriptive commit messages:

```
✨ Add feature: Smart recommendations for new users
🐛 Fix: Product detail page not loading description
📝 Docs: Update README with API documentation
♻️ Refactor: Simplify cart context logic
🎨 Style: Fix spacing in ProductList component
```

### Commit Message Prefixes

- `✨ Add` - New feature
- `🐛 Fix` - Bug fix
- `📝 Docs` - Documentation
- `♻️ Refactor` - Code refactoring
- `🎨 Style` - Code style changes
- `⚡ Perf` - Performance improvement
- `🔒 Security` - Security fix
- `🧪 Test` - Test additions/updates

## Pull Request Process

1. **Update your branch** with latest main:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what was changed and why
   - Reference to any related issues (#123)
   - Screenshots for UI changes

4. **Address review feedback** and push updates:
   ```bash
   git add .
   git commit -m "Address review feedback"
   git push origin feature/your-feature-name
   ```

## Testing Requirements

### Backend

```bash
cd backend
pytest
```

- All new features must have tests
- Maintain >80% code coverage
- Test edge cases and error scenarios

### Frontend

```bash
cd frontend
npm test
```

- Add tests for new components
- Test user interactions
- Verify API integration

## Documentation

- Update README.md if adding new features
- Add inline code comments for complex logic
- Update API documentation in comments
- Include examples in docstrings

## Reporting Issues

When reporting bugs, include:

1. **Clear description** of the issue
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment info**:
   - OS (Windows, macOS, Linux)
   - Python/Node version
   - Browser (for frontend issues)

### Issue Template

```markdown
## Bug Description
A clear description of what the bug is.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 11
- Python: 3.10
- Node: 18.0
- Browser: Chrome 120
```

## Feature Requests

Include:
- Clear description of desired feature
- Use cases and benefits
- Possible implementation approach
- Any related issues or discussions

## Code Review Checklist

Before requesting a review, ensure:

- [ ] Code follows style guidelines
- [ ] New features have tests
- [ ] All tests pass locally
- [ ] No console errors/warnings
- [ ] Updated documentation
- [ ] Commits are clear and logical
- [ ] No sensitive data in commits
- [ ] Changes are focused (not multiple unrelated changes)

## Pull Request Review Checklist

Reviewers will check:

- [ ] Code quality and style
- [ ] Test coverage
- [ ] Documentation
- [ ] Backward compatibility
- [ ] Performance impact
- [ ] Security implications
- [ ] Browser/Python version compatibility

## Areas for Contribution

### Backend
- Improve recommendation algorithm
- Add more ML models
- Optimize database queries
- Add caching layer
- Implement pagination

### Frontend
- Enhanced UI/UX
- Additional filters
- Mobile optimization
- Accessibility improvements
- Dark mode support

### General
- Bug fixes
- Documentation improvements
- Tests and test coverage
- Performance optimization

## Community Guidelines

- Be respectful and constructive
- Welcome diverse perspectives
- Focus on the code, not the person
- Help others when possible
- Report issues responsibly
- Follow the Code of Conduct

## Questions?

- Open an issue with your question
- Check existing issues first
- Ask for help in PRs
- Join discussions on GitHub

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
