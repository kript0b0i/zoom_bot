from discord_webhooks import DiscordWebhooks

URL= 'https://discord.com/api/webhooks/806264854133342238/iS2kNDCwCko32tivh4bYpsKlwqdWkLwBNbCo6HZ3kWSZoz_0lbWEQvpIKfXL_0_9a3QL'

def class_status(Class_name,status, start_time, end_time):
    WEBHOOK_URL = URL
    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_footer(text='zoom bot')
    if(status):
        webhook.set_content(title='Class Joined Succesfully')
        webhook.add_field(name='Class', value=Class_name)
        webhook.add_field(name='Status', value=status)
        webhook.add_field(name='Joined at', value=start_time)
        webhook.add_field(name='Leaving at', value=end_time)
    elif(not status):
        webhook.set_content(title='Class Left Succesfully')
        webhook.add_field(name='Class', value=Class_name)
        webhook.add_field(name='Status', value=status)
        webhook.add_field(name='Joined at', value=start_time)
        webhook.add_field(name='Leaving at', value=end_time)

    webhook.send()
