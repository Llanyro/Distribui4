from S3Controller import ResolutorSolicitudes

res = ResolutorSolicitudes("18.207.191.38", "distribui4")


def lambda_handler(event, context):
    if event is None:
        resultado = {"resultado": "0", "statusCode": "No hay query"}
    elif res.dbconnected() is False:
        resultado = {"resultado": 1, "statusCode": "Conecxion a la db no correcta"}
    else:
        resultado = res.resolverSolicitud(event)
    return resultado
