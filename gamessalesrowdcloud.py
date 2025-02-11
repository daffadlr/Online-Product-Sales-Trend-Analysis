# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Read dataset into a dataframe
# Replace 'vgasales.csv' with your actual file path
df = pd.read_csv("vgasales.csv")

# Display the first few rows for debugging
print(df.head())
print(df.columns)

# Ensure relevant columns are selected (Name, NA_Sales, EU_Sales, JP_Sales, Other_Sales)
# Adjust column names if necessary
df = df[['Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']]

df['Name'] = df['Name'].str.replace(' ', '_')

# Calculate total sales across all regions
df['total_sales'] = df['NA_Sales'] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales']

# Group by 'Name' to calculate the total sales for each game
game_sales_weight = df.groupby('Name')['total_sales'].sum().reset_index()

# Sort games by total sales in descending order
game_sales_weight = game_sales_weight.sort_values(by='total_sales', ascending=False)

# Normalize the total sales for scaling in WordCloud
# Increase the scaling factor to make larger differences in size
max_sales = game_sales_weight['total_sales'].max()
game_sales_weight['normalized_sales'] = (game_sales_weight['total_sales'] / max_sales) * 1000  # Increased scaling

# Debugging: Check if Wii Sports is at the top
print("Top 10 Games by Total Sales:")
print(game_sales_weight.head(10))

# Creating the text for WordCloud, where each game name appears proportionally to its total sales
# Ensure proportionality by adding a minimum of 1 repetition to avoid games with zero visibility
text = " ".join([f"{row['Name']} " * max(1, int(row['normalized_sales'])) for _, row in game_sales_weight.iterrows()])

# Debugging: Print the generated text to ensure it has Wii Sports in correct proportion
print("\nGenerated WordCloud Text:")
print(text[:1000])  # Display first 1000 characters to check

# Create a figure with subplots
fig, (ax_wordcloud, ax_bar) = plt.subplots(1, 2, figsize=(15, 8), gridspec_kw={'width_ratios': [3, 1]})

# Generate WordCloud
word_cloud = WordCloud(collocations=False, background_color='white', width=4096, height=2160).generate(text)

# Display WordCloud in the left subplot
ax_wordcloud.imshow(word_cloud, interpolation='bilinear')
ax_wordcloud.axis("off")  # Remove axis from WordCloud plot

# Prepare data for the bar chart (show top 10 games by total sales)
top_games = game_sales_weight.head(10)

# Plot the bar chart in the right subplot
ax_bar.barh(top_games['Name'], top_games['total_sales'], color='skyblue')
ax_bar.set_xlabel('Total Sales')
ax_bar.set_title('Top 10 Games by Sales')
ax_bar.invert_yaxis()  # Invert y-axis to have the highest value on top

# Adjust layout for better fit
plt.tight_layout()

# Save the combined plot with WordCloud and bar chart
plt.savefig('game_sales_wordcloud_with_barchart.png')

# Show the plot
plt.show()
