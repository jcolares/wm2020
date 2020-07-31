# Desenvolvimento e execução de código em host remoto via SSH usando o VsCode
Aplicação prática das instruções em [https://code.visualstudio.com/docs/remote/ssh] para acesso ao host **deep-01 (ip-deep-01)** através do jumphost **lpsgateway (ip-lpsgateway)**


## 1. Crie sua conta de usuário pessoal no **lpsgateway**
1. Conecte-se ao servidor remoto com o usuário lps@ip-lpsgateway e senha C*******9:
    ~~~ bash
    $ ssh lps@ip-lpsgateway
    ~~~
3. Crie um usuário pessoal no **lpsgateway**: 
    ~~~ bash
    $ sudo adduser <usuario>  
    ~~~
    > Crie uma senha para o novo usuário.
4. Adicione o usuário ao grupo de sudoers: 
    ~~~ bash
    $ sudo usermod -aG sudo <usuario>
    ~~~
5. Desconecte-se: 
    ~~~ bash
    $ exit
    ~~~
1. Teste o novo usuário/senha: 
    ~~~ bash
    $ ssh -p 60000 <usuario>@ip-lpsgateway
    $ exit
    ~~~
## Configure chaves criptográficas para conexão ao **lpsgateway** a partir da máquina local
As chaves criptográficas permitirão o acesso aos hosts a partir da máquina local dispensando o uso de senhas e são pré-requisito para o VsCode.
1. Crie chaves criptográficas na máquina local: 
    ~~~ bash
    $ ssh-keygen 
    ~~~
    > os arquivos com as chaves pública (id_rsa.pub) e privada (id_rsa) ficam armazenados no diretório `~/.ssh`. 
    > Ao gerar as chaves, não informe uma passphrase ou terá que digitá-la em todo login.
1. Copie sua chave pública para o host **lpsgateway**:
    ~~~ bash
    $ ssh-copy-id -i ~/.ssh/id_rsa <usuario>@ip-lpsgateway -p 60000
    ~~~
1. Teste novamente o acesso, agora usando as chaves criptográficas: 
    ~~~ bash
    $ ssh -p 60000 <usuario>@ip-lpsgateway
    $ exit
    ~~~
## Crie sua conta de usuário pessoal no **deep-01**
1. Connecte-se ao host **deep-01** através do **lpsgateway**: 
    ~~~ bash
    $ ssh -tt <usuario>@ip-lpsgateway -p 60000 ssh -tt lps@ip-deep-01
    ~~~
    > A senha solicidata nesse passo é a do usuário lps@ip-deep-01
2. Crie uma conta de usuário pessoal no **deep-01**: 
    ~~~ bash
    $ adduser <usuario> 
    ~~~
3. Adicione o usuário ao grupo de sudoers: 
    ~~~ bash
    $ sudo usermod -aG sudo <usuario>
    ~~~
4. Desconecte-se: 
   ~~~ bash
   $ exit
   ~~~
5. Teste a conexão usando novo usuário e senha: 
    ~~~ bash
    $ ssh -o ProxyCommand='ssh -p 60000 <usuario>@ip-lpsgateway nc ip-deep-01 22' <usuario>@ip-deep-01
    $ exit
    ~~~
## Configure chaves criptográficas para conexão ao **deep-01** a partir do **lpsgateway**
1. Conecte-se ao **lpsgateway**: 
    ~~~ bash
    $ ssh -p 60000 <usuario>@ip-lpsgateway
    ~~~
4. Crie chaves criptográicas para o seu usuário no **lpsgateway**: 
    ~~~ bash
    $ ssh-keygen 
    ~~~
    > O par de chaves fica em ~/.ssh no lpsgateway (não informe passphrase!)
5. Copie sua chave para o servidor **deep-01**: 
    ~~~ bash
    $ ssh-copy-id -i ~/.ssh/id_rsa <usuario>@ip-deep-01 
    ~~~
6. Teste o acesso com chaves ao **deep-01** a partir do **lpsgateway**: 
    ~~~ bash
    $ ssh <usuario>@ip-deep-01
    $ exit
    ~~~
7. Desconecte-se do **lpsgateway**:
    ~~~ bash
    $ exit
    ~~~
## Configure chaves criptográficas para conexão ao **deep-01** a partir da máquina local
Não é necessário gerar novas chaves. Vamos utilizar as chaves geradas anteriormente.
1. Copie a sua chave criptográfica da máquina local, que está no arquivo `~/.ssh/id_rsa.pub`.
> Não copie o arquivo. Copie apenas o conteúdo do arquivo usando CRTL+C.
1. Conecte-se ao **deep-01** através do **lpsgateway** (ainda fornecendo a senha do <usuario>@ip-deep-01): 
    ~~~ bash
    $ ssh -o ProxyCommand='ssh -p 60000 <usuario>@ip-lpsgateway nc ip-deep-01 22' <usuario>@ip-deep-01
    ~~~
9. Abra o arquivo `authorized_keys` e cole a chave pública copiada da máquina local abaixo da chave lá existente: 
    ~~~ bash
    pico ~/.ssh/authorized_keys 
    ~~~
9. Salve o arquivo e saia do editor: CTRL+S, CTRL+X
9. Desconecte-se da **deep-01**: `exit`
9. Teste a conexão direta ao **deep-01**, desta vez já usando as chaves criptográficas: 
    ~~~ bash
    $ ssh -o ProxyCommand='ssh -p 60000 <usuario>@ip-lpsgateway nc ip-deep-01 22' <usuario>@ip-deep-01 
    $ exit 
    ~~~

## Configuração do VsCode
1. Instale a extensão [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) no VSCode
2. Crie uma entrada no arquivo de configuração de SSH remoto para acessar o host **deep-01**:

    `Ctrl+Shift+P` > `remote-SSH: Open Configuration File...`

    -> Adicionar a entrada correspondente ao host **deep-01**:
    ~~~
    Host deep-01
      HostName ip-deep-01
      User <usuario>
      ProxyCommand ssh -p 60000 <usuario>@ip-lpsgateway nc %h %p
    ~~~
2. (OPCIONAL) Crie uma entrada no arquivo de configuração de SSH remoto para acessar o host **lpsgateway**:

    `Ctrl+Shift+P` > `remote-SSH: Open Configuration File...`

    -> Adicionar a entrada correspondente ao host **lpsgateway**:
    ~~~
    Host lpsgateway
      User <usuario>
      HostName ip-lpsgateway
      Port 60000
    ~~~

## Utilização
Na guia Remote Explorer, na gaveta `TARGETS (SSH)`, clique botão direito no **deep-01** e conecte-se.

Espera-se que neste momento você consiga navegar as pastas no host remoto e utilizá-las para editar e executar código como se estivesse trabalhando na máquina local :)


## Referências: 
https://code.visualstudio.com/docs/remote/ssh    
https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack  
https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2
https://www.cyberciti.biz/faq/linux-unix-ssh-proxycommand-passing-through-one-host-gateway-server/ 

   