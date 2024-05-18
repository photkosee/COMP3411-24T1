/*********************************************************
 *  agent.c
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9814 Artificial Intelligence
 *  Alan Blair, CSE, UNSW
 *  Yifan Zhu, Phot Koseekrainiramon 17/04/2024
 *
 *  
    Briefly describe how your program works,
    including any algorithms and data structures employed,
    and explain any design decisions you made along the way.
 *
 *

    We made use of normal alpha-beta pruning algorithm but our heuristic is to
    sum up all the scores of the whole big board at the given state (when reaching the maximum depth).
    The way we evaluate score depends on each sub-board, checking how likely for our agent
    to win or lose by couting the number of plays in a row. If there is only one play
    left to win then we assign more scores than needing to play 2 plays to win (and only if
    the opponent hasn't cut the play we need to play in a row).

    If the win/lose happens before we reach the maximum depth, we just return the maximum/minimum number to
    assure that we'd or would not pick that particular play (if possible). And make sure that we'd like
    to win as fast as possible by having a depth variable and minus the maximum number if a win occurs.

    Unlike the first assignment, we are not using any crazy data structures this time, mostly would be just
    a 2D array to store each cell of the bigboard and a win_conditions array to store all the index of possible
    3 cells in a row to win (start from 1-9, not 0-8).

    We have a prioritization array to prioritize the cell when we have multiple cells with the same evaluation score.
    We prioritize the middle cell than the corner than the other becuase it is more likely to prune when we pick the middle
    cell then the corner. And with more pruning, we'd be able to do more search with in the limited time, improving the
    overall performance.

    At first, we were doing this whole thing in Python but the performance wasn't that great. We were trying
    to come up with a better heuristic but realised that the main issue was the maximum number of depth we can
    search/look ahead. So, we decided to switch to C with the same algorithm we did in Python and able to increase
    the number of maximum depth by almost twice the number. This improved the performace by a lot, being able to beat
    all the lookt levels (maximum 18) with higher win rate at the higher levels compared to before.

 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>

#include "common.h"
#include "agent.h"
#include "game.h"

#define MAX_MOVE 81

int board[10][10];
int move[MAX_MOVE+1];
int player;
int best_move[MAX_MOVE+1];
int m;
#define MIN_EVAL -100000
#define MAX_EVAL  100000
// Win condition (3 in a row) for a normal 9*9 board
int win_conditions[8][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9},
  {1, 4, 7},
  {2, 5, 8},
  {3, 6, 9},
  {1, 5, 9},
  {3, 5, 7}
};
// Prioritize the middle cell than corner than the other
int cell_priority[9] = {5, 1, 3, 7, 9, 4, 6, 2, 8};
int turn = 0;

// Check whether any player has won the sub-board (small board)
// Return 0 if our ai win, 1 if it's the opponent, 2 if none has won
int has_won_small(int small_board[10]) {
  for (int i = 0; i < 8; i++) {
    if (
      small_board[win_conditions[i][0]] == 0 &&
      small_board[win_conditions[i][1]] == 0 &&
      small_board[win_conditions[i][2]] == 0
    ) {
      return 0;
    }
    if (
      small_board[win_conditions[i][0]] == 1 &&
      small_board[win_conditions[i][1]] == 1 &&
      small_board[win_conditions[i][2]] == 1
    ) {
      return 1;
    }
  }
  return 2;
}

// Check whether any player has won any sub-board
// Return the winner (0/1), return 2 if none has won
int has_won_big(int big_board[10][10]) {
  for (int i = 1; i < 10; i++) {
    if (has_won_small(big_board[i]) != 2) {
      return has_won_small(big_board[i]);
    }
  }
  return 2;
}

// Heuristic: checking how likely for a player to win in a small board
// Assign 10 if a player has 2 play in a row, and 1 with 1 play in a row
// player is our agent, !player is the opponent (negative score)
int evaluate_small(int small_board[10]) {
  int score = 0;
  for (int i = 0; i < 8; i++) {
    int position[3] = {
      small_board[win_conditions[i][0]],
      small_board[win_conditions[i][1]],
      small_board[win_conditions[i][2]]
    };

    int count_1 = 0, count_2 = 0;
    for (int j = 0; j < 3; j++) {
      if (position[j] == player)
        count_1++;
      else if (position[j] == !player)
        count_2++;
    }

    if (count_1 == 2 && count_2 == 0)
      score += 10;
    else if (count_1 == 1 && count_2 == 0)
      score += 1;
    else if (count_1 == 0 && count_2 == 2)
      score -= 10;
    else if (count_1 == 0 && count_2 == 1)
      score -= 1;
  }
  return score;
}

// Summing up all the scores across all small boards
int evaluate_big(int big_board[10][10]) {
  int score = 0;
  for (int i = 1; i < 10; i++) {
    score += evaluate_small(big_board[i]);
  }
  return score;
}

// Normal alphabeta algorithm (ref from ttt.c)
int alphabeta(
  int curr_player,
  int curr_depth,
  int big_board[10][10],
  int alpha,
  int beta,
  int curr_best_move[10],
  int curr_board,
  int max_depth
) {
  int this_eval;
  int best_eval = MIN_EVAL;
  int this_move = 0;

  // Checking whether our agent has won or lose
  int winner = has_won_big(big_board);
  if (
    (winner == 0 && curr_player == 1) ||
    (winner == 1 && curr_player == 0)
  ) {
    return MIN_EVAL + curr_depth;
  }
  if (
    (winner == 0 && curr_player == 0) ||
    (winner == 1 && curr_player == 1)
  ) {
    return MAX_EVAL - curr_depth;
  }

  // Positive score for our agent turn, negative otherwise
  if (curr_depth >= max_depth) {
    if (curr_depth % 2 == 0) {
      return evaluate_big(big_board);
    }
    return -evaluate_big(big_board);
  }

  for (int i = 0; i < 9; i++) {
    // Checking for empty cell to play
    if (big_board[curr_board][cell_priority[i]] == 2) {
      // get the priority cell (middle then corner then the other)
      this_move = cell_priority[i];
      int (*tmp)[10] = malloc(10 * sizeof(*tmp));
      if (tmp == NULL) {
        return 1;
      }
      // deep copy the board before passing
      for (int j = 0; j < 10; j++) {
        for (int k = 0; k < 10; k++) {
          tmp[j][k] = big_board[j][k];
        }
      }
      tmp[curr_board][this_move] = curr_player;
      this_eval = -alphabeta(
        !curr_player,
        curr_depth + 1,
        tmp, -beta,
        -alpha,
        curr_best_move,
        this_move,
        max_depth
      );
      free(tmp);

      // Early cut (pruning)
      if (this_eval > best_eval) {
        curr_best_move[curr_depth] = this_move;
        best_eval = this_eval;
        if (best_eval > alpha) {
          alpha = best_eval;
          if (alpha >= beta) {
            return alpha;
          }
        }
      }
    }
  }

  if( this_move == 0 ) { // no legal moves
    return 0;         // DRAW
  }
  else {
    return alpha;
  }
}

// make the best move
int play(int curr_big_board[10][10], int prev_move) {
  turn += 1;
  int max_depth;
  // Tuning for the maximum depth for a better performance
  if (turn < 2) {
    max_depth = 8;
  } else if (turn < 4) {
    max_depth = 9;
  } else if (turn < 8) {
    max_depth = 10;
  } else if (turn < 10) {
    max_depth = 11;
  } else if (turn < 12) {
    max_depth = 12;
  } else if (turn < 14) {
    max_depth = 13;
  } else if (turn < 16) {
    max_depth = 14;
  } else if (turn < 17) {
    max_depth = 15;
  } else if (turn < 18) {
    max_depth = 16;
  } else if (turn < 19) {
    max_depth = 18;
  } else if (turn < 22) {
    max_depth = 21;
  } else {
    max_depth = 24;
  }

  alphabeta(
    player,
    0,
    curr_big_board,
    MIN_EVAL,
    MAX_EVAL,
    best_move,
    prev_move,
    max_depth
  );
  return best_move[0];
}

/*********************************************************
   Print usage information and exit
*/
void usage( char argv0[] )
{
  printf("Usage: %s\n",argv0);
  printf("       [-p port]\n"); // tcp port
  printf("       [-h host]\n"); // tcp host
  exit(1);
}

/*********************************************************
   Parse command-line arguments
*/
void agent_parse_args( int argc, char *argv[] )
{
  int i=1;
  while( i < argc ) {
    if( strcmp( argv[i], "-p" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      port = atoi(argv[i+1]);
      i += 2;
    }
    else if( strcmp( argv[i], "-h" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      host = argv[i+1];
      i += 2;
    }
    else {
      usage( argv[0] );
    }
  }
}

/*********************************************************
   Called at the beginning of a series of games
*/
void agent_init()
{
  struct timeval tp;

  // generate a new random seed each time
  gettimeofday( &tp, NULL );
  srandom(( unsigned int )( tp.tv_usec ));
}

/*********************************************************
   Called at the beginning of each game
*/
void agent_start( int this_player )
{
  reset_board( board );
  m = 0;
  move[m] = 0;
  player = this_player;
}

/*********************************************************
   Choose second move and return it
*/
int agent_second_move( int board_num, int prev_move )
{
  int this_move;
  move[0] = board_num;
  move[1] = prev_move;
  board[board_num][prev_move] = !player;
  m = 2;
  this_move = play(board, prev_move);
  move[m] = this_move;
  board[prev_move][this_move] = player;
  return( this_move );
}

/*********************************************************
   Choose third move and return it
*/
int agent_third_move(
                     int board_num,
                     int first_move,
                     int prev_move
                    )
{
  int this_move;
  move[0] = board_num;
  move[1] = first_move;
  move[2] = prev_move;
  board[board_num][first_move] =  player;
  board[first_move][prev_move] = !player;
  m=3;
  this_move = play(board, prev_move);
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************
   Choose next move and return it
*/
int agent_next_move( int prev_move )
{
  int this_move;
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
  m++;
  this_move = play(board, prev_move);
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************
   Receive last move and mark it on the board
*/
void agent_last_move( int prev_move )
{
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
}

/*********************************************************
   Called after each game
*/
void agent_gameover(
                    int result,// WIN, LOSS or DRAW
                    int cause  // TRIPLE, ILLEGAL_MOVE, TIMEOUT or FULL_BOARD
                   )
{
  if (result == 2) {
    printf("win\n");
  } else if (result == 3) {
    printf("lose\n");
  }
}

/*********************************************************
   Called after the series of games
*/
void agent_cleanup()
{
  // nothing to do here
}
