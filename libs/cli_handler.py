# TODO add questions for ledge creation

from __future__ import print_function, unicode_literals
from typing import Dict, Any

from libs.User import User


from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from pyfiglet import Figlet


class UserNameValidator(Validator):
    def validate(self, document):
        ok = True if len(document.text) != 0 else False
        if not ok:
            raise ValidationError(
                message='Please enter a username',
                cursor_position=len(document.text))  # Move cursor to end

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class CLI_HANDLER:
    def __init__(self):
        # PyInquirer style
        self.style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })

        # PyInquirer questions
        self.questions_users = [
            {
            'type': 'input',
            'name': 'user',
            'message': 'What\'s the user name?',
            'validate': UserNameValidator
            },
            {
                'type': 'confirm',
                'name': 'toEnterNewUser',
                'message': 'Do you want to add new user?',

            }
        ]


        self.figlet_obj = Figlet(font='slant')

    def figlet_text(self):
        print(self.figlet_obj.renderText('Brainless Cost'))

    def users_input_cli(self, users_list: Dict[str, User]) -> Dict[str, Any]:

        answers = prompt(self.questions_users, style=self.style)

        answers['user'] = answers['user'].lower()

        if answers['user'] in users_list:
            print("[ERROR] username repeated please try again !")
            answers['isUserRepeated'] = True
        else:
            answers['isUserRepeated'] = False

        return answers

    def ledge_input_cli(self, users_list: Dict[str, Any]):
        #ledge questions
        all_usernames = [{'name':key.capitalize()} for key, value in users_list.items()]
        for user_name, user_obj in users_list.items():

            self.questions_ledge = [
                {
                    'type': 'input',
                    'name': 'amount',
                    'message': f'How much money did "{user_name.capitalize()}" pay ?',
                    'validate': NumberValidator,
                    'filter': lambda val: int(val)
                },
                {
                    'type': 'checkbox',
                    'name': 'person_owes',
                    'message': 'Select people that are included in the cost:',
                    'choices': all_usernames
                },
                {
                    'type': 'confirm',
                    'name': 'toEnterNewUser',
                    'message': 'Do you want to add new cost?',

                }
            ]

            answers = self._ask_ledge_questions()
            self._handle_answers(answers, user_name, user_obj, users_list)
            if not answers['toEnterNewUser']:
                break


    def _ask_ledge_questions(self) -> Dict[str, Any]:
        answers = prompt(self.questions_ledge, style=self.style)
        return answers

    def _handle_answers(self, answers: Dict[str, Any], user_name: str, user_obj: User, users_list: Dict[str, User]):
        amount_per_person = int(answers['amount'] / len(answers['person_owes']))
        for user in answers['person_owes']:
            if user.lower() == user_name:
                continue
            user_obj.add_money_from(users_list[user.lower()], amount_per_person)