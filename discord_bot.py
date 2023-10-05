import os
import discord
import requests
import random
from discord.ext import commands

pfcLi = ['Pierre', 'Feuille', 'Ciseaux']
randSi = random.choice(pfcLi)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def get_crypto_prices():
    crypto_list = ["bitcoin", "ethereum", "dogecoin", "litecoin", "polygon", "ripple", "tether", "solana"]
    prices = {}

    for crypto in crypto_list:
        try:
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd",
                verify=False  # Disable SSL certificate verification
            )
            response.raise_for_status()  # Raise an exception for non-200 HTTP status codes
            data = response.json()
            if crypto in data:
                prices[crypto] = data[crypto]["usd"]
        except Exception as e:
            print(f"Error fetching {crypto} price: {e}")

    return prices

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$caca') or message.content.startswith('$merde'):
        await message.channel.send('Tu es une merde sale pute 💩')

    if message.content.startswith('$help') or message.content.startswith('$aide'):
        await message.channel.send('$crypto : displays a list of cryptocurrencies and their price')

    if message.content.startswith('$pfc') and message.content.endswith('feuille'):
        await message.channel.send(randSi)

    if message.content.startswith('$pfc') and message.content.endswith('pierre'):
        await message.channel.send(randSi)

    if message.content.startswith('$pfc') and message.content.endswith('ciseaux'):
        await message.channel.send(randSi)

    if message.content.lower().startswith('$crypto'):
        prices = get_crypto_prices()
        if prices:
            price_message = "\n".join(f"{crypto.capitalize()}: ${price}" for crypto, price in prices.items())
            await message.channel.send(f"Real-time cryptocurrency prices:\n{price_message}")
            

# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Pour lancer le bot
bot.run(bot_token)
