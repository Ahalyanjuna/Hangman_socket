# Hangman_socket
Overview
The Hangman game is a word-guessing challenge where the player guesses letters in an attempt to reveal a hidden word before a limited number of incorrect guesses. The server manages the game’s words and logic, while the client provides the interactive interface. The game can support multiple players connecting to the server simultaneously, with each client’s game instance operating independently.

Game Description
In Hangman, players attempt to guess letters of a hidden word. Each incorrect guess brings the player closer to losing, with the hangman figure being progressively drawn. The player wins if they reveal the word before the maximum number of wrong guesses is reached, and loses if they reach the limit without fully uncovering the word. The game also includes an option for guessing the complete word at once.

Logic and Functionalities
1.	Server-Side (Python Sockets and Threading):
i)Socket Communication: The server listens for incoming connections and manages client requests through dedicated threads.
ii)Word Selection: A random word is selected from a predefined list (words.txt) for each game session.
iii)Game State Tracking: The server tracks correct and incorrect guesses, managing win/loss conditions.

2.	Client-Side (Tkinter GUI):
i)Graphical Interface: The Tkinter interface allows players to guess letters or attempt the entire word.
ii)Letter Buttons: Players select letters by clicking on buttons representing each letter of the alphabet. Correct guesses reveal parts of the word, while incorrect guesses update the hangman image.
iii)Guess Word Functionality: Players can attempt to guess the full word using an input dialog.
iv)Hangman Image Update: Each incorrect guess updates the displayed image, progressing toward the hangman’s completion.
v)Score Tracking: Wins and losses are displayed, updating based on game outcomes.
vi)Reset and Exit: A reset function restarts the game with a new word, while an exit option allows players to close the game and notify the server.

Conclusion
This Hangman game combines network programming and GUI development to create a compelling and user-friendly experience. By employing a client-server model, the game ensures efficient handling of multiple players, with each game instance managed independently. The project demonstrates the effective use of Python’s socket and threading libraries for multiplayer applications, and Tkinter for an intuitive, graphical gameplay experience.
