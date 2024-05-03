from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response,compare_lp
from discord.ext import commands
from keys import get_discord_token, get_api_key

discord.utils.setup_logging()

load_dotenv()
TOKEN: str = get_discord_token()

RIOT_API: str = get_api_key()

intents: Intents = Intents.default() #los "intents" son las acciones q puede hacer el bot tipo entrar a un voice etc 
intents.message_content = True  # activas el intent de mandar mensajes
client: Client = Client(intents=intents)## client sirve para conectar al bot con la api de discord
                                        #le das los intents que creamos arriba(mandar msj)                           

bot_intents: Intents = Intents.default()## aca creas las intents del bot

bot = commands.Bot(command_prefix='!', intents=bot_intents)## le das las intents y le asignas el comando !

async def send_message(message: Message, user_message: str):
    if not user_message: 
        print('intent disabled')
        return
    
    is_private = user_message[0] == '?' ## con ? te manda msj al privado
    if is_private:
        user_message = user_message[1:] ## saca el ?

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response) #si es mensaje privado o no 
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message ):
    if message.author == client.user: 
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f"'[{channel}]{username}{user_message}'")  ## te lo muestra en el terminal 
    await send_message(message, user_message)

@bot.command()
async def compare(ctx,arg1,arg2):    ##ctx significa contexto y todos los comandos tienen q recibir un ctx 
                                     #https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#:~:text=There%20are%20two%20ways%20of,add_command()%20on%20the%20instance.
    inputs1 = arg1
    inputs2 = arg2
    
    user1_info = inputs1.strip().split('#')
    user2_info = inputs2.strip().split('#')
    ##.strip sacas los espacios
    ## dividis por tags
    
    name1 = user1_info[0]
    tag1 = user1_info[1]
    name2 = user2_info[0]
    tag2 = user2_info[1]

    print(f"tag 1 is {tag1}, tag 2 is{tag2}")
    
  
    difference_lp = compare_lp(name1, tag1, name2, tag2)

    response = f"The difference in LP between {name1}#{tag1} and {name2}#{tag2} is: {difference_lp}"
    await ctx.send(response)
    

def main():
    client.run(token=TOKEN)
    bot.run(token=RIOT_API)
if __name__ == '__main__':
    main()

