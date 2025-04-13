import random
import time
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

    def qacwb_hash(self, message_bytes: bytes, theta1: float, theta2: float):
        """Implements the Controlled Alternate Quantum Walk-based Block Hash."""
        self.bstr = message_bytes
        self.theta1 = theta1 
        self.theta2 = theta2
        self.N = len(message_bytes)  # Number of positions (2^q)
        self.k = 8   # Number of bits per position for hash output
        self.Q = int(np.log2(self.N)) # number of qubits
        self.T = self.N*self.k//self.Q   # Number of steps (entangling layers)

        # Convert bytes to bitstring
        full_message_bits = ''.join(f'{byte:08b}' for byte in message_bytes)

        # Step 1: Create initial state
        qc, pos, coin = self.create_initial_state(self.N, message_bytes)

        # Global Unitary
        for t in range(self.T):
            step_msg = full_message_bits[t * self.Q:(t + 1) * self.Q]
            for idx, bit in enumerate(step_msg):
                # C(t)
                theta = theta1 if bit == '0' else theta2
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

    def main(self):
        # Example usage:
        message = b'\xa3\xb1\xc4\xd5\xe6\xf7\x89\x0a\x1b\x2c\x3d\x4e\x5f\x60\x71\x82\x93\xa4\xb5\xc6\xd7\xe8\xf9\xa0\xb1\xc2\xd3\xe4\xf5\x06\x17\x28'

        theta1 = np.arccos(3/5)  # Sample values in (0, pi/2)
        theta2 = np.arccos(8/17)

        random.seed(8675309)
        start = time.time()
        runs =1
        for _ in range(runs):
            randbytes = random.randbytes(32) # or message
            hash_output = self.qacwb_hash(randbytes, theta1, theta2)
            print(f"Hash (bytes): {hash_output}")
            print(f"As list of ints: {[int(b) for b in hash_output]}")
            print(f"Sorted: {sorted([int(b) for b in hash_output])}")

        elapsed = time.time()-start
        print(f"Avg time to run ({runs} runs): {elapsed/runs}")


def coin_operator(theta):
        """Returns a 2x2 coin unitary matrix with parameter theta."""
        return np.array([
            [np.cos(theta), np.sin(theta)],
            [np.sin(theta), -np.cos(theta)]
        ])
