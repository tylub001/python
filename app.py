from flask import Flask, render_template, request, session, redirect
import random
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

@app.route("/")
def homepage():
    return render_template("index.html")


# Tip Calculator Logic
@app.route('/homepage')
def home():
    return render_template('homepage.html')  # Portfolio homepage

@app.route('/tip', methods=['GET', 'POST'])
def tip_calculator():
    final_amount = None
    if request.method == 'POST':
        bill = float(request.form['bill'])
        tip = int(request.form['tip'])
        people = int(request.form['people'])

        tip_as_percent = tip / 100
        total_tip_amount = bill * tip_as_percent
        total_bill = bill + total_tip_amount
        bill_per_person = total_bill / people
        final_amount = round(bill_per_person, 2)

    return render_template('tip_calculator.html', final_amount=final_amount)

# Binary Converter Logic
def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)
 
@app.route('/bin', methods=['GET', 'POST'])
def convert_binary():
    binary_result = None
    if request.method == 'POST':
        sentence = request.form['sentence']
        binary_result = text_to_binary(sentence)
    return render_template('convert_binary.html', binary_result=binary_result)


# Check even or odd Logic
@app.route('/even-odd', methods=['GET', 'POST'])
def even_or_odd():
    result = None
    if request.method == 'POST':
        try:
            number = int(request.form['number'])  
            result = f"{number} is even" if number % 2 == 0 else f"{number} is odd"
        except ValueError:
            result = "Please enter a valid number."
    return render_template('even_or_odd.html', result=result)

# BMI caluclator
@app.route('/bmi', methods=['GET', 'POST'])
def bmi_calculator():
    bmi_result = None
    if request.method == 'POST':
        try:
            weight_pounds = float(request.form['weight'])
            feet = int(request.form['feet'])
            inches = int(request.form['inches'])

            total_inches = (feet * 12) + inches
            height_meters = total_inches * 0.0254
            weight_kg = weight_pounds * 0.453592

            if height_meters <= 0:
                bmi_result = "Height must be greater than zero."
            else:
                bmi = weight_kg / (height_meters ** 2)
                bmi = round(bmi, 2)

                if bmi < 18.5:
                    interpretation = "underweight"
                elif 18.5 <= bmi < 25:
                    interpretation = "normal weight"
                else:
                    interpretation = "overweight"

                bmi_result = f"Your BMI is {bmi}. You are {interpretation}."
        except ValueError:
            bmi_result = "Please enter valid numbers."

    return render_template('bmi_calculator.html', bmi_result=bmi_result)


@app.route('/pizza', methods=['GET', 'POST'])
def pizza_order():
    total = None
    if request.method == 'POST':
        size = request.form['size']
        pepperoni = request.form['pepperoni']
        cheese = request.form['cheese']

        # Base price
        if size == "S":
            total = 10
        elif size == "M":
            total = 14
        elif size == "L":
            total = 18

        # Pepperoni
        if pepperoni == "Y":
            total += 3 if size == "S" else 5

        # Cheese
        if cheese == "Y":
            total += 1

    return render_template('order_pizza.html', total=total)

@app.route("/quest")
def orb_quest_js():
    return render_template("orb_quest.html")

elements = ["rock", "paper", "scissors"]

@app.route("/game", methods=["GET", "POST"])
def index():
    result = ""
    computer_choice = ""
    user_choice = ""
    ascii_art = {
    "rock": """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
    "paper": """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",
    "scissors": """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
}
    
    if request.method == "POST":
        user_choice = request.form["element"]
        computer_choice = random.choice(elements)

        if user_choice == computer_choice:
            result = "It's a draw!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"

    return render_template("rock_paper_scissors.html", result=result, computer=computer_choice, user=user_choice, computer_art=ascii_art.get(computer_choice, ""), user_art=ascii_art.get(user_choice, ""))

@app.route("/password", methods=["GET", "POST"])
def generate_password():
    password = ""
    if request.method == "POST":
        input_word = request.form["input_word"]
        pool = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+")

        transformed = "".join(random.choice(pool) for _ in input_word)

        # Add 3 random characters to the beginning and end
        prefix = "".join(random.choice(pool) for _ in range(3))
        suffix = "".join(random.choice(pool) for _ in range(3))

        password = prefix + transformed + suffix

    return render_template("password_gen.html", password=password)

@app.route("/pong")
def pong():
    return render_template("pong.html")

@app.route("/hangman", methods=["GET", "POST"])

def hangman_game():
    if "word" not in session:
        word_list = ["python", "flask", "hangman", "developer"]
        session["word"] = random.choice(word_list)
        session["display"] = ["_"] * len(session["word"])
        session["wrong_guesses"] = []
        session["lives"] = 6

    message = ""
    if request.method == "POST":
        guess = request.form["guess"].lower()
        if guess in session["word"]:
            updated_display = session["display"]
            for i, letter in enumerate(session["word"]):
                if letter == guess:
                    updated_display[i] = guess
            session["display"] = updated_display
        else:
            if guess not in session["wrong_guesses"]:
                session["wrong_guesses"].append(guess)
                session["lives"] -= 1

        if "_" not in session["display"]:
            message = "🎉 You win!"
        elif session["lives"] == 0:
            message = f"💀 Game over! The word was '{session['word']}'"
            session["game_over"] = True

    hangman_stages = [
        """\n +---+\n |   |\n     |\n     |\n     |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n     |\n     |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n |   |\n     |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n/|   |\n     |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n/|\\  |\n     |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n/|\\  |\n/    |\n     |\n=========""",
        """\n +---+\n |   |\n O   |\n/|\\  |\n/ \\  |\n     |\n========="""
    ]
    ascii = hangman_stages[6 - session.get("lives", 6)]

    return render_template("hangman.html",
                           display=" ".join(session.get("display", [])),
                           ascii=ascii,
                           wrong_guesses=", ".join(session.get("wrong_guesses", [])),
                           message=message)
@app.route("/restart")
def restart_game():
    session.clear()
    return redirect("/hangman")

if __name__ == '__main__':
    app.run(debug=True)
