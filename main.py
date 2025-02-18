from email.policy import default
from logging import exception
from bs4 import BeautifulSoup as bs
import discord
from discord.ext import  commands
from discord import app_commands
import secretoso
from secretoso import TOKEN
#secretoso es un archivo de python en el cual guardé mi token de del bot, el cual por obvias razones no esta en el repositorio
import requests


class Client(commands.Bot):
    async def on_ready(self):
        print(f'logged on as {self.user}')

        try:
            guild = discord.Object(id=1051930181637513316)
            synced = await self.tree.sync(guild=guild)
            print(f'sincronizado {len(synced)} comandos a el servidor {guild.id}')
            print(synced)

        except Exception as e:
            print(f'error sincronizando los comandos: {e}')


    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('hola'):
            await message.channel.send(f'hola {message.author} \n https://tenor.com/view/haunter-wave-cobblemon-gif-9636032239076073245')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('reaccionaste omg')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="&", intents=intents)

GUILD_ID = discord.Object(id=1051930181637513316)

@client.tree.command(name="poke", description="envia la foto de un pokemon", guild=GUILD_ID)
async def poke(interaction: discord.Interaction, argumento: str):
    try:
        pokemon = argumento
        print(f" /poke usado! \n{pokemon}")
        result = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.replace(" ", "-" )}")
        if result == "not found":
            await interaction.response.send_message(f"ummm, de hecho, el pokemon {pokemon} no existe :nerd:")
        else:

            img_url = result.json()['sprites']['front_default']
            print(img_url)
            types = ["a", "b"]
            types[0] = result.json()['types'][0]['type']['name']
            try:
                types[1] = result.json()['types'][1]['type']['name']
            except Exception as nosecondtype:
                print(f"{nosecondtype} (no hubo un tipo secundario)")
                types[1] = " "

            embed = discord.Embed(
                title=f"{pokemon}",
                description=f"aquí están los datos del pokemon que ingresaste!",
                color=discord.Color.random(),
            )
            thumbnail = "https://cdn.discordapp.com/attachments/1298495312318693416/1340479011574513664/image.png?ex=67b281dd&is=67b1305d&hm=8423ead878c943d90b8a7480cbb5bc9d0c65f574c0c701e21ce08a8954763481&"
            embed.set_thumbnail(url=thumbnail)
            embed.set_image(url=img_url)

            embed.add_field(name= "types", value=f"{types[0]} {types[1]}", inline=True)
            embed.add_field(name="hp", value=result.json()['stats'][0]['base_stat'], inline=True)
            embed.add_field(name="attack", value=result.json()['stats'][1]['base_stat'], inline=True)
            embed.add_field(name="defense", value=result.json()['stats'][2]['base_stat'], inline=True)
            embed.add_field(name="s.attack", value=result.json()['stats'][3]['base_stat'], inline=True)
            embed.add_field(name="s.defense", value=result.json()['stats'][4]['base_stat'], inline=True)
            embed.add_field(name="speed", value=result.json()['stats'][5]['base_stat'], inline=True)
            #await interaction.response.send_message(f"una foto del pokemon {pokemon}! \n {img_url}")
            await interaction.response.send_message(embed=embed)

    except Exception as e:
        errorembed = discord.Embed(
            title=f"ups, ¡he fallado en algo!",
            description="mis habilidades con el código dignas de un neandertal causaron esto, perdón",
            color=discord.Color.red()
        )
        errorembed.add_field(name="error:", value=f"{e}", inline=True)
        print (f"error: {e}")
        await interaction.response.send_message(embed=errorembed)

@client.tree.command(name="pokeitem", description="envia la descripción y foto de un item", guild=GUILD_ID)
async def pokeitem(interaction: discord.Interaction, argumento: str):
    try:
        item = argumento.replace(" ", "-" )
        result = requests.get(f"https://pokeapi.co/api/v2/item/{item}")
        if result == "not found":
            await interaction.response.send_message(f"ummm, de hecho, el item {item} no existe :nerd:")
        else:

            thumbnail = "https://cdn.discordapp.com/attachments/1298495312318693416/1340479011574513664/image.png?ex=67b281dd&is=67b1305d&hm=8423ead878c943d90b8a7480cbb5bc9d0c65f574c0c701e21ce08a8954763481&"
            efecto = result.json()['effect_entries'][0]['effect']
            img_url = result.json()['sprites']['default']
            print(img_url)

            itemembed = discord.Embed(
                title=f"{argumento}",
                description=f"efecto de {argumento}: {efecto}",
                color = discord.Color.random()
            )

            itemembed.set_thumbnail(url=thumbnail)
            itemembed.set_image(url=img_url)
            await interaction.response.send_message(embed= itemembed)


    except Exception as e:
        errorembed = discord.Embed(
            title=f"ups, ¡he fallado en algo!",
            description="mis habilidades con el código dignas de un neandertal causaron esto, perdón",
            color=discord.Color.red()
        )
        errorembed.add_field(name="error:", value=f"{e}", inline=True)
        print(f"error: {e}")
        await interaction.response.send_message(embed=errorembed)

@client.tree.command(name="saluda", description="hola amiga", guild=GUILD_ID)
async def saludar(interaction: discord.Interaction):
    helloembed = discord.Embed(
        title=f"Hola amiga",
        description=f"como estas",
        color=discord.Color.random()
    )
    helloembed.set_image(url="https://tenor.com/view/haunter-wave-cobblemon-gif-9636032239076073245")
    await interaction.response.send_message(embed = helloembed)

@client.tree.command(name="calcula", description="1. suma 2. resta. 3. mult. 4. div", guild=GUILD_ID)
async def calcular(interaction: discord.Interaction, operacion: int, num1: int, num2: int):
    match operacion:
        case 1:
            await interaction.response.send_message(f"la suma da: {num1 + num2}")
        case 2:
            await interaction.response.send_message(f"la resta da: {num1 - num2}")
        case 3:
            await interaction.response.send_message(f"la multiplicación da: {num1 * num2}")
        case 4:
            await interaction.response.send_message(f"la división da: {num1 / num2}")
        case _:
            await interaction.response.send_message(f"COÑO LEE LA DESCRIPCIÓN DEL COMANDO, ENERGUMENO")

@client.tree.command(name="img", description="primera img de google", guild=GUILD_ID)
async def img(interaction: discord.Interaction, busqueda: str):


    try:
        parametros = {
            "q": busqueda,
            "tbm": "isch",
        }

        html = requests.get("https://www.google.com/search", params=parametros, timeout=30)
        html.text
        soup = bs(html.content)
        images = soup.select('div img')
        img_url = images[1]['src']

        img_embed = discord.Embed(
            title=f"{busqueda}",
            description="aquí esta una imagen de lo que buscaste",
            color=discord.Color.random()
        )
        img_embed.set_image(url=img_url)
        await interaction.response.send_message(embed=img_embed)

    except Exception as e:

        errorembed = discord.Embed(
            title=f"ups, ¡he fallado en algo!",
            description="mis habilidades con el código dignas de un neandertal causaron esto, perdón",
            color=discord.Color.red()
        )
        errorembed.add_field(name="error:", value=f"{e}", inline=True)
        print(f"error: {e}")
        await interaction.response.send_message(embed=errorembed)



client.run(TOKEN)

