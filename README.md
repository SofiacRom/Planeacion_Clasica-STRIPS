# Simulador de Planeación Clásica — Mundo de los Bloques

Herramienta interactiva para explorar la **Anomalía de Sussman** y, en general,
cualquier problema del *Mundo de los Bloques* resuelto mediante planeación
clásica: operadores **STRIPS** (precondiciones, lista de agregar, lista de
eliminar) y **búsqueda en espacio de estados** (BFS).

Permite elegir qué bloques existen, cómo están ubicados al inicio, y qué
torre se quiere lograr — y muestra, paso a paso, cómo el planificador
encontró la solución.

---

## Archivos del proyecto

| Archivo              | Rol                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `blocks_world.py`            | El **modelo**: toda la lógica de planeación. No sabe nada de ventanas ni de gráficos. |
| `simulador.py`        | La **vista**: interfaz gráfica (tkinter) que usa `blocks_world.py` para resolver y dibujar. |
| `sussman_anomaly.py`  | Versión simple y comentada del mismo algoritmo, fija a 3 bloques (A, B, C) — pensada para leer y entender el código paso a paso. |
| `visualizador.py`     | Ventana gráfica sencilla (solo Anterior/Siguiente) que usa `sussman_anomaly.py`. |

Los cuatro archivos deben estar en la **misma carpeta**.

---

## Requisitos

- Python 3.8 o superior.
- `tkinter` (incluido con la instalación estándar de Python en Windows y
  macOS; en Linux a veces requiere instalarlo aparte: `sudo apt install python3-tk`).
- No se necesita instalar ningún paquete adicional con `pip`.
 
 ---

## Qué hace el simulador (`simulador.py`)

1. **Elige tus bloques** — de la A a la F.
2. **Estado inicial** — para cada bloque, un chip de color donde eliges si
   está en la Mesa o sobre otro bloque. Las opciones inválidas (que crearían
   un ciclo, o pondrían dos bloques sobre el mismo bloque) se descartan
   automáticamente. Hay una **vista en vivo** al lado que muestra la torre
   que se va formando.
3. **Objetivo** — misma mecánica, para la torre que se quiere lograr.
4. **Generar plan** — corre el planificador y muestra, en una pantalla
   aparte:
   - El estado inicial y el objetivo, dibujados.
   - Cuántos pasos tiene el plan, cuántos estados se exploraron, y cuánto
     tardó la búsqueda.
   - La secuencia completa como una tira de diagramas — cada bloque se
     mueve solo cuando el plan realmente lo mueve (nunca "salta" de lugar
     sin motivo).
   - **"Cómo se hizo"**: un acordeón por cada paso, donde se puede ver qué
     precondiciones necesitó, qué hechos agregó y cuáles eliminó.
5. **← Volver al menú** regresa a la configuración sin perder lo elegido.

---

## Diseño del código (patrón Modelo-Vista)

`blocks_world.py` no importa `tkinter` ni conoce nada de la interfaz: solo trabaja
con datos (`dict`, `set`, `frozenset`, tuplas). Esto significa que:

- Se puede cambiar por completo el diseño de `simulador.py` sin tocar una
  sola línea de la lógica de planeación.
- Se podría reemplazar `tkinter` por otra tecnología (por ejemplo, una
  versión web) reutilizando `blocks_world.py` tal cual.
- Se puede probar la lógica desde la terminal, sin abrir ninguna ventana:

```python
import blocks_world

bloques = ['A', 'B', 'C']
inicial = {'A': 'Mesa', 'B': 'Mesa', 'C': 'A'}
meta = {'A': 'B', 'B': 'C', 'C': 'Mesa'}

estado_inicial = blocks_world.hechos_desde_posiciones(inicial, bloques, True)
meta_hechos = blocks_world.hechos_desde_posiciones(meta, bloques, False)
acciones = blocks_world.construir_acciones(bloques)

plan, nodos, tiempo = blocks_world.resolver(estado_inicial, meta_hechos, acciones)
for accion in plan:
    print(accion['nombre'])
```

---

## El problema de referencia: la Anomalía de Sussman

Estado inicial por defecto: C sobre A, A y B en la mesa.
Meta por defecto: A sobre B, B sobre C.

Es un problema clásico porque ambas metas compiten por el mismo bloque (B):
lograr una primero arruina la otra si no se planea con cuidado. El
planificador de este proyecto lo resuelve encontrando el plan más corto
posible (gracias a que usa BFS), intercalando los pasos necesarios en el
orden correcto.

---

## Autora

Desarrollado por **Laura Sofia Cardona Román** — Universidad Tecnológica de Pereira  
Asignatura: Inteligencia Artificial
Profesor: Nicolas Narváez Olaya
