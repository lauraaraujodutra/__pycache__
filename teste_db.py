from db import ensuredb, getconnection  
# Importa funções para garantir a existência do banco e criar conexão com ele

try:
    ensuredb()  
    # Chama função que cria o banco de dados e suas tabelas se ainda não existirem
    print("✅ Banco de dados garantido com sucesso!")  
    # Mensagem de confirmação para o usuário

    with getconnection() as conn:  
        # Abre conexão com o banco de dados usando gerenciador de contexto (fecha automático)
        print("🔗 Conexão com o banco estabelecida com sucesso!")  
        # Mensagem de sucesso na conexão

except Exception as e:  
    # Captura qualquer exceção que ocorra durante criação ou conexão ao banco
    print("❌ Ocorreu um erro ao acessar o banco de dados:")  
    print(f"⚠️ Detalhes: {e}")  
    # Exibe o erro para o usuário para diagnóstico
