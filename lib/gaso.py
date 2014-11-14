# -*- coding: utf-8 -*-

import re
from lib.pyphen import pyphen


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
        silabas_rev[0] = gaso(silabas_rev[0])
    elif tipo_palabra == 2:
        silabas_rev[1] = gaso(silabas_rev[1])
    elif tipo_palabra == 3:
        silabas_rev[2] = gaso(silabas_rev[2])
    elif tipo_palabra == 4:
        silabas_rev[3] = gaso(silabas_rev[3])

    return ''.join(silabas_rev[::-1])

def traducir_texto(texto):
    texto_traducido = ''

    for palabra in texto.split():
      texto_traducido += traducir_palabra(palabra) + ' '

    return texto_traducido

def gaso(silaba):
    if re.search(r'[' + get_vocales_planas() + ']{2}', silaba):
      return re.sub(r'([' + get_vocales_planas() + '])', r'\1sag\1', silaba[::-1], 1)[::-1]
    else:
      for vocal_acento, vocal_plana in VOCALES_ACENTUADAS.iteritems():
          silaba = silaba.replace(vocal_acento, vocal_plana)

      return re.sub(r'([' + get_vocales_planas() + '])', r'\1gas\1', silaba, 1)

def get_vocales_planas():
    return ''.join([vocal for vocal in VOCALES_ACENTUADAS.itervalues()])

def get_vocales_acentuadas():
    return ''.join([vocal for vocal, valor in VOCALES_ACENTUADAS.iteritems()])