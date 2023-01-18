# CASK
CASK is a cipher Algorithm, not based on a single key/password but multiple security features, each of which is independent and must be correct to decipher the message

Only main.py file is essential.
Python libraries required: tkinter, customtkinter, random

To cipher/decipher,
1. Select keys (You can select upto 4)
2. Enter 4 digit pin
3. Enter password 0-25 characters, characters after the 25th character will be truncated.
4. Enter the code/message and press decode/encode

Notes:
1. Any newline character added in the "Enter Message" textbox in cipher window will be ommited, and the message recovered after decoding the cipher will be in a single line
2. Default settings (all keys set to key 1, pin set to 0000, password set to empty string) can be used to encode message quickly.
