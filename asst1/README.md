<H3 align=center>Assignment 1 &ndash; Bridge Puzzle</H3>
<p align=center>
Due: Friday 15 March, 10pm
<br align=center>
Marks: 12% of final assessment
<h4>
Specification
</h4>
This project is based on a popular puzzle,
variously known as "Hashiwokakero",
"Hashi" or "Bridges".
You will need to write a program to solve this puzzle,
and provide a brief description of the algorithm and
data structures you have used.

The input to your program will be a rectangular array
of numbers and dots, for example:

<pre>
.1...6...7....4.4.2.
..4.2..2...3.8...6.2
.....2..............
5.c.7..a.a..5.6..8.5
.............2......
...5...9.a..8.b.8.4.
4.5................3
....2..4..1.5...2...
.2.7.4...7.2..5...3.
............4..3.1.2
</pre>

Each number represents an "island",
while the dots represent the empty space (water) between the islands.
Numbers larger than 9 are indicated by <tt>'a'</tt> (10), <tt>'b'</tT> (11)
or <tt>'c'</tt> (12).
The aim is to connect all the islands with a network of
bridges, satisfying these rules:

<ol>
<li> all bridges must run horizontally or vertically
<li> bridges are not allowed to cross each other, or other islands
<li> there can be no more than three bridges connecting any pair of islands
<li> the total number of bridges connected to each island must
be equal to the number on the island
</ol>

For example, after reading the 10-line input above,
your program might produce this output:

<pre>
 1---6EEE7====4=4=2 
  4-2" 2 " 3E8EEE6 2
  # |2 " "   "   # "
5EcE7EEaEa==5"6EE8=5
" #    " #  #2#    |
" #5===9Ea--8=bE8E4|
4=5#   " #  " # " |3
   #2==4 #1-5 # 2 |"
 2=7=4===7=2" 5===3"
            4==3-1 2
</pre>

Note that single bridges are indicated by the characters
<tt>'-'</tt> or <tt>'|'</tt>, pairs of bridges
by <tt>'='</tt> or <tt>'"'</tt> and triples by
<tt>'E'</tt> or <tt>'#'</tt>, depending on whether they run horizontally or vertically.
Water between bridges and islands is indicated by
space characters <tt>' '</tt>.<br>
In some cases, there may be many solutions,
in which case your program should only print one solution.
More details about the puzzle can be found on this
<a href="http://en.wikipedia.org/wiki/Hashiwokakero">Wikipedia
page</a>. Note, however, that our version allows up to 3 bridges
instead of 2; also, we do not insist that the entire graph be connected.

<h4>Tools</h4>

An executable file called <code>bridgen</code> is provided in the
<a href="./tools/"><code>tools</code></a> directory
which can be used to generate sample data of any specified size
(type <code>bridgen -help</code> for details).
Another executable called <code>bridgecheck</code>
is also provided, to help you test the validity of your solutions
(see <a href="./faq.shtml">FAQ</a> for details).

<h4>Questions</h4>

At the top of your code, in a block of comments, you must
provide a <em>brief</em> answer (one or two paragraphs) to
this Question:

<blockquote>
Briefly describe how your program works, including any algorithms
and data structures employed, and explain any design decisions
you made along the way.
</blockquote>

<h4>Language Options</h4>

You are free to write the code in a language of your choosing.

<ul>
<li>
  If you write in C, C++, or another compiled languge,
  your program will be invoked by: <code>./hashi</code><br>
You should submit your source files (no object files) as well as a
<code>Makefile</code> which, when invoked with the command <code>make</code>,
will produce an executable called <code>hashi</code>

<li>
  If you write in Python, your program will be invoked by: <code>./hashi.py</code><br>
  You should submit your <code>.py</code> files
  (including <code>hashi.py</code>).<br>
  The first line of your
  code must specify which version of Python you are using, e.g.
<code>#!/usr/bin/python3</code>

<li>
If you write in Java, your program will be invoked by:
<code>java Hashi</code><br>
You should submit your <code>.java</code> files
(no <code>.class</code> files).<br>
The main file must be called <code>Hashi.java</code>
<p>

<li> If you wish to write in some language not covered by the
    above options, let us know and we will try to accommodate you.
  
<li> Regardless of the language, you are not allowed to use
  dedicated constraint programming packages like
  <code>python-constraint</code>, etc.
  You are expected to implement the search method(s) yourself.

</ul>
<p>

<h4>Submission</h4>

You should submit by typing

<p>
<tt>give cs3411 hashi ...</TT>
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
The submission deadline is Friday 15 March, 10 pm.<br>
5% penalty will be applied to the mark
for every 24 hours late after the deadline, up to a maximum of 5 days
(in accordance with UNSW policy).
<p>
Additional information may be found in the
<a href="faq.shtml">FAQ</a>
and will be considered as part of the specification for the project.
<P>
Questions relating to the project can also be posted to the
Forums on WebCMS.
<p>
If you have a question that has not already been answered on the FAQ
or the Forums, you can email it to
<code>cs3411@cse.unsw.edu.au</code>

<h4>Assessment</h4>

Your program will be tested on a series of sample inputs
of successively increasing size and difficulty.
There will be:

<ul>
<li>6 marks for functionality (automarking)
<li>4 marks for your algorithm and implementation
<li>2 marks for answer to the Question
</ul>
You should always adhere to good coding practices and style.
In general, a program that attempts a substantial
part of the job but does that part correctly
will receive more marks than one attempting to do
the entire job but with many errors.
