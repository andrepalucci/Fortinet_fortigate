# Fortinet_fortigate
ara realizar o upgrade de firmware em um FortiGate 60F via Python, você pode usar a API REST do FortiOS. No entanto, o FortiOS não permite fazer upload e upgrade de firmware diretamente via API — o processo normalmente envolve:

Fazer upload manual do firmware pela GUI.
Ou via CLI (TFTP/USB).
Ou via Automação parcial com Python para:
Fazer login.
Verificar a versão atual.

Agendar o upgrade (caso esteja disponível via FortiManager ou auto-upgrade).
Se seu FortiGate está conectado ao FortiManager, o upgrade pode ser feito por ele. Se não, abaixo está um exemplo de script Python para:

Fazer login.
Verificar a versão.
(Opcional) disparar um reboot depois de upload manual do firmware.

Pré-requisitos
FortiGate com API REST ativada.
Usuário com permissão para exec comandos.

Firmware já enviado via GUI ou TFTP/USB.


Como ativar a API REST no FortiGate
bash
Copiar
Editar
config system global
    set admin-scp enable
    set admin-https-redirect enable
end

config system interface
    edit "port1"
        set allowaccess ping https ssh http fgfm
    next
end
