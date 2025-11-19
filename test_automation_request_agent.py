"""
Unit tests for Automation Request Form Agent
"""

import unittest
import json
from automation_request_agent import (
    AutomationRequestAgent,
    AutomationRequest,
    Stakeholder,
    SystemIntegration,
    NotificationRequirement,
    ScheduleRequirement,
    PriorityLevel,
    NotificationType
)


class TestStakeholder(unittest.TestCase):
    """Test Stakeholder dataclass"""
    
    def test_create_stakeholder(self):
        """Test creating a stakeholder"""
        stakeholder = Stakeholder(
            name="John Doe",
            role="Manager",
            email="john@example.com",
            department="IT",
            responsibility="owner"
        )
        
        self.assertEqual(stakeholder.name, "John Doe")
        self.assertEqual(stakeholder.role, "Manager")
        self.assertEqual(stakeholder.email, "john@example.com")
        self.assertEqual(stakeholder.department, "IT")
        self.assertEqual(stakeholder.responsibility, "owner")
    
    def test_stakeholder_optional_fields(self):
        """Test stakeholder with optional fields"""
        stakeholder = Stakeholder(
            name="Jane Smith",
            role="Developer",
            email="jane@example.com"
        )
        
        self.assertIsNone(stakeholder.department)
        self.assertEqual(stakeholder.responsibility, "")


class TestSystemIntegration(unittest.TestCase):
    """Test SystemIntegration dataclass"""
    
    def test_create_system(self):
        """Test creating a system integration"""
        system = SystemIntegration(
            name="Salesforce",
            type="source",
            description="CRM system",
            api_endpoint="https://api.salesforce.com",
            authentication_required=True,
            authentication_type="oauth"
        )
        
        self.assertEqual(system.name, "Salesforce")
        self.assertEqual(system.type, "source")
        self.assertTrue(system.authentication_required)
    
    def test_system_minimal(self):
        """Test system with minimal fields"""
        system = SystemIntegration(
            name="Database",
            type="target",
            description="MySQL database"
        )
        
        self.assertIsNone(system.api_endpoint)
        self.assertFalse(system.authentication_required)


class TestNotificationRequirement(unittest.TestCase):
    """Test NotificationRequirement dataclass"""
    
    def test_create_notification(self):
        """Test creating a notification requirement"""
        notification = NotificationRequirement(
            type=NotificationType.EMAIL,
            recipients=["admin@example.com"],
            trigger="on_success",
            template="Process completed successfully"
        )
        
        self.assertEqual(notification.type, NotificationType.EMAIL)
        self.assertEqual(len(notification.recipients), 1)
        self.assertEqual(notification.trigger, "on_success")
    
    def test_notification_with_config(self):
        """Test notification with additional config"""
        notification = NotificationRequirement(
            type=NotificationType.SLACK,
            recipients=["#alerts"],
            trigger="on_failure",
            additional_config={"webhook_url": "https://hooks.slack.com/xxx"}
        )
        
        self.assertIn("webhook_url", notification.additional_config)


class TestScheduleRequirement(unittest.TestCase):
    """Test ScheduleRequirement dataclass"""
    
    def test_create_schedule(self):
        """Test creating a schedule"""
        schedule = ScheduleRequirement(
            frequency="daily",
            cron_expression="0 8 * * *",
            timezone="America/New_York"
        )
        
        self.assertEqual(schedule.frequency, "daily")
        self.assertEqual(schedule.cron_expression, "0 8 * * *")
        self.assertEqual(schedule.timezone, "America/New_York")


class TestAutomationRequest(unittest.TestCase):
    """Test AutomationRequest dataclass"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.requester = Stakeholder(
            name="Test User",
            role="Analyst",
            email="test@example.com"
        )
    
    def test_create_request(self):
        """Test creating a basic automation request"""
        request = AutomationRequest(
            title="Test Automation",
            description="Test description",
            business_purpose="Test purpose",
            requested_by=self.requester
        )
        
        self.assertEqual(request.title, "Test Automation")
        self.assertEqual(request.status, "submitted")
        self.assertEqual(request.priority, PriorityLevel.MEDIUM)
    
    def test_request_to_dict(self):
        """Test converting request to dictionary"""
        request = AutomationRequest(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester,
            priority=PriorityLevel.HIGH
        )
        
        data = request.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['title'], "Test")
        self.assertEqual(data['priority'], "high")
    
    def test_request_to_json(self):
        """Test converting request to JSON"""
        request = AutomationRequest(
            title="JSON Test",
            description="Test JSON export",
            business_purpose="Testing",
            requested_by=self.requester
        )
        
        json_str = request.to_json()
        
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)
        self.assertEqual(data['title'], "JSON Test")


class TestAutomationRequestAgent(unittest.TestCase):
    """Test AutomationRequestAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = AutomationRequestAgent()
        self.requester = Stakeholder(
            name="Test User",
            role="Analyst",
            email="test@example.com"
        )
    
    def test_create_request(self):
        """Test creating a request through the agent"""
        request = self.agent.create_request(
            title="Agent Test",
            description="Test description",
            business_purpose="Test purpose",
            requested_by=self.requester
        )
        
        self.assertEqual(len(self.agent.requests), 1)
        self.assertEqual(request.title, "Agent Test")
    
    def test_add_system(self):
        """Test adding a system to a request"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        system = self.agent.add_system(
            request,
            name="Test System",
            system_type="source",
            description="A test system"
        )
        
        self.assertEqual(len(request.systems_involved), 1)
        self.assertEqual(system.name, "Test System")
    
    def test_add_notification(self):
        """Test adding a notification to a request"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        notification = self.agent.add_notification(
            request,
            notification_type=NotificationType.EMAIL,
            recipients=["test@example.com"],
            trigger="on_success"
        )
        
        self.assertEqual(len(request.notifications), 1)
        self.assertEqual(notification.type, NotificationType.EMAIL)
    
    def test_set_schedule(self):
        """Test setting a schedule for a request"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        schedule = self.agent.set_schedule(
            request,
            frequency="daily",
            cron_expression="0 9 * * *"
        )
        
        self.assertIsNotNone(request.schedule)
        self.assertEqual(request.schedule.frequency, "daily")
    
    def test_add_stakeholder(self):
        """Test adding a stakeholder to a request"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        stakeholder = self.agent.add_stakeholder(
            request,
            name="Additional User",
            role="Reviewer",
            email="reviewer@example.com"
        )
        
        self.assertEqual(len(request.stakeholders), 1)
        self.assertEqual(stakeholder.name, "Additional User")
    
    def test_validate_valid_request(self):
        """Test validating a valid request"""
        request = self.agent.create_request(
            title="Valid Request",
            description="Valid description",
            business_purpose="Valid purpose",
            requested_by=self.requester
        )
        
        self.agent.add_system(
            request,
            name="System",
            system_type="source",
            description="A system"
        )
        
        is_valid, errors = self.agent.validate_request(request)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_missing_title(self):
        """Test validation fails for missing title"""
        request = AutomationRequest(
            title="",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        is_valid, errors = self.agent.validate_request(request)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("Title" in error for error in errors))
    
    def test_validate_missing_systems(self):
        """Test validation fails when no systems are specified"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        is_valid, errors = self.agent.validate_request(request)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("system" in error.lower() for error in errors))
    
    def test_validate_notification_without_recipients(self):
        """Test validation fails for notification without recipients"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        self.agent.add_system(request, "System", "source", "Desc")
        
        # Manually add notification without recipients
        notification = NotificationRequirement(
            type=NotificationType.EMAIL,
            recipients=[],
            trigger="on_success"
        )
        request.notifications.append(notification)
        
        is_valid, errors = self.agent.validate_request(request)
        
        self.assertFalse(is_valid)
        self.assertTrue(any("recipients" in error.lower() for error in errors))
    
    def test_get_request_summary(self):
        """Test generating a request summary"""
        request = self.agent.create_request(
            title="Summary Test",
            description="Test summary generation",
            business_purpose="Testing",
            requested_by=self.requester
        )
        
        self.agent.add_system(
            request,
            name="Test System",
            system_type="source",
            description="A test system"
        )
        
        summary = self.agent.get_request_summary(request)
        
        self.assertIsInstance(summary, str)
        self.assertIn("Summary Test", summary)
        self.assertIn("Test System", summary)
    
    def test_export_json(self):
        """Test exporting request as JSON"""
        request = self.agent.create_request(
            title="Export Test",
            description="Test export",
            business_purpose="Testing",
            requested_by=self.requester
        )
        
        self.agent.add_system(request, "System", "source", "Desc")
        
        json_export = self.agent.export_request(request, format="json")
        
        self.assertIsInstance(json_export, str)
        data = json.loads(json_export)
        self.assertEqual(data['title'], "Export Test")
    
    def test_export_summary(self):
        """Test exporting request as summary"""
        request = self.agent.create_request(
            title="Summary Export Test",
            description="Test summary export",
            business_purpose="Testing",
            requested_by=self.requester
        )
        
        self.agent.add_system(request, "System", "source", "Desc")
        
        summary_export = self.agent.export_request(request, format="summary")
        
        self.assertIsInstance(summary_export, str)
        self.assertIn("Summary Export Test", summary_export)
    
    def test_export_invalid_format(self):
        """Test that invalid export format raises error"""
        request = self.agent.create_request(
            title="Test",
            description="Desc",
            business_purpose="Purpose",
            requested_by=self.requester
        )
        
        with self.assertRaises(ValueError):
            self.agent.export_request(request, format="invalid")


class TestComplexScenarios(unittest.TestCase):
    """Test complex real-world scenarios"""
    
    def test_multi_system_automation(self):
        """Test automation with multiple systems"""
        agent = AutomationRequestAgent()
        
        requester = Stakeholder(
            name="Project Manager",
            role="PM",
            email="pm@example.com"
        )
        
        request = agent.create_request(
            title="Multi-System Integration",
            description="Integrate multiple systems",
            business_purpose="Streamline operations",
            requested_by=requester,
            priority=PriorityLevel.HIGH
        )
        
        # Add multiple systems
        for i in range(3):
            agent.add_system(
                request,
                name=f"System {i+1}",
                system_type="source" if i == 0 else "target",
                description=f"Description for system {i+1}"
            )
        
        self.assertEqual(len(request.systems_involved), 3)
        
        # Add notifications
        agent.add_notification(
            request,
            notification_type=NotificationType.EMAIL,
            recipients=["team@example.com"],
            trigger="on_success"
        )
        
        agent.add_notification(
            request,
            notification_type=NotificationType.SLACK,
            recipients=["#alerts"],
            trigger="on_failure"
        )
        
        self.assertEqual(len(request.notifications), 2)
        
        # Set schedule
        agent.set_schedule(request, frequency="hourly", cron_expression="0 * * * *")
        
        # Validate
        is_valid, errors = agent.validate_request(request)
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()
