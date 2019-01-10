from discord.ext.commands import Bot
from taskManager import TaskManager


BOT_PREFIX = ("?", "!")
TOKEN = "NDgxMzIzNjYzNTMxMTgwMDMy.DmeOxg.fHCqzvlcIbXHg-5v58vAyys7t_E"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)
Manager = TaskManager();

@client.command(name='Hi', 
	aliases=['hello', 'Hello', 'Yo', 'Good Evening', 'Konichiwa'],
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
async def DisplayTasks(context):
	response = "";
	for task in Manager.taskList:
		response += task.Name + " of type " + task.Type + " is assigned to " + task.Assigned + "\n";

	await client.say(response);

@client.command(pass_context=True)
async def GoodNight(context):
	response = "Goodnight everyone! See you next week!";
	await client.say(response);
	await client.logout();

client.run(TOKEN)