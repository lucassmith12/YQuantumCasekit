# Python Code Documentation
This is a readme for running our python code. To see our full report, please see our [writeup](./Casekit_Writeup.pdf).

### main.py
This is our submitted code as per the instructions. In it we define the QuantumHasher class, with a function qacwb_hash to hash a bytestring with a quantum circuit using our implementation of Quantum Walks for block hashing. Thus, to utilize our hashing function, call the following:
```QuantumHash().qacwb_hash(bytestring, thetas)```

To hash a bitstring, you must first convert it to bytes. Or, you can create a bytestring right away. We refer you to our ```main()``` method in QuantumHash to see it in action. ```random.randbytes(32)``` will suffice. 

The function takes a list of theta values. It is imperative that you give a list of eight theta values in the set (0, pi/4) U (pi/4, pi/2). Otherwise, the code will not work. Again, see our ```main()``` method for reference.

### proof_of_correctness.py
Obviously this is not a rigorous proof. But it suffices to demonstrate our algorithm's efficacy and security. We used it to generate our plot in the writeup, as well as for generating entropy values. You may modify the theta values and trials to your liking. One circuit for a 256-bit/32-byte string takes about 0.2 seconds to run. Expect 1000 hashes to take a minute or so. We recommend running  ```determinism``` and ```entropy_and_collisions``` separately to neatly return your data, and to return in a shorter time for each (or perhaps run in parallel).

### test_qhash.py
Here we copy-pasted proof of correctness and modified it for testing qHash. Simply run the file to get our results.