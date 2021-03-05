from discord_webhook import DiscordWebhook, DiscordEmbed

URL= 'https://discord.com/api/webhooks/806264854133342238/iS2kNDCwCko32tivh4bYpsKlwqdWkLwBNbCo6HZ3kWSZoz_0lbWEQvpIKfXL_0_9a3QL'

def class_status(class_name, classStatus, start_time, end_time):
    webhook = DiscordWebhook(URL, content ='class info')

    embed = DiscordEmbed(title="Class Joined Succesfully")
    embed.set_timestamp()
    embed.add_embed_field(name='Class', value= class_name, inline=False)
    embed.add_embed_field(name='Status', value= classStatus,inline=False)
    embed.add_embed_field(name='start time', value=start_time, inline=False)
    embed.add_embed_field(name='end time', value= end_time, inline=False)
    with open("zoom.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='zoom.png')
    webhook.add_embed(embed)
    response = webhook.execute()

def Attendance(name):
    webhook = DiscordWebhook(URL)
    embed = DiscordEmbed(title="KeyWordDetection")
    embed.set_timestamp()
    embed.add_embed_field(name='Some call your name', value= name, inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()

