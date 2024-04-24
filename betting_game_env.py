from __future__ import annotations

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class BettingGameEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(
        self, initial_funds: float = 1000, min_bet: float = 0.5, prob_win: float = 0.43,
    ):
        """
        Initialize the betting game environment.

        Parameters:
        - initial_funds (float): The initial amount of money the player starts with.
        - min_bet (float): The minimum bet amount that the player can wager.
        - prob_win (float): The initial probability of winning a bet.

        Attributes:
        - current_funds (float): Tracks the current funds available to the player.
        - action_space (spaces.Box): Defines the range of allowable bets.
        - observation_space (spaces.Box): Defines the state space of the environment which is the current funds.
        """
        super().__init__()
        # Initialize the environment with the given parameters
        self.initial_funds = initial_funds
        self.current_funds = self.initial_funds
        self.min_bet = min_bet
        self.prob_win = prob_win

        # Action space is the bet amount
        self.action_space = spaces.Box(
            low=np.array([self.min_bet]),
            high=np.array([self.current_funds]),
            dtype=np.float32,
        )
        # Observation space is the current funds
        self.observation_space = spaces.Box(
            low=np.array([0]), high=np.array([float('inf')]), dtype=np.float32,
        )

    def reset(self, **kwargs):
        """
        Reset the environment to the initial state.

        Returns:
        - numpy.array: The initial state of the environment (initial funds), wrapped in a numpy array.
        - dict: An empty dictionary that could be used to pass extra information.
        """
        self.current_funds = self.initial_funds
        self.prob_win = 0.43
        return np.array([self.current_funds]), {}

    def step(self, action):
        """
        Execute one time step within the environment based on the agent's action.

        Parameters:
        - action (numpy.array): An array containing the bet amount.

        Returns:
        - numpy.array: The new state of the environment (current funds).
        - float: The reward received after performing the action.
        - bool: A boolean indicating whether the episode has ended (done).
        - bool: A boolean indicating whether the episode was truncated (truncated, always False here).
        - dict: A dictionary containing additional information like current funds and winning probability.

        Raises:
        - AssertionError: If the bet amount is out of allowable range (between min_bet and current_funds).
        """
        bet = action[0]
        self.current_funds -= bet
        assert (
            self.min_bet <= bet <= self.current_funds
        ), f'Bet amount must be between {self.min_bet} and {self.current_funds}'
        result = self.np_random.random()

        if result <= self.prob_win:
            # Win scenario
            money_earned = 0
            win_chance = self.np_random.random()
            # There are three possible win outcomes based on the rules
            if win_chance < 0.87:
                money_earned = 2 * bet
                reward = 2 * bet
            elif win_chance < 0.97:
                money_earned = 3 * bet
                reward = 13 * bet
            else:
                money_earned = 5 * bet
                reward = 20 * bet

            self.current_funds += money_earned
        else:
            # Lose scenario
            reward = -bet
            # Increase the probability of winning if the player loses
            self.prob_win += self.np_random.uniform(0.0035, 0.016)

        done = self.current_funds <= 0 or self.current_funds >= 10 * self.initial_funds
        info = {
            'funds': self.current_funds,
            'prob_win': self.prob_win,
        }

        # Check if the episode is truncated (not applicable in this environment)
        truncated = False  # Set to False as we do not use time limits

        return np.array([self.current_funds]), reward, done, truncated, info

    def render(self):
        """
        Render the environment's state to a visual display (not implemented).

        Currently, this function does nothing. In a complete implementation, it might update a graphical display of the
        environment state to help users or developers visually verify the behavior of the environment.
        """
        pass
