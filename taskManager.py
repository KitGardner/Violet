from task import Task
import json

class TaskManager(object):
	"""Class for managing tasks"""

	def GetTasks(self):
		return self.taskList;

	def SaveTask(self, fileName, task):
		with open(fileName, 'a') as writeObj:
			taskStr = json.dumps(task.__dict__)
			writeObj.write(taskStr + "\n");

	def LoadTasks(self, fileName):
		self.taskList = [];
		try:
			with open(fileName) as readObj:
				for line in readObj:
					taskLine = json.loads(line);
					self.taskList.append(Task._toTask(taskLine));
				return self.taskList;
		except IOError:
			print("The file does not exist. Creating a new file");
			with open(fileName, 'w') as writeObj:
				writeObj.write("");
				return [];

	def FindTask(self, taskName):
		if(self.taskList):
			result = None;
			for task in self.taskList:
				if(task.Name == taskName):
					result = task;
		else:
			result = None;
		return result;

	def FindTasksByAssigned(self, userName):
		if(self.taskList):
			result = [];
			for task in self.taskList:
				if(task.Assigned == userName):
					result.append(task);
		else:
			result = None;
		return result;

	def CreateTask(self, taskName, taskType, taskCat, assignedTo = "unassigned"):
		searchResult = self.FindTask(taskName);
		if(searchResult):
			print("Task with task name of " + taskName + " has already been created");
			return None;
		else:
			newTask = Task(taskName, taskType, taskCat, "Created", assignedTo);
			self.taskList.append(newTask);
			self.SaveTask("saved_tasks.json", newTask);
			return newTask;	

	def SaveTasks(self, fileName):
		if(self.taskList):
			with open(fileName, 'w') as updateObj:
				for task in self.taskList:
					taskStr = json.dumps(task.__dict__)
					updateObj.write(taskStr + "\n");
		else:
			print("There are no created tasks to update");

	def DeleteTask(self, taskName):
		chosenTask = self.FindTask(taskName);
		if(chosenTask):
			self.taskList.remove(chosenTask);
			self.SaveTasks(self.fileName);
			return "Task was deleted successfully";
		else:
			return "This task cannot be deleted because it does not exist.";

	def ChangeTaskStatus(self, taskName, status):
		chosenTask = self.FindTask(taskName);
		if(chosenTask):
			chosenTask.ChangeStatus(status);
			self.SaveTasks(self.fileName);

	def AssignTask(self, taskName, assignTo):
		chosenTask = self.FindTask(taskName);
		if(chosenTask):
			chosenTask._assignTask(assignTo);
			chosenTask.ChangeStatus("Assigned");

	def ChangeTaskName(self, taskName, newName):
		chosenTask = self.FindTask(taskName);
		if(chosenTask):
			chosenTask.ChangeName(newName);
			self.SaveTasks(self.fileName);

	def UpdateTask(self, taskName, updateKey, updateValue):
		searchResult = self.FindTask(taskName);
		if(searchResult):
			self.taskList.remove(searchResult);
			searchResultDict = searchResult.__dict__;
			searchResultDict[updateKey.title()] = updateValue;
			self.taskList.append(Task._toTask(searchResultDict));
			self.SaveTasks(self.fileName);
			return searchResult;
		else:
			return None;

	def CompleteTask(self, taskName):
		completedTask = self.FindTask(taskName);
		print(str(completedTask));
		if(completedTask):
			completedTask.ChangeStatus("Completed");
			exists = False;
			try:
				with open(self.completedFileName) as readObj:
					for line in readObj:
						if taskName in line:
							exists = True;
			except IOError:
				print("The file does not exist. Creating a new file");
				with open(self.completedFileName, 'w') as writeObj:
					writeObj.write("");

			if(exists):
				return "This task has already been completed.";
			else:
				with open(self.completedFileName, 'a') as writeObj:
					completedTaskStr = json.dumps(completedTask.__dict__);
					writeObj.write(completedTaskStr + "\n");
				self.DeleteTask(taskName);
				return "Task successfully completed and saved!"
		else:
			return "I cannot complete this task as it does not exist.";

	def __init__(self, fileName="saved_tasks.json", completedFileName="CompletedTasks.json"):
		self.taskList = [];
		self.fileName = fileName;
		self.completedFileName = completedFileName;
		self.completedList = [];
		self.LoadTasks(self.fileName);