import os
import discord
import requests

# Set the REQUESTS_CA_BUNDLE environment variable to use the certifi bundle
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(__file__), 'certifi', 'cacert.pem')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_crypto_prices():
    crypto_list = ["bitcoin", "ethereum", "dogecoin", "litecoin", "matic"]
    prices = {}

    for crypto in crypto_list:
        try:
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd")
            response.raise_for_status()  # Raise an exception for non-200 HTTP status codes
            data = response.json()
            if crypto in data:
                prices[crypto] = data[crypto]["usd"]
        except Exception as e:
            print(f"Error fetching {crypto} price: {e}")

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

    if message.content.lower().startswith('$crypto'):
        prices = get_crypto_prices()
        if prices:
            price_message = "\n".join(f"{crypto.capitalize()}: ${price}" for crypto, price in prices.items())
            await message.channel.send(f"Real-time cryptocurrency prices:\n{price_message}")

# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Pour lancer le bot
client.run(bot_token)
