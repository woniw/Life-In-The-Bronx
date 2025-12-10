import random 

def generatedClass():
    low = 1
    high = 3
    class_choice = random.randint(low, high)

    if class_choice == 1:
        return "Fighter"
    elif class_choice == 2:
        return "Tank"
    elif class_choice == 3:
        return "Fatty"

def generatedHandedness():
    handedness = {
        "right": 100,
        "left": 40,
        "ambidextrous": 10
    }

    handedness_generator = random.choices(
        population=list(handedness.keys()),
        weights=list(handedness.values()),
        
        k=1
    )[0]

    print(f"Random handedness, generated: {handedness_generator}")
    return handedness_generator