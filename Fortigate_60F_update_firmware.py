import paramiko
import requests
import urllib3
import os

# Configurações FortiGate
FGT_IP = "192.168.1.99"
USERNAME = "admin"
PASSWORD = "sua_senha"
FIRMWARE_FILE = "FGT_60F-v7.4.3.build2575-FORTINET.out"

# Caminho no FortiGate (partição principal)
REMOTE_PATH = f"/data/{os.path.basename(FIRMWARE_FILE)}"

# Desabilita warning SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
API_BASE = f"https://{FGT_IP}/api/v2"

# Função para upload via SCP
def upload_firmware_via_scp():
    print(f"[+] Iniciando upload via SCP para {FGT_IP}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(FGT_IP, username=USERNAME, password=PASSWORD)

    sftp = ssh.open_sftp()
    print(f"[+] Enviando arquivo {FIRMWARE_FILE} para {REMOTE_PATH}")
    sftp.put(FIRMWARE_FILE, REMOTE_PATH)
    sftp.close()
    ssh.close()
    print("[+] Upload concluído.")

# Login via API para obter sessão
def login():
    session = requests.session()
    session.verify = False
    login_data = {
        "username": USERNAME,
        "secretkey": PASSWORD
    }
    login_resp = session.post(f"{API_BASE}/logincheck", data=login_data)
    if login_resp.status_code == 200 and "APSCOOKIE" in session.cookies:
        print("[+] Login API efetuado com sucesso.")
        return session
    else:
        raise Exception("[-] Falha no login API.")

# Executa reboot para aplicar upgrade
def reboot(session):
    confirm = input("[!] Confirma o reboot do FortiGate para aplicar o firmware? (yes/N): ").lower()
    if confirm == "yes":
        resp = session.post(f"{API_BASE}/monitor/system/reboot")
        if resp.status_code == 200:
            print("[+] Reboot iniciado com sucesso.")
        else:
            print("[-] Erro ao executar reboot.")
    else:
        print("[i] Reboot cancelado.")

if __name__ == "__main__":
    try:
        upload_firmware_via_scp()
        session = login()
        reboot(session)
    except Exception as e:
        print(f"[!] Erro: {e}")
