# ProofNumber-Search
Implementation of Proof-Number search variants in Python

## Proof-Number Search
Proof-Number search (PNS) is a best-first tree search algorithm applied to determine the definite value of AND/OR trees. PNS does not require domain knowledge, only terminal positions need to be recognized.
PNS can be used to solve games and endgame positions.

## PN*
PN* is a variant of PNS, which transforms the best-first approach to a depth-first search. PN* applies iterative deepening as a means to solve for memory problems that can arise in PNS, which keeps the entire tree in memory.
Not only does PN* apply multiple iterative deepening at the root node but also at all interior OR nodes.

## PDS
Proof-number and Disproof-number search (PDS) is an extension to the PN* algorithm.
PDS is a depth-first multiple iterative-deepening algorithm and uses *pn* and *dpn* to set thresholds for the search process. By using thresholds for *dpn*, PDS extends PN* in not only performing multiple iterative deepening at OR nodes but also at AND nodes. *pn* and *dpn* thresholds are given to a node and the subtree is searched while *pn* and *dpn* are within the thresholds. 

## df-pn
Another depth-first variant of PNS is depth-first proof-number search (df-pn). Unlike in PN* and PDS, no iterative deepening is performed at the root node.
df-pn uses thresholds for *pn* and *dpn*. *pn* thresholds are called *pnt* and *dpn* thresholds *dnt*.
df-pn initializes *pnt* and *dnt* with infinity and searches subtrees within the thresholds. The search terminates when a solution to the tree has been found.
