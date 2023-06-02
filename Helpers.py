import xml.etree.ElementTree as et


def deleteSentenced(pathToFile):
    tree = et.parse(pathToFile)
    root = tree.getroot()

    for child in root.findall('node'):
        if child.attrib.get('action') == 'delete':
            root.remove(child)

    for child in root.findall('way'):
        if child.attrib.get('action') == 'delete':
            root.remove(child)

    for child in root.findall('relation'):
        if child.attrib.get('action') == 'delete':
            root.remove(child)

    tree.write(pathToFile)