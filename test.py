import requests
import random


URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
data = requests.get(URL).json()

getal = random.randrange(2, 6)

q_a = []
q_a.append(data["results"][0]["question"])
correct_answer = data["results"][0]["correct_answer"]

answer_converter = {1:'A', 2:'B', 3:'C', 4:'D'}

for i in range(2, 6):
    if i < getal:
        q_a.append(data["results"][0]["incorrect_answers"][i - 2])

    elif i > getal:
        q_a.append(data["results"][0]["incorrect_answers"][i - 3])

    else:
        q_a.append(data["results"][0]["correct_answer"])
        kaas = answer_converter[i - 1]

print(kaas)


# @app.route("/questions", methods=["GET", "POST"])
# # @login_required
# def question():
#     """Handles a new question"""
#     # Get the questions and answer(s) from API
#     URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
#     data = requests.get(URL).json()
    
#     # Choose the place for the right answer
#     getal = random.randrange(2, 6)
    
#     # Create list with the question[0], and 4 possible answers in random order
#     q_a = []
#     q_a.append(data["results"][0]["question"])
    
#     # To make sure the right letter (for the right answer) is saved
#     answer_converter = {1:'A', 2:'B', 3:'C', 4:'D'}

#     # Makes a list with 3 wrong answers and a good answer in a random order
#     for i in range(2, 6):
#         if i < getal:
#             q_a.append(data["results"][0]["incorrect_answers"][i - 2])

#         elif i > getal:
#             q_a.append(data["results"][0]["incorrect_answers"][i - 3])

#         else:
#             q_a.append(data["results"][0]["correct_answer"])
#             # Saves right answer (A, B, C or D) in the session
#             session["correct_answer"] = answer_converter[i - 1]

#     return render_template("questions.html", data=q_a)

# @app.route("/answer_check", methods=["GET"])
# def answer_check():
#     """Checks if question is answered correctly"""
#     # return jsonify(session["correct_answer"] != request.form.get('your_answer'))
#     if session["correct_answer"] == request.form.get('your_answer'):
#         return jsonify(True)
#     else:
#         return jsonify(False)