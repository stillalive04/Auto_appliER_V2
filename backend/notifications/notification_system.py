import asyncio
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum

class NotificationType(Enum):
    JOB_FOUND = "job_found"
    APPLICATION_SENT = "application_sent"
    APPLICATION_SUCCESS = "application_success"
    APPLICATION_FAILED = "application_failed"
    CAPTCHA_SOLVED = "captcha_solved"
    COUNTY_SCRAPE_COMPLETE = "county_scrape_complete"
    SYSTEM_UPDATE = "system_update"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class NotificationPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Notification:
    id: str
    user_id: str
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    data: Optional[Dict] = None
    timestamp: Optional[float] = None
    read: bool = False
    expires_at: Optional[float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.expires_at is None:
            # Default expiration: 24 hours for most notifications
            if self.type in [NotificationType.JOB_FOUND, NotificationType.APPLICATION_SUCCESS]:
                self.expires_at = self.timestamp + (24 * 60 * 60)  # 24 hours
            elif self.type in [NotificationType.ERROR, NotificationType.WARNING]:
                self.expires_at = self.timestamp + (7 * 24 * 60 * 60)  # 7 days
            else:
                self.expires_at = self.timestamp + (60 * 60)  # 1 hour
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['type'] = self.type.value
        data['priority'] = self.priority.value
        return data
    
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

class NotificationSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notifications: Dict[str, List[Notification]] = {}  # user_id -> notifications
        self.subscribers: Dict[str, Set] = {}  # user_id -> websocket connections
        self.notification_counter = 0
        self.cleanup_running = False
        
    async def start_cleanup_task(self):
        """Start the cleanup task when event loop is available"""
        if not self.cleanup_running:
            self.cleanup_running = True
            asyncio.create_task(self.cleanup_expired_notifications())
    
    def generate_notification_id(self) -> str:
        """Generate unique notification ID"""
        self.notification_counter += 1
        return f"notif_{int(time.time())}_{self.notification_counter}"
    
    async def add_notification(self, user_id: str, notification_type: NotificationType, 
                             title: str, message: str, priority: NotificationPriority = NotificationPriority.MEDIUM,
                             data: Optional[Dict] = None) -> str:
        """Add a new notification for a user"""
        try:
            notification = Notification(
                id=self.generate_notification_id(),
                user_id=user_id,
                type=notification_type,
                priority=priority,
                title=title,
                message=message,
                data=data or {}
            )
            
            # Initialize user notifications if not exists
            if user_id not in self.notifications:
                self.notifications[user_id] = []
            
            # Add notification
            self.notifications[user_id].append(notification)
            
            # Keep only last 100 notifications per user
            if len(self.notifications[user_id]) > 100:
                self.notifications[user_id] = self.notifications[user_id][-100:]
            
            # Broadcast to subscribers
            await self.broadcast_notification(user_id, notification)
            
            self.logger.info(f"Added notification for user {user_id}: {title}")
            return notification.id
            
        except Exception as e:
            self.logger.error(f"Error adding notification: {e}")
            return ""
    
    async def broadcast_notification(self, user_id: str, notification: Notification):
        """Broadcast notification to all connected clients for a user"""
        try:
            if user_id in self.subscribers:
                message = {
                    "type": "notification",
                    "data": notification.to_dict()
                }
                
                # Send to all connected websockets for this user
                disconnected = set()
                for websocket in self.subscribers[user_id]:
                    try:
                        await websocket.send(json.dumps(message))
                    except Exception as e:
                        self.logger.warning(f"Failed to send notification to websocket: {e}")
                        disconnected.add(websocket)
                
                # Remove disconnected websockets
                for ws in disconnected:
                    self.subscribers[user_id].discard(ws)
                    
        except Exception as e:
            self.logger.error(f"Error broadcasting notification: {e}")
    
    def get_notifications(self, user_id: str, limit: int = 50, unread_only: bool = False) -> List[Dict]:
        """Get notifications for a user"""
        try:
            if user_id not in self.notifications:
                return []
            
            notifications = self.notifications[user_id]
            
            # Filter unread if requested
            if unread_only:
                notifications = [n for n in notifications if not n.read]
            
            # Sort by timestamp (newest first)
            notifications.sort(key=lambda x: x.timestamp or 0, reverse=True)
            
            # Apply limit
            notifications = notifications[:limit]
            
            return [n.to_dict() for n in notifications]
            
        except Exception as e:
            self.logger.error(f"Error getting notifications: {e}")
            return []
    
    def mark_as_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read"""
        try:
            if user_id not in self.notifications:
                return False
            
            for notification in self.notifications[user_id]:
                if notification.id == notification_id:
                    notification.read = True
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error marking notification as read: {e}")
            return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user"""
        try:
            if user_id not in self.notifications:
                return 0
            
            count = 0
            for notification in self.notifications[user_id]:
                if not notification.read:
                    notification.read = True
                    count += 1
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error marking all notifications as read: {e}")
            return 0
    
    def delete_notification(self, user_id: str, notification_id: str) -> bool:
        """Delete a specific notification"""
        try:
            if user_id not in self.notifications:
                return False
            
            self.notifications[user_id] = [
                n for n in self.notifications[user_id] 
                if n.id != notification_id
            ]
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting notification: {e}")
            return False
    
    def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications for a user"""
        try:
            if user_id not in self.notifications:
                return 0
            
            return sum(1 for n in self.notifications[user_id] if not n.read and not n.is_expired())
            
        except Exception as e:
            self.logger.error(f"Error getting unread count: {e}")
            return 0
    
    async def subscribe_user(self, user_id: str, websocket):
        """Subscribe a user's websocket for real-time notifications"""
        try:
            if user_id not in self.subscribers:
                self.subscribers[user_id] = set()
            
            self.subscribers[user_id].add(websocket)
            self.logger.info(f"User {user_id} subscribed for notifications")
            
        except Exception as e:
            self.logger.error(f"Error subscribing user: {e}")
    
    async def unsubscribe_user(self, user_id: str, websocket):
        """Unsubscribe a user's websocket"""
        try:
            if user_id in self.subscribers:
                self.subscribers[user_id].discard(websocket)
                
                # Clean up empty sets
                if not self.subscribers[user_id]:
                    del self.subscribers[user_id]
                    
            self.logger.info(f"User {user_id} unsubscribed from notifications")
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing user: {e}")
    
    async def cleanup_expired_notifications(self):
        """Periodically clean up expired notifications"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                for user_id in list(self.notifications.keys()):
                    original_count = len(self.notifications[user_id])
                    self.notifications[user_id] = [
                        n for n in self.notifications[user_id] 
                        if not n.is_expired()
                    ]
                    
                    cleaned_count = original_count - len(self.notifications[user_id])
                    if cleaned_count > 0:
                        self.logger.info(f"Cleaned up {cleaned_count} expired notifications for user {user_id}")
                
            except Exception as e:
                self.logger.error(f"Error in notification cleanup: {e}")
    
    # Convenience methods for common notification types
    
    async def notify_job_found(self, user_id: str, job_title: str, company: str, 
                             location: str, job_data: Dict) -> str:
        """Notify about a new job found"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.JOB_FOUND,
            title="New Job Found!",
            message=f"Found {job_title} at {company} in {location}",
            priority=NotificationPriority.HIGH,
            data={
                "job_title": job_title,
                "company": company,
                "location": location,
                "job_data": job_data
            }
        )
    
    async def notify_application_sent(self, user_id: str, job_title: str, company: str) -> str:
        """Notify about application sent"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.APPLICATION_SENT,
            title="Application Sent",
            message=f"Applied to {job_title} at {company}",
            priority=NotificationPriority.MEDIUM,
            data={
                "job_title": job_title,
                "company": company
            }
        )
    
    async def notify_application_success(self, user_id: str, job_title: str, company: str) -> str:
        """Notify about successful application"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.APPLICATION_SUCCESS,
            title="Application Successful!",
            message=f"Successfully applied to {job_title} at {company}",
            priority=NotificationPriority.HIGH,
            data={
                "job_title": job_title,
                "company": company
            }
        )
    
    async def notify_application_failed(self, user_id: str, job_title: str, company: str, error: str) -> str:
        """Notify about failed application"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.APPLICATION_FAILED,
            title="Application Failed",
            message=f"Failed to apply to {job_title} at {company}: {error}",
            priority=NotificationPriority.MEDIUM,
            data={
                "job_title": job_title,
                "company": company,
                "error": error
            }
        )
    
    async def notify_captcha_solved(self, user_id: str, site: str) -> str:
        """Notify about CAPTCHA solved"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.CAPTCHA_SOLVED,
            title="CAPTCHA Solved",
            message=f"Successfully solved CAPTCHA on {site}",
            priority=NotificationPriority.LOW,
            data={
                "site": site
            }
        )
    
    async def notify_county_scrape_complete(self, user_id: str, counties_count: int, jobs_found: int) -> str:
        """Notify about county scraping completion"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.COUNTY_SCRAPE_COMPLETE,
            title="County Scraping Complete",
            message=f"Scanned {counties_count} counties and found {jobs_found} new jobs",
            priority=NotificationPriority.MEDIUM,
            data={
                "counties_count": counties_count,
                "jobs_found": jobs_found
            }
        )
    
    async def notify_system_update(self, user_id: str, message: str) -> str:
        """Notify about system updates"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.SYSTEM_UPDATE,
            title="System Update",
            message=message,
            priority=NotificationPriority.LOW
        )
    
    async def notify_error(self, user_id: str, error_message: str, details: Optional[Dict] = None) -> str:
        """Notify about errors"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.ERROR,
            title="Error Occurred",
            message=error_message,
            priority=NotificationPriority.HIGH,
            data=details or {}
        )
    
    async def notify_warning(self, user_id: str, warning_message: str, details: Optional[Dict] = None) -> str:
        """Notify about warnings"""
        return await self.add_notification(
            user_id=user_id,
            notification_type=NotificationType.WARNING,
            title="Warning",
            message=warning_message,
            priority=NotificationPriority.MEDIUM,
            data=details or {}
        )
    
    def get_notification_stats(self, user_id: str) -> Dict:
        """Get notification statistics for a user"""
        try:
            if user_id not in self.notifications:
                return {
                    "total": 0,
                    "unread": 0,
                    "by_type": {},
                    "by_priority": {}
                }
            
            notifications = self.notifications[user_id]
            non_expired = [n for n in notifications if not n.is_expired()]
            
            stats = {
                "total": len(non_expired),
                "unread": sum(1 for n in non_expired if not n.read),
                "by_type": {},
                "by_priority": {}
            }
            
            # Count by type
            for notification in non_expired:
                type_name = notification.type.value
                priority_name = notification.priority.value
                
                stats["by_type"][type_name] = stats["by_type"].get(type_name, 0) + 1
                stats["by_priority"][priority_name] = stats["by_priority"].get(priority_name, 0) + 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting notification stats: {e}")
            return {}

# Global notification system instance
notification_system = NotificationSystem()

# Convenience functions
async def notify_job_found(user_id: str, job_title: str, company: str, location: str, job_data: Dict) -> str:
    return await notification_system.notify_job_found(user_id, job_title, company, location, job_data)

async def notify_application_sent(user_id: str, job_title: str, company: str) -> str:
    return await notification_system.notify_application_sent(user_id, job_title, company)

async def notify_application_success(user_id: str, job_title: str, company: str) -> str:
    return await notification_system.notify_application_success(user_id, job_title, company)

async def notify_application_failed(user_id: str, job_title: str, company: str, error: str) -> str:
    return await notification_system.notify_application_failed(user_id, job_title, company, error)

async def notify_captcha_solved(user_id: str, site: str) -> str:
    return await notification_system.notify_captcha_solved(user_id, site)

async def notify_county_scrape_complete(user_id: str, counties_count: int, jobs_found: int) -> str:
    return await notification_system.notify_county_scrape_complete(user_id, counties_count, jobs_found)

async def notify_error(user_id: str, error_message: str, details: Optional[Dict] = None) -> str:
    return await notification_system.notify_error(user_id, error_message, details)

async def notify_warning(user_id: str, warning_message: str, details: Optional[Dict] = None) -> str:
    return await notification_system.notify_warning(user_id, warning_message, details) 