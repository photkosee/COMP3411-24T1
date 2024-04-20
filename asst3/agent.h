/*********************************************************
 *  agent.c
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9814 Artificial Intelligence
 *  Alan Blair, CSE, UNSW
 *  Yifan Zhu, Phot Koseekrainiramon
 */
extern int   port;
extern char *host;

 //  parse command-line arguments
void agent_parse_args( int argc, char *argv[] );

 //  called at the beginning of a series of games
void agent_init();

 //  called at the beginning of each game
void agent_start( int this_player );

int  agent_second_move(int board_num, int prev_move );

int  agent_third_move(int board_num,int first_move,int prev_move);

int  agent_next_move( int prev_move );

void agent_last_move( int prev_move );

 //  called at the end of each game
void agent_gameover( int result, int cause );

 //  called at the end of the series of games
void agent_cleanup();

int has_won_small(int small_board[10]);

int has_won_big(int big_board[10][10]);

int evaluate_small(int small_board[10]);

int evaluate_big(int big_board[10][10]);

int alphabeta(
  int player,
  int curr_depth,
  int big_board[10][10],
  int alpha,
  int beta,
  int best_move[10],
  int curr_board,
  int max_depth
);

int play(int curr_big_board[10][10], int prev_move);
