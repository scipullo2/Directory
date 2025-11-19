# Quick Start Guide

## Installation

No installation needed! This is a pure Python project with no external dependencies.

```bash
git clone https://github.com/scipullo2/Directory.git
cd Directory
```

## Choose Your Path

### 1. Quick Demo (Recommended for First-Time Users)
See the agent in action with a pre-built example:

```bash
python demo.py
```

This shows a complete automation request being created with systems, notifications, and scheduling.

### 2. Interactive Mode (Best for Creating Real Requests)
Use the interactive CLI to create your own automation request:

```bash
python cli.py
```

Follow the prompts to create a complete automation request. The CLI will:
- Guide you through all required fields
- Let you add multiple systems and notifications
- Validate your input
- Export to JSON at the end

### 3. See Full Examples (Learn Advanced Features)
Run comprehensive examples showing different scenarios:

```bash
python example_usage.py
```

This demonstrates:
- Simple daily reports
- Complex multi-system integrations
- Different notification types
- Various export formats

### 4. Programmatic Use (For Developers)
Use the agent in your own Python code:

```python
from automation_request_agent import (
    AutomationRequestAgent,
    Stakeholder,
    PriorityLevel,
    NotificationType
)

agent = AutomationRequestAgent()

# Create requester
requester = Stakeholder(
    name="Your Name",
    role="Your Role",
    email="your.email@company.com"
)

# Create request
request = agent.create_request(
    title="My Automation",
    description="What it does",
    business_purpose="Why we need it",
    requested_by=requester
)

# Add a system
agent.add_system(
    request,
    name="System Name",
    system_type="source",  # or "target", "intermediate"
    description="System description"
)

# Add notification
agent.add_notification(
    request,
    notification_type=NotificationType.EMAIL,
    recipients=["team@company.com"],
    trigger="on_success"
)

# Set schedule
agent.set_schedule(
    request,
    frequency="daily",
    cron_expression="0 9 * * *"
)

# Validate
is_valid, errors = agent.validate_request(request)

# Export
if is_valid:
    print(request.to_json())
```

## Testing

Run the test suite to verify everything works:

```bash
python -m unittest test_automation_request_agent.py -v
```

## What Gets Captured?

The agent captures comprehensive details about automation requests:

✅ **Basic Info**: Title, description, business purpose  
✅ **Systems**: All systems involved with API details  
✅ **Notifications**: Multiple channels (Email, Slack, etc.)  
✅ **Schedule**: When to run (cron, event-driven, etc.)  
✅ **Stakeholders**: Who's involved and their roles  
✅ **Success Criteria**: How to measure success  
✅ **Compliance**: GDPR, SOX, etc.  
✅ **Risks**: Dependencies and concerns  

## Output Formats

1. **JSON** - Machine-readable format for integration
2. **Summary** - Human-readable text format
3. **Interactive** - During CLI usage

## Next Steps

1. Try the quick demo: `python demo.py`
2. Create your first request: `python cli.py`
3. Read the full README: `README.md`
4. Explore the code: `automation_request_agent.py`

## Getting Help

- Check `README.md` for full documentation
- Look at examples in `example_usage.py`
- Run tests to verify setup: `python -m unittest test_automation_request_agent.py`

## Tips

- Start with the demo to understand capabilities
- Use the interactive CLI for real requests
- Export to JSON to integrate with other tools
- Add validation checks before submitting requests
- Use descriptive titles and clear business purposes
