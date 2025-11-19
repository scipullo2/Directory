"""
Example usage of the Automation Request Form Agent

This script demonstrates how to use the AutomationRequestAgent to create
and manage automation requests.
"""

from automation_request_agent import (
    AutomationRequestAgent,
    Stakeholder,
    PriorityLevel,
    NotificationType
)


def example_basic_request():
    """Example: Create a basic automation request"""
    print("=" * 60)
    print("Example 1: Basic Automation Request")
    print("=" * 60)
    
    # Initialize the agent
    agent = AutomationRequestAgent()
    
    # Create the requester
    requester = Stakeholder(
        name="John Smith",
        role="Business Analyst",
        email="john.smith@company.com",
        department="Finance",
        responsibility="owner"
    )
    
    # Create the automation request
    request = agent.create_request(
        title="Daily Sales Report Automation",
        description="Automate the generation and distribution of daily sales reports from Salesforce to the finance team",
        business_purpose="Reduce manual effort in report generation and ensure timely delivery of sales data to stakeholders",
        requested_by=requester,
        priority=PriorityLevel.HIGH
    )
    
    # Add systems involved
    agent.add_system(
        request,
        name="Salesforce",
        system_type="source",
        description="CRM system containing sales data",
        api_endpoint="https://api.salesforce.com/v1",
        authentication_required=True,
        authentication_type="oauth"
    )
    
    agent.add_system(
        request,
        name="Email Server",
        system_type="target",
        description="Internal email system for report distribution",
        authentication_required=True,
        authentication_type="smtp"
    )
    
    # Add notification requirements
    agent.add_notification(
        request,
        notification_type=NotificationType.EMAIL,
        recipients=["finance-team@company.com", "john.smith@company.com"],
        trigger="on_success",
        template="Daily sales report has been generated and sent successfully."
    )
    
    agent.add_notification(
        request,
        notification_type=NotificationType.SLACK,
        recipients=["#finance-alerts"],
        trigger="on_failure",
        template="ALERT: Daily sales report automation failed. Please investigate.",
        additional_config={"webhook_url": "https://hooks.slack.com/services/xxx"}
    )
    
    # Set schedule
    agent.set_schedule(
        request,
        frequency="daily",
        cron_expression="0 8 * * *",  # 8 AM daily
        timezone="America/New_York",
        additional_details="Run at 8 AM Eastern Time every business day"
    )
    
    # Add stakeholders
    agent.add_stakeholder(
        request,
        name="Sarah Johnson",
        role="Finance Manager",
        email="sarah.johnson@company.com",
        department="Finance",
        responsibility="approver"
    )
    
    agent.add_stakeholder(
        request,
        name="Mike Davis",
        role="IT Manager",
        email="mike.davis@company.com",
        department="IT",
        responsibility="reviewer"
    )
    
    # Add success criteria
    request.success_criteria = [
        "Reports delivered by 8:30 AM daily",
        "100% accuracy in data extraction",
        "Zero manual intervention required",
        "Email delivery confirmation received"
    ]
    
    # Add compliance requirements
    request.compliance_requirements = [
        "GDPR compliant data handling",
        "SOX compliance for financial data",
        "Data encryption in transit and at rest"
    ]
    
    # Additional details
    request.data_volume_estimate = "~500 sales records per day, ~2MB report size"
    request.performance_requirements = "Complete within 5 minutes"
    request.dependencies = ["Salesforce API access", "SMTP credentials"]
    request.risks_and_concerns = ["API rate limits", "Email deliverability issues"]
    
    # Validate the request
    is_valid, errors = agent.validate_request(request)
    
    if is_valid:
        print("✓ Request is valid\n")
    else:
        print("✗ Request has validation errors:")
        for error in errors:
            print(f"  - {error}")
        print()
    
    # Display summary
    print(agent.get_request_summary(request))
    print("\n" + "=" * 60 + "\n")
    
    return request


def example_complex_request():
    """Example: Create a complex automation request with multiple integrations"""
    print("=" * 60)
    print("Example 2: Complex Multi-System Automation")
    print("=" * 60)
    
    agent = AutomationRequestAgent()
    
    requester = Stakeholder(
        name="Emily Chen",
        role="Operations Director",
        email="emily.chen@company.com",
        department="Operations"
    )
    
    request = agent.create_request(
        title="Inventory Synchronization Across Multiple Warehouses",
        description="Synchronize inventory levels across 5 warehouse management systems and update central ERP in real-time",
        business_purpose="Maintain accurate inventory counts, prevent stockouts, and optimize warehouse operations across all facilities",
        requested_by=requester,
        priority=PriorityLevel.CRITICAL
    )
    
    # Add multiple systems
    warehouses = ["North", "South", "East", "West", "Central"]
    for warehouse in warehouses:
        agent.add_system(
            request,
            name=f"{warehouse} Warehouse WMS",
            system_type="source",
            description=f"Warehouse Management System for {warehouse} facility",
            api_endpoint=f"https://wms-{warehouse.lower()}.company.com/api",
            authentication_required=True,
            authentication_type="api_key"
        )
    
    agent.add_system(
        request,
        name="SAP ERP",
        system_type="target",
        description="Central ERP system for inventory tracking",
        api_endpoint="https://erp.company.com/api",
        authentication_required=True,
        authentication_type="oauth"
    )
    
    # Add notifications for different scenarios
    agent.add_notification(
        request,
        notification_type=NotificationType.EMAIL,
        recipients=["operations@company.com"],
        trigger="on_success",
        template="Inventory sync completed successfully for all warehouses."
    )
    
    agent.add_notification(
        request,
        notification_type=NotificationType.SLACK,
        recipients=["#operations-critical"],
        trigger="on_failure"
    )
    
    agent.add_notification(
        request,
        notification_type=NotificationType.WEBHOOK,
        recipients=["https://monitoring.company.com/webhook"],
        trigger="always",
        additional_config={"include_metrics": True}
    )
    
    # Set real-time schedule
    agent.set_schedule(
        request,
        frequency="event-driven",
        additional_details="Triggered by inventory changes in any warehouse system, with 5-minute batching"
    )
    
    # Add stakeholders
    agent.add_stakeholder(
        request,
        name="Robert Brown",
        role="Warehouse Manager",
        email="robert.brown@company.com",
        responsibility="user"
    )
    
    request.success_criteria = [
        "Inventory sync lag < 5 minutes",
        "99.9% uptime",
        "Zero data loss",
        "Discrepancy detection and alerting"
    ]
    
    request.data_volume_estimate = "~10,000 SKUs, 500 updates/hour peak"
    request.performance_requirements = "Process 1000 updates/minute"
    request.compliance_requirements = ["SOX compliance", "Audit trail required"]
    request.dependencies = ["VPN access to all warehouses", "ERP API quota increase"]
    request.risks_and_concerns = [
        "Network connectivity issues between sites",
        "API rate limiting on ERP system",
        "Data conflicts between warehouses"
    ]
    
    is_valid, errors = agent.validate_request(request)
    print(f"Validation: {'✓ Valid' if is_valid else '✗ Invalid'}\n")
    
    print(agent.get_request_summary(request))
    print("\n" + "=" * 60 + "\n")
    
    return request


def example_export_formats():
    """Example: Export request in different formats"""
    print("=" * 60)
    print("Example 3: Export Formats")
    print("=" * 60)
    
    agent = AutomationRequestAgent()
    
    requester = Stakeholder(
        name="Alice Williams",
        role="Data Engineer",
        email="alice.williams@company.com"
    )
    
    request = agent.create_request(
        title="Customer Data Export Automation",
        description="Export customer data from database to data warehouse nightly",
        business_purpose="Enable business intelligence and analytics",
        requested_by=requester
    )
    
    agent.add_system(
        request,
        name="PostgreSQL Database",
        system_type="source",
        description="Production customer database"
    )
    
    agent.add_system(
        request,
        name="Snowflake Data Warehouse",
        system_type="target",
        description="Analytics data warehouse"
    )
    
    agent.set_schedule(request, frequency="daily", cron_expression="0 2 * * *")
    
    # Export as JSON
    print("JSON Export:")
    print("-" * 60)
    print(agent.export_request(request, format="json"))
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # Run examples
    request1 = example_basic_request()
    request2 = example_complex_request()
    example_export_formats()
    
    print("\nAll examples completed successfully!")
