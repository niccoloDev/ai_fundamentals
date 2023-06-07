import random

import pandas as pd
import pandas_datareader as pdr
import numpy as np
import time

from business_logic.data_loader import DataLoader
from business_logic.model import *
import copy
from webapp import socketio


class PortfolioGenerator:
    def __init__(self, start_date, end_date):
        self.last_update_time = time.time()
        self.start_date = start_date
        self.end_date = end_date
        self.risk_free_return = self._calculate_risk_free_return()
        # self.tickers = None
        # self.set_tickers(tickers)

    ''' def set_tickers(self, tickers):
        if isinstance(tickers, int):  # if the user passed a number n we pick n random tickers
            self.tickers = DataLoader.fetch_nasdaq_tickers(tickers)
        else:  # else the user passed a comma separated string with the tickers and we convert it to a list
            self.tickers = tickers.split(',') '''

    def _calculate_risk_free_return(self):
        # we use the 1-year yield of the US treasury bonds as the risk-free return to use in the Sharpe Ratio
        treasury_yield_1year = pdr.get_data_fred('GS1', start=self.start_date, end=self.end_date)
        # print(treasury_yield_1year)
        average_annual_yield = treasury_yield_1year['GS1'].mean() / 100
        # print(average_annual_yield)
        average_daily_yield = np.exp(average_annual_yield / 252) - 1
        # print(average_daily_yield)
        return average_daily_yield

    def _load_local_data(self, csv_path):
        data = pd.read_csv(csv_path)
        data = data.sort_values(by='Date', ascending=True)
        return data

    def _calculate_sharpe_ratio(self, assets):
        # Initializing a series of zeros with the same index as the data
        returns = pd.Series(0, index=assets[0].data.index)

        for asset in assets:
            returns += asset.data['Adj Close'].pct_change() * asset.weight
        returns = returns.dropna()

        excess_returns = returns - self.risk_free_return

        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        return sharpe_ratio

    def _initialize_population(self, assets):
        # Create a population of possible portfolios with randomly generated weights
        population = []

        for i in range(100):
            weights = np.random.random(5)
            # normalize weights so that they sum to one
            weights = weights / weights.sum()

            portfolio = Portfolio()
            for (asset, weight) in zip(assets, weights):
                portfolio.add_asset(Asset(asset.ticker, asset.data, weight))

            population.append(portfolio)

        # print(population)
        return population

    def _normalize_fitness_scores(self, fitness_list):
        # add a shift value to the fitness to avoid negative fitness values
        min_fitness = min(fitness_list)
        shift = abs(min(0, min_fitness))
        fitness_list = fitness_list + shift

        total_fitness = sum(fitness_list)

        if total_fitness == 0:
            # If total fitness is zero, generate random probabilities for each portfolio
            fitness_list = np.random.random(size=len(fitness_list))
            return fitness_list / np.sum(fitness_list)  # Normalize to sum to 1
        else:
            return fitness_list / total_fitness

    def _apply_fitness_function(self, population):
        for portfolio in population:
            portfolio.fitness = self._calculate_sharpe_ratio(portfolio.assets)

        # normalize_fitness_score(population)

    @staticmethod
    def _normalize_weights(portfolio):
        weights_sum = sum(asset.weight for asset in portfolio.assets)
        for asset in portfolio.assets:
            asset.weight = asset.weight / weights_sum

        # Correct the last weight to ensure the sum equals 1.0
        diff = 1.0 - sum(asset.weight for asset in portfolio.assets)
        portfolio.assets[-1].weight += diff

    def _reproduce(self, parents):
        crossing_point = np.random.randint(0, len(parents[0].assets))
        child_assets = parents[0].assets[0:crossing_point] + parents[1].assets[crossing_point:]
        child = Portfolio(child_assets)
        PortfolioGenerator._normalize_weights(child)
        return child

    def _mutate(self, child, mutation_rate=0.1):
        # is_mutated = False
        for asset in child.assets:
            if np.random.random() <= mutation_rate:
                mutation = (np.random.random() - 0.5) * 0.1
                asset.weight = max(0, asset.weight + mutation)  # avoid negative weights
                # is_mutated = True

        PortfolioGenerator._normalize_weights(child)
        '''if is_mutated:
            weights_sum = sum(asset.weight for asset in child.assets)
            for asset in child.assets:
                asset.weight = asset.weight / weights_sum'''

        return child

    def _generate_next_generation(self, population):
        fitness_list = [portfolio.fitness for portfolio in population]
        normalized_fitness_list = self._normalize_fitness_scores(np.array(fitness_list))
        new_generation = []

        # keep the best 10 specimen of the past population for elitism
        population_count = len(population)
        elitism_count = round(population_count * 0.05)     # retain the best 5% of the population for next generation
        random_count = round(population_count * 0.1)     # pick 10% of next generation randomly from this generation, for diversity
        # Sort the population by fitness in ascending order
        sorted_population = sorted(population, key=lambda portfolio: portfolio.fitness)
        # Get the last 'elitism_count' elements(the portfolios with the highest fitness) and add them to next generation
        top_portfolios = sorted_population[-elitism_count:]
        new_generation += top_portfolios
        random_portfolios = random.sample(population=population, k=random_count)
        new_generation += random_portfolios

        # fill the rest of new generation with standard reproduction
        for i in range(0, population_count-elitism_count-random_count):
            parents = np.random.choice(population, size=2, p=normalized_fitness_list)
            new_generation.append(self._mutate(self._reproduce(parents)))

        return new_generation

    def _send_progress_update(self, progress):
        current_time = time.time()
        if current_time - self.last_update_time >= 1.0:  # 1 second has passed
            socketio.emit('progress_update',
                          {'progress': progress},
                          namespace='/portfolio_generation')
            self.last_update_time = current_time

    def generate_portfolio(self, tickers, gen_num=100):
        # TODO: it could be beneficial to run the algorithm more than once and then choose the best option
        #  to escape local maxima, maybe consider multithreaded approach

        # data = load_local_data(r"C:\Users\niccolo\Projects\ai-fundamentals-project\data\TSLA.csv")

        # TODO: there should be some consistency checks for start_date and end_date
        #  (example: start date should not be after end date)
        ''' if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
         if tickers:
             self.set_tickers(tickers) '''

        assets = DataLoader.load_assets(tickers=tickers, start_date=self.start_date, end_date=self.end_date)

        population = self._initialize_population(assets)
        self._apply_fitness_function(population)

        current_best_portfolio = copy.deepcopy(max(population, key=lambda portfolio: portfolio.fitness))

        socketio.emit('server_response',
                      {'current_best_portfolio': current_best_portfolio.to_dict()},
                      namespace='/portfolio_generation')

        generations_since_last_improvement = 0
        restart_timeout = 100
        # Evaluate each member of the population with the sharpe ratio, choose the best and create new generation
        for i in range(gen_num):
            generations_since_last_improvement += 1
            # print('max fitness at iteration {}: {}'.format(i, max(portfolio.fitness for portfolio in population)))
            if generations_since_last_improvement < restart_timeout:
                population = self._generate_next_generation(population)
            # if we get stuck on local minima we try a restart
            else:
                print("RESTARTING...")
                generations_since_last_improvement = 0
                population = self._initialize_population(assets)
            self._apply_fitness_function(population)

            # evaluate new best choice
            next_gen_contender = max(population, key=lambda portfolio: portfolio.fitness)
            if next_gen_contender.fitness > current_best_portfolio.fitness:
                generations_since_last_improvement = 0
                current_best_portfolio = copy.deepcopy(next_gen_contender)

                self._normalize_weights(current_best_portfolio)
                socketio.emit('server_response',
                              {'current_best_portfolio': current_best_portfolio.to_dict()},
                              namespace='/portfolio_generation')

            print(f"Iteration #{i}: {current_best_portfolio.fitness}")
            self._send_progress_update(round(i/gen_num * 100))
        print("--------------DONE-----------------")
        return current_best_portfolio
