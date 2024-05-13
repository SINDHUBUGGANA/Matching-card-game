#AAI - 500 FINAL PROJECT
#Name: SINDHU BUGGANA
#CWID: 20020990

""" 
****RULES****
* The simple card game (Match the card) is played between two players.
* The objective is to match as many pairs of cards as possible within 20 turns.
* Players take turns drawing a card from the deck.
* If a player draws a card that matches a card in their opponent's hand, the opponent scores a point, and the matched card is removed from OPPONENT hand.
    But the players card still remains in the game.
* If a player draws a card that they already have in their hand, no points are awarded.
* The player with the highest score at the end of the game wins.
* If both players have the same score, the game is a tie.
* The scoring is based on the number of matched pairs, not the rank or suit of the cards.
* Players are informed about the current score and the drawn card at the beginning of each turn.
******ADDITIONAL FEATURES:*******
* difficulty level added
* We have 2 Jocker cards. The 2 Joker cards do not belong to any suit and are considered wild cards that can match any other card.
* If a player draws a Joker card, they can choose to match any card from their opponent's hand.
==>Card Tricks or Special Moves:    ( rare occurance as game has only 20 turns )
* Introduce special card combinations or sequences that trigger unique actions or bonuses. For example, if a player matches three or more cards of the same rank, they could earn an extra turn or a chance to swap cards with their opponent.
"""

#CODE: 
import random #library import

# Card class
class Card:
    # Dictionaries to map suit names and rank names to numerical values
    suit_values = {"Spades": 3, "Hearts": 2, "Diamonds": 1, "Clubs": 0}
    rank_values = {"Ace": 14, "King": 13, "Queen": 12, "Jack": 11, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "Joker": 15}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.suit_value = Card.suit_values.get(suit, None)  # Get the numerical value for the suit
        self.rank_value = Card.rank_values[rank]  # Get the numerical value for the rank

    def __str__(self):
        if self.rank == "Joker":
            return "Joker"
        return f"{self.rank} of {self.suit}"
    #returns a string representation of the card

    def __eq__(self, other):
        return self.rank_value == other.rank_value
    #compares the rank values of two cards for equality

# Deck class
class Deck:
    def __init__(self, num_jokers=2):
        # Create a list of cards excluding Jokers
        self.cards = [Card(suit, rank) for suit in Card.suit_values for rank in Card.rank_values if rank != "Joker"]
        self.cards.extend([Card(None, "Joker") for _ in range(num_jokers)])

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
    #removes and returns the last card from the deck.

# Hand class (inheritance from Deck)
class Hand(Deck):
    def __init__(self, name=""):
        self.cards = [] #empty list
        self.name = name

    def add_card(self, card):
        self.cards.append(card)
        #adds a card to the hand

    def __str__(self):
        if not self.cards:
            return f"Hand {self.name} is empty"
        hand_str = f"Hand {self.name} contains\n"
        for card in self.cards:
            hand_str += f"{' ' * (len(str(card)) - 1)}{card}\n"
        return hand_str

# Card game class(base)
class CardGame:
    def __init__(self):
        self.deck = Deck() #creates a Deck object and shuffles it.
        self.deck.shuffle()

# Match Cards game class
class MatchCardsGame(CardGame):
    """
    The game of Match Cards is played by two players.
    The goal is to match as many pairs of cards as possible within 20 turns.
    Players take turns drawing a card from the deck. If the first player has a matching card, the second player scores a point.
    IF PLAYER 1 DRAWS THE MATCHING CARD FROM THIS OWN CARDS THEN NO POINTS GIVEN.
    The game ends after 20 turns, and the player with the highest score wins.
    """
    DIFFICULTY_SETTINGS = {
        "easy": {"turns": 40, "jokers": 2, "scoring": "normal"},
        "medium": {"turns": 30, "jokers": 1, "scoring": "normal"},
        "hard": {"turns": 20, "jokers": 0, "scoring": "rank_based"}
    }

    def __init__(self, player1_name, player2_name, difficulty="easy"):
        super().__init__() #calls the constructor of the parent class (CardGame) to initialize any necessary attributes or set up the game
        self.player1_hand = OldMaidHand(player1_name)
        self.player2_hand = OldMaidHand(player2_name)
        self.difficulty = difficulty
        settings = MatchCardsGame.DIFFICULTY_SETTINGS[difficulty]
        self.turns = settings["turns"]
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = 1

        self.deck = Deck(settings["jokers"])
        self.deck.shuffle()

    def play_game(self): # actual game loop
        tracker = CardValueTracker(self.deck)  # tracker within the method

        for _ in range(self.turns):
            if self.current_player == 1:
                card = self.deck.deal()
                self.player1_hand.add_card(card)
                tracker.track_card_values(card)  # Track the dealt card
                print(f"Turn: {21 - self.turns}")
                print(f"{self.player1_hand.name}'s turn")
                print(f"Drew: {card}")

                if card.rank == "Joker":
                    self.handle_joker(card, self.player1_hand, self.player2_hand)
                elif card in self.player2_hand.cards:
                    print(f"{self.player2_hand.name} scored a point!")
                    self.player2_score += 1
                    self.player2_hand.cards.remove(card)
                matched_cards = [card for card in self.player1_hand.cards if card in self.player2_hand.cards]
                special_moves = self.check_special_moves(self.player1_hand, self.player2_hand, matched_cards)
                self.perform_special_moves(special_moves, self.player1_hand, self.player2_hand)
                if self.difficulty == "hard":
                    self.score_based_on_rank(self.player1_hand, self.player2_hand, card)
                else:
                    self.score_normal(self.player1_hand, self.player2_hand, card)

            else:
                card = self.deck.deal()
                self.player2_hand.add_card(card)
                tracker.track_card_values(card)  # Track the dealt card
                print(f"Turn: {21 - self.turns}")
                print(f"{self.player2_hand.name}'s turn")
                print(f"Drew: {card}")

                if card.rank == "Joker":
                    self.handle_joker(card, self.player2_hand, self.player1_hand)
                elif card in self.player1_hand.cards:
                    print(f"{self.player1_hand.name} scored a point!")
                    self.player1_score += 1
                    self.player1_hand.cards.remove(card)
                matched_cards = [card for card in self.player2_hand.cards if card in self.player1_hand.cards]
                special_moves = self.check_special_moves(self.player2_hand, self.player1_hand, matched_cards)
                self.perform_special_moves(special_moves, self.player2_hand, self.player1_hand)
                if self.difficulty == "hard":
                    self.score_based_on_rank(self.player2_hand, self.player1_hand, card)
                else:
                    self.score_normal(self.player2_hand, self.player1_hand, card)

            self.current_player = 3 - self.current_player  # Switch player for the next turn
            print(f"Score: {self.player1_hand.name} {self.player1_score} - {self.player2_hand.name} {self.player2_score}\n")
            self.turns -= 1

        print("Game over!")
        if self.player1_score > self.player2_score:
            print(f"{self.player1_hand.name} wins with a score of {self.player1_score}!")
        elif self.player2_score > self.player1_score:
            print(f"{self.player2_hand.name} wins with a score of {self.player2_score}!")
        else:
            print("It's a tie!")


#Aditional feature added was joker card as wild entry and card trick (10 marks)


    def handle_joker(self, joker_card, current_hand, opponent_hand):
        """
        Handles the case when a player draws a Joker card.
        Allows the player to match any card from the opponent's hand.
        """
        print(f"{current_hand.name} drew a Joker and can match any card from {opponent_hand.name}'s hand.")
        opponent_cards = [str(card) for card in opponent_hand.cards]
        print("Opponent's cards:", ", ".join(opponent_cards))
        card_to_match = input(f"Enter the card you want to match (or 'skip' to skip): ")

        if card_to_match.lower() == "skip":
            return

        matched_card = None
        for card in opponent_hand.cards:
            if str(card) == card_to_match:
                matched_card = card
                break

        if matched_card:
            print(f"{current_hand.name} matched {matched_card} with the Joker!")
            opponent_hand.cards.remove(matched_card)
            if current_hand == self.player1_hand:
                self.player1_score += 1
            else:
                self.player2_score += 1
        else:
            print(f"Invalid card entered. {current_hand.name} skipped this turn.")


    def check_special_moves(self, player_hand, opponent_hand, matched_cards):
        """
        Check for special moves based on the matched cards.
        Returns a list of special move actions to be performed.
        """
        special_moves = []
        matched_ranks = [card.rank for card in matched_cards]

        # Check for three or more cards of the same rank
        rank_counts = {rank: matched_ranks.count(rank) for rank in set(matched_ranks)}
        for rank, count in rank_counts.items():
            if count >= 3:
                special_moves.append(("extra_turn", player_hand.name))
                break

        # Check for a specific combination (e.g., three Kings)
        if set(matched_ranks) == set(["King"]):
            special_moves.append(("swap_cards", player_hand.name, opponent_hand.name))

        return special_moves

    def perform_special_moves(self, special_moves, player_hand, opponent_hand):
        """
        Perform the special moves based on the list of actions.
        """
        for move in special_moves:
            if move[0] == "extra_turn":
                print(f"{move[1]} earned an extra turn!")
                self.turns += 1
            elif move[0] == "swap_cards":
                print(f"{move[1]} and {move[2]} swapped cards!")
                player_hand.cards, opponent_hand.cards = opponent_hand.cards, player_hand.cards


    def score_normal(self, current_hand, opponent_hand, card):
        if card in opponent_hand.cards:
            print(f"{opponent_hand.name} scored a point!")
            if current_hand == self.player1_hand:
                self.player2_score += 1
            else:
                self.player1_score += 1
            opponent_hand.cards.remove(card)

    def score_based_on_rank(self, current_hand, opponent_hand, card):
        if card in opponent_hand.cards:
            rank_score = card.rank_value
            print(f"{opponent_hand.name} scored {rank_score} points!")
            if current_hand == self.player1_hand:
                self.player2_score += rank_score
            else:
                self.player1_score += rank_score
            opponent_hand.cards.remove(card)


# Old Maid Hand class (from youtube)
class OldMaidHand(Hand):
    def remove_matches(self):
        """
        Removes matched pairs of cards from the hand.
        Returns the number of pairs removed.
        """
        count = 0
        original_cards = self.cards[:]
        for card in original_cards:
            match = Card(card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                count += 1
        return count

class CardValueTracker:
    """
    Tracks the count of each rank value in the deck.
    """
    def __init__(self, deck):
        self.deck = deck
        self.card_values = {}
        self.initialize_card_values()

    def initialize_card_values(self):
        """
        Initializes the card_values dictionary with all rank values
        and sets their count to 0.
        """
        for card in self.deck.cards:
            rank_value = card.rank_value
            if rank_value not in self.card_values:
                self.card_values[rank_value] = 0
    
    def track_card_values(self, card):
        """
        Increments the count for the given card's rank value
        in the card_values dictionary.

        Args:
        card (Card): The card object whose rank value will be tracked.
        """
        rank_value = card.rank_value
        self.card_values[rank_value] += 1

    def get_card_value_counts(self):
        """
        Returns the card_values dictionary containing the count
        for each rank value.

        Returns:
        dict: A dictionary where the keys are rank values,
              and the values are the counts of those ranks.
        """
        return self.card_values
    
    
# Example  
difficulty_level = input("Enter difficulty level (easy, medium, hard): ")
player1_name = input("Enter Player 1's name: ")
player2_name = input("Enter Player 2's name: ")
game = MatchCardsGame(player1_name, player2_name, difficulty=difficulty_level)
game.play_game()