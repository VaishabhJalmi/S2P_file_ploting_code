import skrf as rf
import matplotlib.pyplot as plt

# List of S2P file paths
s2p_files = [
    r'C:\Users\vaish\OneDrive\Documents\projects\Test_Python\11W_POLE_TEST_EVM\test2H.s2p',
    r'C:\Users\vaish\OneDrive\Documents\projects\Test_Python\11W_POLE_TEST_EVM\testH1.s2p',
    r'C:\Users\vaish\OneDrive\Documents\projects\Test_Python\11W_POLE_TEST_EVM\test2V.s2p',
    r'C:\Users\vaish\OneDrive\Documents\projects\Test_Python\11W_POLE_TEST_EVM\testV1.s2p',
    # Add more file paths as needed
]

# Corresponding labels for each file
labels = [
    'Before 1',
    'after 1',
    'Before 2',
    'after 2',
    # Add more labels as needed
]

# Plot S11 parameters
plt.figure(figsize=(10, 6))

# Loop through each file and corresponding label
for file, label in zip(s2p_files, labels):
    network = rf.Network(file)  # Load the S2P file

    # Plot S11
    network.plot_s_db(m=0, n=0, label=label)

# Set title and labels
plt.title('S11 Parameters (dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
