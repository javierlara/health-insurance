import requests
from lxml import html

# page = requests.post('http://apres.com.ar/prestadores.php', data={'plan': 32, 'especialidad': 217, 'orden': 'nombre', 'listar': 'Buscar'})
page = requests.post('http://apres.com.ar/prestadores.php', data={'orden': 'nombre', 'listar': 'Buscar'})

tree = html.fromstring(page.content)

planes = tree.xpath('//*[@id="selplan"]/option/@value')
especialidades = tree.xpath('//*[@id="selespecialidad"]/option/@value')

dict = {}


for esp_id in especialidades:
    if not esp_id:
        continue
    for plan_id in planes:
        if not plan_id:
            continue
        page = requests.post('http://apres.com.ar/prestadores.php', data={'plan': int(plan_id), 'especialidad': int(esp_id), 'orden': 'nombre', 'listar': 'Buscar'})
        tree = html.fromstring(page.content)

        nombres = tree.xpath('//*[@id="prestadores"]/ul/li/b/text()')

        direcciones = tree.xpath('//*[@id="prestadores"]/ul/li/text()[3]')
        direcciones = [d.replace('\n\t\t\t\t\t', '') for d in direcciones]

        telefonos = tree.xpath('//*[@id="prestadores"]/ul/li/span/text()')
        telefonos = [t.replace(' // ', '') for t in telefonos]
        telefonos = [t.replace('Tel.: ', '') for t in telefonos]

        print(plan_id)
        print(esp_id)
        print(nombres)
        print(direcciones)
        print(telefonos)

        for i in range(len(nombres)):
            if nombres[i] not in dict:
                dict[nombres[i]] = {
                    'tel': telefonos[i],
                    'dir': direcciones[i],
                    'plan': set([plan_id]),
                    'esp': set([esp_id]),
                }
            else:
                dict[nombres[i]]['plan'].add(plan_id)
                dict[nombres[i]]['esp'].add(esp_id)
print(dict)
