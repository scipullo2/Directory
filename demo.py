#!/usr/bin/env python3
"""
Quick Demo of Automation Request Form Agent

This demonstrates the agent's capabilities with a simple example.
"""

from automation_request_agent import (
    AutomationRequestAgent,
    Stakeholder,
    PriorityLevel,
    NotificationType
)


def main():
    print("\n" + "="*70)
    print("AUTOMATION REQUEST FORM AGENT - Quick Demo")
    print("="*70 + "\n")
    
    # Initialize the agent
    agent = AutomationRequestAgent()
    print("✓ Agent initialized\n")
    
    # Create a simple automation request
    print("Creating automation request...")
    requester = Stakeholder(
        name="Demo User",
        role="Business Analyst",
        email="demo.user@example.com",
        department="Operations"
    )
    
    request = agent.create_request(
        title="Customer Data Sync Automation",
        description="Synchronize customer data between CRM and marketing platform nightly",
        business_purpose="Ensure marketing has up-to-date customer information for campaigns",
        requested_by=requester,
        priority=PriorityLevel.MEDIUM
    )
    print("✓ Request created\n")
    
    # Add systems
    print("Adding systems...")
    agent.add_system(
        request,
        name="Salesforce CRM",
        system_type="source",
        description="Customer relationship management system",
        api_endpoint="https://api.salesforce.com/v1",
        authentication_required=True,
        authentication_type="oauth"
    )
    
    agent.add_system(
        request,
        name="HubSpot Marketing",
        system_type="target",
        description="Marketing automation platform",
        api_endpoint="https://api.hubspot.com/v3",
        authentication_required=True,
        authentication_type="api_key"
    )
    print("✓ Added 2 systems\n")
    
    # Add notifications
    print("Adding notifications...")
    agent.add_notification(
        request,
        notification_type=NotificationType.EMAIL,
        recipients=["ops-team@example.com"],
        trigger="on_success",
        template="Daily customer sync completed successfully at {timestamp}"
    )
    
    agent.add_notification(
        request,
        notification_type=NotificationType.SLACK,
        recipients=["#ops-alerts"],
        trigger="on_failure",
        template="ALERT: Customer sync failed - please investigate"
    )
    print("✓ Added 2 notifications\n")
    
    # Set schedule
    print("Setting schedule...")
    agent.set_schedule(
        request,
        frequency="daily",
        cron_expression="0 2 * * *",  # 2 AM daily
        timezone="UTC",
        additional_details="Runs at 2 AM UTC every day during maintenance window"
    )
    print("✓ Schedule configured\n")
    
    # Add success criteria
    request.success_criteria = [
        "All customer records synced within 30 minutes",
        "100% data accuracy",
        "No duplicate records created",
        "Sync completion notification received"
    ]
    
    request.compliance_requirements = ["GDPR compliance", "Data encryption in transit"]
    request.data_volume_estimate = "~5000 customer records per day"
    request.performance_requirements = "Complete sync within 30 minutes"
    
    # Validate
    print("Validating request...")
    is_valid, errors = agent.validate_request(request)
    
    if is_valid:
        print("✓ Validation passed!\n")
    else:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        print()
        return
    
    # Display summary
    print("="*70)
    print("REQUEST SUMMARY")
    print("="*70)
    print(agent.get_request_summary(request))
    
    # Export as JSON
    print("\n" + "="*70)
    print("JSON EXPORT (first 500 characters)")
    print("="*70)
    json_export = agent.export_request(request, format="json")
    print(json_export[:500] + "...\n")
    
    print("="*70)
    print("Demo completed successfully!")
    print("="*70)
    print("\nTo try the interactive CLI, run: python cli.py")
    print("To see more examples, run: python example_usage.py")
    print("To run tests, run: python -m unittest test_automation_request_agent.py\n")


if __name__ == "__main__":
    main()
