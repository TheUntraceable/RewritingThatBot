from io import StringIO
import discord
from discord.ext import commands
from datetime import datetime, 
from discord.ext import commands

def success(title : str = "Success!", desc : str =  "Command executed successfully!"):
    embed = discord.Embed(
      title = title,
      description = desc,
      color = discord.Color.green(),
      timestamp = datetime.datetime.utcnow()
    )
    embed.set_author(name = "Success")
    return embed

def ErrorEmbed(title,reason):
    embed = discord.Embed(
      title = title,
      description = reason,
      color = discord.Color.red(),
      timestamp = datetime.datetime.utcnow()
    )
    embed.set_author(name = "Error")
    return embed

import ui

class Connect4Game:
	WIDTH = 7
	HEIGHT = 6

	H1 = HEIGHT + 1
	H2 = HEIGHT + 2
	SIZE = HEIGHT * WIDTH
	SIZE1 = H1 * WIDTH
	ALL1 = (1 << SIZE1) - 1
	COL1 = (1 << H1) - 1
	BOTTOM = ALL1 // COL1
	TOP = BOTTOM << HEIGHT

	PIECES = '@0'

	def __init__(self):
		self.turns = 0
		self.lowest_free_squares = [self.H1 * i for i in range(self.WIDTH)]
		self.boards = [0, 0]

	reset = __init__

	def is_playable(self, col):
		"""return whether the column has room"""
		return self.is_legal(self.boards[self.turns & 1] | (1 << self.lowest_free_squares[col]))

	def is_legal(self, board):
		"""return whether the board lacks an overflowing column"""
		return board & self.TOP == 0

	def has_won(self, player):
		board = self.boards[player]
		y = board & (board >> self.HEIGHT)
		if (y & (y >> 2 * self.HEIGHT)) != 0:  # diagonal \
			return True
		y = board & (board >> self.H1)
		if (y & (y >> 2 * self.H1)) != 0:  # horizontal -
			return True
		y = board & (board >> self.H2)
		if (y & (y >> 2 * self.H2)) != 0:  # diagonal /
			return True
		y = board & (board >> 1)
		return (y & (y >> 2)) != 0  # vertical |

	def move(self, col):
		self.boards[self.turns & 1] |= 1 << self.lowest_free_squares[col]
		self.lowest_free_squares[col] += 1
		self.turns += 1

	def whomst_turn(self):
		return self.turns & 1

	def __getitem__(self, xy):
		x, y = xy
		i = x * self.H1 + y
		mask = 1 << i
		return 0 if self.boards[0] & mask != 0 else 1 if self.boards[1] & mask != 0 else -1

	def __str__(self):
		buf = StringIO()

		for w in range(self.WIDTH):
			# column indexes
			buf.write(' ')
			buf.write(str(w + 1))

		buf.write('\n')

		for h in range(self.HEIGHT-1, -1, -1):
			for w in range(h, self.SIZE1, self.H1):
				mask = 1 << w
				buf.write(' ')
				buf.write(
					self.PIECES[0] if self.boards[0] & mask != 0
					else self.PIECES[1] if self.boards[1] & mask != 0
					else '.')
			buf.write('\n')

		return buf.getvalue()

class CodeBlockConnect4Game(Connect4Game):
	def __str__(self):
		return f'```{super().__str__()}```'

class Connect4Session(ui):
	def __init__(self, *args, **kwargs):
		self.game = kwargs.pop('game')
		self.players = kwargs.pop('players')
		super().__init__(
			*args,
			allowed_users={u.id for u in self.players},
			delete_after=False,
			**kwargs)
		for i in range(1, Connect4Game.WIDTH + 1):
			self.add_button(self.button, str(i) + '\N{combining enclosing keycap}')
		self.add_button(self.forfeit, '🚫')

	def won_string(self):
		def s(i): return f'{self.players[i]} (`{self.game.PIECES[i]}`) won!'
		if self.game.has_won(0):
			return s(0)
		if self.game.has_won(1):
			return s(1)
		return ''

	def current_player(self):
		player_i = self.game.whomst_turn()
		piece = self.game.PIECES[player_i]
		player = self.players[player_i]
		return piece, player

	def current_player_string(self):
		piece, player = self.current_player()
		return f"{player} (`{piece}`)'s turn"

	async def get_current_message(self, *, append_player=True):
		message = str(self.game)

		won = self.won_string()
		if won:
			await self.stop()

		if append_player:
			message += won
			if not won:
				message += self.current_player_string()

		return discord.utils.escape_mentions(message)

	get_initial_message = get_current_message

	async def button(self, payload):
		col = int(str(payload.emoji)[0]) - 1
		player = self.game.whomst_turn()
		if payload.user_id != self.players[player].id:
			return
		if not self.game.is_playable(col):
			return

		self.game.move(col)
		await self.message.edit(content=await self.get_current_message())

	def forfeit_string(self, player_i):
		player = self.players[player_i]
		player_piece = self.game.PIECES[player_i]
		winner_i = (player_i + 1) & 1
		winner = self.players[winner_i]
		winner_piece = self.game.PIECES[winner_i]
		return discord.utils.escape_mentions(f'{winner} (`{winner_piece}`) won ({player} (`{player_piece}`) forfeited)')

	async def forfeit(self, payload):
		whomst = self.players.index(self.context.bot.get_user(payload.user_id))
		message = await self.get_current_message(append_player=False) + self.forfeit_string(whomst)
		await self.message.edit(content=message)
		await self.stop()

class Connect4(commands.Cog):
	@commands.command()
	async def connect4(self, ctx, member: discord.Member):
		game = CodeBlockConnect4Game()
		player1, player2 = ctx.author, member
		players = [player1, player2]
		session = Connect4Session(game=game, players=players)
		await session.start(ctx)

def setup(bot):
	bot.add_cog(Connect4())