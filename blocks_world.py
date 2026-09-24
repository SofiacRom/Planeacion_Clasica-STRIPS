from collections import deque
import time

TODOS_LOS_BLOQUES = ['A', 'B', 'C', 'D', 'E', 'F']

def bloque_ocupado_por(posiciones, bloques, excluir=None):
    ocupado = {}
    for b in bloques:
        if b == excluir:
            continue
        destino = posiciones[b]
        if destino != 'Mesa':
            ocupado[destino] = b
    return ocupado

def crearia_ciclo(bloque, destino, posiciones, bloques):
    actual = destino
    saltos = 0
    while actual != 'Mesa':
        if actual == bloque:
            return True
        actual = posiciones[actual]
        saltos += 1
        if saltos > len(bloques) + 2:
            return True
    return False

def opciones_validas(bloque, posiciones, bloques):
    ocupado = bloque_ocupado_por(posiciones, bloques, excluir=bloque)
    opciones = ['Mesa']
    for y in bloques:
        if y == bloque:
            continue
        if ocupado.get(y) not in (None, bloque):
            continue
        if crearia_ciclo(bloque, y, posiciones, bloques):
            continue
        opciones.append(y)
    return opciones

def corregir_posiciones(posiciones, bloques):
    cambio = True
    intentos = 0
    while cambio and intentos < len(bloques) + 2:
        cambio = False
        intentos += 1
        for b in bloques:
            if posiciones[b] not in opciones_validas(b, posiciones, bloques):
                posiciones[b] = 'Mesa'
                cambio = True

def validar_posiciones(posiciones, bloques, etiqueta):
    ocupantes = {}
    for b in bloques:
        destino = posiciones[b]
        if destino != 'Mesa':
            if destino in ocupantes:
                return f'En {etiqueta}: "{ocupantes[destino]}" y "{b}" no pueden estar sobre "{destino}" a la vez.'
            ocupantes[destino] = b

    for inicio in bloques:
        actual = inicio
        vistos = set()
        while posiciones[actual] != 'Mesa':
            if actual in vistos:
                return f'En {etiqueta}: hay un ciclo imposible empezando en "{inicio}".'
            vistos.add(actual)
            actual = posiciones[actual]

    return None

def hechos_desde_posiciones(posiciones, bloques, incluir_clear_y_mano):
    hechos = set()
    for b in bloques:
        hechos.add(('on', b, posiciones[b]))

    if incluir_clear_y_mano:
        for b in bloques:
            tiene_algo_encima = any(posiciones[x] == b for x in bloques)
            if not tiene_algo_encima:
                hechos.add(('clear', b))
        hechos.add(('handempty',))

    return frozenset(hechos)

def construir_acciones(bloques):
    acciones = []
    for b in bloques:
        acciones.append({
            'nombre': f'Pickup({b})',
            'pre': frozenset({('on', b, 'Mesa'), ('clear', b), ('handempty',)}),
            'add': frozenset({('holding', b)}),
            'del': frozenset({('on', b, 'Mesa'), ('clear', b), ('handempty',)}),
        })
        acciones.append({
            'nombre': f'PutDown({b})',
            'pre': frozenset({('holding', b)}),
            'add': frozenset({('on', b, 'Mesa'), ('clear', b), ('handempty',)}),
            'del': frozenset({('holding', b)}),
        })
        for x in bloques:
            if b == x:
                continue
            acciones.append({
                'nombre': f'Unstack({b}, {x})',
                'pre': frozenset({('on', b, x), ('clear', b), ('handempty',)}),
                'add': frozenset({('holding', b), ('clear', x)}),
                'del': frozenset({('on', b, x), ('clear', b), ('handempty',)}),
            })
            acciones.append({
                'nombre': f'Stack({b}, {x})',
                'pre': frozenset({('holding', b), ('clear', x)}),
                'add': frozenset({('on', b, x), ('clear', b), ('handempty',)}),
                'del': frozenset({('holding', b), ('clear', x)}),
            })
    return acciones

def aplicar_accion(estado, accion):
    nuevo = set(estado)
    nuevo -= accion['del']
    nuevo |= accion['add']
    return frozenset(nuevo)

def resolver(estado_inicial, meta, acciones):
    inicio = time.perf_counter()
    nodos_explorados = 0

    fila = deque()
    fila.append((estado_inicial, []))
    visitados = {estado_inicial}

    while fila:
        estado_actual, plan_hasta_aqui = fila.popleft()
        nodos_explorados += 1

        if meta.issubset(estado_actual):
            tiempo = time.perf_counter() - inicio
            return plan_hasta_aqui, nodos_explorados, tiempo

        for accion in acciones:
            if accion['pre'].issubset(estado_actual):
                nuevo_estado = aplicar_accion(estado_actual, accion)
                if nuevo_estado not in visitados:
                    visitados.add(nuevo_estado)
                    fila.append((nuevo_estado, plan_hasta_aqui + [accion]))

    tiempo = time.perf_counter() - inicio
    return None, nodos_explorados, tiempo

def columnas_desde_estado(estado, bloques):
    sobre_de = {}
    for hecho in estado:
        if hecho[0] == 'on':
            _, x, y = hecho
            sobre_de[x] = y

    sosteniendo = None
    for hecho in estado:
        if hecho[0] == 'holding':
            sosteniendo = hecho[1]

    bases = [b for b in bloques if sobre_de.get(b) == 'Mesa' and b != sosteniendo]
    columnas = []
    for base in bases:
        columna = [base]
        actual = base
        sigue = True
        while sigue:
            sigue = False
            for b in bloques:
                if b != sosteniendo and sobre_de.get(b) == actual:
                    columna.append(b)
                    actual = b
                    sigue = True
                    break
        columnas.append(columna)

    return columnas, sosteniendo