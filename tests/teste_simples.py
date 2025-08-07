import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

BASE_URL = "http://localhost:5000"  # Altere se necessário

usuario_teste = {
    "nome": "Teste User",
    "email": "user@example.com",
    "senha": "senha123"
}

def chamada_segura(metodo, url, **kwargs):
    try:
        response = metodo(url, timeout=5, **kwargs)
        return response
    except ConnectionError:
        print(f"❌ Erro: não foi possível conectar a {url}")
    except Timeout:
        print(f"❌ Erro: tempo de resposta excedido para {url}")
    except RequestException as e:
        print(f"❌ Erro inesperado em {url}: {e}")
    return None

def main():
    nota = 0
    print("=== TESTE DE API RESTFUL COM JWT ===\n")

    # 1️⃣ Criar usuário
    print("1. Criando usuário...")
    resp_usuario = chamada_segura(requests.post, f"{BASE_URL}/usuarios", json=usuario_teste)
    if resp_usuario and resp_usuario.status_code == 201:
        nota += 5
        print("   ✅ Usuário criado com sucesso.")
    else:
        print("   ❌ Falha ao criar usuário.")

    # 2️⃣ Autenticar
    print("\n2. Autenticando usuário...")
    login_resp = chamada_segura(requests.post, f"{BASE_URL}/auth/login", json={
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })
    if login_resp and login_resp.status_code == 200 and "access_token" in login_resp.json():
        token = login_resp.json()["access_token"]
        nota += 5
        print("   ✅ Autenticação bem-sucedida. Token obtido.")
    else:
        print("   ❌ Falha na autenticação.")
        token = None

    # 3️⃣ Criar mensagem
    mensagem_id = None
    if token:
        print("\n3. Criando mensagem autenticada...")
        headers = {"Authorization": f"Bearer {token}"}
        mensagem_resp = chamada_segura(requests.post, f"{BASE_URL}/mensagens", json={
            "titulo": "Mensagem Teste",
            "conteudo": "Conteúdo de teste com token válido."
        }, headers=headers)

        if mensagem_resp and mensagem_resp.status_code == 201:
            mensagem_id = mensagem_resp.json().get("id")
            nota += 10
            print("   ✅ Mensagem criada. ID:", mensagem_id)
        else:
            print("   ❌ Falha ao criar mensagem.")

    # 4️⃣a Acessar mensagem com token
    if mensagem_id and token:
        print("\n4a. Acessando mensagem com token...")
        headers = {"Authorization": f"Bearer {token}"}
        acesso_token = chamada_segura(requests.get, f"{BASE_URL}/mensagens/{mensagem_id}", headers=headers)
        if acesso_token and acesso_token.status_code == 200:
            nota += 5
            print("   ✅ Mensagem acessada com token.")
        else:
            print("   ❌ Falha ao acessar mensagem com token.")

    # 4️⃣b Acessar mensagem sem token
    if mensagem_id:
        print("\n4b. Acessando mensagem sem token...")
        acesso_sem_token = chamada_segura(requests.get, f"{BASE_URL}/mensagens/{mensagem_id}")
        if acesso_sem_token and acesso_sem_token.status_code == 401:
            nota += 5
            print("   ✅ Acesso sem token corretamente negado (401).")
        else:
            print("   ❌ Acesso sem token não retornou erro esperado.")

    # Resultado
    print("\n🎯 NOTA FINAL:", nota, "/ 30")
    if nota == 30:
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    elif nota == 0:
        print("❌ A API parece estar fora do ar ou com erros críticos.")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM. Verifique os logs acima.")

if __name__ == "__main__":
    main()