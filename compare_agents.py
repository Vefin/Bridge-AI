import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

from match import *

GAMES_PER_MATCH = 100

all_simple_agents_names = [
                           # 'HighestFirstAgent',
                           # 'LowestFirstAgent',
                           # 'RandomAgent',
                           'HardGreedyAgent',
                           'HardGreedyAllPlayersAgent',
                           'SoftGreedyAgent',
                           'SoftGreedyAllPlayersAgent'
                           ]

all_simple_action_funcs_names = [
                          # 'highest_first_action',
                          # 'lowest_first_action',
                          # 'random_action',
                          'hard_greedy_action',
                          'hard_greedy_all_players_action',
                          'soft_greedy_action',
                          'soft_greedy_all_players_action'
                          ]

all_ab_evaluation_func = ['greedy_evaluation_function1',
                          'greedy_evaluation_function2',
                          'hand_evaluation_heuristic',
                          'count_tricks_won_evaluation_function',
                          ]

all_ab_evaluation_names = ['GreedyEvaluationCurrPlayer',
                           'GreedyEvaluationAllPlayers',
                           'HandEvaluation',
                           'CountOfTricksWon']

results = np.empty((len(all_simple_action_funcs_names),
                    len(all_simple_action_funcs_names)))
results[:] = np.nan


def run_all_simple_actions_matches():
    for i in range(len(all_simple_action_funcs_names)):
        for j in range(len(all_simple_action_funcs_names)):
            # For each pair of agents
            agent0, agent1 = \
                all_simple_action_funcs_names[i], all_simple_action_funcs_names[j]
            print(f"{all_simple_agents_names[i]} vs. "
                  f"{all_simple_agents_names[j]}")

            # Run match
            curr_match = Match(SimpleAgent(agent0),
                               SimpleAgent(agent1),
                               GAMES_PER_MATCH, False)
            curr_match.run()

            # Print match result and update scores table
            print(f"Score: {curr_match.games_counter[0]:02} -"
                  f" {curr_match.games_counter[1]:02}\n")
            results[i, j] = 100 * curr_match.games_counter[0] / GAMES_PER_MATCH


def display_table_simple_agents():
    fig, ax = plt.subplots(dpi=300)
    im = ax.imshow(results, cmap='plasma', vmin=0, vmax=100)
    ax.set_xticks(np.arange(len(all_simple_agents_names)))
    ax.set_yticks(np.arange(len(all_simple_agents_names)))
    ax.set_xticklabels(all_simple_agents_names)
    ax.set_yticklabels(all_simple_agents_names)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    for i in range(len(all_simple_agents_names)):
        for j in range(len(all_simple_agents_names)):
            text = ax.text(
                j, i, f"{results[i, j]:05.2f}",
                ha="center", va="center", color="w")
            text.set_path_effects(
                [path_effects.Stroke(linewidth=2, foreground='black'),
                 path_effects.Normal()])
    ax.set_title("Win rate % (of agent on y-axis)",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    plt.show()


def compare_simple_agents():
    print()
    run_all_simple_actions_matches()
    display_table_simple_agents()


def compare_ab_vs_ab_agents():
    agent0, agent1 = all_ab_evaluation_func[1], all_ab_evaluation_func[1]
    depth0, depth1 = 2, 2
    print(f"{all_ab_evaluation_names[1]} vs. {all_ab_evaluation_names[1]}")

    # Run match
    curr_match = Match(AlphaBetaAgent(evaluation_function=agent0,
                                      depth=depth0),
                       AlphaBetaAgent(evaluation_function=agent1,
                                      depth=depth1), GAMES_PER_MATCH, False)
    curr_match.run()

    # Print match result and update scores table
    print(f"Score: {curr_match.games_counter[0]:02} - "
          f"{curr_match.games_counter[1]:02}\n")


def run_all_simple_agents_vs_ab_matches(depth):
    for i in range(len(all_simple_action_funcs_names)):
        for j in range(len(all_ab_evaluation_func)):
            agent0 = all_simple_action_funcs_names[i]
            print(f"{all_simple_agents_names[i]} vs. AlphaBeta({all_ab_evaluation_names[j]})")
            curr_match = Match(SimpleAgent(agent0),
                               AlphaBetaAgent(evaluation_function=all_ab_evaluation_func[j],
                                              depth=depth),
                               GAMES_PER_MATCH, False, cards_in_hand=5)
            curr_match.run()
            print(f"Score: {curr_match.games_counter[0]:02} -"
                  f" {curr_match.games_counter[1]:02}\n")
            results[i, j] = 100 * curr_match.games_counter[0] / GAMES_PER_MATCH
            # taking the score of the first agent curr_match.games_counter[0] to fill the left
            # column of the table, which containing the win rate of the single agent vs. alpha-beta
            # when single agent starts the game.


def run_all_simple_agents_vs_ab_matches_ab_first(depth):
    for i in range(len(all_simple_action_funcs_names)):
        for j in range(len(all_ab_evaluation_func)):
            agent0 = all_simple_action_funcs_names[i]
            print(f"AlphaBeta({all_ab_evaluation_names[j]}) vs. {all_simple_agents_names[i]}")
            curr_match = Match(AlphaBetaAgent(evaluation_function=all_ab_evaluation_func[j],
                                              depth=depth), SimpleAgent(agent0),
                               GAMES_PER_MATCH, False, cards_in_hand=5)
            curr_match.run()
            print(f"Score: {curr_match.games_counter[0]:02} -"
                  f" {curr_match.games_counter[1]:02}\n")
            results[i, j] = 100 * curr_match.games_counter[0] / GAMES_PER_MATCH
            # taking the score of the first agent curr_match.games_counter[0] to fill the left
            # column of the table, which containing the win rate of the single agent vs. alpha-beta
            # when single agent starts the game.


def display_table_simple_agents_vs_ab(depth):
    fig, ax = plt.subplots(dpi=300)
    im = ax.imshow(results, cmap='plasma', vmin=0, vmax=100)
    ax.set_xticks(np.arange(len(all_ab_evaluation_names)))
    ax.set_yticks(np.arange(len(all_simple_agents_names)))
    ax.set_xticklabels(all_ab_evaluation_names)
    ax.set_yticklabels(all_simple_agents_names)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    for i in range(len(all_simple_agents_names)):
        for j in range(len(all_ab_evaluation_names)):
            text = ax.text(
                j, i, f"{results[i, j]:05.2f}",
                ha="center", va="center", color="w")
            text.set_path_effects(
                [path_effects.Stroke(linewidth=2, foreground='black'),
                 path_effects.Normal()])
    ax.set_title(f"Win rate % for y axis \nvs AlphaBeta, "
                 f"depth: {depth}",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    plt.show()


def compare_simple_agents_vs_ab_agents():
    print()
    depth = 20
    run_all_simple_agents_vs_ab_matches(depth)
    display_table_simple_agents_vs_ab(depth)


def compare_simple_agents_vs_ab_agents_ab_first():
    print()
    depth = 20
    run_all_simple_agents_vs_ab_matches_ab_first(depth)
    display_table_simple_agents_vs_ab(depth)


compare_simple_agents_vs_ab_agents_ab_first()
# compare_simple_agents_vs_ab_agents()
# compare_simple_agents()