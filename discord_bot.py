import os
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_crypto_prices():
    crypto_list = ["bitcoin", "ethereum", "dogecoin", "litecoin", "matic"]
    prices = {}

    for crypto in crypto_list:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd")
        data = response.json()
        if crypto in data:
            prices[crypto] = data[crypto]["usd"]

    return prices

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$caca'):
        await message.channel.send('Tu es une merde sale pute 💩')

    if message.content.startswith('$crypto'):
        prices = get_crypto_prices()
        if prices:
            price_message = "\n".join(f"{crypto.capitalize()}: ${price}" for crypto, price in prices.items())
            await message.channel.send(f"Real-time cryptocurrency prices:\n{price_message}")

# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Pour lancer le bot
client.run(bot_token)
