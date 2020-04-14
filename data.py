import pandas, os
from flask import Flask, render_template, request, send_file
from geopy.geocoders import ArcGIS
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success-table/', methods=["POST"])
def success_table():
    global filename
    if request.method == "POST":
        file = request.files["myfile"]
        try:
            df = pandas.read_csv(file)            
            nom = ArcGIS()

            df["Latitude"]=df["Address"].apply(nom.geocode).apply(lambda x: x.latitude if x != None else None)
            df["Longitude"]=df["Address"].apply(nom.geocode).apply(lambda x: x.longitude if x != None else None)

            # Writes new updated DataFrame to csv file.
            filename = datetime.datetime.now().strftime("../App/uploads/geocoded_"+"%Y-%m-%d-%H-%M-%S"+".csv")
            df.to_csv(filename, index=None)

            # Generates HTML code for DataFrame df and writes it as newTable.html
            # with open("../App/templates/newTable.html", 'x') as newFile:
            #     newFile.write(df.to_html())
            #     newFile.close()

            return render_template('index.html', text=df.to_html(), btn='download.html')
            
        except:
            return render_template('index.html', text="Please make sure you have an address column in your .CSV file!")

@app.route('/download-file/')
def download():
    return send_file(filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug = False
    app.run()