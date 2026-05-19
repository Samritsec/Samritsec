from datetime import datetime
import uuid

class TaskRegistry:
    """
    Tracks active and pending background tasks orchestrated by the AI.
    """
    def __init__(self):
        self.tasks = {}

    def register_task(self, name: str, description: str, category: str = "general") -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "name": name,
            "description": description,
            "category": category,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "result": None
        }
        return task_id

    def update_task_status(self, task_id: str, status: str, result: str = None):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            if result:
                self.tasks[task_id]["result"] = result
            if status in ["completed", "failed", "cancelled"]:
                self.tasks[task_id]["completed_at"] = datetime.now().isoformat()

    def get_active_tasks(self):
        return {tid: t for tid, t in self.tasks.items() if t["status"] in ["pending", "running"]}

    def get_all_tasks(self):
        return self.tasks

# Global instance
task_registry = TaskRegistry()
