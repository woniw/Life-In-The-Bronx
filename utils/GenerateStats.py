import random 

def generateClass():
    classes = ["Fighter", "Tank", "Fatty"]
    class_generator = random.choices(classes)

    return class_generator

def generateHandedness():
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

    return handedness_generator