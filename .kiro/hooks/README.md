# SumiClock Agent Hooks

This directory contains Kiro agent hooks that automate development workflows for the SumiClock project.

## Available Hooks

### Code Quality Hooks

#### 1. Format Code on Save (`format-on-save.json`)
- **Trigger**: When any Python file is saved
- **Action**: Automatically formats code with black and isort
- **Purpose**: Maintain consistent code style without manual intervention
- **Command**: `black --line-length 100 ${file} && isort --profile black --line-length 100 ${file}`

#### 2. Type Check on Save (`type-check-on-save.json`)
- **Trigger**: When Python files in `src/` are saved
- **Action**: Runs mypy type checking on the saved file
- **Purpose**: Catch type errors immediately during development
- **Command**: `mypy ${file}`

#### 3. Lint Before Commit (`lint-on-commit.json`)
- **Trigger**: When user mentions "commit" or "push" in chat
- **Action**: Reminds to run flake8 linting
- **Purpose**: Ensure code quality before committing
- **Message**: Suggests running `flake8 src/ tests/`

### Testing Hooks

#### 4. Run Tests on Save (`test-on-save.json`)
- **Trigger**: When any Python file is saved
- **Action**: Runs pytest test suite
- **Purpose**: Catch bugs early with immediate test feedback
- **Command**: `pytest tests/ -v --tb=short`

#### 5. Validate Clock Image Generation (`validate-image-generation.json`)
- **Trigger**: When `src/clock_generator.py` is saved
- **Action**: Tests clock image generation
- **Purpose**: Verify core functionality after changes
- **Command**: Quick validation of image generation

### Infrastructure Hooks

#### 6. Docker Health Check (`docker-health-check.json`)
- **Trigger**: When docker-compose files are modified
- **Action**: Reminds to check Docker services health
- **Purpose**: Ensure Docker configuration changes don't break services
- **Message**: Suggests checking container status and logs

#### 7. Update Requirements Reminder (`update-requirements.json`)
- **Trigger**: When `pyproject.toml` is modified
- **Action**: Reminds to sync requirements.txt
- **Purpose**: Keep dependency files in sync
- **Message**: Reminder to update requirements.txt

## Hook Configuration

Each hook is defined in a JSON file with the following structure:

```json
{
  "name": "Hook Name",
  "description": "What this hook does",
  "trigger": {
    "type": "onFileSave|onMessage|onSessionStart",
    "filePattern": "**/*.py",  // For onFileSave
    "pattern": "keyword"       // For onMessage
  },
  "action": {
    "type": "executeCommand|sendMessage",
    "command": "command to run",           // For executeCommand
    "message": "message to display",       // For sendMessage
    "workingDirectory": "${workspaceFolder}",
    "showOutput": true
  },
  "enabled": true
}
```

## Enabling/Disabling Hooks

To disable a hook, set `"enabled": false` in its JSON file.

To enable a disabled hook, set `"enabled": true`.

## Variables

Hooks support the following variables:

- `${workspaceFolder}`: Root directory of the workspace
- `${file}`: Full path to the file that triggered the hook
- `${fileBasename}`: Name of the file that triggered the hook
- `${fileDirname}`: Directory containing the file

## Development Workflow

With these hooks enabled, the typical development workflow becomes:

1. **Edit code** → Auto-format on save (black + isort)
2. **Save file** → Type check runs automatically (mypy)
3. **Save file** → Tests run automatically (pytest)
4. **Modify clock_generator.py** → Image generation validated
5. **Ready to commit** → Reminded to run linting
6. **Modify Docker config** → Reminded to check services
7. **Update dependencies** → Reminded to sync requirements

## Benefits for Kiroween Hackathon

These hooks demonstrate:

- **Workflow Automation**: Automated code quality checks
- **Development Efficiency**: Immediate feedback on code changes
- **Best Practices**: Enforced code standards and testing
- **Integration**: Seamless integration with development tools
- **Productivity**: Reduced manual tasks and context switching

## Customization

Feel free to customize these hooks for your workflow:

- Adjust file patterns to target specific files
- Modify commands to use different tools or options
- Add new hooks for project-specific needs
- Change trigger conditions based on your preferences

## Testing Hooks

To test if hooks are working:

1. Save a Python file → Should see formatting and type checking
2. Mention "commit" in chat → Should see linting reminder
3. Modify docker-compose.yaml → Should see Docker reminder
4. Edit clock_generator.py → Should see image validation

## Troubleshooting

If hooks aren't working:

1. Check that the hook file is valid JSON
2. Verify `"enabled": true` is set
3. Ensure required tools are installed (black, mypy, pytest, etc.)
4. Check file patterns match your file structure
5. Review Kiro's hook execution logs

## Future Enhancements

Potential additional hooks:

- Coverage report generation after tests
- Automatic documentation updates
- Security scanning on dependency changes
- Performance benchmarking on core changes
- Automatic changelog updates
- Git commit message validation
