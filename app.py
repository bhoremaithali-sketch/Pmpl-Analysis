from flask import Flask
import pandas as pd

app = Flask(__name__)

# Read the CSV file
df = pd.read_csv("pmpml.csv")

@app.route("/")
def home():
    total_rows = len(df)
    total_columns = len(df.columns)

    html = f"""
    <html>
    <head>
        <title>PMPML Data Analysis</title>
    </head>
    <body>
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
    html += df.head(10).to_html()

    html += """
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
