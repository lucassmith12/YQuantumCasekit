from collections import defaultdict
from main import QuantumHash
import random
import numpy as np

#Modify these to your liking
some_bytes = random.randbytes(32)
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
trials = 1000 
hasher = QuantumHash()


# OUTPUT DETERMINISM #
def determinism():
    """
    Must prove that all inputs are deterministic
    """    
    some_bytes = random.randbytes(32)
    set_out = set([hasher.qacwb_hash(some_bytes, thetas) for _ in range(trials)])
    if len(set_out) > 1:
        raise ValueError(f"ERROR: Inputs not equal:{set_out}")
    return True
    
# ENTROPY PRESERVATION #
def entropy_and_collisions():
    """
    Must show we have high entropy
    """
    from scipy.stats import entropy
    from collections import Counter

    print("Running trials (this may take some time):")
    random_outputs = [hasher.qacwb_hash(random.randbytes(32), thetas) for _ in range(trials)]
    print("Trials complete!")

    byte_vals = b''.join(random_outputs)  # Flatten to a big byte string

    # Bit level
    output_bits = ''.join(bin(int.from_bytes(x, 'big'))[2:].zfill(len(x)*8) for x in random_outputs)
    bit_counts = Counter(output_bits)
    bit_probs = [v / len(output_bits) for v in bit_counts.values()]
    bit_e = entropy(bit_probs, base=2)
    print("Estimated entropy:", bit_e)

    # Byte level
    counts = Counter(byte_vals)
    probs = [count / len(byte_vals) for count in counts.values()]
    byte_e = entropy(probs, base=2)
    print("Estimated byte-level entropy:", byte_e)


    selected_indices = [0, 8, 16, 24, 31]  # Choose the bytes you want to inspect
    
    # Count byte frequencies at each position
    byte_freq = [defaultdict(int) for _ in range(hasher.N)]
    for h in random_outputs:
        for i, b in enumerate(h):
            byte_freq[i][b] += 1

    # Plot histograms for selected byte positions
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(len(selected_indices), 1, figsize=(10, 12), sharex=True)

    for idx, byte_index in enumerate(selected_indices):
        data = byte_freq[byte_index]
        x = list(data.keys())
        y = list(data.values())
        axs[idx].bar(x, y, width=1.0, edgecolor='black')
        axs[idx].set_title(f"Byte Position {byte_index}")
        axs[idx].set_ylabel("Frequency")
        axs[idx].set_xlim(0, 255)

    axs[-1].set_xlabel("Byte Value (0–255)")
    plt.suptitle("Quantum Hash Byte Value Distribution (Selected Byte Positions)", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()

    set_out = set()
    count = 0
    for o in random_outputs:
        if o not in set_out:
            set_out.add(o)
        else:
            count +=1
            print(f"Collision: {o}")
    print(f"Total Collisions: {count}")
    

    
# run one of these two if you just want one or the other due to time constraints
# determinism() 
entropy_and_collisions()




