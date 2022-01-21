import datetime
import time

from twitchio.ext import commands

ACCESS_TOKEN = 'yrvh5mzx0jet83xvez5b4u6ffmkn4e'
CHANNEL = 'mister_quokka'
PREFIX = 'pykaDoven'
TIMEOUT = 1.5
CHECK_TIMEOUT = 0.5

storage = {
  'last_send_time': None
}


class Bot(commands.Bot):
  def __init__(self):
    super().__init__(
      token=ACCESS_TOKEN, prefix='PREFIX', initial_channels=[CHANNEL])

  async def event_ready(self):
    print('Ботик {} загружен'.format(self.nick))

  async def send_message_prompt(self, context, responce):
    if storage['last_send_time'] is not None:
      while True:
        diff = datetime.datetime.now() - storage['last_send_time']
        if diff.total_seconds() < TIMEOUT:
          time.sleep(CHECK_TIMEOUT)
        else:
          break
    responce_text = '{}! Сейчас {}'.format(responce, datetime.datetime.now())
    await context.send(responce_text)
    storage['last_send_time'] = datetime.datetime.now()

  async def event_message(self, message_obj):
    content = message_obj.content
    if message_obj.echo or not content.startswith(PREFIX):
      return
    prefix = await self.get_prefix(message_obj)
    context = commands.Context(
      message=message_obj, prefix=prefix, valid=False, bot=self)
    author_name = context.author.name
    result = 'Привет, {}'.format(author_name)
    try:
      content = content[len(PREFIX)::].lstrip()
      # print(content)
      # print(message_obj, context)
      # print(message_obj.__dict__)
      # for user in context.users:
      #   print(user.display_name, user.badges, user.is_mod,
      #         user.is_subscriber, user.is_turbo)
    except Exception:
      result = 'Я сломалсо, {}'.format(author_name)
    await self.send_message_prompt(context, result)


def main():
  bot = Bot()
  bot.run()


if __name__ == '__main__':
  main()
