from libs.cli_handler import CLI_HANDLER
from libs.User import User

from typing import Dict, Any
from collections import defaultdict

users_list = {}

def user_adding_fn(cli_handler_obj: CLI_HANDLER) -> Dict[str, Any]:
    global users_list
    answers = cli_handler_obj.users_input_cli(users_list)

    if answers["isUserRepeated"]:
        return True

    #handle user creation and adding info
    user_obj = User(answers['user'])
    users_list[answers['user']] = user_obj

    return answers['toEnterNewUser']

def get_net_costs(users_list: Dict[str, User]) -> Dict[str, int]:
    net_costs = defaultdict(lambda:0)
    for user_name, user_obj in users_list.items():
        for un, amount in user_obj.money_from.items():
            # print(f"{un.username.capitalize()} owes {user_name.capitalize()} ${amount}")
            net_costs[user_name] += amount
            net_costs[un.username] -= amount
    return net_costs

def greedy_ledge_algo(net_costs: Dict[str, int]):
    max_credit = 0
    max_debit = 0
    pd, pc = "", ""
    for user, net_cost in net_costs.items():
        if net_cost > max_credit:
            pc = user
            max_credit = net_cost
        if net_cost < max_debit:
            max_debit = net_cost
            pd = user

    if max_credit == 0 and max_debit == 0:
        return net_costs

    minimum_cost = min([abs(max_debit), max_credit])
    net_costs[pc] -= minimum_cost
    net_costs[pd] += minimum_cost

    print(f"{pd} pays to {pc} ${minimum_cost}")

    net_costs = greedy_ledge_algo(net_costs)

    return net_costs

def main():

    cli_handler_obj = CLI_HANDLER()

    cli_handler_obj.figlet_text()
    is_new_user = user_adding_fn(cli_handler_obj)

    while is_new_user:
        is_new_user = user_adding_fn(cli_handler_obj)

    # handle single point of entries for payments algorithm

    cli_handler_obj.ledge_input_cli(users_list)

    # handle user graph
    net_costs: Dict[str,int] = get_net_costs(users_list)

    greedy_ledge_algo(net_costs)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)