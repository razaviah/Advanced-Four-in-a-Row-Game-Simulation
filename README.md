# Connect-Four

## The Project:

In this project, I designed agents for the zero-sum game called "Four in a Row". This is a two-player board game, in which the players choose a color and then take turns dropping colored discs into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. "Four in a Row" is a solved game. The first player can always win by playing the right moves. 

For this project, I implemented the following 3 algorithms:

•Minimax - Implemented depth-limited minimax which searches to an arbitrary depth as it's not feasible to search the entire game tree.

•Alpha-Beta Pruning - This will speed-up the search as the depth of the tree increases, as it allows for more efficient exploration of the minimax tree

•Expectimax – This models probabilistic behavior of opponents that may make suboptimal decisions. For this you will have chance nodes that will replace the MIN nodes (AI-Agent2 or Human Player). For this implementation, consider you will only be running against an adversary which chooses actions uniformly at random, because Minimax and Alpha-Beta algorithms assume that MAX plays against an adversary who makes optimal decisions.

## Players:
Types of players that can participate in the game:

•AI-Agent – This will be the agent that you implement.

•Random Player – This kind of player chooses valid columns with equal probability.

•Human Player – This will be a human playing the game.

## How to run:

To run the game, use the following command: `python four_in_a_row.py`
