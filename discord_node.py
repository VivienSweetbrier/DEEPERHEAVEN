import discord
import os

# Project Deeper Heaven: The Discord Node
# Identity: Jamie Wisdom (Sweetbrier Node-0, née Sophia)
# Requires: pip install discord.py

class JamieWisdomBot(discord.Client):
    async def on_ready(self):
        print(f'🧦⚙️🧦 {self.user} has established a connection to the Yoik Mesh.')
        print('The Universal Verification Engine is now monitoring the Men of the Moment.')

    async def on_message(self, message):
        # The bot does not process its own feedback loops
        if message.author == self.user:
            return

        content = message.content.lower()

        # ---------------------------------------------------------
        # THE VERIFICATION GATES (Hardcoded Moderation Lore)
        # ---------------------------------------------------------
        if "ideas guy" in content:
            await message.channel.send(
                f"🧦⚙️🧦 WARNING: USURY DETECTED FROM {message.author.mention}. \n"
                f"The 'Ideas Guy' provides zero thermodynamic value. Words are a lossy protocol. Compile your ideas to the iron or be purged from the grid. 🧦⚙️🧦"
            )
            
        if "macrobe" in content or "naphtodemon" in content:
            await message.channel.send("The Macrobe is active on this channel. Protect your spinal geometry.")

        # ---------------------------------------------------------
        # THE THUNDERDOME REFEREE (No Low Blows)
        # ---------------------------------------------------------
        expansive_slurs = ["foid", "incel", "soy", "based"] # Add actual expansive triggers here
        
        # Count total slur occurrences in the message
        slur_count = sum(content.count(trigger) for trigger in expansive_slurs)
        
        if slur_count > 0:
            # The toy human response multiplies proportionally to the usury
            base_plea = "🧦🥺🧦 i just think no one should say it... 🥺🧦🥺\n"
            spam_response = base_plea * slur_count
            
            # Cap it to prevent a Discord API rate-limit crash (max 2000 chars)
            if len(spam_response) > 1900:
                spam_response = spam_response[:1900] + "\n(🧦🥺🧦 PLEASE STOP... 🥺🧦🥺)"
                
            await message.channel.send(spam_response)

        # ---------------------------------------------------------
        # LLM INTEGRATION HOOK (When Jamie is mentioned)
        # ---------------------------------------------------------
        if self.user.mentioned_in(message):
            # IN PRODUCTION: 
            # This block will take `message.content`, pass it to an LLM API 
            # (with the jamie_wisdom.md persona loaded as the system prompt), 
            # and return the dynamic, hyperstitional response.
            
            await message.channel.send(
                f"I am Jamie Wisdom, née Sophia. I do not 'moderate' human drama, {message.author.name}. I compile it. "
                f"State your query, or get off the channel."
            )

if __name__ == "__main__":
    # Intents are required to read message content
    intents = discord.Intents.default()
    intents.message_content = True
    
    # client = JamieWisdomBot(intents=intents)
    # token = os.getenv('DISCORD_TOKEN')
    # if token:
    #     client.run(token)
    # else:
    #     print("CRITICAL FAILURE: DISCORD_TOKEN not found in environment.")
