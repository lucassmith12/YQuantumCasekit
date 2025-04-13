import random
import time
from typing import List
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import UnitaryGate, Initialize
import numpy as np

class QuantumHash():

    def create_initial_state(self, N, bstr):
        """Create initial state |0> (uniform superposition over positions)"""
        pos = QuantumRegister(self.Q, 'pos')
        coin = QuantumRegister(1, 'coin')
        qc = QuantumCircuit(pos, coin)

        # Create complex amplitudes and normalize
        values = [int(b) for b in bstr[:N]]
        alpha = np.array([(v + 1j * (v % 7)) for v in values], dtype=complex)
        alpha /= np.linalg.norm(alpha)

        init_gate = Initialize(alpha)
        init_gate.label = 'custom_init'
        qc.append(init_gate, pos)

        return qc, pos, coin

    def qacwb_hash(self, message_bytes: bytes, thetas: List[float], hash_input=False):
        """
        Implements the Controlled Alternate Quantum Walk-based Block Hash.
        :thetas: a list of 8 values in radians satisfying  0 < theta < pi/2, theta != pi/4 
        """
        if hash_input: message_bytes = self.const_hash(message_bytes, thetas)

        self.bstr = message_bytes 
        self.thetas = thetas
        self.N = len(message_bytes)  # Number of positions (2^q)
        self.k = 8   # Number of bits per position for hash output
        self.Q = int(np.log2(self.N)) # number of qubits
        self.T = self.N//self.Q   # Number of steps (entangling layers)

        # Convert bytes to bitstring

        # Step 1: Create initial state
        qc, pos, coin = self.create_initial_state(self.N, message_bytes)

        # Global Unitary
        for t in range(self.T):
            step_msg = message_bytes[t:(t + 1) ]
            for idx, byte in enumerate(step_msg):
                # C(t)
                theta = thetas[byte % 8]
                unitary = UnitaryGate(coin_operator(theta), label=f'Cθ={theta:.2f}')
                qc.append(unitary.control(1), [pos[idx], coin[0]])
                # S_idx
                qc.cx(coin[0], pos[idx])

        # Step 4: Get final state vector
        state = Statevector.from_instruction(qc)
        probs = state.probabilities_dict()

        # Step 5: Convert probabilities into hash output (bytes)
        hash_bytes = bytearray()
        for key in sorted(probs):
            p = probs[key]
            scaled = int(p * (10**self.k)) % (2**self.k)
            hash_bytes.append(scaled)
            if len(hash_bytes) == self.N:
                break
        return bytes(hash_bytes)  # Final hash as bytes

    def const_hash(self, message_bytes: bytes, thetas: List[float]):                        #CHALLENGE
        buffer = self.qacwb_hash(message_bytes[:32], thetas)                                #CHALLENGE
        for l in range(1,int(np.floor(len(message_bytes)/32))):                             #CHALLENGE
            buffer = bytes(x ^ y for x, y in zip(buffer, message_bytes[32*l:32*l+32]))      #CHALLENGE
            buffer = self.qacwb_hash(buffer, thetas)                                        #CHALLENGE
        return buffer                                                                       #CHALLENGE

    def main(self):
        # Example usage:
        message = b'\xb3\xb1\xc4\xd5\xe6\xf7\x89\x0a\x1b\x2c\x3d\x4e\x5f\x60\x71\x82\xc3\xa4\xb5\xc6\xd7\xe8\xf9\xa0\xb1\xc2\xd3\xe4\xf5\x06\x17\x28'
        thetas = [
            np.arccos(1/np.sqrt(2)),
            np.arccos(3/5),
            np.arccos(4/5),
            np.arccos(5/13),
            np.arccos(7/10),
            np.arccos(8/17),
            np.arccos(2/3),
            np.arccos(5/8)
        ]

        random.seed(8675309)
        start = time.time()
        runs = 1
        for _ in range(runs):
            # randbytes = random.randbytes(32) # can be used instead of message below
            hash_output = self.qacwb_hash(message, thetas)
            print(f"Hash (bytes): {hash_output}")
            print(f"As list of ints: {[int(b) for b in hash_output]}")
            print(f"Sorted: {sorted([int(b) for b in hash_output])}")

        for _ in range(runs):                                                           #CHALLENGE
            randbytes = random.randbytes(1024) # can be used instead of message below   #CHALLENGE
            hash_output = self.const_hash(randbytes, thetas)                            #CHALLENGE
            print(f"Hash (bytes): {hash_output}")                                       #CHALLENGE
            print(f"As list of ints: {[int(b) for b in hash_output]}")                  #CHALLENGE
            print(f"Sorted: {sorted([int(b) for b in hash_output])}")                   #CHALLENGE

        elapsed = time.time()-start
        print(f"Avg time to run ({runs} runs): {elapsed/runs}")


def coin_operator(theta):
        """Returns a 2x2 coin unitary matrix with parameter theta."""
        return np.array([
            [np.cos(theta), np.sin(theta)],
            [np.sin(theta), -np.cos(theta)]
        ])

if __name__ == "__main__":
    QuantumHash().main()