#!/usr/bin/env python3
"""
Interactive CLI for Automation Request Form Agent

This provides an interactive command-line interface for creating automation
requests step by step.
"""

import sys
from automation_request_agent import (
    AutomationRequestAgent,
    Stakeholder,
    PriorityLevel,
    NotificationType,
    AutomationRequest
)


class InteractiveCLI:
    """Interactive CLI for creating automation requests"""
    
    def __init__(self):
        self.agent = AutomationRequestAgent()
    
    def get_input(self, prompt: str, required: bool = True, default: str = None) -> str:
        """Get user input with optional default value"""
        full_prompt = prompt
        if default:
            full_prompt += f" [{default}]"
        full_prompt += ": "
        
        while True:
            value = input(full_prompt).strip()
            if not value and default:
                return default
            if value or not required:
                return value
            if required:
                print("  This field is required. Please provide a value.")
    
    def get_yes_no(self, prompt: str, default: bool = False) -> bool:
        """Get yes/no input from user"""
        default_str = "Y/n" if default else "y/N"
        response = self.get_input(f"{prompt} ({default_str})", required=False, default="y" if default else "n")
        return response.lower() in ['y', 'yes']
    
    def get_list_input(self, prompt: str, required: bool = False) -> list:
        """Get a list of values from user"""
        print(f"\n{prompt}")
        print("  (Enter items one per line, empty line to finish)")
        items = []
        while True:
            item = input("  - ").strip()
            if not item:
                break
            items.append(item)
        
        if required and not items:
            print("  At least one item is required.")
            return self.get_list_input(prompt, required)
        
        return items
    
    def create_stakeholder(self, prompt: str) -> Stakeholder:
        """Create a stakeholder interactively"""
        print(f"\n{prompt}")
        name = self.get_input("  Name")
        role = self.get_input("  Role")
        email = self.get_input("  Email")
        department = self.get_input("  Department (optional)", required=False)
        responsibility = self.get_input("  Responsibility (e.g., owner, approver, user)", required=False, default="user")
        
        return Stakeholder(
            name=name,
            role=role,
            email=email,
            department=department if department else None,
            responsibility=responsibility
        )
    
    def select_priority(self) -> PriorityLevel:
        """Let user select priority level"""
        print("\nSelect Priority Level:")
        priorities = list(PriorityLevel)
        for i, priority in enumerate(priorities, 1):
            print(f"  {i}. {priority.value.upper()}")
        
        while True:
            choice = self.get_input("Enter number (1-4)", default="2")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(priorities):
                    return priorities[idx]
            except ValueError:
                pass
            print("  Invalid choice. Please enter a number between 1 and 4.")
    
    def add_systems(self, request: AutomationRequest):
        """Add systems to the request"""
        print("\n" + "=" * 60)
        print("SYSTEMS INVOLVED")
        print("=" * 60)
        
        while True:
            print("\nAdd a system:")
            name = self.get_input("  System name")
            system_type = self.get_input("  Type (source/target/intermediate)", default="source")
            description = self.get_input("  Description")
            
            has_api = self.get_yes_no("  Does this system have an API endpoint?")
            api_endpoint = None
            auth_required = False
            auth_type = None
            
            if has_api:
                api_endpoint = self.get_input("  API endpoint URL", required=False)
                auth_required = self.get_yes_no("  Is authentication required?")
                if auth_required:
                    auth_type = self.get_input("  Authentication type (oauth/api_key/basic)", required=False)
            
            self.agent.add_system(
                request,
                name=name,
                system_type=system_type,
                description=description,
                api_endpoint=api_endpoint,
                authentication_required=auth_required,
                authentication_type=auth_type
            )
            
            if not self.get_yes_no("\nAdd another system?"):
                break
    
    def add_notifications(self, request: AutomationRequest):
        """Add notification requirements"""
        print("\n" + "=" * 60)
        print("NOTIFICATION REQUIREMENTS")
        print("=" * 60)
        
        if not self.get_yes_no("\nDo you need notifications for this automation?", default=True):
            return
        
        while True:
            print("\nAdd a notification:")
            print("  Available types: email, slack, webhook, sms, teams")
            notif_type_str = self.get_input("  Notification type", default="email")
            
            try:
                notif_type = NotificationType(notif_type_str.lower())
            except ValueError:
                print(f"  Invalid type. Using email.")
                notif_type = NotificationType.EMAIL
            
            recipients = self.get_list_input("  Recipients (emails, channels, or URLs):", required=True)
            trigger = self.get_input("  Trigger (on_success/on_failure/on_start/always)", default="on_success")
            template = self.get_input("  Message template (optional)", required=False)
            
            self.agent.add_notification(
                request,
                notification_type=notif_type,
                recipients=recipients,
                trigger=trigger,
                template=template if template else None
            )
            
            if not self.get_yes_no("\nAdd another notification?"):
                break
    
    def add_schedule(self, request: AutomationRequest):
        """Add schedule requirements"""
        print("\n" + "=" * 60)
        print("SCHEDULE REQUIREMENTS")
        print("=" * 60)
        
        if not self.get_yes_no("\nDoes this automation need a schedule?", default=True):
            return
        
        print("\nSchedule details:")
        frequency = self.get_input("  Frequency (daily/weekly/monthly/hourly/on-demand/event-driven)", default="daily")
        cron_expression = self.get_input("  Cron expression (optional)", required=False)
        timezone = self.get_input("  Timezone", default="UTC")
        additional_details = self.get_input("  Additional details (optional)", required=False)
        
        self.agent.set_schedule(
            request,
            frequency=frequency,
            cron_expression=cron_expression if cron_expression else None,
            timezone=timezone,
            additional_details=additional_details
        )
    
    def add_stakeholders(self, request: AutomationRequest):
        """Add additional stakeholders"""
        print("\n" + "=" * 60)
        print("ADDITIONAL STAKEHOLDERS")
        print("=" * 60)
        
        if not self.get_yes_no("\nAre there additional stakeholders (approvers, reviewers, etc.)?"):
            return
        
        while True:
            stakeholder = self.create_stakeholder("\nAdd stakeholder:")
            self.agent.add_stakeholder(
                request,
                name=stakeholder.name,
                role=stakeholder.role,
                email=stakeholder.email,
                department=stakeholder.department,
                responsibility=stakeholder.responsibility
            )
            
            if not self.get_yes_no("\nAdd another stakeholder?"):
                break
    
    def add_additional_details(self, request: AutomationRequest):
        """Add additional details to the request"""
        print("\n" + "=" * 60)
        print("ADDITIONAL DETAILS")
        print("=" * 60)
        
        # Success criteria
        if self.get_yes_no("\nAdd success criteria?", default=True):
            request.success_criteria = self.get_list_input("Success criteria:")
        
        # Compliance requirements
        if self.get_yes_no("\nAre there compliance requirements?"):
            request.compliance_requirements = self.get_list_input("Compliance requirements:")
        
        # Data volume
        request.data_volume_estimate = self.get_input("\nEstimated data volume (optional)", required=False)
        
        # Performance requirements
        request.performance_requirements = self.get_input("Performance requirements (optional)", required=False)
        
        # Dependencies
        if self.get_yes_no("\nAre there any dependencies?"):
            request.dependencies = self.get_list_input("Dependencies:")
        
        # Risks and concerns
        if self.get_yes_no("\nAre there any risks or concerns?"):
            request.risks_and_concerns = self.get_list_input("Risks and concerns:")
        
        # Additional requirements
        request.additional_requirements = self.get_input("\nAny additional requirements? (optional)", required=False)
    
    def run(self):
        """Run the interactive CLI"""
        print("=" * 60)
        print("AUTOMATION REQUEST FORM")
        print("=" * 60)
        print("\nWelcome! Let's create an automation request.\n")
        
        # Basic information
        print("=" * 60)
        print("BASIC INFORMATION")
        print("=" * 60)
        
        title = self.get_input("\nRequest Title")
        description = self.get_input("Description")
        business_purpose = self.get_input("Business Purpose/Justification")
        
        # Requester information
        requester = self.create_stakeholder("\nRequester Information:")
        
        # Priority
        priority = self.select_priority()
        
        # Create the request
        request = self.agent.create_request(
            title=title,
            description=description,
            business_purpose=business_purpose,
            requested_by=requester,
            priority=priority
        )
        
        # Add systems
        self.add_systems(request)
        
        # Add notifications
        self.add_notifications(request)
        
        # Add schedule
        self.add_schedule(request)
        
        # Add stakeholders
        self.add_stakeholders(request)
        
        # Add additional details
        self.add_additional_details(request)
        
        # Validate
        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)
        
        is_valid, errors = self.agent.validate_request(request)
        
        if is_valid:
            print("\n✓ Request is valid!")
        else:
            print("\n✗ Request has validation errors:")
            for error in errors:
                print(f"  - {error}")
        
        # Display summary
        print("\n" + "=" * 60)
        print("REQUEST SUMMARY")
        print("=" * 60)
        
        print(self.agent.get_request_summary(request))
        
        # Export options
        print("\n" + "=" * 60)
        print("EXPORT OPTIONS")
        print("=" * 60)
        
        if self.get_yes_no("\nWould you like to export this request as JSON?", default=True):
            filename = self.get_input("Filename", default="automation_request.json")
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w') as f:
                f.write(request.to_json())
            
            print(f"\n✓ Request exported to {filename}")
        
        print("\n" + "=" * 60)
        print("Thank you! Your automation request has been created.")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    try:
        cli = InteractiveCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
