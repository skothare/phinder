import pandas as pd  # For reading and processing CSV files
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For creating advanced plots
import itertools  # For generating combinations (fixed undefined variable warning)
from matplotlib.colors import ListedColormap  # For custom colormap

# File paths for the CSV files
moonshot_csv = 'f1_scores_CoVMoonshot.csv'
fresco_csv = 'f1_scores_fresco.csv'

# Benchmark F1 scores for each k value
benchmarks = {
    3: {'Max': 0.680435, 'Mean': 0.4514086},
    4: {'Max': 0.706093, 'Mean': 0.227813},
    5: {'Max': 0.698305, 'Mean': 0.04272389}
}

# Function to calculate the number of unique feature kinds per pharmacophore
def calculate_unique_kinds(df):
    # Group rows by 'json_file' and calculate the number of unique values in 'name'
    unique_kinds = df.groupby('json_file')['name'].nunique().reset_index()
    unique_kinds.columns = ['json_file', 'unique_kinds']
    return unique_kinds

# Function to plot F1 scores with boxplot and swarmplot overlay for a specific dataset (CSV file)
def plot_f1_scores(csv_file, dataset_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Calculate the number of unique feature kinds per json_file
    unique_kinds_df = calculate_unique_kinds(df)

    # Merge the unique_kinds back into the main DataFrame
    df = df.drop_duplicates(subset=['n', 'json_file'])  # Drop duplicate F1 scores
    df = df.merge(unique_kinds_df, on='json_file', how='left')

    # Define a custom reversed color palette for unique kinds (red -> green -> blue with brighter yellow)
    palette = {1: 'gold', 2: 'blue', 3: 'darkred'}

    # Group by `k` values (3, 4, 5) and create a plot for each
    for k in [3, 4, 5]:
        # Filter data for the specific k value
        k_data = df[df['k'] == k]

        # Ensure the data is sorted by `n` for consistent x-axis values
        k_data = k_data.sort_values('n')

        # Create the plot
        plt.figure(figsize=(8, 6))

        # Create a boxplot for F1 scores with `n` on the x-axis
        sns.boxplot(x=k_data['n'], y=k_data['f1_score'], color='lightgray', width=0.6, showfliers=False)

        # Overlay a swarmplot for individual F1 scores, colored by unique kinds
        sns.swarmplot(
            x='n', y='f1_score', hue='unique_kinds', palette=palette, data=k_data, dodge=False, size=4, alpha=0.8, legend=False)

        # Add benchmark lines (Max and Mean)
        plt.axhline(y=benchmarks[k]['Max'], color='darkorange', linestyle='--', label=f'Fragment Max (k={k})')
        plt.axhline(y=benchmarks[k]['Mean'], color='green', linestyle='--', label=f'Fragment Mean (k={k})')

        # Add labels, title, and legend
        plt.xlabel('n Value (Total Features)', fontsize=12)
        plt.ylabel('F1 Score', fontsize=12)
        plt.title(f'F1 Scores for {dataset_name} (k={k})', fontsize=14)

        # Manually adjust legend to include custom color mapping for unique kinds and benchmarks
        legend_labels = {1: '1 Unique Kind', 2: '2 Unique Kinds', 3: '3 Unique Kinds'}
        handles = [plt.Line2D([0], [0], marker='o', color=palette[key], linestyle='', markersize=6) for key in legend_labels]
        benchmark_handles = [
            plt.Line2D([0], [0], color='darkorange', linestyle='--', label=f'Fragment Max (k={k})'),
            plt.Line2D([0], [0], color='green', linestyle='--', label=f'Fragment Mean (k={k})')
        ]
        plt.legend(handles + benchmark_handles, list(legend_labels.values()) + [f'Fragment Max (k={k})', f'Fragment Mean (k={k})'],
                   title='Legend', loc='upper left', bbox_to_anchor=(1, 1))

        plt.grid(True)

        # Save the plot as a PNG file
        output_file = f'{dataset_name}_k{k}_F1Scores_colored.png'
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Saved plot: {output_file}")

        # Show the plot
        plt.show()

# Plot for both datasets
plot_f1_scores(moonshot_csv, 'Covid Moonshot')
plot_f1_scores(fresco_csv, 'Fresco')
