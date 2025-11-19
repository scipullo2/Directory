# Automation Request Form Agent

A comprehensive Python-based agent for intaking and managing business automation requests. This tool helps collect all relevant details about automation requirements including systems involved, notification needs, schedules, and stakeholder information.

## Features

- **Comprehensive Form Structure**: Captures all essential details for automation requests
- **System Integration Tracking**: Documents all systems involved with authentication details
- **Notification Management**: Supports multiple notification types (Email, Slack, Webhooks, SMS, Teams)
- **Schedule Definition**: Flexible scheduling with cron expressions and timezone support
- **Stakeholder Management**: Tracks all stakeholders with roles and responsibilities
- **Validation**: Built-in validation to ensure all required information is provided
- **Export Capabilities**: Export requests as JSON or human-readable summaries
- **Interactive CLI**: User-friendly command-line interface for creating requests
- **Extensible**: Easy to extend with custom fields and validation rules

## Installation

This is a standalone Python module with no external dependencies (uses only Python standard library).

```bash
# Clone the repository
git clone https://github.com/scipullo2/Directory.git
cd Directory

# No installation required - pure Python!
```

## Quick Start

### Option 1: Interactive CLI

The easiest way to create an automation request is using the interactive CLI:

```bash
python cli.py
```

This will guide you through all the steps to create a complete automation request.

### Option 2: Programmatic Usage

```python
from automation_request_agent import (
    AutomationRequestAgent,
    Stakeholder,
    PriorityLevel,
    NotificationType
)

# Initialize the agent
agent = AutomationRequestAgent()

# Create the requester
requester = Stakeholder(
    name="John Smith",
    role="Business Analyst",
    email="john.smith@company.com",
    department="Finance"
)

# Create the automation request
request = agent.create_request(
    title="Daily Sales Report Automation",
    description="Automate daily sales report generation and distribution",
    business_purpose="Reduce manual effort and ensure timely delivery",
    requested_by=requester,
    priority=PriorityLevel.HIGH
)

# Add systems
agent.add_system(
    request,
    name="Salesforce",
    system_type="source",
    description="CRM system containing sales data",
    api_endpoint="https://api.salesforce.com/v1",
    authentication_required=True,
    authentication_type="oauth"
)

# Add notifications
agent.add_notification(
    request,
    notification_type=NotificationType.EMAIL,
    recipients=["finance-team@company.com"],
    trigger="on_success"
)

# Set schedule
agent.set_schedule(
    request,
    frequency="daily",
    cron_expression="0 8 * * *",
    timezone="America/New_York"
)

# Validate the request
is_valid, errors = agent.validate_request(request)

if is_valid:
    # Export as JSON
    print(agent.export_request(request, format="json"))
    
    # Or get a summary
    print(agent.get_request_summary(request))
```

### Option 3: Run Examples

```bash
python example_usage.py
```

This will run several example scenarios demonstrating different use cases.

## Form Fields

### Basic Information
- **Title**: Short, descriptive title for the automation
- **Description**: Detailed description of what the automation does
- **Business Purpose**: Justification and business value
- **Requested By**: Primary stakeholder submitting the request
- **Priority**: LOW, MEDIUM, HIGH, or CRITICAL

### Systems Involved
Each system can include:
- Name and type (source, target, intermediate)
- Description
- API endpoint (if applicable)
- Authentication requirements and type

### Notification Requirements
Configure multiple notifications with:
- Type: Email, Slack, Webhook, SMS, Teams
- Recipients (emails, channels, URLs)
- Trigger: on_success, on_failure, on_start, always
- Custom message templates
- Additional configuration (webhook URLs, etc.)

### Schedule Requirements
- Frequency (daily, weekly, monthly, hourly, on-demand, event-driven)
- Cron expression for precise timing
- Timezone
- Start and end dates
- Additional scheduling details

### Stakeholders
- Additional stakeholders beyond the requester
- Roles and responsibilities (owner, approver, reviewer, user)
- Contact information
- Department

### Success Criteria
- Define measurable success criteria
- Performance requirements
- Data volume estimates
- SLA requirements

### Compliance & Risk
- Compliance requirements (GDPR, SOX, HIPAA, etc.)
- Dependencies on other systems or processes
- Identified risks and concerns

## API Reference

### AutomationRequestAgent

The main agent class for managing automation requests.

#### Methods

- `create_request(title, description, business_purpose, requested_by, **kwargs)`: Create a new automation request
- `add_system(request, name, system_type, description, **kwargs)`: Add a system integration
- `add_notification(request, notification_type, recipients, trigger, **kwargs)`: Add a notification requirement
- `set_schedule(request, frequency, **kwargs)`: Set schedule requirements
- `add_stakeholder(request, name, role, email, **kwargs)`: Add a stakeholder
- `validate_request(request)`: Validate the request and return errors
- `get_request_summary(request)`: Get human-readable summary
- `export_request(request, format)`: Export in specified format (json, summary)

### Data Classes

- `AutomationRequest`: Main request container
- `Stakeholder`: Represents a person involved in the automation
- `SystemIntegration`: Represents a system/application
- `NotificationRequirement`: Notification configuration
- `ScheduleRequirement`: Scheduling configuration

### Enums

- `PriorityLevel`: LOW, MEDIUM, HIGH, CRITICAL
- `NotificationType`: EMAIL, SLACK, WEBHOOK, SMS, TEAMS

## Testing

Run the test suite:

```bash
python -m unittest test_automation_request_agent.py
```

Or run with verbose output:

```bash
python -m unittest test_automation_request_agent.py -v
```

## Examples

### Example 1: Simple Daily Report

```python
agent = AutomationRequestAgent()

request = agent.create_request(
    title="Daily Sales Report",
    description="Generate and email daily sales report",
    business_purpose="Keep management informed of daily performance",
    requested_by=Stakeholder("Jane Doe", "Manager", "jane@company.com")
)

agent.add_system(request, "Salesforce", "source", "CRM system")
agent.add_notification(
    request,
    NotificationType.EMAIL,
    ["management@company.com"],
    "on_success"
)
agent.set_schedule(request, "daily", cron_expression="0 8 * * *")
```

### Example 2: Complex Multi-System Integration

```python
# Create request with high priority
request = agent.create_request(
    title="Inventory Sync",
    description="Real-time inventory synchronization",
    business_purpose="Maintain accurate inventory across warehouses",
    requested_by=requester,
    priority=PriorityLevel.CRITICAL
)

# Add multiple systems
for warehouse in ["North", "South", "East", "West"]:
    agent.add_system(
        request,
        name=f"{warehouse} WMS",
        system_type="source",
        description=f"{warehouse} warehouse system"
    )

agent.add_system(request, "ERP", "target", "Central ERP system")

# Multiple notification channels
agent.add_notification(
    request,
    NotificationType.EMAIL,
    ["ops@company.com"],
    "on_success"
)

agent.add_notification(
    request,
    NotificationType.SLACK,
    ["#alerts"],
    "on_failure"
)

# Event-driven schedule
agent.set_schedule(request, "event-driven")
```

## Use Cases

This agent is ideal for:

1. **IT Service Management**: Standardize automation request intake
2. **RPA Implementations**: Document automation requirements for RPA tools
3. **Integration Projects**: Plan and document system integrations
4. **Process Automation**: Capture requirements for workflow automations
5. **DevOps**: Document CI/CD pipeline requirements
6. **Data Engineering**: Plan ETL and data pipeline automations

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is available for use under standard open source terms.

## Support

For questions or issues, please open a GitHub issue in the repository.

## Roadmap

Future enhancements planned:
- [ ] Web UI for form submission
- [ ] Integration with ticketing systems (Jira, ServiceNow)
- [ ] Template library for common automation types
- [ ] Approval workflow management
- [ ] Cost estimation capabilities
- [ ] Integration with automation platforms (Zapier, Power Automate, etc.)