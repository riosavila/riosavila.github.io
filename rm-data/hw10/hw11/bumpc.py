import pandas as pd
import plotly.express as px

# Create the DataFrame with the updated data
data = {
    "Name": ["Chenning", "Emilia", "Joe", "Brendon", "Shane", "Laz2"],
    "LROC": [0.88933, 0.86962, 0.88913, 0.87401, 0.89118, 0.87839],
    "Sensitivity": [66.98413, 59.52381, 66.34921, 63.01587, 67.14286, 63.49206],
    "Specificity": [89.57806, 89.95781, 89.66245, 90.29536, 89.78903, 89.95781],
    "Correctly Class": [84.83333, 83.56667, 84.76667, 84.56667, 85.03333, 84.40000]
}

df = pd.DataFrame(data)

# Rank the data
df["LROC Rank"] = df["LROC"].rank(ascending=False)
df["Sensitivity Rank"] = df["Sensitivity"].rank(ascending=False)
df["Specificity Rank"] = df["Specificity"].rank(ascending=False)
df["Correctly Class Rank"] = df["Correctly Class"].rank(ascending=False)

# Melt the DataFrame to long format
df_melted = df.melt(id_vars=["Name"], value_vars=["LROC Rank", "Sensitivity Rank", "Specificity Rank", "Correctly Class Rank"],
                    var_name="Metric", value_name="Rank")

# Create the bump chart with a LitRPG-inspired theme
fig = px.line(df_melted, x="Metric", y="Rank", color="Name", markers=True,
              color_discrete_sequence=["#8B0000", "#FF8C00", "#FFD700", "#32CD32", "#1E90FF", "#4B0082"])

# Update layout for better visualization
fig.update_layout(title="Bump Chart of Rankings",
                  title_font=dict(size=24, family="Fantasy", color="#FFD700"),
                  xaxis_title="Metric",
                  yaxis_title="Rank",
                  yaxis=dict(autorange="reversed"),
                  plot_bgcolor="#2F4F4F",
                  paper_bgcolor="#2F4F4F",
                  font=dict(family="Fantasy", size=14, color="#FFFFFF"))

# Save the chart as an HTML file with limited interactivity
fig.write_html("bump_chart.html", config={'displayModeBar': False, 'scrollZoom': True})

# Display the chart in the notebook (optional)
fig.show()