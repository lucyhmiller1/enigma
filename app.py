from flask import Flask, render_template, request, redirect, url_for
from enigma_code_r3 import EnigmaMachine, Rotor, Reflector, Plugboard

app = Flask(__name__)

# Initialize the Enigma machine components
rotors = [
    Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 17),
    Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 5),
    Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 22)
]
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})  # Example swaps

enigma = EnigmaMachine(rotors, reflector, plugboard)

# Store encrypted messages in memory (for the session)
saved_outputs = []

@app.route("/", methods=["GET", "POST"])
def index():
    global saved_outputs
    if request.method == "POST":
        if "encrypt" in request.form:
            # Encrypt the message
            message = request.form.get("message", "").upper()
            encrypted_message = enigma.encrypt(message)
            saved_outputs.append(encrypted_message)
        elif "reset" in request.form:
            # Reset the input field and rotors
            print("Resetting rotors to initial positions.")
            enigma.reset_rotors()  # Reset rotors to their starting positions
            return redirect(url_for("index"))
        elif "delete" in request.form:
            # Delete a specific output
            try:
                index = int(request.form.get("delete"))
                if 0 <= index < len(saved_outputs):
                    saved_outputs.pop(index)
            except (ValueError, IndexError):
                pass  # Ignore invalid delete requests
        elif "adjust_rotor" in request.form:
            # Adjust rotor positions
            try:
                rotor_index = int(request.form.get("rotor_index"))
                direction = request.form.get("direction")
                if 0 <= rotor_index < len(enigma.rotors):
                    rotor = enigma.rotors[rotor_index]
                    if direction == "up":
                        rotor.position = (rotor.position + 1) % len(rotor.wiring)
                    elif direction == "down":
                        rotor.position = (rotor.position - 1) % len(rotor.wiring)
            except (ValueError, IndexError):
                pass  # Ignore invalid rotor adjustment requests
    return render_template("index.html", saved_outputs=saved_outputs, enigma=enigma)

if __name__ == "__main__":
    app.run(debug=True)