from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index():
    # خواندن داده‌ها از فایل CSV
    path= 'outputs/raw-data.xlsx'
    df = pd.read_excel(path)
    # ایجاد نمودار
    heatmap = go.Heatmap(
        z=df.values.tolist(),
        colorscale='Viridis'
    )
    layout = go.Layout(title='Heatmap')
    fig = go.Figure(data=heatmap, layout=layout)

    # تبدیل نمودار به کد HTML
    plot_html = fig.to_html(full_html=False)

    return render_template('index.html', plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
