import openai
import os


import openai
import os

class GPT4AutoCoder:
    def __init__(self, api_key, gpt_engine_choice):
        # Set the API key for OpenAI
        openai.api_key = api_key
        self.gpt_engine_choice = gpt_engine_choice
        self.system_message = self.get_system_message()

    def get_system_message(self):
        try:
            with open("system-message.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            print("Error: 'input.txt' file not found. Using default system message.")
            return "You are a helpful python coding AI who will generate code and provide suggestions for Python projects based on the user's input or generate ideas and code if the user doesn't provide an idea. Start the code block with 'python' word."

    def ask_gpt3(self, question):
        response = openai.chat.completions.create(
            model=self.gpt_engine_choice,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": question}
            ]
        )

        # this part tries to parse the code from the response
        try:
            generated_text = response.choices[0].message.content
            print("GENERATED TEXT: " + generated_text)
            generated_text = generated_text[:generated_text.rfind('```')]
            return generated_text.split('python', 1)[1]
        except IndexError:
            for i in range(2):
                response = self.ask_gpt3(question)
                try:
                    return generated_text.split('python', 1)[1]
                except IndexError:
                    print("Error: GPT-3 failed to generate code. Please try again.")
                    pass

# if __name__ == "__main__":
#     api_key = "<your_api_key>"
#     auto_coder = GPT4AutoCoder(api_key, "text-davinci-003")  # Example engine choice
#     print(auto_coder.ask_gpt3("Write a Python script to reverse a string."))


    # this part is used to get the project idea from the user
    def get_project_idea(self, user_input):
        if user_input == "":
            return "Generate a Python project idea and provide sample code . Write the code in one code block between triple backticks."
        else:
            return f"Generate code for the Python project '{user_input}' . Write the code in one code block between triple backticks. comment the code."
  

# if __name__ == "__main__":
#     api_key = "<your_api_key>"
#     auto_coder = GPT4AutoCoder(api_key)
#     auto_coder.run()

