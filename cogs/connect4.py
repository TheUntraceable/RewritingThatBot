import random
from typing import List, Dict
import discord
from discord.ext import commands
import random
import asyncio
import math

ROW_COUNT = 6  # used to represent number of rows in a board
COL_COUNT = 7  # used to represent number of columns in a board
EMPTY = '*'  # used to represent an empty part of the board
board_piece = {EMPTY: ':blue_circle: ', 'R': ':red_circle: ',
               'Y': ':yellow_circle: '}
PLAYER_PIECE = 'R'
AI_PIECE = 'Y'


class Board:
    """The board for the connect 4 game
    """
    # === Private Attributes ===
    # _board:
    # The array representing the game board.
    _board: List[List[str]]

    # Methods
    def __init__(self) -> None:
        """Initialize a Board with empty (blue) circles.
        self._arr is an empty 7x6 board.
        """
        arr = [[EMPTY] * 7 for _ in range(6)]
        self._board = arr

    def print_board(self) -> str:
        """Used to print the board with blue circles as empty areas,
        red circles as player 1 moves, and yellow circles as player 2 moves"""
        msg = ''
        for row in self._board:
            for item in row:
                msg += board_piece[item]
            msg += '\n'
        return msg

    def is_valid_location(self, r: int, c: int):
        """Check if the section of the board is not already filled"""
        if self._board[r][c] == EMPTY:
            return True
        return False

    def drop_piece(self, r: int, c: int, piece: str):
        """Drop piece of one of the players into the board"""
        self._board[r][c] = piece

    # for piece can use i from other function
    def is_win(self, piece: str) -> bool:
        """Checks if there are any connect fours"""

        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):

                # Horizontal Wins
                if c < COL_COUNT - 3:
                    if (self._board[r][c] == self._board[r][c + 1] == self.
                            _board[r][c + 2] == self._board[r][c + 3] == piece):
                        return True

                # Vertical Wins
                if r < ROW_COUNT - 3:
                    if self._board[r][c] == self._board[r + 1][c] == \
                            self._board[r + 2][c] == \
                            self._board[r + 3][c] == piece:
                        return True

                # Positive Diagonal Wins
                if c < COL_COUNT - 3 and r < ROW_COUNT - 3:
                    if self._board[r][c] == self._board[r + 1][c + 1] == \
                            self._board[r + 2][c + 2] == \
                            self._board[r + 3][c + 3] == piece:
                        return True

                # Negative Diagonal Wins
                if c < COL_COUNT - 3 and 3 <= r < ROW_COUNT:
                    if self._board[r][c] == self._board[r - 1][c + 1] == \
                            self._board[r - 2][c + 2] == \
                            self._board[r - 3][c + 3] == piece:
                        return True
        return False

    def score_position(self, piece: str):
        """
        Return the Score of the position.
        """
        score = 0
        # Score center column
        center_list = [self._board[r][COL_COUNT // 2] for r in range(ROW_COUNT)]
        center_count = center_list.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row = self._board[r]
            for c in range(COL_COUNT - 3):
                section = row[c:c + 4]
                score += evaluate_section(section, piece)

        # Score Vertical
        for c in range(COL_COUNT):
            col = [self._board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                section = col[r:r + 4]
                score += evaluate_section(section, piece)

        # Score Positive Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r + i][c + i] for i in range(4)]
                score += evaluate_section(section, piece)

        # Score Negative Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT - 3):
                section = [self._board[r + 3 - i][c + i] for i in range(4)]
                score += evaluate_section(section, piece)
        return score

    def is_terminal_node(self) -> bool:
        """
        Return if the game is finished or if there are no valid locations left.
        """
        return self.is_win(PLAYER_PIECE) or \
            self.is_win(AI_PIECE) or (len(self.get_valid_locations()) == 0)

    def get_valid_locations(self) -> Dict[int, int]:
        """
        Return a dict with key as column, and value as row, representing places
        the piece can be dropped into.
        """
        valid_locations = {}
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT):
                if self.is_valid_location(r, c):
                    valid_locations[c] = r
        return valid_locations

    def minimax(self, depth, alpha, beta, maximizing_player) -> tuple:
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_win(AI_PIECE):
                    return None, 100000000000000
                elif self.is_win(PLAYER_PIECE):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(AI_PIECE)

        if maximizing_player:  # Maximizing player (for bot turn)
            value = -math.inf
            column = random.choice(list(valid_locations.keys()))
            for col in valid_locations:
                row = valid_locations[col]
                temp_board = Board()
                temp_board._board = [sublist.copy() for sublist in self._board]
                temp_board.drop_piece(row, col, AI_PIECE)
                new_score = temp_board.minimax(depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player (for player turn)
            value = math.inf
            column = random.choice(list(valid_locations.keys()))
            for col in valid_locations:
                row = valid_locations[col]
                temp_board = Board()
                temp_board._board = [sublist.copy() for sublist in self._board]
                temp_board.drop_piece(row, col, PLAYER_PIECE)
                new_score = temp_board.minimax(depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


# Helper
def evaluate_section(section: list, piece: str) -> int:
    """Evaluates the score of a specific section on the board based on
    how close the section is to giving a connect 4"""
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if section.count(piece) == 4:
        score += 10000
    elif section.count(piece) == 3 and section.count(EMPTY) == 1:
        score += 10
    elif section.count(piece) == 2 and section.count(EMPTY) == 2:
        score += 5

    if section.count(opp_piece) == 3 and section.count(EMPTY) == 1:
        score -= 8
    elif section.count(opp_piece) == 4:
        score -= 8000

    return score
	


PLAYER_PIECE = 'R'
AI_PIECE = 'Y'
BOT_ID = 837837082948534272
# Prefix to call bot
client = commands.Bot(command_prefix='4', case_insensitive=True)
client.remove_command('help')  # Removes default help command

# Emotes used for the player to choose their move
EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6,
          '🏳': 'F'}
# numbers to print above connect 4 board
TOP_NUM = '** **\n:one: :two: :three: :four: :five: :six: :seven: \n'
# dictionary to keep track of where the game is happening
IDS = {}
# what index stands for what in IDS
BRD, P1, P2, CURR_P, TIMER, CHAN = 0, 1, 2, 3, 4, 5
# to differentiate between both players
P_DICT = {True: [P1, 'R', discord.Colour.red()],
          False: [P2, 'Y', discord.Colour.gold()]}
# list of gifs to send when a player wins
GIFS = []
gif_file = open("win_gifs.txt", "r")
content = gif_file.readline()
while content != '':
    content = gif_file.readline()
    GIFS.append(content)

class Connect4(commands.Cog):
	def __init__(self,client):
		self.client = client
	@commands.command()
	async def connect4(self,ctx):
		"""Starts a game with either a mentioned user or the bot and then
		adds it to IDS with message id as key, and a list with the board,
		player ids, and first move as the values"""
		# Doesn't start if no one or a bot is mentioned
		if len(ctx.message.mentions) == 0 or ctx.message.mentions[0] == client.user:
			player2 = client.user
		elif ctx.message.mentions[0].bot or \
				ctx.message.mentions[0] == ctx.author:
			await ctx.send(':x: ERROR: You cannot tag a bot or yourself. '
						'\nEither tag another user you want to play with'
						' or the bot/no one if you want to play with the bot.')
			return None
		else:
			player2 = ctx.message.mentions[0]
		player1 = ctx.author
		board = Board()
		# Prints starting board
		message = await ctx.send(f':red_circle: '
								f'{player1.display_name} :crossed_swords: '
								f'{player2.display_name} :yellow_circle: \n'
								+ TOP_NUM + board.print_board() +
								f'\n Current player: <@{player1.id}>'
								f'\n :flag_white:: Forfeit')
		# Adds the emotes the players will be clicking on and adds
		# the game to the global dictionary
		for emoji in EMOTES:
			await message.add_reaction(emoji)
		IDS[message.id] = [board, player1, player2, 'R', 0, ctx.channel]


	@commands.Cog.listener()
	async def on_reaction_add(self,reaction, user) -> None:
		"""
		Check which reaction role was pressed and changes the board accordingly.
		"""
		# If reaction is in a channel where no one is playing, or if the person
		# adding the reactions is the bot, do nothing.
		if reaction.message.id not in IDS or \
				user.id == BOT_ID:
			return None
		curr_channel = IDS[reaction.message.id]
		channel = curr_channel[CHAN]
		curr_piece = curr_channel[CURR_P]
		curr_board = curr_channel[BRD]
		# for P_DICT
		player_red = True if curr_piece == 'R' else False
		curr_player = curr_channel[P_DICT[player_red][0]]
		other_player = curr_channel[P_DICT[not player_red][0]]
		await reaction.remove(user)
		# stops the function if a reaction was added or if the reaction
		# was sent by a non-player
		if reaction.emoji not in EMOTES.keys() \
				or (user != curr_player and user != other_player):
			return None
		# At this point we know it's one of the two players who reacted to an emote.
		# Thus, we can directly cancel the game if one of the players forfeit.
		elif EMOTES[reaction.emoji] == 'F':
			del IDS[reaction.message.id]
			embed = discord.Embed(title=f' {user.display_name} forfeited, '
										f'{curr_channel[1].display_name}'
										f' :crossed_swords: '
										f'{curr_channel[2].display_name}',
								color=discord.Colour.green())
			embed.set_image(url='https://media1.tenor.com/images/'
								'8c3cb918305bf277589c6ad84dfcea53/tenor.gif')
			await channel.send(embed=embed)
			return None
		# if the column is already filled, sends error message and does nothing
		# with the board
		if not curr_board.is_valid_location(0, EMOTES[reaction.emoji]):
			await reaction.message.edit(content=f':red_circle:'
												f'{curr_channel[1].display_name}'
												f' :crossed_swords: '
												f'{curr_channel[2].display_name}'
												f' :yellow_circle: \n'
												+ TOP_NUM + curr_board.print_board()
												+ f':x: ERROR: Column full. :x:'
												f'\n Current player: '
												f'<@{curr_player.id}>'
												f'\n :flag_white:: Forfeit')
			return None
		# stops the function if user is the other player
		if user != curr_player:
			return None
		# changes current piece to next player
		curr_channel[CURR_P] = P_DICT[not player_red][1]
		r = 5
		# finds a valid location to drop the piece in starting from the bottom
		# of the column
		while not curr_board.is_valid_location(r, EMOTES[reaction.emoji]):
			r -= 1
		# drops the piece then edits the message to the updated board
		curr_board.drop_piece(r, EMOTES[reaction.emoji], curr_piece)
		# reset afk timer
		curr_channel[TIMER] = 0
		# Checks if there are no more positions to drop a piece, then ends the game
		# as a draw if this is true.
		if len(curr_board.get_valid_locations()) == 0:
			del IDS[reaction.message.id]
			embed = discord.Embed(title="It's a draw!",
								color=discord.Colour.red())
			embed.set_image(url='https://media1.tenor.com/images/'
								'729fc07335063f9d8a23002a71fdb0a8/tenor.gif')
			await channel.send(embed=embed)
			return None
		# Checks if there is a connect 4, and if so, sends a winner message and
		# removes the game from IDS
		if curr_board.is_win(curr_piece):
			curr_color = P_DICT[player_red][2]
			embed = discord.Embed(title=f'{curr_player.display_name} wins!',
								color=curr_color)
			embed.set_image(url=random.choice(GIFS))
			await channel.send(embed=embed)
			await reaction.message.edit(content=f':red_circle: '
												f'{curr_channel[1].display_name}'
												f' :crossed_swords: '
												f'{curr_channel[2].display_name}'
												f' :yellow_circle: \n'
												+ TOP_NUM + curr_board.print_board()
												+ f'\n<@{curr_player.id}> wins!')
			del IDS[reaction.message.id]
			return None
		# If there is no connect 4, print the board and go to the next turn.
		else:
			await reaction.message.edit(content=f':red_circle: '
												f'{curr_channel[1].display_name}'
												f' :crossed_swords: '
												f'{curr_channel[2].display_name}'
												f' :yellow_circle: \n'
												+ TOP_NUM + curr_board.print_board()
												+ f'\n Current player: '
												f'<@{other_player.id}>'
												f'\n :flag_white:: Forfeit')
		# If playing with bot, run the minimax algorithm and then drop the piece
		# the algorithm has chosen.
		if other_player.bot:
			await asyncio.sleep(1)
			# Goes 6 layers deep into the tree
			col, minimax_score = curr_board.minimax(6, -math.inf, math.inf, True)
			row = curr_board.get_valid_locations()[col]
			# drop the piece into the board
			curr_board.drop_piece(row, col, AI_PIECE)
			curr_channel[TIMER] = 0
			# If bot plays winning move, send winning message and delete
			# game from IDS.
			if curr_board.is_win(curr_channel[CURR_P]):
				other_color = P_DICT[not player_red][2]
				embed = discord.Embed(title=f'{other_player.display_name} '
											f'wins!', color=other_color)
				embed.set_image(url=random.choice(GIFS))
				await channel.send(embed=embed)
				await reaction.message.edit(
					content=f':red_circle: '
							f'{curr_channel[1].display_name}'
							f' :crossed_swords: '
							f'{curr_channel[2].display_name}'
							f' :yellow_circle: \n'
							+ TOP_NUM + curr_board.print_board()
							+ f'\n<@{other_player.id}> wins!')
				del IDS[reaction.message.id]
			# Otherwise, just print the board
			else:
				await reaction.message.edit(
					content=f':red_circle: '
							f'{curr_channel[1].display_name}'
							f' :crossed_swords: '
							f'{curr_channel[2].display_name}'
							f' :yellow_circle: \n'
							+ TOP_NUM + curr_board.print_board()
							+ f'\n Current player:'
							f' <@{curr_player.id}>'
							f'\n :flag_white:: Forfeit')
			# changes current piece back to user
			curr_channel[CURR_P] = curr_piece
def setup(client):
	client.add_cog(Connect4(client))