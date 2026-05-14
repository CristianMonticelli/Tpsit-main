from flask import Flask, render_template, request
from zeep import Client
from zeep.exceptions import Fault
from zeep.helpers import serialize_object

app = Flask(__name__)

url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

SERVICE_LABELS = {
    "CapitalCity": "Capitale",
    "CountryIntPhoneCode": "Prefisso telefonico internazionale",
    "FullCountryInfo": "Informazioni complete",
}

FULL_INFO_FIELDS = {
    "sISOCode": "Codice ISO",
    "sName": "Nome",
    "sCapitalCity": "Capitale",
    "sPhoneCode": "Prefisso telefonico",
    "sContinentCode": "Continente",
    "sCurrencyISOCode": "Valuta (ISO)",
    "sCountryFlag": "Bandiera",
}


def _format_items(container, sub_key, name_f, iso_f):
    if container:
        items = container.get(sub_key)
    else:
        items = None
    if not items:
        return None
    if isinstance(items, dict):
        items = [items]
    return ", ".join(f"{i.get(name_f, '')} ({i.get(iso_f, '')})" for i in items)


def flatten_full_info(raw):
    data = serialize_object(raw)
    result = {label: data.get(key, "") for key, label in FULL_INFO_FIELDS.items()}

    lang_str = _format_items(data.get("Languages"), "tLanguage", "sName", "sISOCode")
    if lang_str:
        result["Lingue"] = lang_str

    cur_str = _format_items(data.get("Currencies"), "tCurrency", "sName", "sISOCode")
    if cur_str:
        result["Valute"] = cur_str

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    selected_code = request.form.get("iso_code", "")
    selected_service = request.form.get("service", "CapitalCity")

    try:
        client = Client(wsdl=url)
        countries = client.service.ListOfCountryNamesByCode()

        if request.method == "POST":
            if not selected_code:
                error = "Seleziona un paese dalla lista."
            elif selected_service not in SERVICE_LABELS:
                error = "Seleziona un servizio valido."
            else:
                raw = getattr(client.service, selected_service)(selected_code)
                if selected_service == "FullCountryInfo":
                    result = flatten_full_info(raw)
                else:
                    result = raw
                print(result)

    except Fault as e:
        error = f"Errore SOAP: {e}"

    return render_template(
        "index.html",
        countries=countries,
        result=result,
        error=error,
        selected_code=selected_code,
        selected_service=selected_service,
        service_labels=SERVICE_LABELS,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5678)
