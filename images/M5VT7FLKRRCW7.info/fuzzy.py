from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.shortcuts import print_formatted_text

# Sample data for autocomplete
fruits_list = [
    'Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 
    'Grape', 'Honeydew', 'Icaco', 'Jackfruit', 'Kiwi', 'Lime', 
    'Mango', 'Nectarine', 'Orange', 'Papaya', 'Quince', 'Raspberry', 
    'Strawberry', 'Tomato', 'Ugli fruit', 'Vanilla', 'Watermelon', 
    'Xigua', 'Yellow watermelon', 'Zucchini'
]
fruits_completer = FuzzyCompleter(WordCompleter(fruits_list, ignore_case=True))

# Create a PromptSession
session = PromptSession()

def get_relevant_fruits(user_input):
    """Filter the list of fruits based on user input."""
    lower_input = user_input.lower()
    return [fruit for fruit in fruits_list if lower_input in fruit.lower()]

def main():
    while True:
        # Continuous listening with autocomplete
        user_input = session.prompt('Enter fruit name: ', completer=fruits_completer)
        
        # Break the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            break
        
        relevant_fruits = get_relevant_fruits(user_input)
        print_formatted_text('Relevant Results:')
        for fruit in relevant_fruits:
            print_formatted_text(fruit)

if __name__ == '__main__':
    main()
    