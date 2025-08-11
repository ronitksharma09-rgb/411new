
from flask import Flask, render_template, request
import json
import requests
from PyPDF2 import PdfReader

app = Flask(__name__)

def dtccaip_check(target):
    url = "https://www.dtcc.com/-/media/Files/Downloads/Investment-Product-Services/Wealth-Management-Services/AIP/AIP-Client-List.pdf"
    response = requests.get(url)
    
    with open("dtcc-aip-client-list.pdf", "wb") as f:
        f.write(response.content)

    reader = PdfReader("dtcc-aip-client-list.pdf")
    pages = [page.extract_text() for page in reader.pages]

    for value in pages:
        if target.lower() in value.lower():
            return "The LLC is under DTCC AIP."
    
    return " The LLC could not be found under DTCC AIP."

@app.route("/backend", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        llc_name = request.form["llc"]
        message = dtccaip_check(llc_name)
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)









