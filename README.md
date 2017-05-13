PRE REQUISITES :-
-----------------

1) Blockchain.info python API package.
2) python graph-tool package.

Bitcoin_v1
----------
1) Preliminary Codes.
2) Used to dump information related to high valued transactions, taking 25 blocks at a time. (~ 1 hour data).
3) Shamir's assumption has been used to dump data, and create entity graph.
4) First graph was created, then high value transactions were filtered out. Union find algorithm to create graph was quite costly operation.


Bitcoin_v2
----------
1) Efficient Code : First Filtering out High valued transactions and then creation of graphs.
2) Processing of data for (~100 blocks) was happening in roughly 2hours.

First, Dump the blockdata using dumpBLocks.py in testdata folder, and then do the processing.