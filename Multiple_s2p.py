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

# Plot S-parameters
fig, ax = plt.subplots(2, 2, figsize=(12, 8))

# Define titles for subplots
titles = ['S11 (dB)', 'S21 (dB)', 'S12 (dB)', 'S22 (dB)']

# Loop through each file
for file in s2p_files:
    network = rf.Network(file)  # Load the S2P file

    # Plot each S-parameter
    network.plot_s_db(m=0, n=0, ax=ax[0, 0], label=file)
    network.plot_s_db(m=1, n=0, ax=ax[0, 1], label=file)
    network.plot_s_db(m=0, n=1, ax=ax[1, 0], label=file)
    network.plot_s_db(m=1, n=1, ax=ax[1, 1], label=file)

# Set titles for subplots
for i, axis in enumerate(ax.flat):
    axis.set_title(titles[i])
    axis.legend()

# Adjust layout
#plt.tight_layout()
plt.show()