# Python Code Documentation

This is a readme for running our python code. To see our full report, please see our [writeup](http://./Casekit_Writeup.pdf).

### main.py

This is our submitted code as per the instructions. In it we define the QuantumHasher class, with a function qacwb\_hash to hash a bytestring with a quantum circuit using our implementation of Quantum Walks for block hashing. Thus, to utilize our hashing function, call the following: `QuantumHash().qacwb_hash(bytestring, thetas)`

To hash a bitstring, you must first convert it to bytes. Or, you can create a bytestring right away. We refer you to our `main()` method in QuantumHash to see it in action. `random.randbytes(32)` will suffice.

The function takes a list of theta values. It is imperative that you give a list of eight theta values in the set (0, pi/4) U (pi/4, pi/2). Otherwise, the code will not work. Again, see our `main()` method for reference.

FOR THE OPTIONAL CHALLENGE TO DEFAULT TO 256-bit STRING: run `QuantumHash().qacwb_hash(bytestring, thetas, hash_input=True)`
This is an optional parameter that defaults to false - in other words, normal implementation.

### proof\_of\_correctness.py

Obviously this is not a rigorous proof. But it suffices to demonstrate our algorithm's efficacy and security. We used it to generate our plot in the writeup, as well as for generating entropy values. You may modify the theta values and trials to your liking. One circuit for a 256-bit/32-byte string takes about 0.2 seconds to run. Expect 1000 hashes to take a minute or so. We recommend running  `determinism` and `entropy_and_collisions` separately to neatly return your data, and to return in a shorter time for each (or perhaps run in parallel).

Additionally, we perform an avalanche analysis of our hash function, where we were able to demonstrate a 49% change in the resulting hash for every bit that is changed. This is done in the avalanche function, where N decides the number of shots. 

### test\_qhash.py

Here we copy-pasted proof of correctness and modified it for testing qHash. Simply run the file to get our results.  

### All others
Artifacts of accidentally pushing that I can't get rid of in time. Please ignore qHash.py for example, it is the same as the original.
