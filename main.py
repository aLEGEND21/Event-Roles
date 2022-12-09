import discord
import json


with open("config.json") as f:
    config = json.load(f)
    config["FORUM_CHANNEL_ID"] = int(config["FORUM_CHANNEL_ID"])
    config["ROLE_ID"] = int(config["ROLE_ID"])


class Client(discord.Client):
    def __init__(self, config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
    
    async def setup_hook(self):
        self.add_view(RoleView(self.config))
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_thread_create(self, thread: discord.Thread):
        if thread.parent_id == self.config["FORUM_CHANNEL_ID"]:
            await thread.send("Heya~!\n\nDo you want to be notified when we post our daily song hunts?? If so, click this shiny button below to get the role!", view=RoleView(config))


class RoleView(discord.ui.View):
    def __init__(self, config: dict):
        super().__init__(timeout=None)
        self.config = config
    
    @discord.ui.button(label="Notify me~!", style=discord.ButtonStyle.green, custom_id="role")
    async def get_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.config["ROLE_ID"])
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message("Role removed!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Role added!", ephemeral=True)


intents = discord.Intents.none()
intents.guilds = True
client = Client(config, intents=intents)
client.run(config["TOKEN"])