from bs4 import BeautifulSoup
import requests
import csv

# functions


def obtainWebpage(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    source = requests.get(url, headers=hdr).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def writeProductData(textileCompaniesPage):
    productList = textileCompaniesPage.find('div', class_='resultatDivId')
    for productBlock in productList.find_all('div', class_='prod_list'):
        productLink = productBlock.find(
            'div', class_='product-list-data').h2.a['href']
        #!pagina dentro de producto
        productPage = obtainWebpage(productLink)

        # *TITULO
        name = productPage.find(
            'div', class_='blockNameCompany').h1.text.replace('"', "").replace(",", "").replace("\n", "").strip()
        locationData = productPage.find('div', class_='addressCoordinates')
        addressBlock = productPage.find('p', class_='blockAddress')
        # *DIRECCION Y REFERENCIA
        address = " ".join(locationData.find('span', class_='spRight').span.text.replace(
            '\n', ' ').replace('\r', '').split()).strip().replace('"', "").replace("\n", "")
        # *CODIGO POSTAL
        postCode = locationData.find(
            'span', class_='spRight').contents[2].strip().replace('"', "").replace("\n", "")
        # *PAIS
        country = addressBlock.next_sibling.next_sibling.find(
            'span', class_='spRight').text.strip().replace('"', "").replace("\n", "")
        # *TELEFONO
        telephone = locationData.next_sibling.next_sibling.div.div.a.input["value"].strip(
        ).replace('"', "").replace("\n", "")
        # *ACTIVIDADES
        activitiesTree = productPage.find(class_='activitiesTree').ul
        activity = ''
        if(activitiesTree != None):
            for activityCat in activitiesTree.find_all('li', recursive=False):
                activity += activityCat.a.text.replace(
                    '\n', ' ')
                if(activityCat.ul != None):
                    activity += ': '
                    for activitySubCat in activityCat.ul.find_all('li'):

                        """ activityType = (
                            ' '.join(activitySubCat.i['class'])).lower().strip() """

                        #! elimina los <i> para coger solo el texto
                        for activityCircle in activitySubCat.find_all('i'):
                            activityType = (
                                ' '.join(activityCircle['class'])).lower().strip()
                            if(activityType == 'circle supplier'):
                                activity += '(Productor) '
                            elif(activityType == 'circle distributor'):
                                activity += '(Distribuidor) '
                            elif(activityType == 'circle service'):
                                activity += '(Servicio) '
                            else:
                                activity += ' '
                            activityCircle.decompose()

                        activity += activitySubCat.text.replace(
                            '\n', '').replace(',', '').strip().replace('"', "").replace("\n", "")
                else:
                    activity += '/'

        print(name, address, postCode, country, telephone, activity)

        csvWriter.writerow(
            [name, address, postCode, country, telephone, activity])


# * @@@ PROGRAM @@@
with open('kompass-textiles.csv', 'w') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter=',')
    csvWriter.writerow(['nombre', 'direccion', 'codigo postal',
                        'pais', 'telefono', 'actividades'])

    #! Pagina 1
    textileCompaniesPage = obtainWebpage(
        'https://pe.kompass.com/a/textiles/12/r/lima/pe_2183/')

    nextPageLink = textileCompaniesPage.find(
        'li', class_='searchItemLi active').next_sibling.next_sibling.a['href']

    while(nextPageLink):

        #!Escribe productos de la pagina actual
        writeProductData(textileCompaniesPage)

        #!Obtiene la siguiente pagina
        textileCompaniesPage = obtainWebpage(nextPageLink)

        try:
            nextPageLink = textileCompaniesPage.find(
                'li', class_='searchItemLi active').next_sibling.next_sibling.a['href']
        except:
            #!realizar el mismo proceso para la última pagina
            writeProductData(textileCompaniesPage)
            nextPageLink = False
