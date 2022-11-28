import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import credenciais

def get_tag_script(soup):
    for script in soup.find_all('script'):
        script = str(script.string)
        if(script.find('window.runParams')!= -1):
            return script
    return ""

def extrai_nome_produto(soup):
    content = get_tag_script(soup)

    indice_start = content.find("\"spanishPlaza\":")
    indice_end = content.find("\"preSaleModule\":")
    content = content[indice_start:indice_end]

    indice_start = content.find("\"title\":\"") + 9
    indice_end = content.find("\"},")
    content = content[indice_start:indice_end]

    return content

def extrai_avaliacao_produto(soup):
    content = get_tag_script(soup)

    indice_start = content.find("\"averageStar\":")
    indice_end = content.find("\"averageStarRage\":")
    content = content[indice_start:indice_end]

    indice_start = content.find("\"averageStar\":\"") + 15
    indice_end = content.find("\",")
    content = content[indice_start:indice_end]

    qtd_stars_int = round(float(content))
    qtd_stars_str = content
    content = ""
    for i in range(0,qtd_stars_int):
        content += "★"
    for i in range (qtd_stars_int,5):
        content += "☆"
    content = qtd_stars_str + " " + content
    return content

def extrai_qtd_avaliacoes(soup):
    content = get_tag_script(soup)

    indice_start = content.find("\"totalValidNum\":")
    indice_end = content.find("\"twoStarNum\":")
    content = content[indice_start:indice_end]

    indice_start = content.find("\"totalValidNum\":\"") + 17
    indice_end = content.find(",\"")
    content = content[indice_start:indice_end]

    return content

def extrai_valor_a_vista(soup):
    #maxActivityAmount
    content = get_tag_script(soup)

    indice_start = content.find(",\"formatedAmount\":\"")
    indice_end = content.find(",\"value\":")
    content = content[indice_start:indice_end]

    indice_start = content.find(",\"formatedAmount\":\"") + 19
    indice_end = content.find("\",\"")
    content = content[indice_start:indice_end].replace("R$","").replace(",",".")
    return content

def extrai_imagem_produto(soup):
    content = get_tag_script(soup)

    indice_start = content.find("\"imagePathList\":[\"")
    indice_end = content.find(",\"name\":",indice_start)
    content = content[indice_start:indice_end]

    indice_start = content.find("\"imagePathList\":[\"") + 18
    indice_end = content.find("\",\"")
    content = content[indice_start:indice_end]
    return content

def gera_relatorio_produto_html(soup,link_produto):
     nome_produto = extrai_nome_produto(soup)
     if len(nome_produto) > 15:
         nome_produto = nome_produto[0:45 + 1].strip() + '...' + nome_produto[-15:]

     link_imagem_produto = extrai_imagem_produto(soup)
     avaliacao_produto = extrai_avaliacao_produto(soup)
     qtd_avaliacoes = extrai_qtd_avaliacoes(soup)
     valor_a_vista = extrai_valor_a_vista(soup).replace(".",",")

     html = f'<table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius:6px;border-collapse:separate!important;width:100%;overflow:hidden;border:1px solid #e2e8f0" bgcolor="#ffffff"><tbody><tr><td style="line-height:24px;font-size:16px;width:100%;margin:0" align="left" bgcolor="#ffffff"><table class="pt-1 pl-1" role="presentation" border="0" cellpadding="0" cellspacing="0"><tbody><tr><td style="line-height:24px;font-size:16px;padding-top:4px;padding-left:4px;margin:0" align="left"><h7 class="">{nome_produto}</h7></td></tr></tbody></table><div class="row gap-12" style="margin-right:-48px;margin-bottom:-48px"><table class="" role="presentation" border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed;width:100%" width="100%"><tbody><tr><td class="col-2" style="line-height:24px;font-size:16px;min-height:1px;font-weight:400;padding-right:48px;width:16.666667%;padding-bottom:48px;margin:0;padding: 4px;" align="left" valign="top"><img class="img-fluid" src="{link_imagem_produto}" alt="Some Image" style="height:auto;line-height:100%;outline:0;text-decoration:none;display:block;max-width:100%;width:100%;border-style:none;border-width:0" width="100%"></td><td class="col-10" style="line-height:24px;font-size:16px;min-height:1px;font-weight:400;padding-right:48px;width:83.333333%;padding-bottom:48px;margin:0" align="left" valign="top"><ul><li><strong>Valor &#224; Vista: </strong>R$ {valor_a_vista}</li><li><strong>Avalia&#231;&#227;o do(s) {qtd_avaliacoes} comprador(es): </strong>{avaliacao_produto}</li><li><strong>Link: </strong><a href="{link_produto}" target="_blank" style="color:#0d6efd">Clique aqui</a></li></ul></td></tr></tbody></table></div></td></tr></tbody></table><table class="s-3 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:12px;font-size:12px;width:100%;height:12px;margin:0" align="left" width="100%" height="12">&#160;</td></tr></tbody></table>'

     return html

def gera_relatorio_produto_text(soup, link):
    nome_produto = extrai_nome_produto(soup)
    if len(nome_produto) > 15:
        nome_produto = nome_produto[0:45+1].strip() + '...' + nome_produto[-15:]

    avaliacao_produto = extrai_avaliacao_produto(soup)
    qtd_avaliacoes = extrai_qtd_avaliacoes(soup)
    valor_a_vista = extrai_valor_a_vista(soup)

    text = "➜ " + nome_produto + '\n'
    text += "\t Valor à vista: R$ " + valor_a_vista.replace(".",",") + '\n'
    text += "\t Avaliação do(s) "+qtd_avaliacoes+" comprador(es): " + avaliacao_produto + '\n'
    text += "\t Link: " + link + '\n'
    text += "\n"
    return text

if __name__ == '__main__':
    print(" --- Monitorador de Preços Aliexpress --- ")

    url_base = "https://pt.aliexpress.com/item/"
    email_relatorio = "*************************" # o e-mail para o qual queira receber os alertas do monitorador de preços

    lista_produtos_analisados = []
    data = [
        {
            'id': 0, # ID único criado para o produto
            'codigo_produto': '1005002611857804', # o código do produto
            'preco_bom' : 48.10 # o preço ao qual deseja que o alerta seja enviado caso o produto esteja abaixo desta meta
        },
        {
            'id': 1,
            'codigo_produto': '1005004957723357',
            'preco_bom': 621.00
        }
    ]

    deve_monitorar_preco = True

    while(deve_monitorar_preco):
        relatorio_completo_html = ""
        relatorio_completo_text = ""

        print("Executando nova busca de dados dos produtos.",end='')

        qtd_produtos_bom_preco = 0
        qtd_produtos_total = 0

        for d in data:
            link_produto = url_base + d['codigo_produto'] + '.html'
            request = requests.get(link_produto)

            if (request.url.find('404.html') != -1):
                print(f"\nO código do produto {d['codigo_produto']} inserido não foi encontrado. Verifique o código e tente novamente. \nContinuando..",end='')
            else:
                soup = BeautifulSoup(request.text, 'html5lib')

                valor_a_vista = extrai_valor_a_vista(soup)
                qtd_produtos_total +=1

                if float(valor_a_vista) < d['preco_bom'] and not d['id'] in lista_produtos_analisados:
                    lista_produtos_analisados.append(d['id'])
                    qtd_produtos_bom_preco += 1
                    relatorio_completo_html += gera_relatorio_produto_html(soup, link_produto)
                    relatorio_completo_text += gera_relatorio_produto_text(soup, link_produto)
                print(".",end='')
            sleep(5)

        print('\nBusca realizada')

        if relatorio_completo_html != "":
            header = r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html><head><meta http-equiv="x-ua-compatible" content="ie=edge"><meta name="x-apple-disable-message-reformatting"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="format-detection" content="telephone=no, date=no, address=no, email=no"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><style type="text/css">body,table,td{font-family:Helvetica,Arial,sans-serif!important}.ExternalClass{width:100%}.ExternalClass,.ExternalClass div,.ExternalClass font,.ExternalClass p,.ExternalClass span,.ExternalClass td{line-height:150%}a{text-decoration:none}*{color:inherit}#MessageViewBody a,a[x-apple-data-detectors],u+#body a{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}img{-ms-interpolation-mode:bicubic}table:not([class^=s-]){font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0;mso-table-rspace:0;border-spacing:0;border-collapse:collapse}table:not([class^=s-]) td{border-spacing:0;border-collapse:collapse}@media screen and (max-width:600px){.gap-12.row,.gap-x-12.row{margin-right:-48px!important}.gap-12.row>table>tbody>tr>td,.gap-x-12.row>table>tbody>tr>td{padding-right:48px!important}.gap-12.row,.gap-y-12.row{margin-bottom:-48px!important}.gap-12.row>table>tbody>tr>td,.gap-y-12.row>table>tbody>tr>td{padding-bottom:48px!important}table.gap-12.stack-x>tbody>tr>td{padding-right:48px!important}table.gap-12.stack-y>tbody>tr>td{padding-bottom:48px!important}.w-full,.w-full>tbody>tr>td{width:100%!important}.pt-1.btn td a,.pt-1:not(.btn)>tbody>tr>td,.pt-1:not(table),.py-1.btn td a,.py-1:not(.btn)>tbody>tr>td,.py-1:not(table){padding-top:4px!important}.pl-1.btn td a,.pl-1:not(.btn)>tbody>tr>td,.pl-1:not(table),.px-1.btn td a,.px-1:not(.btn)>tbody>tr>td,.px-1:not(table){padding-left:4px!important}[class*=s-lg-]>tbody>tr>td{font-size:0!important;line-height:0!important;height:0!important}.s-3>tbody>tr>td{font-size:12px!important;line-height:12px!important;height:12px!important}.s-5>tbody>tr>td{font-size:20px!important;line-height:20px!important;height:20px!important}.s-10>tbody>tr>td{font-size:40px!important;line-height:40px!important;height:40px!important}}</style></head><body class="bg-light" style="outline:0;width:100%;min-width:100%;height:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;font-family:Helvetica,Arial,sans-serif;line-height:24px;font-weight:400;font-size:16px;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;box-sizing:border-box;color:#000;margin:0;padding:0;border-width:0" bgcolor="#f7fafc"><table class="bg-light body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline:0;width:100%;min-width:100%;height:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;font-family:Helvetica,Arial,sans-serif;line-height:24px;font-weight:400;font-size:16px;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;box-sizing:border-box;color:#000;margin:0;padding:0;border-width:0" bgcolor="#f7fafc"><tbody><tr><td valign="top" style="line-height:24px;font-size:16px;margin:0" align="left" bgcolor="#f7fafc"><table class="container" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%"><tbody><tr><td align="center" style="line-height:24px;font-size:16px;margin:0;padding:0 16px"><!--[if (gte mso 9)|(IE)]><table align="center" role="presentation"><tbody><tr><td width="600"><![endif]--><table align="center" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;margin:0 auto"><tbody><tr><td style="line-height:24px;font-size:16px;margin:0" align="left"><table class="s-10 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:40px;font-size:40px;width:100%;height:40px;margin:0" align="left" width="100%" height="40">&#160;</td></tr></tbody></table><table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius:6px;border-collapse:separate!important;width:100%;overflow:hidden;border:1px solid #e2e8f0" bgcolor="#ffffff"><tbody><tr><td style="line-height:24px;font-size:16px;width:100%;margin:0" align="left" bgcolor="#ffffff"><table class="card-body" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%"><tbody><tr><td style="line-height:24px;font-size:16px;width:100%;margin:0;padding:20px" align="left"><h1 class="text-3xl" style="padding-top:0;padding-bottom:0;font-weight:500;vertical-align:baseline;font-size:30px;line-height:36px;margin:0" align="left">Alerta do Monitorador de Pre&#231;os Aliexpress</h1><h6 class="text-teal-700" style="color:#13795b;padding-top:0;padding-bottom:0;font-weight:500;vertical-align:baseline;font-size:16px;line-height:19.2px;margin:0" align="left">Um ou mais produtos alcan&#231;aram um bom pre&#231;o para compra. Confira abaixo:</h6><table class="s-3 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:12px;font-size:12px;width:100%;height:12px;margin:0" align="left" width="100%" height="12">&#160;</td></tr></tbody></table><div class="space-y-3">'
            content = relatorio_completo_html
            footer = r'<table class="s-5 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:20px;font-size:20px;width:100%;height:20px;margin:0" align="left" width="100%" height="20">&#160;</td></tr></tbody></table><table class="hr" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%"><tbody><tr><td style="line-height:24px;font-size:16px;border-top-width:1px;border-top-color:#e2e8f0;border-top-style:solid;height:1px;width:100%;margin:0" align="left"></td></tr></tbody></table><table class="s-5 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:20px;font-size:20px;width:100%;height:20px;margin:0" align="left" width="100%" height="20">&#160;</td></tr></tbody></table><center>Desenvolvido por Michel Galv&#227;o</center><table class="s-10 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width:100%" width="100%"><tbody><tr><td style="line-height:40px;font-size:40px;width:100%;height:40px;margin:0" align="left" width="100%" height="40">&#160;</td></tr></tbody></table><!--[if (gte mso 9)|(IE)]><![endif]-->'
            html = header + content + footer

            s = smtplib.SMTP(host=credenciais.HOST, port=credenciais.PORT)
            s.starttls()
            s.login(credenciais.MY_ADDRESS, credenciais.PASSWORD)
            email_msg = MIMEMultipart()
            email_msg['To'] = email_relatorio
            email_msg['From'] = credenciais.MY_ADDRESS
            email_msg['Subject'] = 'Alerta do Monitorador de Preços Aliexpress'
            email_msg.attach(MIMEText(html, 'html'))
            s.sendmail(credenciais.MY_ADDRESS, email_relatorio, email_msg.as_string())

            print('Gerado relatório do(s) produto(s) e enviado para o e-mail ' + email_relatorio)
            print('Resumo do relatório:')
            print("O(s) produto(s) à seguir obtiveram valor inferior à meta de preço, COMPRE-O(S)!:\n" + relatorio_completo_text)

        if qtd_produtos_bom_preco == qtd_produtos_total:
            deve_monitorar_preco = False
        else:
            print('Esperando 15 minutos para a próxima busca de dados')
            sleep(15*60)