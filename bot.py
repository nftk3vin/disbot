import discum
from discum.utils.embed import Embedder
import config

bot = discum.Client(token=config.token, log=False)


@bot.gateway.command
def helloworld(resp):
    if resp.event.message:
        message = resp.parsed.auto()
    else:
        return
    try:
        if message['author']['id'] != config.poster_user_id:
            return

        dm = bot.createDM([config.target_user_id]).json()["id"]

        if message['content'] and message['content'] != "":
            try:
                bot.sendMessage(dm, message['content'])
            except Exception as e:
                pass
        if len(message['embeds']) > 0:
            for i in range(len(message['embeds'])):
                content = message['embeds'][i]
                try:
                    embed = Embedder()
                    embed.title(content['title'])
                    embed.color(15158332)
                except Exception as e:
                    continue
                try:
                    embed.description(content['description'])
                except Exception as e:
                    pass
                try:
                    embed.thumbnail(url=content['thumbnail']['url'])
                except Exception as e:
                    pass
                try:
                    embed.footer(text=content['footer']['text'])
                except Exception as e:
                    pass
                try:
                    embed.author(name=content['author']['name'], url=content['author']['url'], icon_url=content['author']['icon_url'])
                except Exception as e:
                    pass

                if 'fields' in content.keys():
                    for field in content['fields']:
                        try:
                            name = field['name']
                            value = field['value']

                            if name == "":
                                name = "\u200b"
                            if value == "":
                                value = "\u200b"
                            embed.fields(name=name, value=value, inline=field['inline'])
                        except Exception as e:
                            continue

                try:
                    bot.sendMessage(dm, "", embed=embed.read())
                except Exception as e:
                    continue
        if len(message['attachments']) > 0:
            for attachment in message['attachments']:
                try:
                    bot.sendMessage(dm, attachment['url'])
                except Exception as e:
                    pass
    except Exception as e:
        pass


bot.gateway.run()
