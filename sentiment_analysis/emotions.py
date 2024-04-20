import json
def add_element_to_file(filepath, company, emotion_value):
    # define the JSON data to append

    # open the JSON file for appending

    with open(filepath, "w") as f:
        # write the updated JSON data back to the file1
        json_data = {
            "company": company,
            "emotion": emotion_value
        }

        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()


def load_emotions(filepath, company):
    with open(filepath, "r") as f:
        # read the JSON data
        json_data = json.load(f)

    # get a specific element from the JSON data

    return json_data["emotion"]
