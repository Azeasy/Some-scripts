from random import randint
import json


class Game():
    """
    A cat is hiding in one of the five boxes.
    The boxes are numbered one to five and are all sitting in a row,
    lined up in order. Each night,
    the sneaky little cat hides in an adjacent box,
    exactly one box away from the box it's in during the day.
    Each morning, you can open exactly one box to see if the cat is in there.

    Find the strategy to always find the cat
    """
    def __init__(self, number_of_boxes):
        if number_of_boxes < 1:
            raise IndexError("Number of boxes could not be less than 1!")
        self.number_of_boxes = number_of_boxes
        self.cat_index = randint(0, self.number_of_boxes - 1)
        self.day = 1
        self.guess = None
        self.game_ended = False

    def start_cli(self):
        while not self.game_ended:
            self.find(int(input("Please enter your guess: ")))
            print(self)
            self.move()
        print(f'You won!\nIt took you {self.day - 1} days')

    def move(self):
        """
        randomly move cat on the next day
        """
        if self.cat_index == 0:
            self.cat_index +=1
        elif self.cat_index == self.number_of_boxes - 1:
            self.cat_index -= 1
        else:
            self.cat_index += (-1)**(randint(0, 1))
        self.day += 1
        self.guess = None

    def find(self, i):
        """
        guess the index of box where the cat is now
        """
        if 0 <= i < self.number_of_boxes:
            self.guess = i
        if self.guess == self.cat_index:
            self.game_ended = True

    def __str__(self):
        representation = f'Day: {self.day}\n'
        for i in range(self.number_of_boxes):
            if self.guess is not None and i == self.guess:
                l, r = '>', '<'
            else:
                l, r = ' ', ' '

            if i == self.cat_index:
                representation += f'{l}|X|{r}'
            else:
                representation += f'{l}| |{r}'
            representation += ' '

        return representation.strip()


class Player():
    """
    The player who knows the best strategy to won the Game game
    """
    def __init__(self, game):
        self.game = game
        self.guess = 1 if self.game.number_of_boxes > 1 else 0
        self.step = 1
        self.reverse = False

    def play(self, silent=False):
        while not self.game.game_ended:
            self.game.find(self.guess)
            if not silent:
                print(f'Guessing: {self.guess}')
                print(self.game)
            self.game.move()
            self.make_guess()

        if not silent:
            print(f'You won!\nIt took you {self.game.day - 1} days')
        return self.game.day - 1

    def make_guess(self):
        if self.guess + 1 < self.game.number_of_boxes - 1 or self.reverse:
            self.guess += self.step
        else:
            self.step = -1
            self.reverse = True


class RandomPlayer(Player):
    """
    The player who plays at random to won the Game game
    """
    def __init__(self, game):
        super(RandomPlayer, self).__init__(game=game)
        self.guess = randint(0, self.game.number_of_boxes - 1)

    def make_guess(self):
        self.guess = randint(0, self.game.number_of_boxes - 1)


if __name__ == "__main__":
    # game = Game(1)
    # game.start_cli()

    # player = Player(game)
    # player.play()

    # random_player = RandomPlayer(Game(5))
    # random_player.play()

    # playing many games
    statistics = {}
    for number_of_boxes in range(1, 20):
        attempts = 10**2
        total_days = 0
        max_days = 1
        for i in range(attempts):
            player = Player(Game(number_of_boxes))
            days = player.play(silent=True)
            total_days += days
            if days > max_days:
                max_days = days
        avg_days = total_days / attempts
        statistics[number_of_boxes] = {
            'max': max_days,
            'avg': avg_days,
        }
    statistics_str = json.dumps(statistics, indent=2)
    print(statistics_str)

"""
Results for 1 million runnings of every game:
{
  "1": {
    "max": 1,
    "avg": 1.0
  },
  "2": {
    "max": 2,
    "avg": 1.49909
  },
  "3": {
    "max": 2,
    "avg": 1.666525
  },
  "4": {
    "max": 4,
    "avg": 2.43687
  },
  "5": {
    "max": 6,
    "avg": 3.548579
  },
  "6": {
    "max": 8,
    "avg": 4.357455
  },
  "7": {
    "max": 10,
    "avg": 5.52347
  },
  "8": {
    "max": 12,
    "avg": 6.335543
  },
  "9": {
    "max": 14,
    "avg": 7.51427
  },
  "10": {
    "max": 16,
    "avg": 8.324622
  },
  "11": {
    "max": 18,
    "avg": 9.501123
  },
  "12": {
    "max": 20,
    "avg": 10.335968
  },
  "13": {
    "max": 22,
    "avg": 11.495473
  },
  "14": {
    "max": 24,
    "avg": 12.332512
  },
  "15": {
    "max": 26,
    "avg": 13.481789
  },
  "16": {
    "max": 28,
    "avg": 14.33746
  },
  "17": {
    "max": 30,
    "avg": 15.491617
  },
  "18": {
    "max": 32,
    "avg": 16.334594
  },
  "19": {
    "max": 34,
    "avg": 17.498934
  }
}
"""



