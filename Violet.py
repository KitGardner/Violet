from discord.ext.commands import Bot
from taskManager import TaskManager
from discord import Game


BOT_PREFIX = ("?", "!", "Violet ", "violet ")
TOKEN = self.GetToken();  #Will validate another time.
TASK_KEYS = ["Name", "Type", "Category", "Assigned", "Status"];

client = Bot(command_prefix=BOT_PREFIX)
Manager = TaskManager();

def GetToken()
	with open("environment.json") as readObj:
		for line in readObj:
			TokenLine = json.loads(line);
			return TokenLine["TOKEN"];

@client.command(name='Hi',
	aliases=['hello', 'Hello', 'Yo', 'Good Evening', 'Konichiwa', 'hi'],
	pass_context=True)
async def Hi(context):
	response = "Hi there, " + context.message.author.mention;
	await client.say(response)

@client.command(pass_context=True)
async def CreateTask(context):
	await client.say("Certainly, what is the name of the task you would like to make?");
	taskName = await client.wait_for_message(author=context.message.author);
	await client.say("and who is this task assigned to?");
	assignedTo = await client.wait_for_message(author=context.message.author);
	await client.say("Category?");
	category = await client.wait_for_message(author=context.message.author);
	await client.say("Asset type?");
	assetType = await client.wait_for_message(author=context.message.author);
	response ="You are creating a task with a name of " + str(taskName.content) + " and is assigned to " + str(assignedTo.content) + ". Is this correct?"
	await client.say(response);
	answer = await client.wait_for_message(author=context.message.author);
	if(answer.content.lower() == 'yes'):
		createdTask = Manager.CreateTask(taskName.content, assetType.content, category.content, assignedTo.content);
		if(createdTask):
			response = createdTask.DisplayTask();
			await client.say(response);
		else:
			await client.say("This task has already been created.");
	elif(answer.content.lower() == 'no'):
		await client.say("Changed your mind huh? Ok deleting Task.");

@client.command(pass_context=True)
async def QuickCreateTask(context, Name, Assigned, Category, Type):
	createdTask = Manager.CreateTask(Name, Type, Category, Assigned);
	if(createdTask):
		response = createdTask.DisplayTask();
		await client.say(response);
	else:
		await client.say("This task has already been created.");

@client.command(pass_context=True)
async def DisplayTasks(context):
	response = "";
	for task in Manager.taskList:
		response += task.Name + " of type " + task.Type + " is assigned to " + task.Assigned + "\n";

	await client.say(response);


@client.command(pass_context=True)
async def UpdateTask(context, taskName=None, key=None, value=None):
	if(key and value and taskName):
		if(value.title() == 'Completed'):
			await client.say("I have recieved a value of Completed, are you meaning to complete a task?");
			response = await client.wait_for_message(author=context.message.author);
			if(response.content.lower() == 'yes'):
				result = Manager.CompleteTask(taskName);
				await client.say(result);
				return;
			else:
				client.say("No problem, please provide another value then.")
				return;
		await client.say("I have received the following info: Name: " + taskName + ", key: " + key + ", value: " + value);
		if(key.title() not in TASK_KEYS):
			await client.say("Invalid Property. Please provide one of the following properties");
			response = "";
			for key in TASK_KEYS:
				response += key + "\n";
			await client.say(response);
		else:
			updateResult = Manager.UpdateTask(taskName, key, value);
			if(updateResult):
				await client.say("Updated task successfully\n" + updateResult.DisplayTask());
			else:
				await client.say("There was an error updating the task.");
	else:
		await client.say("I am missing some information. I need to know the task name, what to update, and what to update it to.")

@client.command(pass_context=True)
async def GoodNight(context):
	response = "Goodnight everyone! See you next week!";
	await client.say(response);
	await client.logout();

@client.command(pass_context=True)
async def TaskDetails(context, taskName):
	foundTask = Manager.FindTask(taskName);
	if(foundTask):
		await client.say(foundTask.DisplayTask());
	else:
		await client.say("Can't find the chosen task to display");

@client.command(name="SearchTasksByUserName", pass_context=True, aliases=["What_are_they_working_on?"])
async def SearchTasksByUserName(context, name):
	result = Manager.FindTasksByAssigned(name);
	if(result):
		response = "";
		for task in result:
			response += task.DisplayTask() + "\n";
		await client.say(response);
	else:
		await client.say("I could not find any tasks assigned to " + name);

@client.command(pass_context=True)
async def DeleteTask(context, taskName):
	result = Manager.DeleteTask(taskName);
	await client.say(result);

@client.command(pass_context=True)
async def CompleteTask(context):
	await client.say("What task is ready for completion?");
	taskName = await client.wait_for_message(author=context.message.author);
	print("The bot has recieved " + taskName.content + " for the task name");
	result = Manager.CompleteTask(taskName.content);
	await client.say(result);

@client.command(pass_context=True)
async def AreYouSingle(ctx):
	await client.say("Hmm, I've never been with a human before; are you offering? " + ctx.message.author.mention);

@client.command(pass_context=True)
async def NewTaskManager(context, activeTaskFileName, completedTaskFileName):
	self.Manager = TaskManager(activeTaskFileName, completedTaskFileName);
	await client.say("I have created a new manager");

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)

client.run(TOKEN)
