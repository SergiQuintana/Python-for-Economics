"""
Exercise 1 for brush up.

Tristany Armangue i Jubert
"""

### Dependencies
import pyfiglet
from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import style_from_dict, Token, prompt, Separator

### EXERCISE 1
# Helper function 
class FloatValidator(Validator):
    def validate(self, document):
        try:
            if 0 > float(document.text):
                raise ValidationError(
                    message = 'Please enter a valid amount of money (positive number)',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            try:
                if 0 > int(document.text):
                    raise ValidationError(
                        message = 'Please enter a valid amount of money (positive number)',
                        cursor_position=len(document.text))  # Move cursor to end
            except ValueError:
                raise ValidationError(
                        message = 'Please enter a valid amount of money (positive number)',
                        cursor_position=len(document.text))  # Move cursor to end

# Main class
class vending_machine:
    """
    Vending machine class.

    Attributes: 
        - Initial stocks.
        - Initial prices.

    Methods:
        - Turn on (agents can interact here.)
        - Update stocks.
        - Update prices.
    """

    def __init__(self, products:list, prices:list, stock:list) -> None:
        # Check input types are correct
        try:
            assert all(isinstance(item, str) for item in products)
            assert all((isinstance(item, int)) | (isinstance(item, float)) for item in prices)
            assert all((isinstance(item, int)) | (isinstance(item, float)) for item in prices)
        except:
            raise Exception("Incorrect types in input lists.")

        # Check prices and stock are positive numbers
        try:
            assert all((item > 0) for item in prices)
            assert all((item > 0) for item in stock)
        except:
            raise Exception("Prices and stocks must be positive numbers.")

        # Check input lists are same length
        try:
            assert len(products) == len(prices) == len(stock)
        except:
            raise Exception("Products, prices and stock must be equal length.")

        # Keep list of buyable products
        self.products = products

        # Initiate dictionary of prices and stocks
        self.stocks = dict(zip(products, stock))
        self.prices = dict(zip(products, prices))

        # Balance holder
        self.balance = 0

    def turn_on(self):
        # Reset balance
        self.balance = 0

        # Welcome message
        print(''.center(80, '#'))
        print('')
        print('')
        print(pyfiglet.figlet_format("Bonpreu IDEA", font="banner3", justify="center"))
        print('')
        print('')
        print(''.center(80, '#'))
        print('')
        print('')

        # Style for input questionnaire
        style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })

        # Product Selection
        questions = [
            {
                'type': 'list',
                'message': 'Please select the product of interest:',
                'name': 'product',
                'choices': self.products,
            }
        ]
        answer_q1 = prompt(questions, style=style)

        # Check choice
        print("You have selected {}. Do you wish to continue?".format(answer_q1["product"]))
        questions = [
            {
                'type': 'list',
                'message': 'Continue?',
                'name': 'continue_1',
                'choices': [
                    "Yes",
                    "No",
                ],
                'default' : 'Yes'
            }
        ]
        answer_q2 = prompt(questions, style=style)

        # If mistake, restart
        if answer_q2["continue_1"] != "Yes":
            self.turn_on()

        # Give price
        print("You have selected {}. The price is {}".format(answer_q1["product"], self.prices[answer_q1["product"]]))

        # Ask for money
        questions = [
            {
                'type': 'input',
                'message': 'Input some money:',
                'name': 'balance',
                'default': '2',
                'validate': FloatValidator
            }
        ]
        answer_q3 = prompt(questions, style=style)
        self.balance = float(answer_q3["balance"])

        # Check balance, if sufficient -> effectuate purchase, if 
        # insufficient -> state insufficient and give option to add more
        # or to return money
        self.check_balance(answer_q1["product"])

        # Finished, back to welcome
        self.turn_on()
        
    def check_balance(self, product):
        # Style for input questionnaire
        style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })

        # Checks
        if self.balance > self.prices[product]:
            print("Here is your {}, your change is {}".format(product, 
            (self.balance - self.prices[product])))
            # Update stock
            if self.stocks[product] > 0:
                self.stocks[product] -= 1
            else:
                self.products.remove(product)
        elif self.balance == self.prices[product]:
            print("Here is your {}".format(product))
            # Update stock
            if self.stocks[product] > 0:
                self.stocks[product] -= 1
            else:
                self.products.remove(product)
        else:
            print("Your balance is insufficient. How do you wish to proceed?")
            questions = [
                {
                    'type': 'list',
                    'message': 'Insufficient balance.',
                    'name': 'insuf_1',
                    'choices': [
                        "Return money",
                        "Add money",
                    ],
                    'default' : 'Return money'
                }
            ]
            answer_q4 = prompt(questions, style=style)
            # Evaluate choice 
            if answer_q4["insuf_1"] == "Return money":
                print("Here is your money (${})".format(self.balance))
                self.balance = 0
            else:
                questions = [
                    {
                        'type': 'input',
                        'message': 'Input some money:',
                        'name': 'balance',
                        'default': '2',
                        'validate': FloatValidator
                    }
                ]
                answer_q5 = prompt(questions, style=style)
                self.balance += float(answer_q5["balance"])
                
                # Check again
                self.check_balance(product)

# Initiate VM object
VM = vending_machine(["coke","pepsi","pringles"],[1.5, 1.4, 2],[20,30,5])

# Turn on VM
VM.turn_on()
