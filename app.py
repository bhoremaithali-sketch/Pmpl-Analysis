from flask import Flask
import pandas as pd
import matplotlib
matpoltlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Read CSV file
df = pd.read_csv("pmpl.csv", encoding="latin1")

# Function to convert graph to HTML
def create_graph():
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph

@app.route("/")
def home():

    total_rows = len(df)
    total_columns = len(df.columns)

    # ---------------- BAR CHART ----------------
    plt.figure(figsize=(8,4))
    plt.bar(df["Route ID"].head(10), df["Kilometer"].head(10))
    plt.title("Bar Chart")
    plt.xlabel("Route ID")
    plt.ylabel("Kilometer")
    plt.xticks(rotation=45)
    bar_graph = create_graph()

    # ---------------- LINE CHART ----------------
    plt.figure(figsize=(8,4))
    plt.plot(df["Route ID"].head(10), df["Kilometer"].head(10), marker="o")
    plt.title("Line Chart")
    plt.xlabel("Route ID")
    plt.ylabel("Kilometer")
    plt.xticks(rotation=45)
    line_graph = create_graph()

    # ---------------- PIE CHART ----------------
    plt.figure(figsize=(6,6))
    pie_data = df.groupby("Route ID")["Kilometer"].sum().head(5)
    plt.pie(
        pie_data,
        labels=pie_data.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Pie Chart")
    pie_graph = create_graph()

    # ---------------- HISTOGRAM ----------------
    plt.figure(figsize=(8,4))
    plt.hist(df["Kilometer"], bins=10)
    plt.title("Histogram")
    plt.xlabel("Kilometer")
    plt.ylabel("Frequency")
    hist_graph = create_graph()

    # ---------------- SCATTER PLOT ----------------
    plt.figure(figsize=(8,4))
    plt.scatter(range(20), df["Kilometer"].head(20))
    plt.title("Scatter Plot")
    plt.xlabel("Index")
    plt.ylabel("Kilometer")
    scatter_graph = create_graph()

    html = f"""
    <html>
    <head>
        <title>PMPML Data Analysis Dashboard</title>
    </head>

    <body style="font-family:Arial; margin:40px">

    <h1>PMPML Data Analysis Dashboard</h1>

    <h2>Dataset Summary</h2>

    <p><b>Total Records:</b> {total_rows}</p>
    <p><b>Total Columns:</b> {total_columns}</p>

    <h2>Column Names</h2>

    <ul>
    """

    for col in df.columns:
        html += f"<li>{col}</li>"

    html += "</ul>"

    html += "<h2>First 10 Records</h2>"

    html += df.head(10).to_html(index=False)

    html += f"""

    <h2>Bar Chart</h2>
    <img src="data:image/png;base64,{bar_graph}" width="700">

    <h2>Line Chart</h2>
    <img src="data:image/png;base64,{line_graph}" width="700">

    <h2>Pie Chart</h2>
    <img src="data:image/png;base64,{pie_graph}" width="700">

    <h2>Histogram</h2>
    <img src="data:image/png;base64,{hist_graph}" width="700">

    <h2>Scatter Plot</h2>
    <img src="data:image/png;base64,{scatter_graph}" width="700">

    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
