import json 

class Task(object):
	"""Class for storing information about assigned Tasks"""

	def __init__(self, taskName, taskType, category, taskStatus, assignedTo = "unassigned"):
		self.Name = taskName;
		self.Type = taskType;
		self.Category = category;
		self.Assigned = assignedTo;
		self.Status = taskStatus;

	def DisplayTask(self):
		displayText = "Task: " + self.Name + "\n" + "Category: " + self.Category + "\n" + "Type: " + self.Type + "\n" + "Assigned: " + self.Assigned + "\n" + "Status: " + self.Status + "\n";
		return displayText;

	def _assignTask(self, assignedTo):

		if self.Assigned == assignedTo:
			print("This task is already assigned to " + self.Assigned.title());

		else:
			self.Assigned = assignedTo;
			print("This task is now assigned to " + self.Assigned.title());

	def _toText(self):
		taskText = self.Name + "," + self.Assigned + "," + self.Type + "," + self.Category + "," + self.Status + "\n";
		return taskText;

	@staticmethod
	def _toTask(newModelDict):

		returnTask = Task(newModelDict["Name"], newModelDict["Type"], newModelDict["Category"], newModelDict["Status"], newModelDict["Assigned"]);
		return returnTask;

	def ChangeStatus(self, status):
		self.Status = status;

	def ChangeName(self, newName):
		self.Name = newName;