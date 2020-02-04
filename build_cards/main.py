import json
import os
from yattag import Doc


def build_html(data):
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            doc.asis('<meta charset="utf-8"/>')
            doc.asis('<link href="../css/default.css" rel="stylesheet">')
        with tag('body'):
            for id, card in data['cards'].items():
                with tag('div', klass='card'):
                    with tag('div', klass='card-text'):
                        doc.text(card['text'])
                    if 'details' in card:
                        with tag('div', klass='card-details'):
                            doc.text(card['details'])
                    if 'image' in card:
                        with tag('div', klass='card-image'):
                            doc.stag('img', src='../img/' + card['image'])
            for empty_id in range(0, 8 - (len(data['cards'].items()) % 8)):
                with tag('div', klass='card card-empty'):
                    with tag('div', klass='card-image card-image-empty'):
                        pass

    return doc.getvalue()


datadir = os.path.relpath('../data', os.path.dirname(__file__))
outdir = os.path.relpath('../html', os.path.dirname(__file__))
for root, dirs, files in os.walk(datadir):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file)) as json_file:
                lang = file.replace('.json', '')
                data = json.load(json_file)
                htmldata = build_html(data)
                with open(os.path.join(outdir, lang + '.html'), 'w') as html_file:
                    html_file.write(htmldata)

