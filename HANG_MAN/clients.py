from tkinter import *
from tkinter import messagebox, simpledialog
import socket

# Connect to the server
c = socket.socket()
port = 12000
c.connect(("localhost", port))

# Global variables
selected_word = ""
correct_guesses = []
wrong_guesses = 0
wins = 0
losses = 0
buttons = []
dash_labels = []

# Function to reset the game
def reset_game():
    global selected_word, correct_guesses, wrong_guesses
    c.send("req".encode())
    selected_word = c.recv(1024).decode()
    correct_guesses = ['_'] * len(selected_word)
    wrong_guesses = 0

    # Reset hangman image
    hangman_label.config(image=hangman_images[0])

    # Remove old letter buttons
    for btn in buttons:
        btn.destroy()
    buttons.clear()

    # Create new letter buttons
    create_letter_buttons()
    update_display()

# Function to check guessed letter
def check(letter, button):
    global wrong_guesses, correct_guesses
    button.destroy()  # Destroy the button after being clicked
    c.send("guess".encode())  # Notify server to check the guess
    c.send(letter.encode())  # Send guessed letter
    response = c.recv(1024).decode()

    if response == 'correct':
        for i in range(len(selected_word)):
            if selected_word[i] == letter:
                correct_guesses[i] = letter.upper()
        update_display()
        if "_" not in correct_guesses:
            global wins
            wins += 1
            update_score_display()
            end_game("Congratulations! You won!")
    else:
        global wrong_guesses
        wrong_guesses += 1
        update_hangman_image()
        if wrong_guesses == 7:
            global losses
            losses += 1
            update_score_display()
            end_game(f"Game Over! The word was: {selected_word}")

# Function to update the hangman image based on wrong guesses
def update_hangman_image():
    hangman_label.config(image=hangman_images[wrong_guesses])

# Function to update the display for the current word
def update_display():
    for i in dash_labels:
        i.destroy()
    dash_labels.clear()
    x = screen_width // 2 - len(selected_word) * 30
    for i in range(len(selected_word)):
        x += 60
        dash = Label(root, text=correct_guesses[i], bg="#E7FFFF", font=("arial", 40))
        dash.place(x=x, y=450)
        dash_labels.append(dash)

# Function to create letter buttons
def create_letter_buttons():
    button_x = screen_width // 2 - 600  # Adjusted starting X position for the buttons
    button_y = 600  # Starting Y position for the buttons

    h_spacing = 100  # Horizontal space between buttons
    v_spacing = 100  # Vertical space between rows of buttons

    for i, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
        btn = Button(root, image=letter_images[letter], bd=0)
        btn.place(x=button_x + (i % 13) * h_spacing, y=button_y + (i // 13) * v_spacing)
        
        # Pass both the letter and the button reference to check
        btn.config(command=lambda ch=letter, button=btn: check(ch, button))
        buttons.append(btn)  # Store the button reference in a list


# Function to end the game
def end_game(message):
    result = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
    if result:
        reset_game()  # Restart the game
    else:
        close()  # Show scores before closing

# Exit button functionality
def close():
    c.send("exit".encode())  # Notify server before closing
    root.destroy()

# Function to update the score display
def update_score_display():
    wins_label.config(text=f"Wins: {wins}")
    losses_label.config(text=f"Losses: {losses}")

# Guess word function
def guess_word():
    global wins, losses
    word_guess = simpledialog.askstring("Guess the Word", "Enter your guess:").lower()  # Ask user for word guess
    if word_guess == selected_word:
        wins += 1
        update_score_display()
        answer = messagebox.askyesno('GAME OVER', 'YOU GUESSED THE WORD! YOU WON!\nWANT TO PLAY AGAIN?')
        if answer:
            reset_game()
        else:
            close()
    else:
        losses += 1
        update_score_display()
        answer = messagebox.askyesno('GAME OVER', f'WRONG GUESS! THE WORD: {selected_word.upper()}\nYOU LOST!\nWANT TO PLAY AGAIN?')
        if answer:
            reset_game()
        else:
            close()

# Create main window
root = Tk()
root.title('HANG MAN')
root.config(bg='#E7FFFF')
root.geometry('800x800')  # Adjust the window size as needed
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load hangman images (from h1.png to h8.png)
hangman_images = [PhotoImage(file=f'h{i}.png') for i in range(1, 9)]

# Place the first image (empty gallows)
hangman_label = Label(root, bg='#E7FFFF', image=hangman_images[0])
hangman_label.place(x=screen_width // 2 - 50, y=100)

# Initialize a list to store button references
buttons = []

# Load images for letters (assuming a.png, b.png, ..., z.png are available)
letter_images = {}
for letter in 'abcdefghijklmnopqrstuvwxyz':
    letter_images[letter] = PhotoImage(file=f'{letter}.png')

# Create score labels
wins_label = Label(root, text=f"Wins: {wins}", bg="#E7FFFF", font=("arial", 20))
wins_label.place(x=20, y=20)

losses_label = Label(root, text=f"Losses: {losses}", bg="#E7FFFF", font=("arial", 20))
losses_label.place(x=20, y=60)

# Create exit button
e1 = PhotoImage(file='exit.png')
ex = Button(root, bd=0, command=close, bg="#E7FFFF", activebackground="#E7FFFF", font=10, image=e1)
ex.place(x=screen_width - 130, y=10)

# Add 'Guess Word' button below letter buttons
guess_btn = Button(root, text="Guess Word", font=("arial", 20), command=guess_word, bg="#E7FFFF", activebackground="#E7FFFF")
guess_btn.place(x=screen_width - 195, y=90)  # Adjust y position for visibility

# Start the game
reset_game()

# Run the Tkinter event loop
root.mainloop()
