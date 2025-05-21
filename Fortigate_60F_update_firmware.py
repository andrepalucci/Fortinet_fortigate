import requests
import urllib3

# Desabilita warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FGT_IP = "192.168.1.99"
USERNAME = "admin"
PASSWORD = "sua_senha"
API_BASE = f"https://{FGT_IP}/api/v2"

# Login e coleta do token de sessão
def login():
    url = f"{API_BASE}/monitor/system/status"
    session = requests.session()
    session.verify = False
    login_data = {
        "username": USERNAME,
        "secretkey": PASSWORD
    }
    login_resp = session.post(f"{API_BASE}/logincheck", data=login_data)
    if login_resp.status_code == 200 and "APSCOOKIE" in session.cookies:
        print("[+] Login efetuado com sucesso.")
        return session
    else:
        raise Exception("[-] Falha no login.")

# Verifica versão atual
def check_version(session):
    url = f"{API_BASE}/monitor/system/status"
    resp = session.get(url)
    if resp.status_code == 200:
        data = resp.json()
        version = data.get("version", "desconhecida")
        print(f"[i] Versão atual: {version}")
    else:
        print("[-] Erro ao verificar versão.")

# Reboot para aplicar firmware (se já enviado)
def reboot(session):
    url = f"{API_BASE}/monitor/system/reboot"
    confirm = input("[!] Confirma o reboot do equipamento? (yes/N): ").lower()
    if confirm == "yes":
        resp = session.post(url)
        if resp.status_code == 200:
            print("[+] Reboot iniciado com sucesso.")
        else:
            print("[-] Falha ao iniciar reboot.")
    else:
        print("[i] Reboot cancelado.")

if __name__ == "__main__":
    try:
        session = login()
        check_version(session)
        reboot(session)
    except Exception as e:
        print(e)
