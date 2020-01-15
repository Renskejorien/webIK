import requests
import random


URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
data = requests.get(URL).json()

getal = random.randrange(2, 6)

q_a = []
q_a.append(data["results"][0]["question"])
# q_a.append(data["results"][0]["correct_answer"])

for i in range(2, 6):

    if i < getal:
        q_a.append(data["results"][0]["incorrect_answers"][i - 2])
                        
    elif i > getal:
        q_a.append(data["results"][0]["incorrect_answers"][i - 3])
                        
    else:
        q_a.append(data["results"][0]["correct_answer"])

your_answer = request.form.get("username")




# if your_answer == data["results"][0]["correct_answer"]:
#     return True
# else:
#     return False

print(q_a)