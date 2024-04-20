#!/usr/bin/python3

import sys

"""
We first start by paring all adjacent islands in a list. This is the functionality of the "scanBridge" function.
The data structure below show how we manage the data:

bridge = {
  "start": (i, j),
  "end": (ni, nj),
  "type": "H" | "V",
  "n1": (i, j),
  "n2": (ni, nj),
}

We use dictionary to keep track of all pairs. The "start" key represents one island and the "end" key represents its adjacent island.
The "n1" and "n2" keys are the same as "start" and "end" respectively but we do it this way to avoid duplicated code when recursively calling.
With the "type" key represents whether those islands are connected vertically (V) or horizontally (H).

One adjacent dictionary is also contructed to accelerate the minimum and maximum degree finding for each bridge in later steps.
Minimum degree is the least number of extra bridges needed to connect 2 islands while maximum degree is the maximum number of
extra bridges needed.

{
  "Island A": ["Island B", "Island C"],
  "Island B": ["Island A"],
  "Island C": ["Island A"]
}

The neighbours of each island could be easily found with this dictionary.

After that, we have two main functions working behind the screen. Both about how we choose to construct the bridges connecting islands.

The first is the "constructCertaintyBridges" function. It will construct only certainty bridges,
this means the bridges that can only be constructed in that certain way (no other possible options).

The second main function is the "backtrack" function. This will come whenever there is no more certainty connections left
(and the puzzle isn't complete). Leaving some islands that have multiple possible ways to connect to the others.
Then what we can only do is to pick one of those possible bridges to construct and go on from there.
Constructing certainty bridges again until none left, and redo the process whenever face muliple possible bridges.
This is the main cost of this algorithm's time complexity. And retry the whole thing whenever it fails to configure the islands.
Doing it this way, we can only try to fail the configuration as fast as possible to minimize the cost.

Both of "constructCertaintyBridges" and backtrack make use of 2 main support fuctions; "getMaxRemainingDree" and "getMinRemainingDegree".
"GetMaxRemainingDree" helps finding the current maximum number of extra bridges possible to construct from the island.
And "getMinRemainingDegree" helps finding the least number of extra bridges needed to connect two adjacent islands given.
With those values known, we can tell whether there are possible certainty bridges by checking whether the those two values are the same.
Note that we also check whether there is any bridges across the pair's connection to minimize the cost of this algorithm
because we cannot have 2 bridges crosing each other. Fail early to not do unneccessary configuration.

In addition, when we were trying to minimize the cost, we came up with an idea to priority the bridges.
Which bridges have more potential to fail and end the "backtrack" early.
In the recurssion, each time, the first bridge in the list will be popped out for checking.
We find the possible degree of current bridge and set new recursions.
Before each recursion, we sort the remaining bridges list by the number of possible degrees of the bridge (max degree - min degree).
In this way the bridges which are easier to solve are processed first.
All of those are in the "sortPriority" function.

"""

# Mapping number of population
POPULATION_MAP = {
  '1': 1,
  '2': 2,
  '3': 3,
  '4': 4,
  '5': 5,
  '6': 6,
  '7': 7,
  '8': 8,
  '9': 9,
  'a': 10,
  'b': 11,
  'c': 12,
}

# Mapping type of bridges to the number of bridges
VERTICAL_BRIDGE_TYPE = {
  '|': 1,
  '"': 2,
  '#': 3,
}

HORIZONTAL_BRIDGE_TYPE = {
  '-': 1,
  '=': 2,
  'E': 3,
}

# Mapping number of bridges to the type of bridges
HORIZONTAL_BRIDGE_NUMBER = {
  0: '.',
  1: '-',
  2: '=',
  3: 'E',
}

VERTICAL_BRIDGE_NUMBER = {
  0: '.',
  1: '|',
  2: '"',
  3: '#',
}

################################################## Algorithm ##################################################

# Reading input from the terminal and store in a 2D array
def scanMap():
  puzzle = []
  for line in sys.stdin:
    row = []
    for ch in line:
      if ch != '\n':
        row.append(ch)
    puzzle.append(row)

  return puzzle

# Print out the puzzle
def printPuzzle(puzzle):
  for i in range(len(puzzle)):
    for j in range(len(puzzle[0])):
      if puzzle[i][j] == '.':
        print(' ', end = '')
      else:
        print(puzzle[i][j], end='')
    print()

# Get the current number of bridges from the island
def getCurrNumBridges(i, j, puzzle):
  numBridges = 0
  rows = len(puzzle)
  cols = len(puzzle[0])
  if i > 0:
    numberOfBridges = puzzle[i - 1][j]
    if numberOfBridges in VERTICAL_BRIDGE_TYPE:
      numBridges += VERTICAL_BRIDGE_TYPE[numberOfBridges]
  if i < rows - 1:
    numberOfBridges = puzzle[i + 1][j]
    if numberOfBridges in VERTICAL_BRIDGE_TYPE:
      numBridges += VERTICAL_BRIDGE_TYPE[numberOfBridges]
  if j > 0:
    numberOfBridges = puzzle[i][j - 1]
    if numberOfBridges in HORIZONTAL_BRIDGE_TYPE:
      numBridges += HORIZONTAL_BRIDGE_TYPE[numberOfBridges]
  if j < cols - 1:
    numberOfBridges = puzzle[i][j + 1]
    if numberOfBridges in HORIZONTAL_BRIDGE_TYPE:
      numBridges += HORIZONTAL_BRIDGE_TYPE[numberOfBridges]

  return numBridges

# Checking whether the island has bridges equal to the number of its population
def isCompleteIsland(i, j, puzzle):
  population = puzzle[i][j]
  if population not in POPULATION_MAP:
    return True

  return POPULATION_MAP[population] == getCurrNumBridges(i, j, puzzle)

# Checking whether the solution is found
def isPuzzleComplete(puzzle):
  for i, row in enumerate(puzzle):
    for j, cell in enumerate(row):
    # Checking each island one by one
      if isCompleteIsland(i, j, puzzle) == False:
        return False
  return True

# Scan the puzzle to gather all bridges and keep track of all bridges and the adjacency list
def scanBridge(puzzle):
  adj = {}

  # Add horizontal bridges and edges
  horizontalBridges = []
  for i, row in enumerate(puzzle):
    l = []
    for j, population in enumerate(row):
      if population in POPULATION_MAP:
        l.append(j)
    for index in range(len(l) - 1):
      left = l[index]
      right = l[index + 1]
      if right != left + 1:
        n1 = (i, left)
        n2 = (i, right)
        horizontalBridges.append({
          "start": (i, left + 1),
          "end": (i, right - 1),
          "type": "H",
          "n1": n1,
          "n2": n2,
        })
        if n1 in adj:
          adj[n1].append(n2)
        else:
          adj[n1] = [n2]
        if n2 in adj:
          adj[n2].append(n1)
        else:
          adj[n2] = [n1]

  # Add verticle bridges and edges
  verticalBridges = []
  j = 0
  while j in range(len(puzzle[0])):
    l = []
    i = 0
    while i in range(len(puzzle)):
      population = puzzle[i][j]
      if population in POPULATION_MAP:
        l.append(i)
      i += 1
    for index in range(len(l) - 1):
      top = l[index]
      bottom = l[index + 1]
      if bottom != top + 1:
        n1 = (top, j)
        n2 = (bottom, j)
        verticalBridges.append({
          "start": (top + 1, j),
          "end": (bottom - 1, j),
          "type": "V",
          "n1": n1,
          "n2": n2,
        })
        if n1 in adj:
          adj[n1].append(n2)
        else:
          adj[n1] = [n2]
        if n2 in adj:
          adj[n2].append(n1)
        else:
          adj[n2] = [n1]

    j += 1

  return horizontalBridges, verticalBridges, adj

# Checking whether there are any bridges in the way of given bridge
def hasBridgesAcrossBridge(puzzle, bridge):
  if bridge["type"] == "H":
    row, left = bridge["start"]
    row, right = bridge["end"]
    while left <= right:
      if puzzle[row][left] != ".":
        return True
      left += 1
  else:
    top, col = bridge["start"]
    bottom, col = bridge["end"]
    while top <= bottom:
      if puzzle[top][col] != ".":
        return True
      top += 1
  
  return False

# Get the current maximum number of extra bridges possible to construct from the island
def getMaxRemainingDegree(i, j, puzzle):
  population = puzzle[i][j]

  return POPULATION_MAP[population] - getCurrNumBridges(i, j, puzzle)

# Checking whether the islands are adjacent without having any bridges in the way
def hasBridgesAcrossIslands(i, j, ni, nj, puzzle):
  if i == ni:
    if j < nj:
      j += 1
      while j < nj:
        if puzzle[i][j] != ".":
          return False
        j += 1
    else:
      nj += 1
      while nj < j:
        if puzzle[i][nj] != ".":
          return False
        nj += 1
  else:
    if i < ni:
      i += 1
      while i < ni:
        if puzzle[i][j] != ".":
          return False
        i += 1
    else:
      ni += 1
      while ni < i:
        if puzzle[ni][j] != ".":
          return False
        ni += 1
  
  return True

# Get the least number of extra bridges needed to connect 2 islands
def getMinRemainingDegree(i, j, ni, nj, puzzle, maxDegree, adj):
  degree = 0
  for nbr in adj[(i, j)]:
    if nbr != (ni, nj) and hasBridgesAcrossIslands(i, j, nbr[0], nbr[1], puzzle):
      nodeMax = min(3, getMaxRemainingDegree(nbr[0], nbr[1], puzzle))
      degree += nodeMax

  return maxDegree - degree

# Constructing a bridge connecting 2 adjacent islands
def constructBridge(puzzle, bridge, typeOfBridge):
  if bridge["type"] == "H":
    row, left = bridge["start"]
    row, right = bridge["end"]
    while left <= right:
      puzzle[row][left] = HORIZONTAL_BRIDGE_NUMBER[typeOfBridge]
      left += 1
  else:
    top, col = bridge["start"]
    bottom, col = bridge["end"]
    while top <= bottom:
      puzzle[top][col] = VERTICAL_BRIDGE_NUMBER[typeOfBridge]
      top += 1

# Constructing bridges that are absolutely necessary (only one possible choice)
def constructCertaintyBridges(puzzle, bridges, adj, originalBridges):
  for bridge in originalBridges:
    # Cannot add a bridge if there is already a bridge
    # or if there is one cutting off the connection of two adjacent islands
    if hasBridgesAcrossBridge(puzzle, bridge):
      continue
    else:
      # Start preprocessing
      i1, j1 = bridge["n1"]
      i2, j2 = bridge["n2"]
      
      max1 = getMaxRemainingDegree(i1, j1, puzzle)
      max2 = getMaxRemainingDegree(i2, j2, puzzle)
      maxDegree = min(max1, max2, 3)
      
      min1 = getMinRemainingDegree(i1, j1, i2, j2, puzzle, max1, adj)
      min2 = getMinRemainingDegree(i2, j2, i1, j1, puzzle, max2, adj)
      minDegree = max(min1, min2, 0)

      if maxDegree == minDegree and minDegree != 0:
        constructBridge(puzzle, bridge, minDegree)
        if bridge in bridges:
          bridges.remove(bridge)

        return True

      if maxDegree == minDegree and minDegree == 0:
        if bridge in bridges:
          # Removing constructed bridges to reduce the iteration cost
          bridges.remove(bridge)

          return True

  return False

# Create a copy of an array of a puzzle
# (Came up with our own instead of using a library to reduce the cost of recursion)
def deepCopyPuzzle(puzzle):
  copied = []
  for row in puzzle:
    copied.append([item for item in row])
  return copied

# Create a copy of an array of bridges
# (Came up with our own instead of using a library to reduce the cost of recursion)
def deepCopyBridges(bridges):
  copied = []
  for bridge in bridges:
    copiedBridge = {}
    for key, value in bridge.items():
      copiedBridge[key] = value
    copied.append(copiedBridge)
  return copied

# Constructing all certainty bridges then uncertainty bridges
# and configured all the islands until the puzzle is complete
# If fail, start constructing from new certainty bridges and repeat the process
def backtrack(currPuzzle, bridges, adj, originalBridges):
  # Start by constructing only certainty bridges first
  while (constructCertaintyBridges(currPuzzle, bridges, adj, originalBridges)):
    continue
  
  # Stop when a solution is found
  if isPuzzleComplete(currPuzzle):
    printPuzzle(currPuzzle)
    exit()

  # End of failed branches
  if len(bridges) == 0:
    return

  # Get current bridge
  bridge = bridges.pop(0)

  # Start backtracking
  i1, j1 = bridge["n1"]
  i2, j2 = bridge["n2"]
  
  max1 = getMaxRemainingDegree(i1, j1, currPuzzle)
  max2 = getMaxRemainingDegree(i2, j2, currPuzzle)
  maxDegree = min(max1, max2, 3)
  
  min1 = getMinRemainingDegree(i1, j1, i2, j2, currPuzzle, max1, adj)
  min2 = getMinRemainingDegree(i2, j2, i1, j1, currPuzzle, max2, adj)
  minDegree = max(min1, min2, 0)
  
  # Construct none
  if maxDegree >= 0 and minDegree <= 0:
    tmp_puzzle = deepCopyPuzzle(currPuzzle)
    tmpBridges = deepCopyBridges(bridges)
    tmpBridges = sorted(tmpBridges, key=lambda bridge: sortPriority(tmp_puzzle, bridge))
    tmp_adj = adj
    backtrack(tmp_puzzle, tmpBridges, tmp_adj, originalBridges)
  
  # Fail early if the bridge is not valid (crossing other bridges)
  if hasBridgesAcrossBridge(currPuzzle, bridge):
    return
  
  # Backtracking all possible number of bridges (by priority)
  degreeList = [1, 2, 3]
  for degree in degreeList:
    if maxDegree >= degree and minDegree <= degree:
      tmp_puzzle = deepCopyPuzzle(currPuzzle)
      constructBridge(tmp_puzzle, bridge, degree)
      tmpBridges = deepCopyBridges(bridges)
      tmpBridges = sorted(tmpBridges, key=lambda bridge: sortPriority(tmp_puzzle, bridge))
      tmp_adj = adj
      backtrack(tmp_puzzle, tmpBridges, tmp_adj, originalBridges)

# Prioritizing bridges which most likely to fail early (violate our constraints)
# To minimize the iteration cost
def sortPriority(puzzle, bridge):
  i1, j1 = bridge["n1"]
  i2, j2 = bridge["n2"]
  
  max1 = getMaxRemainingDegree(i1, j1, puzzle)
  max2 = getMaxRemainingDegree(i2, j2, puzzle)
  maxDegree = min(max1, max2, 3)
  
  min1 = getMinRemainingDegree(i1, j1, i2, j2, puzzle, max1, adj)
  min2 = getMinRemainingDegree(i2, j2, i1, j1, puzzle, max2, adj)
  minDegree = max(min1, min2, 0)

  return maxDegree - minDegree

# Reorder bridges based on their priority
def reorderBridges(horizontalBridges, verticalBridges, puzzle):
  bridges = horizontalBridges + verticalBridges

  bridges = sorted(bridges, key=lambda bridge: sortPriority(puzzle, bridge))  
  return bridges

if __name__ == '__main__':
  puzzle = scanMap()
  horizontalBridges, verticalBridges, adj = scanBridge(puzzle)
  bridges = reorderBridges(horizontalBridges, verticalBridges, puzzle)
  tmpBridges = deepCopyBridges(bridges)
  backtrack(puzzle, tmpBridges, adj, bridges)
