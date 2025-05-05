from dataclasses import dataclass
from discord.member import Member
from discord.message import Message
from discord.channel import TextChannel


@dataclass
class DiscordEventObject:
    author: Member
    channel: TextChannel
    content: str
    mentions: list

    def __init__(self, message: Message):
        self.author = getattr(message, 'author', None)
        self.channel = getattr(message, 'channel', None)
        self.content = getattr(message, 'content', None)
        self.mentions = getattr(message, 'mentions', None)

    def __str__(self) -> str:
        return '\n'.join(f'{k.ljust(13)} : {v}' for k, v in vars(self).items())

    @property
    def message(self) -> str:
        index = list(self.content).index('>')
        return self.content[index + 2:]
