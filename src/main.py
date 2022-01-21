from twitchio.ext import commands

ACCESS_TOKEN = '3gq9clr0r5perfcg7hh044o1nwpj9s'
CHANNEL = 'mister_quokka'


class Bot(commands.Bot):

  def __init__(self):
    super().__init__(
      token=ACCESS_TOKEN, prefix='pykaDoven', initial_channels=[CHANNEL])

  async def event_ready(self):
    print('Ботик {} загружен'.format(self.nick))

  async def event_message(self, message):
    if message.echo:
      return
    prefix = await self.get_prefix(message)
    context = commands.Context(
      message=message, prefix=prefix, valid=False, bot=self)
    print(message, context)
    for user in context.users:
      print(user.display_name, user.badges, user.is_mod,
            user.is_subscriber, user.is_turbo)
    await context.send(f'Выгоняем алкоголь, {context.author.name}!')


def main():
  bot = Bot()
  bot.run()


if __name__ == '__main__':
  main()
