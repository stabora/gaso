# -*- coding: utf-8 -*-

"""
Éste es el módulo gasó.

Éste módulo provee la función gasear. Por ejemplo:

>>> gasear(u'rosarino')
u'rosarigasino'
"""

import unicodedata
import re

def gas(letra):
    '''dada una letra X devuelve XgasX
    excepto si X es una vocal acentuada, en cuyo caso devuelve
    la primera X sin acento

    >>> gas(u'a')
    u'agasa'

    >>> gas (u'\xf3')
    u'ogas\\xf3'

    '''
    return u'%sgas%s'%(unicodedata.normalize('NFKD', letra).encode('ASCII', 'ignore'), letra)

def umuda(palabra):
    '''
    Si una palabra no tiene "!":
        Reemplaza las u mudas de la palabra por !

    Si la palabra tiene "!":
        Reemplaza las "!" por u

    >>> umuda (u'queso')
    u'q!eso'

    >>> umuda (u'q!eso')
    u'queso'

    >>> umuda (u'cuis')
    u'cuis'

    '''

    if '!' in palabra:
        return palabra.replace('!', 'u')
    if re.search('([qg])u([ei])', palabra):
        return re.sub('([qg])u([ei])', u'\\1!\\2', palabra)
    return palabra

def es_diptongo(par):
    '''Dado un par de letras te dice si es un diptongo o no

    >>> es_diptongo(u'ui')
    True

    >>> es_diptongo(u'pa')
    False

    >>> es_diptongo(u'ae')
    False

    >>> es_diptongo(u'ai')
    True

    >>> es_diptongo(u'a')
    False

    >>> es_diptongo(u'cuis')
    False

    '''

    if len(par) != 2:
        return False

    if (par[0] in 'aeiou' and par[1] in 'iu') or \
       (par[1] in 'aeiou' and par[0] in 'iu'):
        return True
    return False

def elegir_tonica(par):
    '''Dado un par de vocales que forman diptongo, decidir cual de las
    dos es la tónica.

    >>> elegir_tonica(u'ai')
    0

    >>> elegir_tonica(u'ui')
    1
    '''
    if par[0] in 'aeo':
        return 0
    return 1

def gasear(palabra):
    """
    Convierte una palabra de castellano a rosarigasino.

    >>> gasear(u'rosarino')
    u'rosarigasino'

    >>> gasear(u'pas\xe1')
    u'pasagas\\xe1'

    Los diptongos son un problema a veces:

    >>> gasear(u'cuis')
    u'cuigasis'

    >>> gasear(u'caigo')
    u'cagasaigo'


    Los adverbios son especiales para el castellano pero no
    para el rosarino!

    >>> gasear(u'especialmente')
    u'especialmegasente'

    """
    #from pudb import set_trace; set_trace()

    # Primero el caso obvio: acentos.
    # Lo resolvemos con una regexp

    if re.search(u'[\xe1\xe9\xed\xf3\xfa]',palabra):
        return re.sub(u'([\xe1\xe9\xed\xf3\xfa])',lambda x: gas(x.group(0)),palabra,1)


    # Siguiente problema: u muda
    # Reemplazamos gui gue qui que por g!i g!e q!i q!e
    # y lo deshacemos antes de salir
    palabra=umuda(palabra)

    # Que hacemos? Vemos en qué termina

    if palabra[-1] in 'nsaeiou':
        # Palabra grave, acento en la penúltima vocal
        # Posición de la penúltima vocal:
        pos=list(re.finditer('[aeiou]',palabra))[-2].start()
    else:
        # Palabra aguda, acento en la última vocal
        # Posición de la última vocal:
        pos=list(re.finditer('[aeiou]',palabra))[-1].start()

    # Pero que pasa si esa vocal es parte de un diptongo?

    if es_diptongo(palabra[pos-1:pos+1]):
        pos += elegir_tonica(palabra[pos-1:pos+1])-1
    elif es_diptongo(palabra[pos:pos+2]):
        pos += elegir_tonica(palabra[pos:pos+2])


    return umuda(palabra[:pos]+gas(palabra[pos])+palabra[pos+1:])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
