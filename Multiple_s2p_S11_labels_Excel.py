import skrf as rf
import pandas as pd
import matplotlib.pyplot as plt

# List of S2P file paths add your file path
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
    'After 1',
    'Before 2',
    'After 2',
    # Add more labels as needed
]

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Plot S11 parameters
plt.figure(figsize=(10, 6))

# Loop through each file and corresponding label
for file, label in zip(s2p_files, labels):
    network = rf.Network(file)  # Load the S2P file
    s11_db = network.s_db[:, 0, 0]  # Extract S11 in dB
    frequency = network.f  # Extract frequency

    # Create a DataFrame for the current file
    data = pd.DataFrame({
        'Frequency (Hz)': frequency,
        f'S11 (dB) - {label}': s11_db
    })

    # Merge with the main DataFrame
    if all_data.empty:
        all_data = data
    else:
        all_data = pd.merge(all_data, data, on='Frequency (Hz)', how='outer')

    # Plot S11
    network.plot_s_db(m=0, n=0, label=label)

# Set title and labels
plt.title('Plots of Before After vibration')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

# Export all data to an Excel file
all_data.to_excel('s11_parameters.xlsx', index=False)
