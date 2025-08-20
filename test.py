

weeks_in_year = 52

def life_in_weeks(age):
    print(f"you are {age} years old")
    remaining_years = 90 - (age)
    weeks_left = remaining_years * 52
    print(f"you have {weeks_left} weeks to live")
    


life_in_weeks(34)

def greet(name, location):
    print(f"hello I'm {name}! I'm from {location}")

greet(location="Key West", name="Cloud")
    

def calculate_love_score(name1, name2):
    combined_names = (name1 + name2).lower()

    count = 0
    for letter in "true":
        count += combined_names.count(letter)

    love_count = 0
    for letter in "love":
        love_count += combined_names.count(letter)

    love_score = int(str(count) + str(love_count))
    print(f"Your love score is {love_score}")

calculate_love_score("cloud strife", "aerith gainsborough")