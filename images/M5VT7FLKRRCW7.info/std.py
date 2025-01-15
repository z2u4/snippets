from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Sample data for autocomplete
fruits_completer = WordCompleter([
    'Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 
    'Grape', 'Honeydew', 'Icaco', 'Jackfruit', 'Kiwi', 'Lime', 
    'Mango', 'Nectarine', 'Orange', 'Papaya', 'Quince', 'Raspberry', 
    'Strawberry', 'Tomato', 'Ugli fruit', 'Vanilla', 'Watermelon', 
    'Xigua', 'Yellow watermelon', 'Zucchini'
], ignore_case=True)

# Create a PromptSession, which will enable the continuous listening
session = PromptSession()

def main():
    while True:
        # The prompt that continuously listens and provides autocomplete
        user_input = session.prompt('Enter fruit name: ', completer=fruits_completer)
        print(f'You selected: {user_input}')
        # Break the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            break

if __name__ == '__main__':
    main()