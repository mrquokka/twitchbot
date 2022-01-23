import asyncio
import datetime
import random
import time

from twitchio.ext import commands

ACCESS_TOKEN = 'yrvh5mzx0jet83xvez5b4u6ffmkn4e'
CHANNEL = 'mideli'
PREFIX = 'ботик'
TIMEOUT = 1.5
CHECK_TIMEOUT = 0.5
BASE_RANDOM_COUNTER = 4
RANDOM_WAIT_TIME = 10

storage = {
  'current_random': None,
  'started_bot': None,
  'messages': []
}


async def checker():
  started_bot = storage['started_bot']
  if started_bot is not None:
    ws_connection = started_bot._connection._websocket
    if ws_connection is not None:
      if not ws_connection.closed:
        messages = list(storage['messages'])
        storage['messages'].clear()
        if storage['current_random']:
          random_result = check_random_ended()
          if random_result is not None:
            messages.append(random_result)
        if len(messages) > 0:
          content = '. '.join(messages)
          await started_bot._connection.send(
            'PRIVMSG #{} :{}\r\n'.format(
              CHANNEL, content)
          )
  await asyncio.sleep(1.5)
  await checker()


def check_random_ended():
  diff = datetime.datetime.now() - storage[
    'current_random'
  ]['start_date']
  if diff.total_seconds() < RANDOM_WAIT_TIME:
    return None
  values = {}
  for id, info in storage['current_random'].items():
    if id == 'start_date':
      continue
    sum = info['sum']
    if sum not in values:
      values[sum] = []
    values[sum].append(info['name'])
  text_rows = ['Результаты:']
  for sum in reversed(list(sorted(values.keys()))):
    for name in values[sum]:
      text_rows.append('@{} - {}'.format(name, sum))
  result = '. '.join(text_rows)
  storage['current_random'] = None
  return result


class Bot(commands.Bot):
  def __init__(self):
    loop = asyncio.get_event_loop()
    super().__init__(
      token=ACCESS_TOKEN, prefix='PREFIX', initial_channels=[CHANNEL],
      loop=loop)
    storage['started_bot'] = self
    loop.create_task(checker())

  async def close(self):
    """|coro|

    Cleanly disconnects from the twitch IRC server
    """
    await self._connection._close()

  async def event_ready(self):
    print('Ботик {} загружен'.format(self.nick))

  async def event_message(self, message_obj):
    content = message_obj.content
    if message_obj.echo or not content.startswith(PREFIX):
      return
    prefix = await self.get_prefix(message_obj)
    context = commands.Context(
      message=message_obj, prefix=prefix, valid=False, bot=self)
    author = context.author
    author_id = author.id
    author_name = author.display_name
    content = content[len(PREFIX)::].lstrip()
    if content == 'рандом':
      is_new = storage['current_random'] is None
      if is_new:
        storage['messages'].append(
          'Запущен рандомайзер, завершится через 10 секунд, ' +
          'после вступления последнего игрока'
        )
        storage['current_random'] = {}
      if author_id in storage['current_random']:
        storage['messages'].append(
          '@{}, вы уже участвуете'.format(author_name)
        )
        return
      storage['current_random']['start_date'] = datetime.datetime.now()
      counter = BASE_RANDOM_COUNTER
      if author.is_mod:
        counter = counter + 1
      if author.is_subscriber or (
        # TODO turbo bugged?
        author.is_turbo is not None and author.is_turbo != '0'
      ):
        counter = counter + 1
      random_result = []
      sum = 0
      for item in range(counter):
        item = random.randint(1, 6)
        sum = sum + item
        random_result.append(chr(9855 + item))

      storage['messages'].append(
        '@{}, ваш результат - {} ({})'.format(
          author_name, ' '.join(random_result), sum
        )
      )
      storage['current_random'][author_id] = {
        'name': author_name,
        'sum': sum
      }
    else:
      storage['messages'].append('Привет, {}'.format(author_name))


def main():
  bot = Bot()
  bot.run()


if __name__ == '__main__':
  main()
