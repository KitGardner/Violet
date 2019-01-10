from datetime import datetime
from datetime import date
class Entry(object):
	"""Individual entries meant to be stored in an agenda. Contains entry information such as entry date, points of discussion, and notes"""

	def GenerateFileName(self):
		return str(self.Date) + "_" + self.Title.strip() + "_" + self.Author.strip() + ".json";
		

	def __init__(self, entryDate, author, title, goals=[], notes=[]):
		self.Date = entryDate;
		self.Author = author.title();
		self.Title = title;
		self.Notes = notes;
		self.Goals = goals;
		self.CreatedUtc = datetime.utcnow();
		self.FileName = self.GenerateFileName();

	def GetFileName(self):
		self.FileName = self.GenerateFileName();
		return self.FileName;

	def AddEntryGoal(self, goal):
		self.Goals.append(goal);

	def AddEntryNote(self, note):
		self.Notes.append(note);

	def ReadGoals(self):
		return self.Goals;

	def ReadNotes(self):
		return self.Notes;

	def DisplayEntry(self):
		goalStr = "";
		NoteStr = "";
		for goal in self.Goals:
			goalStr += goal + "\n";

		for note in self.Notes:
			NoteStr += note + "\n";

		return str(self.Date) + ": " + self.Title + ", " + self.Author + "\n" + "Goals\n" + goalStr + "\n" + "Notes\n" + NoteStr;
