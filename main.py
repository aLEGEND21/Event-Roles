import discord
import json


with open("config.json") as f:
    config = json.load(f)
    config["GUESS_THE_SONG_FORUM_CHANNEL_ID"] = int(config["GUESS_THE_SONG_FORUM_CHANNEL_ID"])
    config["GUESS_THE_SONG_ROLE_ID"] = int(config["GUESS_THE_SONG_ROLE_ID"])
    config["SONG_HUNT_FORUM_CHANNEL_ID"] = int(config["SONG_HUNT_FORUM_CHANNEL_ID"])
    config["SONG_HUNT_ROLE_ID"] = int(config["SONG_HUNT_ROLE_ID"])


class Client(discord.Client):
    def __init__(self, config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
    
    async def setup_hook(self):
        self.add_view(RoleView(self.config["GUESS_THE_SONG_ROLE_ID"]))
        self.add_view(RoleView(self.config["SONG_HUNT_ROLE_ID"]))
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_thread_create(self, thread: discord.Thread):
        if thread.parent_id == self.config["GUESS_THE_SONG_FORUM_CHANNEL_ID"]:
            await thread.send("Heya~!\n\nDo you want to be notified when we post our daily guess the song posts?? If so, click this shiny button below to get the role!", view=RoleView(self.config["GUESS_THE_SONG_ROLE_ID"]))
        elif thread.parent_id == self.config["SONG_HUNT_FORUM_CHANNEL_ID"]:
            await thread.send("Heya~!\n\nDo you want to be notified when we post our daily song hunts?? If so, click this shiny button below to get the role!", view=RoleView(self.config["SONG_HUNT_ROLE_ID"]))


class RoleView(discord.ui.View):
    def __init__(self, role_id: int):
        super().__init__(timeout=None)
        self.role_id = role_id
    
    @discord.ui.button(label="Notify me~!", style=discord.ButtonStyle.green, custom_id="role")
    async def get_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
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