import skrf as rf
import matplotlib.pyplot as plt

# Turn off interactive mode
plt.ioff()

# Load the S2P file
network = rf.Network(r'C:\Users\vaish\OneDrive\Documents\projects\Test_Python\test2H.s2p')  # Use raw string to avoid unicode escape error

# Plot S-parameters
fig, ax = plt.subplots(2, 2, figsize=(12, 8))

# S11
network.plot_s_db(m=0, n=0, ax=ax[0, 0])
ax[0, 0].set_title('S11 (dB)')

# S21
network.plot_s_db(m=1, n=0, ax=ax[0, 1])
ax[0, 1].set_title('S21 (dB)')

# S12
network.plot_s_db(m=0, n=1, ax=ax[1, 0])
ax[1, 0].set_title('S12 (dB)')

# S22
network.plot_s_db(m=1, n=1, ax=ax[1, 1])
ax[1, 1].set_title('S22 (dB)')

# Adjust layout
plt.tight_layout()
plt.show()
