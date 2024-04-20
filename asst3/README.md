<H3 align=center>Assignment 3 &ndash; Nine-Board Tic-Tac-Toe</H3>
<p align=center>
Due: Friday 19 April, 10 pm
<br align=center>
Marks: 16% of final assessment

<h4>Introduction</h4>

In this assignment you will be writing an agent to play the
game of Nine-Board Tic-Tac-Toe.
This game is played on a 3 x 3 array of 3 x 3 Tic-Tac-Toe boards.
The first move is made by placing an X in a randomly
chosen cell of a randomly chosen board.
After that, the two players take turns placing an O
or X alternately into an empty cell of the board
corresponding to the cell of the previous move.
(For example, if the previous move was into the upper right corner
of a board, the next move must be made into the upper right board.)

<p>
The game is won by getting three-in-a row either horizontally,
vertically or diagonally in one of the nine boards.
If a player is unable to make their move
(because the relevant board is already full)
the game ends in a draw.

<h4>Getting Started</h4>

Copy the archive <a href="./src.zip"><code>src.zip</code></a>
into your own filespace and unzip it. Then type

<pre>
cd src
make all

./servt -x -o
</pre>

You should then see something like this:

<pre>
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . . | . . .
 ------+-------+------
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . x | . . .
 ------+-------+------
 . . . | . . . | . . .
 . . . | . . . | . . .
 . . . | . . . | . . .

next move for O ? 
</pre>

You can now play Nine-Board Tic-Tac-Toe against yourself,
by typing a number for each move.
The cells in each board are numbered 1, 2, 3, 4, 5, 6, 7, 8, 9
as follows:

<pre>
+-----+
|1 2 3|
|4 5 6|
|7 8 9|
+-----+
</pre>
<p>
To play against a computer player,
you need to open another terminal window
(and <code>cd</code> to the <code>src</code> directory).
<p>
Type this into the first window:
<pre>
./servt -p 12345 -x
</pre>
This tells the server to use port <code>12345</code> for communication,
and that the moves for <code>X</code> will be chosen by you, the human,
typing at the keyboard.
(If port <code>12345</code> is busy, choose another 5-digit number.)
<p>
You should then type this into the second window
(using the same port number):
<pre>
./randt -p 12345
</pre>
The program <code>randt</code>
simply chooses each move randomly among the available legal moves.
The Python program <code>agent.py</code> behaves in exactly the same
way. You can play against it by typing this into the second window:
<pre>
python3 agent.py -p 12345
</pre>
You can play against a somewhat more sophisticated player by typing
this into the second window:
<pre>
./lookt -p 12345
</pre>
(If you are using a Mac, type <code>./lookt.mac</code> instead of <code>./lookt</code>)
<p>

<h4>Writing a Player</h4>

Your task is to write a program to play the game of
nine-board tic-tac-toe as well as you can.
Your program will receive commands from the server
<code>(init, start(), second_move(), third_move(), last_move(), win(), loss(), draw(), end())</code>
and must send back a single digit specifying the chosen move.<br>
(the parameters for these commands
are explained in the comments of <code>agent.py)</code>

<p>
Communication between the server and the player(s)
is illustrated in this brief example:
<center>
<table border=0>
<tr><th><u>Player X</u></th><th></th><th align="center"><u>Server</u></th><th></th><th><u>Player O</u></th></tr>
<tr><td></td><td>&larr;</td><td align="left">init</td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">init</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td>&larr;</td><td align="left">start(x)</td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">start(o)</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td></td><td align="center">second_move(6,1)</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td></td><td></td><td>&larr;</td><td>6</td></tr>
<tr><td></td><td>&larr;</td><td align="center">third_move(6,1,6)</td><td></td><td></td></tr>
<tr><td align="right">9</td><td>&rarr;</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">next_move(9)</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td></td><td></td><td>&larr;</td><td>6</td></tr>
<tr><td></td><td>&larr;</td><td align="left">next_move(6)</td><td></td><td></td></tr>
<tr><td align="right">5</td><td>&rarr;</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">last_move(5)</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td>&larr;</td><td align="left">win(triple)</td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">loss(triple)</td><td>&rarr;</td><td></td></tr>
<tr><td></td><td>&larr;</td><td align="left">end</td><td></td><td></td></tr>
<tr><td></td><td></td><td align="right">end</td><td>&rarr;</td><td></td></tr>
</table>
</center>

<h4>Language Options</h4>
  
You are free to write your player in any language you wish.

<ol>

<li>
  If you write in Python, you should submit your .py files
  (including <code>agent.py);</code>
  your program will be invoked by:
<pre>
python3 agent.py -p (port)
</pre>

<li>
  If you write in Java, you should submit your .java files
(no .class files).
The main file must be called <code>Agent.java;</code>
your program will be invoked by:
<pre>
java Agent -p (port)
</pre>

<li>
  If you write in C or C++, You should submit your source files (no object files) as well as a
Makefile which, when invoked with the command "make",
will produce an executable called <code>agent;</code>
your program will be invoked by:
<pre>
./agent -p (port)
</pre>

</ol>

<p>
If you wish to write in some other language, let us know.

<h4>Starter Code</h4>

Two types of starter code are provided.
The
<a href="https://www.cse.unsw.edu.au/~cs3411/24T1/hw3/src/">src</a> directory contains a minimally functioning agent in each language which connects to the socket
and plays random moves <code>(agent.py, Agent.java, agent.c).</code>
The directory <a href="https://www.cse.unsw.edu.au/~cs3411/24T1/code/ttt/">code/ttt</a>
contains a standalone program in each language which plays normal (single board) tic-tac-toe
and chooses its moves via alpha-beta search
<code>(ttt.py, ttt.java, ttt.c).</code>

<p>
  Note: You are free to use some method other than alpha-beta search if you wish.
  The starter code is simply meant to provide you with one viable option.

<h4>Testing Your Code</h4>

To play two computer programs against each other,
you may need to open three windows.
For example, to play <code>agent</code> against <code>lookt</code>
using port <code>54321,</code> type as follows:

<pre>
  window 1:  ./servt -p 54321
  window 2:  ./agent -p 54321
  window 3:  ./lookt -p 54321
</pre>

(Whichever program connects first will play X;
the other program will play O.)<br>

You can alternatively use the shell script <code>playt.sh,</code> and provide the executables
and port number as command-line arguments. Here are some examples:

<pre>
./playt.sh ./agent ./lookt 12345
./playt.sh "java Agent" ./lookt 12346
./playt.sh "python3 agent.py" ./lookt 12347
</pre>

The strength of <code>lookt</code> can be adjusted by specifying a maximum search depth
(default value is 9; reasonable range is 1 to 18), e.g.

<pre>
./playt.sh "python3 agent.py" "./lookt -d 6" 31415
</pre>

<h4>Question</h4>

<p>
At the top of your code, in a block of comments,
you must provide a brief answer (one or two paragraphs)
to this Question:
<blockquote>
Briefly describe how your program works, including any algorithms
and data structures employed, and explain any design decisions
you made along the way.
</blockquote>

<h4>Groups</h4>

This assignment may be done individually, or in groups of two students.
Groups are determined by an SMS field called <code>pair3</code>.

Every student has initially been assigned a unique <code>pair3</code> which is
<code>"h"</code> followed by their student ID number, e.g. <code>h1234567</code>.

<ol type="1">
<li>
  If you plan to complete the assignment individually, you don't need to
  do anything (but, if you do create a group with only you as a member,
  that's ok too).
<li>
  If you wish to form a pair, you should go to the
  <a href="https://webcms3.cse.unsw.edu.au/COMP3411/24T1/">WebCMS page</a>
  and click on "Groups" in the left hand column, then click "Create".

Click on the menu for "Group Type" and select "pair". After creating
a group, click "Edit", search for the other member, and click "Add".
WebCMS assigns a unique group ID to each group, in the form of
<code>"g"</code> followed by six digits (e.g. <code>g012345</code>).
We will periodically run a script to load these values into SMS.

</ol>
  
<h4>Submission</h4>

You should submit by typing:

<p>
<tt>give cs3411 hw3 ...</TT>
<p>
Remember to include all necessary files in your submission
(including the one with the answer to the Question).
<p>
You can submit as many times as you like &ndash; later submissions
will overwrite earlier ones. You can check that your submission
has been received by using the following command:
<P>
<tt>3411 classrun -check</tt>
<P>
The submission deadline is Friday 19 April, 10 pm.<br>
5% penalty will be applied to the mark
for every 24 hours late after the deadline, up to a maximum of 5 days
(in accordance with UNSW policy).
<p>
Additional information may be found in the
<a href="faq.shtml">FAQ</a>
and will be considered as part of the specification for the project.
<P>
Questions relating to the project can also be posted to the
Forum on WebCMS.
<p>
If you have a question that has not already been answered on the FAQ
or the Forum, you can email it to
<code>cs3411@cse.unsw.edu.au</code>

<h4>Marking scheme</h4>

<ul>
<li>10 marks for performance against a number of pre-defined opponents.
<li>&nbsp;6 marks for Algorithms, Style, Comments and answer to the Question
</ul>
You should always adhere to good coding practices and style.
In general, a program that attempts a substantial
part of the job but does that part correctly
will receive more marks than one attempting to do
the entire job but with many errors.
