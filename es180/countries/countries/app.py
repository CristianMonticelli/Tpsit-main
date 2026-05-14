from zeep import Client
from zeep.exceptions import Fault
from flask import Flask, request, render_template

app = Flask(__name__)

# soap service
url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

def getAllISOCodes(client):
    response = client.service.ListOfCountryNamesByCode()
    return response


@app.route("/", methods=["GET", "POST"])
def load():
    result = None
    response = None
    try:
        client = Client(wsdl=url)
        if request.method == "POST":
            if not request.form["isocode"].strip():
                result = "Fill in the ISO code"
            else:
                #chiamata a uno delle funzionalità
                pass
            return render_template("home.html.jinja", response=response, result=result)
        else:
            response = getAllISOCodes(client)
            #scoprire metodi disponibili
            oplist = []
            for service in client.wsdl.services.values():
                for port in service.ports.values():
                    for op in port.binding._operations.values():
                        if op.name not in oplist:
                            oplist.append(op.name)
            return render_template("home.html.jinja", countries=response, oplist=oplist)
    except Fault as exception:
        return f"Errore SOAP: {exception}"

# pip install zeep
# rif. https://docs.python-zeep.org/en/master/
if __name__ == "__main__":
    app.run()