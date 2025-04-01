from api_key import API_KEY  # Import API key from external file
from groq import Groq

# Initialize Groq client with API key
client = Groq(api_key=API_KEY)


def getResponse(user_prompt):
    """Query the Groq model with the given user prompt."""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""

        return response_text

    except Exception as e:
        return f"Error querying the model: {e}"


def create():
    """Reads input from input.txt, generates a workout plan, and writes to output.txt."""
    with open('input.txt', 'r') as f:
        my_dict = {key: value for line in f for key, value in [line.strip().split(': ')]}

    print(my_dict)

    user_prompt = (
        f"Can you generate a {my_dict['days_per_week']}-day workout plan for someone whose weight is "
        f"{my_dict['weight']} kg, height is {my_dict['height']} cm, and their goal is {my_dict['workout_type']}. "
        f"They are at a {my_dict['location']} and have {my_dict['experience']} level experience. "
        f"They can only do the following exercises: jumping jacks, squat, situp, pushups. "
        f"They have 1 hour per day to work out. Please specify the days of the week by name. "
        f"At the end, provide guidance on what types of food to eat and what to avoid. "
        f"Limit your response to a few lines and make it visually appealing."
    )

    workout_suggestion = getResponse(user_prompt)
    print(workout_suggestion)

    with open("output.txt", "w") as f:
        f.write(workout_suggestion)

