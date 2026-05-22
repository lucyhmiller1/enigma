class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard
        self.initial_rotor_positions = [rotor.position for rotor in rotors]  # Save initial positions

    def encrypt(self, message):
        # Remove spaces from the input message
        message = message.replace(" ", "")
        encrypted_message = ""
        
        for char in message:
            char = self.plugboard.swap(char)
            for rotor in self.rotors:
                char = rotor.forward(char)
            char = self.reflector.reflect(char)
            for rotor in reversed(self.rotors):
                char = rotor.backward(char)
            char = self.plugboard.swap(char)
            encrypted_message += char
            self.rotate_rotors()
        
        # Add a space every five letters in the output
        formatted_message = " ".join(
            encrypted_message[i:i+5] for i in range(0, len(encrypted_message), 5)
        )
        return formatted_message

    def rotate_rotors(self):
        for rotor in self.rotors:
            if not rotor.rotate():
                break

    def reset_rotors(self):
        """Reset all rotors to their initial positions."""
        for rotor, initial_position in zip(self.rotors, self.initial_rotor_positions):
            rotor.position = initial_position
class Rotor:
    def __init__(self, wiring, notch, position=0):
        self.wiring = wiring
        self.notch = notch
        self.position = position  # Current position of the rotor

    def forward(self, char):
        index = (ord(char) - ord('A') + self.position) % 26
        return self.wiring[index]

    def backward(self, char):
        index = self.wiring.index(char)
        return chr((index - self.position) % 26 + ord('A'))

    def rotate(self):
        """Rotate the rotor by one position."""
        self.position = (self.position + 1) % len(self.wiring)
        return self.position == self.notch
class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        index = ord(char) - ord('A')
        return self.wiring[index]

class Plugboard:
    def __init__(self, swaps):
        self.swaps = swaps

    def swap(self, char):
        return self.swaps.get(char, char)
    

if __name__ == "__main__":
    rotors = [
        Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 17),
        Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 5),
        Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 22)
    ]
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})  # Example swaps

    enigma = EnigmaMachine(rotors, reflector, plugboard)

    while True:
        message = input("Enter a message (A-Z) or 'exit' to quit: ").upper()
        if message == "EXIT":
            break
        print("Encrypted letter:", enigma.encrypt(message))
