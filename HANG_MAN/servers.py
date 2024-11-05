import socket
import threading
import random

# Load words from file
def load_words():
    try:
        with open('words.txt', 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print("Error: words.txt file not found.")
        return []

words_list = load_words()

# Function to select a new word
def select_word():
    return random.choice(words_list) if words_list else ""

# Function to handle each client
def handle_client(c, addr):
    print(f"Got connection from {addr}")
    selected_word = ""
    correct_guesses = ['_']
    wrong_guesses = 0

    while True:
        try:
            msg = c.recv(1024).decode()  # Receive message from client
            if not msg:  # Check if the client has closed the connection
                print(f"Connection closed by {addr}")
                break
            
            if msg == 'req':  # If the client requests a new word
                selected_word = select_word()
                c.send(bytes(selected_word, "utf-8"))  # Send the selected word
            elif msg == 'guess':
                letter = c.recv(1024).decode()  # Receive guessed letter
                if letter in selected_word:
                    c.send(b'correct')
                else:
                    wrong_guesses += 1
                    c.send(b'incorrect')
                if wrong_guesses == 7:  # Max wrong guesses
                    c.send(bytes(f'lose,{selected_word}', "utf-8"))
                elif "_" not in correct_guesses:  # Player won
                    c.send(b'win')
            elif msg == 'exit':  # If the client requests to close the connection
                print("Closing connection as requested by client.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    
    c.close()

# Server setup
s = socket.socket()
port = 12000
s.bind(("localhost", port))
s.listen(3)  # Listen for up to 3 connections
print("Server listening on port", port)

while True:
    c, addr = s.accept()
    threading.Thread(target=handle_client, args=(c, addr)).start()  # Handle each client in a new thread
