# Custom Review Guidelines

## Code Quality Standards

- Always prefer explicit error handling over generic try-catch blocks
- Use meaningful variable names that clearly indicate their purpose
- Ensure all public methods have proper docstrings
- Follow the principle of single responsibility for functions

## Security Considerations

- Never hardcode credentials or sensitive information
- Validate all user inputs to prevent injection attacks
- Use secure communication protocols (HTTPS, TLS)
- Implement proper authentication and authorization checks

## Performance Guidelines

- Avoid unnecessary database queries in loops
- Use appropriate data structures for the use case
- Consider memory usage for large datasets
- Profile code before optimizing for performance

## Testing Requirements

- Write unit tests for all new functionality
- Ensure edge cases are covered in tests
- Mock external dependencies properly
- Maintain test coverage above 80%

## Documentation

- Update README.md when adding new features
- Document API changes in CHANGELOG.md
- Include examples in docstrings where helpful
- Keep inline comments focused on "why" not "what"