from __future__ import annotations

import random

import numpy as np


class Jeonjeok():

    def __init__(self):
        self.prob_win = 0.43

    def bet(self, bet):

        result = random.uniform(0, 1)
        money_earned = 0
        if result <= self.prob_win:
            # Win scenario
            win_chance = random.uniform(0, 1)
            # There are three possible win outcomes based on the rules
            if win_chance < 0.87:
                money_earned = 2 * bet
            elif win_chance < 0.97:
                money_earned = 3 * bet
            else:
                money_earned = 5 * bet

            self.prob_win = 0.43
        else:
            # Lose scenario
            money_earned = -bet
            # Increase the probability of winning if the player loses
            self.prob_win += random.uniform(0.0035, 0.016)
            # print("Lose!")

        return money_earned


def mc_simulation(sim_length, min_bet, start_funds):
    model = Jeonjeok()
    funds = start_funds
    betting_proportions = []

    for i in range(sim_length):
        if model.prob_win > 0.4566:
            betting_proportion = (model.prob_win - 0.4566) * 1.73
            betting_proportions.append(betting_proportion)

            funds += model.bet(funds * betting_proportion)
        else:
            funds += model.bet(min_bet)

    return funds, betting_proportions


funds = 1000
sim_length = 5000
min_bet = 0.5
post_simulation_funds, betting_proportions = mc_simulation(
    sim_length, min_bet, funds,
)

print(f'Starting fund: {funds}, Post Simuation funds: {post_simulation_funds}')
print(f'Average winning: {(post_simulation_funds - funds) / sim_length}')
print(f'Average betting proportions: {np.mean(betting_proportions)}')
