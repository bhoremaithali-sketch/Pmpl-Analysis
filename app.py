from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Read CSV file
df = pd.read_csv("pmpl.csv", encoding="latin1")

@app.route("/")
def home():

    total_rows = len(df)
    total_columns = len(df.columns)

    # Create Bar Graph
    plt.figure(figsize=(10,5))
    plt.bar(df["Route ID"].head(10), df["Kilometer"].head(10))
    plt.title("Route Distance Analysis")
    plt.xlabel("Route ID")
    plt.ylabel("Kilometer")
    plt.xticks(rotation=45)

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    graph = base64.b64encode(img.getvalue()).decode()
    plt.close()

    html = f"""
    <html>
    <head>
        <title>PMPML Data Analysis Dashboard</title>
    </head>

    <body style="font-family:Arial; margin:40px;">

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
    <h2>Route Distance Graph</h2>

    <img src="data:image/png;base64,{graph}" width="900">

    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
