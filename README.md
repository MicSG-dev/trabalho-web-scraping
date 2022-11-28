# Monitorador de Preços Aliexpress
## O que este projeto faz?
Este projeto faz o monitoramento constante, de 15 em 15 minutos, do preço de um ou mais produtos do Aliexpress. Caso o preço de algum dos produtos cadastrados tenha diminuído, é enviado um Email HTML, que faz uso recursos de formatação e marcação semântica em email que não estão disponíveis com texto simples. O template do email é estilizado com uso do framework Bootstrap, através da ferramenta Bootstrap Email (https://github.com/bootstrap-email/bootstrap-email). O monitoramento dos preços é feito sempre, até que todos os produtos tenham seu alerta de preço enviado (após o preço abaixar) ou até que o usuário encerre o processo.
## Como o projeto funciona?
Este projeto foi desenvolvido em Python, que dentre outras bibliotecas, possui a biblioteca Beautiful Soup (https://github.com/wention/BeautifulSoup4) que é utilizada para extrair dados de arquivos HTML e XML. Ele fornece formas idiomáticas de navegar, pesquisar e modificar a árvore de análise. Para envio de Email HTML é utilizada a bibliteca smtplib (https://docs.python.org/3/library/smtplib.html) e as subclasses MIMEMultiparte e MIMEText (https://docs.python.org/3/library/email.mime.html).
## Quais as configurações necessárias para o projeto funcionar?
Antes de executar o projeto, configure as variáveis do arquivo [credenciais.py](https://github.com/MicSG-dev/trabalho-web-scraping/blob/main/credenciais.py), sendo elas:
```
HOST = "*******" # Nome do servidor do seu plano de hospedagem
PORT = 587 # A porta SSL ou TTL
MY_ADDRESS = "**********" # o e-mail remetente para enviar mensagens
PASSWORD = "*************" # a senha do e-mail remetente (MY_ADDRESS)
```    
> Nota: A variável `PORT` requere a porta de seu servidor SMTP, que normalmente é 587 para protocolo TTL e 465 para protocolo SSL.

Também altere a variável `email_relatorio` que se encontra na [linha 122 do arquivo main.py](https://github.com/MicSG-dev/trabalho-web-scraping/blob/main/main.py#L122). Esta variável deve ter o Email para qual deseja que o alerta Email HTML seja enviado.
```
email_relatorio = "*************************"
```

### Obtendo o codigo_produto no Aliexpress
1. Acesse o site do produto no Aliexpress;
2. No URL do produto, extraia o código do produto, onde este está localizado entre a barras item e a extensão da página (.html). Exemplo: https://pt.aliexpress.com/item/1005002611857804.html neste exemplo, o código do produto seria 1005002611857804;

### Cadastrando os produtos no monitorador
Cadastre os produtos que deseja receber alertas na variável `data`. Cada produto tem três "atributos":
- `id`: um número único que identifique o produto (normalmente se inicia a contagem em 0);
- `codigo_produto`: o código do produto no Aliexpress. Consulte as instruções abaixo para ver como obter;
- `preco_bom`: a meta de preço à qual o produto deva ser inferior para que o alerta de preço seja enviado para o usuário;

No exemplo abaixo, está cadastrado dois produtos. O produto de código 1005002611857804 possui a meta de preço R$ 48,10 e o id de identificação 0. já o produto de código 1005004957723357 possui a meta de preço R$ 651,00 e o id de identificação 1:
```
    data = [
        {
            'id': 0,
            'codigo_produto': '1005002611857804',
            'preco_bom' : 48.10
        },
        {
            'id': 1,
            'codigo_produto': '1005004957723357',
            'preco_bom': 621.00
        }
    ]
```
## Exemplo de alerta Email HTML recebido 
Email aberto no Gmail:

![image](https://user-images.githubusercontent.com/71986598/204199367-f14881c8-4cc3-489b-aaf4-36a15f8b9639.png)

Console aberto no Pycham:

![image](https://user-images.githubusercontent.com/71986598/204198948-792cb731-258c-4d73-bcaa-e2299fe4e963.png)
