from entries import Entry
from datetime import date
from datetime import datetime
from datetime import timedelta
import json
import os

class Agenda(object):
	"""This object is meant to maintain the weekly meeting Agenda including meeting topics, notes, and schedules"""

	def __init__(self):
		#self.Entries = [];
		self.EntryHeaderFile = "AgendaEntries.json";
		self.EntryFileNames = self.LoadEntryFileNames();

	def FindEntryByDate(self, entryDate):
		#chosenEntry = self.SearchLoadedEntries(entryDate);
		#if chosenEntry:
			#print("The entry is in memory.")
			#return chosenEntry;
		#else:
		if not entryDate:
			return "Please provide an entry Date";

		foundEntries = [];
		for entryName in self.EntryFileNames:
			if str(entryDate) in entryName:
				foundEntry = self.LoadEntry(entryName);
				foundEntries.append(foundEntry);

		if foundEntries:
			return foundEntries;
		else:
			return "No entries have been created for this date.";

	def FindEntriesWithinDates(self, dateFrom=None, dateTo=None):
		if not dateFrom and not dateTo:
			return "I don't know which dates to search for. Please provide at least one of them.";

		foundEntries = [];
		for entryName in self.EntryFileNames:
			dateExtracted = datetime.strptime(entryName[:10], "%Y-%m-%d").date();
			if dateFrom and dateTo:
				if dateFrom <= dateExtracted and dateExtracted <= dateTo:
					foundEntries.append(entryName);
			elif dateFrom:
				if dateFrom <= dateExtracted:
					foundEntries.append(entryName);
			else:
				if dateExtracted <= dateTo:
					foundEntries.append(entryName);

		if foundEntries:
			return foundEntries;

		else:
			return "I did not find any entries within those dates."  

	def FindEntriesByAuthor(self, author):
		chosenEntries = [];

		if not author:
			return "Please provide an author for me to search for."

		for entryName in self.EntryFileNames:
			if author in entryName:
				foundEntry = self.LoadEntry(entryName);
				chosenEntries.append(foundEntry);
		return chosenEntries;

	def ListEntries(self):
		self.EntryFileNames = self.LoadEntryFileNames();
		formattedEntries = [];
		for entry in self.EntryFileNames:
			formattedEntries.append(entry[:-5]);
		return formattedEntries;

	def FindNextMeetingDate(self, dayOfWeek=2, currentDate=date.today()):
		startDate = currentDate;
		timeGap = 7;
		if(dayOfWeek != startDate.weekday()):
			timeGap = (dayOfWeek - startDate.weekday()) % 7;
		nextMeetingDate = startDate + timedelta(days=timeGap);
		return nextMeetingDate;

	def CreateEntry(self, author, title, entryDate=None, goals=[], notes=[]):
		if not entryDate:
			entryDate = self.FindNextMeetingDate();

		searchResult = self.EntryExists(entryDate, title, author);
		if searchResult:
			return "An entry for this entry date has already been created.";
		else:
			newEntry = 	Entry(entryDate, author, title, goals, notes);
			#self.Entries.append(newEntry);
			#self.EntryFileNames.append(newEntry.GetFileName());
			self.WriteEntry(newEntry);
			self.WriteEntryHeader(newEntry); #I should add some exception handling
			return newEntry;

	def EntryExists(self, entryDate, title, author):
		foundEntryName = None;
		fileToCheck = str(entryDate) + "_" + title.strip() + "_" + author.strip() + ".json";
		print(fileToCheck);
		for entryName in self.EntryFileNames:
			if fileToCheck in entryName:
				foundEntryName = entryName;
				print("I found the entry");
		return foundEntryName;

	def WriteEntryHeader(self, newEntry):
		entryFullName = newEntry.GetFileName();
		if "AgendaEntries/" not in entryFullName:
			entryFullName = "AgendaEntries/" + entryFullName;
		try:
			with open(self.EntryHeaderFile, 'a') as WriteObject:
				WriteObject.write(entryFullName + "\n");
				self.EntryFileNames.append(newEntry.GetFileName());
			return "Entry Header updated";
		except Exception:
			return "Something unexpected occured while writing to the Entry Header File."

	def WriteEntry(self, newEntry):
		writeFileName = "AgendaEntries/" + newEntry.GetFileName();
		try:
			with open(writeFileName, 'w') as entryWriteObj:
				json.dump(newEntry.__dict__, entryWriteObj, sort_keys=True, default=str, indent=4);
			return "Entry successfully written";
		except IOError:
			print("Folder path may not be setup.");
			os.makedirs("AgendaEntries");
			with open(writeFileName, 'w') as entryWriteObj:
				json.dump(newEntry.__dict__, entryWriteObj, sort_keys=True, default=str, indent=4);

	def LoadEntry(self, entryName):
		filePath = "AgendaEntries/" + entryName;
		with open(filePath) as LoadObj:
			entry = json.load(LoadObj);
			loadedEntry = Entry(entry['Date'], entry['Author'], entry['Title'], entry['Goals'], entry['Notes']);
			#self.Entries.append(loadedEntry);
		return loadedEntry;
			

	def LoadEntryFileNames(self):
		fileNames = [];
		try:
			with open(self.EntryHeaderFile) as loadObj:
				for line in loadObj:
					fileNames.append(line[14:-1]);
			return fileNames;
		except IOError:
			return [];

	def ListEntryGoals(self, entry): #Possibly obsolete since entries has it's own display function for this
		if entry:
			goals = entry.ReadGoals();
			goalStr = "";
			for goal in goals:
				goalStr += goal + "\n";
			return goalStr;
		else:
			return "Please provide an entry.";

	def ListEntryNotes(self, entry): #Possibly obsolete since entries has it's own display function for this
		if entry:
			notes = entry.ReadNotes();
			noteStr = "";
			for note in notes:
				noteStr += note + "\n";
			return noteStr;
		else:
			return "Please provide an entry.";


	def AddEntryGoal(self, entry, goal):
		entry.AddEntryGoal(goal);
		return entry;

	def AddEntryNote(self, entry, note):
		entry.AddEntryNote(note);
		return entry;

	def ChangeEntryDate(self, entry, newDate):
		if entry.Date == newDate:
			return "The change date is the same as the entries current date. Please provide a different date";

		entry.Date = newDate;
		return entry;

	def ChangeEntryTitle(self, entry, newTitle):
		entry.Title = newTitle;
		return entry;

	def ChangeEntryAuthor(self, entry, newAuthor):
		if entry.Author == newAuthor:
			return "This entry is already authored by " + newAuthor;

		entry.Author = newAuthor;
		return entry;

	def UpdateEntry(self, entry, oldEntryName):
		print(entry.GenerateFileName());

		if oldEntryName in entry.GenerateFileName(): #If it is still the same file
			print("No changes were made to the file name")
			self.WriteEntry(entry);

		else:
			print("The file name is now different")	#Date, Title, Or Author was changed, which changes the file name
			deletedResult = self.DeleteEntry(oldEntryName);
			if deletedResult not in "File deleted Successfully":
				return "There was an issue with deleting " + oldEntryName;

			headerWriteResult = self.WriteEntryHeader(entry);
			if headerWriteResult not in "Entry Header updated":
				return "There was an issue writing the file to the header."
			writeEntryResult = self.WriteEntry(entry);
			if writeEntryResult not in "Entry successfully written":
				return "There was an error when writing the entry."
			return "Entry was updated Successfully";
		

	def SearchForEntriesWith(self, key, value):
		result = [];
		if key:
			key = key.title();
		else:
			return "Key is required for searching";

		if not value:
			return "I have no idea what I am looking for. Please provide a value";

		if key == "Date":
			return FindEntryByDate(key);

		if key == "Author":
			return FindEntriesByAuthor(key);

		for entryName in self.EntryFileNames:
			filePath = "AgendaEntries/" + entryName;
			with open(filePath) as readObj:
				entryTxt = json.load(readObj);

				if entryTxt[key]:
					for text in entryTxt[key]:
						if value in text:
							print("I found the value in this entry.")
							loadedEntry = Entry(entryTxt['Date'], entryTxt['Author'], entryTxt['Title'], entryTxt['Goals'], entryTxt['Notes']);
							result.append(loadedEntry);
							break;
				else:
					continue;

		return result;

	def DeleteEntry(self, fileName):

		if "\n" in fileName:
			fileName = fileName[:-1];

		if ".json" not in fileName:
			fileName = fileName + ".json";
		try:
			self.EntryFileNames.remove(fileName);
			fileNamesString = "";

			if "AgendaEntries/" not in fileName:
				fileName = "AgendaEntries/" + fileName;
			print("I am about to remove " + fileName);
			os.remove(fileName);
			exists = os.path.isfile(fileName);
			print("The file still exists? " + str(exists));
			if self.EntryFileNames:
				for entryName in self.EntryFileNames:
					fileNamesString += "AgendaEntries/" + entryName + "\n";
				try:
					with open(self.EntryHeaderFile, 'w') as WriteObject:
						WriteObject.write(fileNamesString);
				except Exception:
					print("Something happened when writing to the file");
					return "Something unexpected occured while writing to the Entry Header File."
			else:
				os.remove(self.EntryHeaderFile);
				os.rmdir("AgendaEntries")

			return "File deleted Successfully";
		except ValueError:
			print(fileName + " was not found in the stored fileNames.")
			return "There is no file with that file name.";
		
		





#What I need this agenda to do with times
#Allow user to enter a datetime for an entry that is converted into UTC
#User should be able to search by datetime relative to their timezone and return matching entries
#Agenda should be able to display entries with entry datetimes in correct timezone
#Agenda should be able to find the next date based on the day provided
#The Agenda should be able to parse human readable date times
#Agenda should be able to write human readable Datetimes.		
#((dayOfWeek - startDate.weekday()) % 7)


#Things I want Violet to be able to do with the Agenda
#Create Entries for any date -- Check
#Add entry goals - should only be able to affect current and next entry -- removing constraint since the entry to modify is passed in -- Check
#Add entry notes - should only be able to affect current entry -- removing constraint since the entry to modify is passed in -- Check
#LoadEntries - it loads the entry file names, will work on the entries themselves. Load Entries completed -- Check
#Determine when the next weekly meeting is - I would like if it could give the user the time in their timezone
#Search entries by date, author, goals, and notes -- for the goals and notes it should return the entry dates as well.
#Save entries to a file -- not sure if it should be one large file with all entries or each entry is their own file. - I am going to try the header and individual files approach. --Check
#Update entries - this will be determined by the solution to saving files --Check
#List Entry Notes -- Check
#List Entry Goals -- Check
#List existing entries -- Check
#Possbily be able to delete Entries.