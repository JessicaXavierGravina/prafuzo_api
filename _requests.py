import requests

data = {"plate": plate}
url = "/parking"

# Realiza a solicitação POST como um formulário
response = requests.post(url, data=data)

if response.status_code == 201:
    try:
        reservation_id = response.json()["reservation_id"]
        print("Reserva feita com sucesso!")
        print("ID da reserva:", reservation_id)
    except (KeyError, ValueError):
        print("Erro ao analisar a resposta JSON")
else:
    print("Erro na reserva. Código de status:", response.status_code)
    print("Mensagem de erro:", response.text)