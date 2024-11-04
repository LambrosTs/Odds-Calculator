import random
import tkinter as tk
from treys import Evaluator, Card

# Define ranks and suits
RANKS = "23456789TJQKA"
SUITS = "shdc"
SYMBOLS = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}
DECK = [rank + suit for rank in RANKS for suit in SUITS]

# Initialize evaluator
evaluator = Evaluator()

# Function to evaluate hand strength
def evaluate_hand(hand, board):
    hand_cards = [Card.new(card) for card in hand]
    board_cards = [Card.new(card) for card in board]
    return evaluator.evaluate(board_cards, hand_cards)

# Function to calculate winning probability
def simulate_win_probability(my_hand, community_cards, simulations=1000):
    wins = 0
    ties = 0
    losses = 0
    
    remaining_deck = [card for card in DECK if card not in my_hand + community_cards]
    
    for _ in range(simulations):
        opponent_hand = random.sample(remaining_deck, 2)
        opponent_score = evaluate_hand(opponent_hand, community_cards)
        my_score = evaluate_hand(my_hand, community_cards)
        
        if my_score < opponent_score:
            wins += 1
        elif my_score > opponent_score:
            losses += 1
        else:
            ties += 1
    
    win_rate = wins / simulations
    tie_rate = ties / simulations
    loss_rate = losses / simulations
    return win_rate, tie_rate, loss_rate

# Function to convert a card like "As" to "A♠" for display
def display_card(card):
    rank, suit = card[0], card[1]
    return f"{rank}{SYMBOLS[suit]}"

class PokerCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Texas Hold'em Odds Calculator")

        self.my_hand = []
        self.community_cards = []
        self.available_cards = DECK[:]
        
        # Display for selected cards and odds
        self.hand_label = tk.Label(root, text="Your Hand: ")
        self.hand_label.grid(row=0, column=0, columnspan=5, sticky="w")
        
        self.community_label = tk.Label(root, text="Community Cards: ")
        self.community_label.grid(row=1, column=0, columnspan=5, sticky="w")
        
        self.odds_label = tk.Label(root, text="Odds: ")
        self.odds_label.grid(row=2, column=0, columnspan=5, sticky="w")
        
        # Card buttons with symbols
        self.card_buttons = {}
        for i, card in enumerate(self.available_cards):
            btn_text = display_card(card)
            btn = tk.Button(root, text=btn_text, width=5, command=lambda c=card: self.select_card(c))
            btn.grid(row=3 + i // 13, column=i % 13)  # Arrange in rows of 13 cards
            self.card_buttons[card] = btn

        # Control buttons
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_selections, fg="red")
        self.clear_button.grid(row=7, column=0, columnspan=3, sticky="we")
        
        self.undo_button = tk.Button(root, text="Undo", command=self.undo_selection, fg="blue")
        self.undo_button.grid(row=7, column=3, columnspan=3, sticky="we")

    def select_card(self, card):
        # Determine if we are still selecting hand or community cards
        if len(self.my_hand) < 2:
            self.my_hand.append(card)
        elif len(self.community_cards) < 5:
            self.community_cards.append(card)
        
        # Disable selected card button
        self.card_buttons[card].config(state="disabled")
        
        # Update display
        self.update_display()
        
        # Calculate odds after each stage
        if len(self.my_hand) == 2 and len(self.community_cards) >= 3:
            self.calculate_odds()

    def calculate_odds(self):
        win_rate, tie_rate, loss_rate = simulate_win_probability(self.my_hand, self.community_cards, simulations=1000)
        
        self.odds_label.config(text=(
            f"Winning odds: {win_rate * 100:.2f}%\n"
            f"Tie odds: {tie_rate * 100:.2f}%\n"
            f"Losing odds: {loss_rate * 100:.2f}%"
        ))

    def update_display(self):
        # Update hand and community card display with symbols
        hand_display = " ".join(display_card(card) for card in self.my_hand)
        community_display = " ".join(display_card(card) for card in self.community_cards)
        
        self.hand_label.config(text=f"Your Hand: {hand_display}")
        self.community_label.config(text=f"Community Cards: {community_display}")

    def clear_selections(self):
        # Reset all selections
        self.my_hand = []
        self.community_cards = []
        
        # Enable all card buttons again
        for btn in self.card_buttons.values():
            btn.config(state="normal")
        
        # Clear display
        self.update_display()
        self.odds_label.config(text="Odds: ")

    def undo_selection(self):
        # Undo the last card selection
        if self.community_cards:
            last_card = self.community_cards.pop()
        elif self.my_hand:
            last_card = self.my_hand.pop()
        else:
            return  # Nothing to undo
        
        # Re-enable the last selected card
        self.card_buttons[last_card].config(state="normal")
        
        # Update display and odds
        self.update_display()
        if len(self.my_hand) == 2 and len(self.community_cards) >= 3:
            self.calculate_odds()
        else:
            self.odds_label.config(text="Odds: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerCalculatorApp(root)
    root.mainloop()
