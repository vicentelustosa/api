import requests
from requests.exceptions import RequestException

BASE_URL = "http://localhost:5000"

def chamada_segura(metodo, url, **kwargs):
    try:
        return metodo(url, timeout=5, **kwargs)
    except RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return None

def criar_usuario(nome, email, senha):
    return chamada_segura(requests.post, f"{BASE_URL}/usuarios", json={
        "nome": nome,
        "email": email,
        "senha": senha
    })

def autenticar(email, senha):
    resp = chamada_segura(requests.post, f"{BASE_URL}/auth/login", json={
        "email": email,
        "senha": senha
    })
    if resp and 200 <= resp.status_code < 300:
        return resp.json().get("access_token")
    return None

def main():
    print("=== FLUXO DE TESTE: 2 USUÁRIOS INTERAGINDO ===")
    nota = 0

    # 1️⃣ Criar usuários
    print("\n1. Criando dois usuários...")
    user1 = {"nome": "User Um", "email": "user1@example.com", "senha": "senha123"}
    user2 = {"nome": "User Dois", "email": "user2@example.com", "senha": "senha123"}

    criar_usuario(**user1)
    criar_usuario(**user2)
    print("   ✅ Usuários criados.")

    # 2️⃣ Autenticar o primeiro usuário
    print("\n2. Autenticando User1...")
    token1 = autenticar(user1["email"], user1["senha"])
    if token1:
        print("   ✅ Token obtido.")
        nota += 5
    else:
        print("   ❌ Falha na autenticação de User1.")

    headers1 = {"Authorization": f"Bearer {token1}"} if token1 else {}

    # 3️⃣ Criar mensagem sem título (inválida)
    print("\n3. Criando mensagem inválida (sem título)...")
    invalida = chamada_segura(requests.post, f"{BASE_URL}/mensagens", json={
        "conteudo": "Mensagem sem título"
    }, headers=headers1)
    if invalida and invalida.status_code == 422:
        print("   ✅ Erro 422 retornado corretamente.")
        nota += 5
    else:
        print("   ❌ Esperado erro 422, obtido:", invalida.status_code if invalida else "N/A")

    # 4️⃣ Criar mensagem válida
    print("\n4. Criando mensagem válida...")
    msg_id = None
    valida = chamada_segura(requests.post, f"{BASE_URL}/mensagens", json={
        "titulo": "Mensagem Teste",
        "conteudo": "Conteúdo válido"
    }, headers=headers1)
    if valida and 200 <= valida.status_code < 300:
        msg_id = valida.json().get("id")
        print(f"   ✅ Mensagem criada com ID {msg_id}")
        nota += 5
    else:
        print("   ❌ Falha ao criar mensagem válida.")

    # 5️⃣ Autenticar o segundo usuário
    print("\n5. Autenticando User2...")
    token2 = autenticar(user2["email"], user2["senha"])
    if token2:
        print("   ✅ Token obtido.")
        nota += 5
    else:
        print("   ❌ Falha na autenticação de User2.")

    headers2 = {"Authorization": f"Bearer {token2}"} if token2 else {}

    # 6️⃣ Tentar editar mensagem do user1 com user2 (esperado 403)
    print("\n6. User2 tentando editar mensagem de User1...")
    if token2 and msg_id:
        edita = chamada_segura(requests.put, f"{BASE_URL}/mensagens/{msg_id}", json={
            "titulo": "Edição Indevida",
            "conteudo": "Tentativa de outro usuário"
        }, headers=headers2)
        if edita and edita.status_code == 403:
            print("   ✅ Acesso proibido corretamente (403).")
            nota += 5
        else:
            print("   ❌ Esperado 403, recebido:", edita.status_code if edita else "N/A")
    else:
        print("   ⚠️ Dados insuficientes para testar edição da mensagem.")

    # 7️⃣ User2 comenta na mensagem do User1
    print("\n7. User2 comentando na mensagem...")
    comentario_id = None
    if token2 and msg_id:
        comentario = chamada_segura(requests.post, f"{BASE_URL}/mensagens/{msg_id}/comentarios", json={
            "conteudo": "Comentário de User2"
        }, headers=headers2)
        if comentario and 200 <= comentario.status_code < 300:
            comentario_id = comentario.json().get("id")
            print(f"   ✅ Comentário criado com ID {comentario_id}")
            nota += 3
        else:
            print("   ❌ Falha ao criar comentário.")
    else:
        print("   ⚠️ Dados insuficientes para testar comentário.")

    # 8️⃣ User2 altera seu comentário
    print("\n8. User2 editando seu comentário...")
    if comentario_id:
        edita_coment = chamada_segura(requests.put, f"{BASE_URL}/comentarios/{comentario_id}", json={
            "conteudo": "Comentário editado"
        }, headers=headers2)
        if edita_coment and 200 <= edita_coment.status_code < 300:
            print("   ✅ Comentário editado com sucesso.")
            nota += 2
        else:
            print("   ❌ Falha ao editar comentário.")
    else:
        print("   ⚠️ Comentário não foi criado. Edição não testada.")

    # Resultado final
    print("\n🎯 NOTA FINAL:", nota, "/ 30")
    if nota == 30:
        print("✅ TODOS OS PASSOS REALIZADOS COM SUCESSO.")
    else:
        print("⚠️ ALGUMAS ETAPAS FALHARAM. VERIFIQUE OS LOGS.")

if __name__ == "__main__":
    main()
