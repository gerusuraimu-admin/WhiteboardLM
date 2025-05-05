class SlackEventObject:
    user: str
    text: str
    channel: str

    def __init__(self, **kwargs) -> None:
        self.user = kwargs.get('user')
        self.text = kwargs.get('text')
        self.channel = kwargs.get('channel')

    def __str__(self) -> str:
        return '\n'.join(f'{k.ljust(13)} : {v}' for k, v in vars(self).items())

    @property
    def message(self) -> str:
        ret = ''
        if hasattr(self, 'text'):
            index = list(self.text).index('>')
            return self.text[index+2:]
        return ret
