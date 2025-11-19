"""
Automation Request Form Agent

This agent intakes and processes automation request forms for business requirements.
It collects all relevant details about the automation including systems involved,
notifications, schedules, and stakeholders.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import json


class PriorityLevel(Enum):
    """Priority levels for automation requests"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationType(Enum):
    """Types of notifications supported"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    TEAMS = "teams"


@dataclass
class SystemIntegration:
    """Represents a system involved in the automation"""
    name: str
    type: str  # e.g., "source", "target", "intermediate"
    description: str
    api_endpoint: Optional[str] = None
    authentication_required: bool = False
    authentication_type: Optional[str] = None  # e.g., "oauth", "api_key", "basic"


@dataclass
class NotificationRequirement:
    """Represents notification requirements for the automation"""
    type: NotificationType
    recipients: List[str]
    trigger: str  # e.g., "on_success", "on_failure", "on_start", "always"
    template: Optional[str] = None
    additional_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScheduleRequirement:
    """Represents scheduling requirements for the automation"""
    frequency: str  # e.g., "daily", "weekly", "monthly", "on-demand", "event-driven"
    cron_expression: Optional[str] = None
    timezone: str = "UTC"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    additional_details: str = ""


@dataclass
class Stakeholder:
    """Represents a stakeholder in the automation"""
    name: str
    role: str
    email: str
    department: Optional[str] = None
    responsibility: str = ""  # e.g., "owner", "approver", "reviewer", "user"


@dataclass
class AutomationRequest:
    """Complete automation request form data"""
    # Basic Information
    title: str
    description: str
    business_purpose: str
    requested_by: Stakeholder
    request_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Systems and Integrations
    systems_involved: List[SystemIntegration] = field(default_factory=list)
    
    # Notifications
    notifications: List[NotificationRequirement] = field(default_factory=list)
    
    # Scheduling
    schedule: Optional[ScheduleRequirement] = None
    
    # Priority and Stakeholders
    priority: PriorityLevel = PriorityLevel.MEDIUM
    stakeholders: List[Stakeholder] = field(default_factory=list)
    
    # Success Criteria and Requirements
    success_criteria: List[str] = field(default_factory=list)
    data_volume_estimate: Optional[str] = None
    performance_requirements: Optional[str] = None
    compliance_requirements: List[str] = field(default_factory=list)
    
    # Additional Information
    dependencies: List[str] = field(default_factory=list)
    risks_and_concerns: List[str] = field(default_factory=list)
    additional_requirements: str = ""
    attachments: List[str] = field(default_factory=list)
    
    # Metadata
    request_id: Optional[str] = None
    status: str = "submitted"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the request to a dictionary"""
        def convert_value(value):
            if isinstance(value, Enum):
                return value.value
            elif isinstance(value, list):
                return [convert_value(item) for item in value]
            elif hasattr(value, '__dict__'):
                return {k: convert_value(v) for k, v in value.__dict__.items()}
            else:
                return value
        
        return {k: convert_value(v) for k, v in self.__dict__.items()}

    def to_json(self, indent: int = 2) -> str:
        """Convert the request to JSON format"""
        return json.dumps(self.to_dict(), indent=indent)


class AutomationRequestAgent:
    """
    Agent that intakes and processes automation request forms.
    
    This agent helps collect all necessary information for automation requests
    including systems, notifications, schedules, and business requirements.
    """
    
    def __init__(self):
        self.requests: List[AutomationRequest] = []
    
    def create_request(
        self,
        title: str,
        description: str,
        business_purpose: str,
        requested_by: Stakeholder,
        **kwargs
    ) -> AutomationRequest:
        """
        Create a new automation request.
        
        Args:
            title: Title of the automation request
            description: Detailed description of the automation
            business_purpose: Business justification for the automation
            requested_by: Stakeholder submitting the request
            **kwargs: Additional optional fields
            
        Returns:
            AutomationRequest: The created request
        """
        request = AutomationRequest(
            title=title,
            description=description,
            business_purpose=business_purpose,
            requested_by=requested_by,
            **kwargs
        )
        self.requests.append(request)
        return request
    
    def add_system(
        self,
        request: AutomationRequest,
        name: str,
        system_type: str,
        description: str,
        **kwargs
    ) -> SystemIntegration:
        """Add a system integration to the request"""
        system = SystemIntegration(
            name=name,
            type=system_type,
            description=description,
            **kwargs
        )
        request.systems_involved.append(system)
        return system
    
    def add_notification(
        self,
        request: AutomationRequest,
        notification_type: NotificationType,
        recipients: List[str],
        trigger: str,
        **kwargs
    ) -> NotificationRequirement:
        """Add a notification requirement to the request"""
        notification = NotificationRequirement(
            type=notification_type,
            recipients=recipients,
            trigger=trigger,
            **kwargs
        )
        request.notifications.append(notification)
        return notification
    
    def set_schedule(
        self,
        request: AutomationRequest,
        frequency: str,
        **kwargs
    ) -> ScheduleRequirement:
        """Set schedule requirements for the request"""
        schedule = ScheduleRequirement(
            frequency=frequency,
            **kwargs
        )
        request.schedule = schedule
        return schedule
    
    def add_stakeholder(
        self,
        request: AutomationRequest,
        name: str,
        role: str,
        email: str,
        **kwargs
    ) -> Stakeholder:
        """Add a stakeholder to the request"""
        stakeholder = Stakeholder(
            name=name,
            role=role,
            email=email,
            **kwargs
        )
        request.stakeholders.append(stakeholder)
        return stakeholder
    
    def validate_request(self, request: AutomationRequest) -> tuple[bool, List[str]]:
        """
        Validate the automation request.
        
        Returns:
            tuple: (is_valid, list of validation errors)
        """
        errors = []
        
        # Required fields
        if not request.title or len(request.title.strip()) == 0:
            errors.append("Title is required")
        
        if not request.description or len(request.description.strip()) == 0:
            errors.append("Description is required")
        
        if not request.business_purpose or len(request.business_purpose.strip()) == 0:
            errors.append("Business purpose is required")
        
        if not request.requested_by:
            errors.append("Requested by stakeholder is required")
        
        # System validations
        if not request.systems_involved:
            errors.append("At least one system must be specified")
        
        # Notification validations
        for notification in request.notifications:
            if not notification.recipients:
                errors.append(f"Notification of type {notification.type.value} has no recipients")
        
        # Stakeholder validations
        for stakeholder in [request.requested_by] + request.stakeholders:
            if stakeholder and not stakeholder.email:
                errors.append(f"Stakeholder {stakeholder.name} is missing email")
        
        return (len(errors) == 0, errors)
    
    def get_request_summary(self, request: AutomationRequest) -> str:
        """Generate a human-readable summary of the request"""
        summary = f"""
Automation Request Summary
==========================

Title: {request.title}
Priority: {request.priority.value.upper()}
Requested By: {request.requested_by.name} ({request.requested_by.email})
Request Date: {request.request_date}
Status: {request.status}

Description:
{request.description}

Business Purpose:
{request.business_purpose}

Systems Involved ({len(request.systems_involved)}):
"""
        for system in request.systems_involved:
            summary += f"  - {system.name} ({system.type}): {system.description}\n"
        
        if request.notifications:
            summary += f"\nNotifications ({len(request.notifications)}):\n"
            for notif in request.notifications:
                summary += f"  - {notif.type.value} to {', '.join(notif.recipients)} ({notif.trigger})\n"
        
        if request.schedule:
            summary += f"\nSchedule:\n"
            summary += f"  - Frequency: {request.schedule.frequency}\n"
            if request.schedule.cron_expression:
                summary += f"  - Cron: {request.schedule.cron_expression}\n"
            summary += f"  - Timezone: {request.schedule.timezone}\n"
        
        if request.stakeholders:
            summary += f"\nAdditional Stakeholders ({len(request.stakeholders)}):\n"
            for stakeholder in request.stakeholders:
                summary += f"  - {stakeholder.name} ({stakeholder.role}): {stakeholder.email}\n"
        
        if request.success_criteria:
            summary += f"\nSuccess Criteria:\n"
            for criteria in request.success_criteria:
                summary += f"  - {criteria}\n"
        
        if request.compliance_requirements:
            summary += f"\nCompliance Requirements:\n"
            for req in request.compliance_requirements:
                summary += f"  - {req}\n"
        
        return summary
    
    def export_request(self, request: AutomationRequest, format: str = "json") -> str:
        """
        Export the request in various formats.
        
        Args:
            request: The request to export
            format: Export format ("json", "summary")
            
        Returns:
            str: Formatted export
        """
        if format == "json":
            return request.to_json()
        elif format == "summary":
            return self.get_request_summary(request)
        else:
            raise ValueError(f"Unsupported export format: {format}")
