from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.resources import CDN
    from bokeh.embed import components

    starta=datetime.datetime(2016,1,1)
    enda=datetime.datetime(2016,3,10)

    df=data.DataReader(name='GOOG', data_source="yahoo", start=starta, end=enda)

    def inc_dec(c,o):
        if c>o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    #define new column 
    df["Status"]= [inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    df["Middle"]= (df.Open+df.Close)/2
    df["Height"]= abs(df.Close-df.Open)


    p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="stretch_width"
    , title = "Candlestick") 
    ''' "stretch_width"
    #Component will responsively resize to stretch to the available width, without maintaining any aspect ratio. The height of the component depends on the type of the component and may be fixed or fit to component’s contents.'''

    hours_12=12*60*60*1000
    p.grid.grid_line_alpha=0.1 #grid lines visibility
    p.grid.grid_line_color="#FF3333"

    p.segment(df.index, df.High, df.index, df.Low, line_color="black")

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],
            hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")

    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
            hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")

    script1, div1 = components(p)

    js_data = CDN.js_files[0]
    return render_template("plot.html", script1=script1, div1=div1, js_data=js_data)

@app.route('/test/')
def test():
    return render_template("test.html")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
