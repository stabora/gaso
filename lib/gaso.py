# -*- coding: utf-8 -*-

import re
from pyphen import pyphen

dic = pyphen.Pyphen(lang='es_AR')
LETRAS_FINALES = ['n', 's', 'a', 'e', 'i', 'o', 'u', u'á', u'é', u'í', u'ó', u'ú']

VOCALES_ACENTUADAS = {
    u'á': 'a',
    u'é': 'e',
    u'í': 'i',
    u'ó': 'o',
    u'ú': 'u',
}

CANTIDAD_SILABAS = {
    1: u'Monosílaba',
    2: u'Bisílaba',
    3: u'Trisílaba',
    4: u'Polisílaba',
}

TIPO_ACENTO = {
    1: u'Aguda',
    2: u'Grave',
    3: u'Esdrújula',
    4: u'Sobreesdrújula',
}


def analizar_palabra(palabra):
    palabra_separada = dic.inserted(palabra)

    # Fuerzo la separación de diptongos
    palabra_separada = re.sub(ur'(í)([' + get_vocales_planas() + '])', r'\1-\2', palabra_separada)

    silabas = palabra_separada.split('-')
    cantidad_silabas = len(silabas) if len(silabas) < 5 else 4
    silaba_acentuada = -1

    for indice, silaba in enumerate(reversed(silabas), start=1):
        if re.search(ur'[' + get_vocales_acentuadas() + ']', silaba):
            silaba_acentuada = indice

    if silaba_acentuada >= 4:
        tipo_acento = 4
    elif silaba_acentuada == 3:
        tipo_acento = 3
    elif cantidad_silabas == 1:
        tipo_acento = 1
    else:
        if palabra[-1] in LETRAS_FINALES:
            if silaba_acentuada == 1:
                tipo_acento = 1
            else:
                tipo_acento = 2
        else:
            if silaba_acentuada == 2:
                tipo_acento = 2
            else:
                tipo_acento = 1

    return tipo_acento, silabas, (
        u'Palabra: {}<br>'
        u'Palabra separada en sílabas: {}<br>'
        u'Cantidad de sílabas: ({}) {}<br>'
        u'Sílaba acentuada: {}<br>'
        u'Tipo de palabra según acento: {}</br>'
    ).format(
        palabra,
        palabra_separada,
        cantidad_silabas, CANTIDAD_SILABAS[cantidad_silabas],
        silaba_acentuada,
        TIPO_ACENTO[tipo_acento],
    )


def traducir_palabra(palabra):
    tipo_palabra, silabas, detalle = analizar_palabra(palabra)
    silabas_rev = silabas[::-1]

    if tipo_palabra == 1 and len(silabas) > 1:
        silabas_rev[0] = gasear(silabas_rev[0])
    elif tipo_palabra == 2:
        silabas_rev[1] = gasear(silabas_rev[1])
    elif tipo_palabra == 3:
        silabas_rev[2] = gasear(silabas_rev[2])
    elif tipo_palabra == 4:
        silabas_rev[3] = gasear(silabas_rev[3])

    return ''.join(silabas_rev[::-1])


def traducir_texto(texto):
    #for palabra in re.split(r'[\s.,]', texto):
        #texto_traducido += traducir_palabra(palabra) + ' '

    return re.sub(ur'([\w' + get_vocales_acentuadas() + '])+', lambda p: traducir_palabra(p.group()), texto)


def gasear(silaba):
    if re.search(r'[' + get_vocales_planas() + ']{2}', silaba):
        return re.sub(r'([' + get_vocales_planas() + '])', r'\1sag\1', silaba[::-1], 1)[::-1]
    else:
        silaba_gaseada = re.sub(
            r'([' + get_vocales_planas() + get_vocales_acentuadas() + '])',
            '{}gas{}'.format(
                ur'\1',
                ur'\1'
            ),
            silaba,
            1
        )

        return re.sub(
            ur'([' + get_vocales_acentuadas() + '])',
            lambda s: VOCALES_ACENTUADAS[s.group(1)],
            silaba_gaseada,
            1
        )


def get_vocales_planas():
    return ''.join([vocal for vocal in VOCALES_ACENTUADAS.itervalues()])


def get_vocales_acentuadas():
    return ''.join([vocal for vocal, valor in VOCALES_ACENTUADAS.iteritems()])
