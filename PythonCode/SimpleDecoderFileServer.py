from flask import Flask, request, make_response, abort
from Singleton import variableCorrectaList, allTrueList
import requests
import json
import codecs

app = Flask(__name__)
num = 3000


def subir(cookieaws, nombrevideo, etiquetas, visualizacion, bites, pos: str):
    print(pos)
    parametros = {"peticion": "subirVideo", "cookie": cookieaws, "nombreVideo": nombrevideo, "etiquetas": etiquetas,
                  "visualizacion": visualizacion, "file": bites, "subida": pos}
    print(parametros)
    return requests.post(url="https://9pmvwa88yc.execute-api.us-east-1.amazonaws.com/login",
                         headers={"Authorization": "AWS4-HMAC-SHA256 Credential=ASIAVY64N4P5BWLLJY7M/"
                                                   "20200505/us-east-1/execute-api/aws4_request, "
                                                   "SignedHeaders=accept;content-type;host;x-amz-date, "
                                                   "Signature=f7170836540e1e13f598ff546a178f146491a2009d0f"
                                                   "4989699d70464b71fb5a"},
                         data=json.dumps(parametros)).content


@app.route("/formDecoder", methods=["POST"])
def formDecoder():
    file = request.files.get("file")
    cookieaws = request.form.get("cookie")
    nombrevideo = request.form.get("nombreVideo")
    etiquetas = request.form.get("etiquetas")
    visualizacion = request.form.get("visualizacion")
    print(request.form)
    if file is None:
        abort(403, "File not found")
    elif variableCorrectaList([cookieaws, nombrevideo, etiquetas, visualizacion]) is False:
        abort(404, "Faltan parametros")
    else:
        filecontent = file.read()
        test = codecs.encode(filecontent, 'hex_codec').decode("utf-8")
        size: int = test.__len__()
        i = 0
        resultados: list = []
        resultgeneral: dict

        # Inicio + bucle
        if i + num <= size:
            resultgeneral = subir(cookieaws, nombrevideo, etiquetas, visualizacion, test[i: i + num], "0")
            print(resultgeneral)
            i += num
            while i < size:
                if i + num < size:
                    print(subir(cookieaws, nombrevideo, etiquetas,
                                            visualizacion, test[i: i + num], "1"))
                    i += num
                elif i + num == size:
                    print(subir(cookieaws, nombrevideo, etiquetas,
                                            visualizacion, test[i: i + num], "2"))
                else:
                    value = size - i
                    print(subir(cookieaws, nombrevideo, etiquetas,
                                            visualizacion, test[i: i + value], "2"))
                    i += value
        # Inicio / Inicio + Fin
        else:
            value = size - i
            resultgeneral = subir(cookieaws, nombrevideo, etiquetas, visualizacion, test[i: i + value], "3")
            print(resultgeneral)
            i += value

        """if resultgeneral is not None:
            boolres = resultgeneral.get("filesubido")
            if boolres is not None:
                resultados.append(boolres)
                if allTrueList is False:
                    resultgeneral["filesubido"] = False
                else:
                    resultgeneral["filesubido"] = True
            else:
                resultgeneral = {"Error": "filesubido: None"}
        else:
            resultgeneral = {"Error": "resultado: None"}"""
        print(resultgeneral)
        result = make_response()
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result


if __name__ == '__main__':
    app.run(port=37853, host='0.0.0.0', debug=False)
