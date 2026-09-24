import tkinter as tk
from tkinter import ttk, font as tkfont

import blocks_world

BG = '#0c1626'
PANEL = '#142642'
PANEL_2 = '#10203a'
INK = '#eef2f6'
MUTED = '#9fb3c8'
LINE = '#6fa8dc'
LINE_SOFT = '#2c4667'
OK = '#7fc79e'
ERR = '#f2867b'

COLOR_DE_BLOQUE = {
    'A': '#d9822b', 'B': '#3f8f5f', 'C': '#b34a3f',
    'D': '#4a6fa5', 'E': '#8a5cb0', 'F': '#b0762a',
}

F_TITULO = ('Segoe UI', 19, 'bold')
F_EYEBROW = ('Segoe UI', 9, 'bold')
F_SUBTITULO = ('Segoe UI', 12, 'bold')
F_CUERPO = ('Segoe UI', 10)
F_MONO = ('Consolas', 9)
F_MONO_CHICO = ('Consolas', 8)
F_BLOQUE = ('Segoe UI', 10, 'bold')

MARGEN_SUP = 54
MARGEN_INF = 40
MARGEN_LAT = 20

def rect_redondeado(canvas, x1, y1, x2, y2, radio=6, **kwargs):
    puntos = [
        x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
        x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
        x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1,
    ]
    return canvas.create_polygon(puntos, smooth=True, **kwargs)


def tamano_canvas(bloques, alto_bloque=30, ancho_bloque=30):
    espacio_columna = ancho_bloque + 16
    total_carriles = len(bloques)

    ancho = MARGEN_LAT * 2 + total_carriles * espacio_columna
    alto = MARGEN_SUP + MARGEN_INF + total_carriles * (alto_bloque + 4)

    return max(160, int(ancho)), max(110, int(alto))

def dibujar_estado(canvas, estado, bloques, alto_bloque=30, ancho_bloque=30):
    canvas.update_idletasks()
    canvas.delete('all')
    w = canvas.winfo_width() if canvas.winfo_width() > 1 else canvas.winfo_reqwidth()
    h = canvas.winfo_height() if canvas.winfo_height() > 1 else canvas.winfo_reqheight()
    y_mesa = h - MARGEN_INF + 16

    canvas.create_line(14, y_mesa, w - 14, y_mesa, width=3, fill=LINE)

    columnas, sosteniendo = blocks_world.columnas_desde_estado(estado, bloques)

    espacio_columna = ancho_bloque + 16
    total_carriles = len(bloques)
    ancho_total = total_carriles * espacio_columna - 16 if total_carriles > 0 else 0
    x_inicio = max(MARGEN_LAT, (w - ancho_total) / 2)

    for columna in columnas:
        base = columna[0]
        carril = bloques.index(base)          
        x = x_inicio + carril * espacio_columna
        y = y_mesa - 4
        for bloque in columna:
            color = COLOR_DE_BLOQUE[bloque]
            rect_redondeado(canvas, x, y - alto_bloque, x + ancho_bloque, y,
                             radio=6, fill=color, outline='')
            canvas.create_text(x + ancho_bloque / 2, y - alto_bloque / 2, text=bloque,
                                fill='white', font=F_BLOQUE)
            y -= alto_bloque + 4

    if sosteniendo:
        color = COLOR_DE_BLOQUE[sosteniendo]
        x = w - ancho_bloque - 16
        rect_redondeado(canvas, x, 14, x + ancho_bloque, 14 + alto_bloque, radio=6,
                         fill=color, outline='white', width=3)
        canvas.create_text(x + ancho_bloque / 2, 14 + alto_bloque / 2, text=sosteniendo,
                            fill='white', font=F_BLOQUE)

def formatear_hecho(hecho):
    if len(hecho) == 1:
        return hecho[0]
    if len(hecho) == 2:
        return f'{hecho[0]}({hecho[1]})'
    return f'{hecho[0]}({hecho[1]}, {hecho[2]})'

def crear_chips(marco, hechos, tipo):
    color_borde = LINE_SOFT
    color_texto = INK
    tachado = False
    if tipo == 'add':
        color_borde = OK
        color_texto = OK
    elif tipo == 'del':
        color_borde = ERR
        color_texto = ERR
        tachado = True

    fila = tk.Frame(marco, bg=PANEL)
    fila.pack(anchor='w', fill='x', pady=(4, 0))
    ancho_acumulado = 0
    ANCHO_MAX = 480

    for h in hechos:
        prefijo = '+ ' if tipo == 'add' else ''
        texto = prefijo + formatear_hecho(h)
        ancho_estimado = len(texto) * 7 + 22

        if ancho_acumulado + ancho_estimado > ANCHO_MAX and ancho_acumulado > 0:
            fila = tk.Frame(marco, bg=PANEL)
            fila.pack(anchor='w', fill='x', pady=(4, 0))
            ancho_acumulado = 0

        chip_font = tkfont.Font(family=F_MONO_CHICO[0], size=F_MONO_CHICO[1])
        if tachado:
            chip_font.configure(overstrike=True)

        chip = tk.Label(fila, text=texto, font=chip_font, fg=color_texto, bg=PANEL_2,
                         highlightbackground=color_borde, highlightthickness=1,
                         padx=7, pady=3)
        chip.pack(side='left', padx=(0, 5), pady=2)
        ancho_acumulado += ancho_estimado

class PasoAccordion(tk.Frame):
    def __init__(self, master, numero, accion):
        super().__init__(master, bg=PANEL, highlightbackground=LINE_SOFT, highlightthickness=1)
        self.abierto = False
        self.accion = accion

        self.header = tk.Frame(self, bg=PANEL_2, cursor='hand2')
        self.header.pack(fill='x')

        texto_izq = tk.Frame(self.header, bg=PANEL_2)
        texto_izq.pack(side='left', padx=14, pady=9)
        tk.Label(texto_izq, text=f'Paso {numero}', font=('Segoe UI', 9, 'bold'),
                 fg=LINE, bg=PANEL_2).pack(side='left', padx=(0, 10))
        tk.Label(texto_izq, text=accion['nombre'], font=F_MONO,
                 fg=INK, bg=PANEL_2).pack(side='left')

        self.flecha = tk.Label(self.header, text='▸', font=('Segoe UI', 10), fg=MUTED, bg=PANEL_2)
        self.flecha.pack(side='right', padx=14)

        self.cuerpo = tk.Frame(self, bg=PANEL)
        self._construir_cuerpo()

        clicables = [self.header, texto_izq, self.flecha] + list(texto_izq.winfo_children())
        for w in clicables:
            w.bind('<Button-1>', self.alternar)

    def _construir_cuerpo(self):
        marco = tk.Frame(self.cuerpo, bg=PANEL)
        marco.pack(fill='x', padx=16, pady=(10, 14))

        tk.Label(marco, text='PRECONDICIONES NECESARIAS', font=('Segoe UI', 8, 'bold'),
                 fg=MUTED, bg=PANEL).pack(anchor='w')
        crear_chips(marco, self.accion['pre'], 'normal')

        tk.Label(marco, text='HECHOS QUE AGREGA', font=('Segoe UI', 8, 'bold'),
                 fg=MUTED, bg=PANEL).pack(anchor='w', pady=(10, 0))
        crear_chips(marco, self.accion['add'], 'add')

        tk.Label(marco, text='HECHOS QUE ELIMINA', font=('Segoe UI', 8, 'bold'),
                 fg=MUTED, bg=PANEL).pack(anchor='w', pady=(10, 0))
        crear_chips(marco, self.accion['del'], 'del')

    def alternar(self, evento=None):
        self.abierto = not self.abierto
        if self.abierto:
            self.cuerpo.pack(fill='x')
            self.flecha.config(text='▾')
        else:
            self.cuerpo.pack_forget()
            self.flecha.config(text='▸')

class Chip(tk.Checkbutton):
    def __init__(self, master, texto, color, variable, command):
        super().__init__(
            master, text=f'  {texto}  ', variable=variable, command=command,
            indicatoron=False, font=F_BLOQUE, fg=color, bg=PANEL_2,
            activebackground=PANEL, selectcolor=PANEL,
            relief='solid', bd=1, padx=6, pady=5, cursor='hand2',
        )

class SelectorBloque(tk.Frame):
    def __init__(self, master, opciones, valor_inicial, on_change):
        super().__init__(master, bg=PANEL_2)
        self.opciones = opciones
        self.valor = valor_inicial
        self.on_change = on_change

        self.etiqueta = tk.Label(
            self, text=valor_inicial, font=F_BLOQUE, width=6,
            cursor='hand2', padx=8, pady=5,
        )
        self.etiqueta.pack()
        self._pintar()
        self.etiqueta.bind('<Button-1>', self._abrir_menu)

    def _color_de(self, valor):
        if valor == 'Mesa':
            return PANEL, MUTED
        return COLOR_DE_BLOQUE[valor], 'white'

    def _pintar(self):
        bg, fg = self._color_de(self.valor)
        self.etiqueta.config(bg=bg, fg=fg, text=self.valor,
                              highlightbackground=LINE_SOFT, highlightthickness=1)

    def _abrir_menu(self, evento):
        menu = tk.Menu(self, tearoff=0, bg=PANEL_2, fg=INK,
                        activebackground=LINE, activeforeground='white', bd=0)
        for op in self.opciones:
            color_fg = MUTED if op == 'Mesa' else COLOR_DE_BLOQUE[op]
            menu.add_command(label=op, foreground=color_fg, font=F_BLOQUE,
                              command=lambda o=op: self._elegir(o))
        menu.tk_popup(evento.x_root, evento.y_root)

    def _elegir(self, opcion):
        self.valor = opcion
        self._pintar()
        self.after_idle(lambda: self.on_change(opcion))

class Tarjeta(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=PANEL, highlightbackground=LINE_SOFT, highlightthickness=1, bd=0, **kwargs)

class Simulador:
    def __init__(self, root):
        self.root = root
        self.seleccionados = ['A', 'B', 'C']
        self.pos_inicial = {}
        self.pos_objetivo = {}
        self.check_vars = {}

        root.title('Simulador de Planeación Clásica — Mundo de los Bloques')
        root.configure(bg=BG)
        root.geometry('900x860')
        root.minsize(620, 500)

        self._configurar_estilos()

        contenedor = tk.Frame(root, bg=BG)
        contenedor.pack(fill='both', expand=True)
        self.lienzo_scroll = tk.Canvas(contenedor, bg=BG, borderwidth=0, highlightthickness=0)
        barra = ttk.Scrollbar(contenedor, orient='vertical', command=self.lienzo_scroll.yview)
        self.marco = tk.Frame(self.lienzo_scroll, bg=BG)
        self.marco_id = self.lienzo_scroll.create_window((0, 0), window=self.marco, anchor='nw')

        self.marco.bind('<Configure>', lambda e: self.lienzo_scroll.configure(scrollregion=self.lienzo_scroll.bbox('all')))
        self.lienzo_scroll.bind('<Configure>', lambda e: self.lienzo_scroll.itemconfig(self.marco_id, width=e.width))
        self.lienzo_scroll.configure(yscrollcommand=barra.set)
        self.lienzo_scroll.pack(side='left', fill='both', expand=True)
        barra.pack(side='right', fill='y')
        self._activar_rueda_mouse(self.lienzo_scroll)

        pad = {'padx': 26}
        tk.Label(self.marco, text='PLANEACIÓN CLÁSICA · STRIPS · BÚSQUEDA EN ESPACIO DE ESTADOS', font=F_EYEBROW, fg=LINE, bg=BG).pack(anchor='w', **pad, pady=(22, 4))
        tk.Label(self.marco, text='Simulador del Mundo de los Bloques', font=F_TITULO, fg=INK, bg=BG).pack(anchor='w', **pad)
        tk.Label(self.marco, text='Elige tus bloques, selecciona cómo están ubicados y qué torre quieres lograr. El planificador calcula los movimientos automáticamente.', font=F_CUERPO, fg=MUTED, bg=BG, justify='left').pack(anchor='w', **pad, pady=(4, 16))

        self.pantalla_config = tk.Frame(self.marco, bg=BG)
        self.pantalla_config.pack(fill='x')

        t1 = Tarjeta(self.pantalla_config)
        t1.pack(fill='x', padx=20, pady=8)
        tk.Label(t1, text='1. ¿Qué bloques tienes?', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 8))
        self.marco_chips = tk.Frame(t1, bg=PANEL)
        self.marco_chips.pack(anchor='w', padx=18, pady=(0, 16))
        self._dibujar_chips()

        t2 = Tarjeta(self.pantalla_config)
        t2.pack(fill='x', padx=20, pady=8)
        tk.Label(t2, text='2. Estado inicial — ¿cómo están ubicados?', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 8))
        marco_t2 = tk.Frame(t2, bg=PANEL)
        marco_t2.pack(fill='x', padx=18, pady=(0, 16))
        self.marco_inicial = tk.Frame(marco_t2, bg=PANEL)
        self.marco_inicial.pack(side='left', anchor='n')
        marco_preview_ini = tk.Frame(marco_t2, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        marco_preview_ini.pack(side='left', padx=(16, 0), anchor='n')
        tk.Label(marco_preview_ini, text='ESTADO INICIAL', font=('Segoe UI', 8, 'bold'),fg=MUTED, bg=PANEL_2).pack(anchor='w', padx=10, pady=(8, 0))
        self.canvas_preview_inicial = tk.Canvas(marco_preview_ini, bg=PANEL_2, highlightthickness=0)
        self.canvas_preview_inicial.pack(padx=8, pady=8)

        t3 = Tarjeta(self.pantalla_config)
        t3.pack(fill='x', padx=20, pady=8)
        tk.Label(t3, text='3. Objetivo — ¿cómo deben quedar?', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 8))
        marco_t3 = tk.Frame(t3, bg=PANEL)
        marco_t3.pack(fill='x', padx=18, pady=(0, 16))
        self.marco_objetivo = tk.Frame(marco_t3, bg=PANEL)
        self.marco_objetivo.pack(side='left', anchor='n')
        marco_preview_obj = tk.Frame(marco_t3, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        marco_preview_obj.pack(side='left', padx=(16, 0), anchor='n')
        tk.Label(marco_preview_obj, text='OBJETIVO', font=('Segoe UI', 8, 'bold'), fg=MUTED, bg=PANEL_2).pack(anchor='w', padx=10, pady=(8, 0))
        self.canvas_preview_objetivo = tk.Canvas(marco_preview_obj, bg=PANEL_2, highlightthickness=0)
        self.canvas_preview_objetivo.pack(padx=8, pady=8)

        self._refrescar_grids()   

        self.etiqueta_error = tk.Label(self.pantalla_config, text='', fg=ERR, bg=BG, font=F_CUERPO, wraplength=700, justify='left')
        self.etiqueta_error.pack(anchor='w', padx=26, pady=(2, 6))

        marco_botones = tk.Frame(self.pantalla_config, bg=BG)
        marco_botones.pack(anchor='w', padx=20, pady=(4, 20))
        ttk.Button(marco_botones, text='Generar plan', style='Primario.TButton', command=self.generar_plan).pack(side='left', padx=(0, 8))
        ttk.Button(marco_botones, text='Reiniciar', style='Secundario.TButton', command=self.reiniciar).pack(side='left')


        self.pantalla_resultado = tk.Frame(self.marco, bg=BG)
        marco_volver = tk.Frame(self.pantalla_resultado, bg=BG)
        marco_volver.pack(anchor='w', padx=20, pady=(0, 10))
        ttk.Button(marco_volver, text='← Volver al menú', style='Secundario.TButton', command=self.volver_al_menu).pack(side='left')

        self.marco_resultados = tk.Frame(self.pantalla_resultado, bg=BG)
        self.marco_resultados.pack(fill='x')

        tk.Label(self.marco, text='Simulador de planeación clásica (STRIPS) · búsqueda en espacio de estados (BFS)', font=('Segoe UI', 8), fg=MUTED, bg=BG).pack(anchor='w', padx=26, pady=(10, 22))

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('Primario.TButton', background=LINE, foreground='#0c1626', font=F_BLOQUE, padding=(16, 9), borderwidth=0)
        estilo.map('Primario.TButton', background=[('active', '#8fc0e8')])
        estilo.configure('Secundario.TButton', background=PANEL_2, foreground=INK, font=F_BLOQUE, padding=(16, 9), borderwidth=1)
        estilo.map('Secundario.TButton', background=[('active', '#1b2f4d')])
        estilo.configure('Vertical.TScrollbar', background=LINE_SOFT, troughcolor=BG)
        estilo.configure('Horizontal.TScrollbar', background=LINE_SOFT, troughcolor=BG)

    def _activar_rueda_mouse(self, widget):
        widget.bind_all('<MouseWheel>', lambda e: widget.yview_scroll(int(-e.delta / 120), 'units'))

    def _mostrar_pantalla_resultado(self):
        self.pantalla_config.pack_forget()
        self.pantalla_resultado.pack(fill='x')

    def volver_al_menu(self):
        self.pantalla_resultado.pack_forget()
        self.pantalla_config.pack(fill='x')

    def _dibujar_chips(self):
        for w in self.marco_chips.winfo_children():
            w.destroy()
        for b in blocks_world.TODOS_LOS_BLOQUES:
            var = tk.BooleanVar(value=(b in self.seleccionados))
            self.check_vars[b] = var
            chip = Chip(self.marco_chips, b, COLOR_DE_BLOQUE[b], var, self._cambio_bloques)
            chip.pack(side='left', padx=4)

    def _cambio_bloques(self):
        self.seleccionados = sorted([b for b, v in self.check_vars.items() if v.get()])
        self._refrescar_grids()

    def _refrescar_grids(self):
        for b in self.seleccionados:
            self.pos_inicial.setdefault(b, 'Mesa')
            self.pos_objetivo.setdefault(b, 'Mesa')
        self.pos_inicial = {b: self.pos_inicial[b] for b in self.seleccionados}
        self.pos_objetivo = {b: self.pos_objetivo[b] for b in self.seleccionados}

        blocks_world.corregir_posiciones(self.pos_inicial, self.seleccionados)
        blocks_world.corregir_posiciones(self.pos_objetivo, self.seleccionados)

        self._construir_grid(self.marco_inicial, self.pos_inicial, 'está sobre')
        self._construir_grid(self.marco_objetivo, self.pos_objetivo, 'debe quedar sobre')
        self._actualizar_previews()

    def _construir_grid(self, marco, posiciones, texto_label):
        for w in marco.winfo_children():
            w.destroy()

        for b in self.seleccionados:
            fila = tk.Frame(marco, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
            fila.pack(anchor='w', pady=4, fill='x')

            tk.Label(fila, text=b, fg='white', bg=COLOR_DE_BLOQUE[b], width=3, font=F_BLOQUE).pack(side='left', padx=8, pady=6)
            tk.Label(fila, text=texto_label, fg=MUTED, bg=PANEL_2, width=16, anchor='w', font=F_CUERPO).pack(side='left')

            opciones = blocks_world.opciones_validas(b, posiciones, self.seleccionados)

            def al_cambiar(valor, bloque=b, marco=marco, posiciones=posiciones, texto=texto_label):
                posiciones[bloque] = valor
                blocks_world.corregir_posiciones(posiciones, self.seleccionados)
                self._construir_grid(marco, posiciones, texto)
                self._actualizar_previews()

            selector = SelectorBloque(fila, opciones, posiciones[b], al_cambiar)
            selector.pack(side='left', padx=8, pady=6)

    def _actualizar_previews(self):
        bloques = self.seleccionados
        ancho, alto = tamano_canvas(bloques, alto_bloque=26, ancho_bloque=26)

        self.canvas_preview_inicial.config(width=ancho, height=alto)
        estado_inicial = blocks_world.hechos_desde_posiciones(self.pos_inicial, bloques, True)
        dibujar_estado(self.canvas_preview_inicial, estado_inicial, bloques, alto_bloque=26, ancho_bloque=26)

        self.canvas_preview_objetivo.config(width=ancho, height=alto)
        meta = blocks_world.hechos_desde_posiciones(self.pos_objetivo, bloques, False)
        dibujar_estado(self.canvas_preview_objetivo, frozenset(meta), bloques, alto_bloque=26, ancho_bloque=26)

    def generar_plan(self):
        self.etiqueta_error.config(text='')

        if len(self.seleccionados) < 2:
            self.etiqueta_error.config(text='Selecciona al menos 2 bloques.')
            return

        error = blocks_world.validar_posiciones(self.pos_inicial, self.seleccionados, 'el estado inicial')
        if error:
            self.etiqueta_error.config(text=error)
            return
        error = blocks_world.validar_posiciones(self.pos_objetivo, self.seleccionados, 'el objetivo')
        if error:
            self.etiqueta_error.config(text=error)
            return

        estado_inicial = blocks_world.hechos_desde_posiciones(self.pos_inicial, self.seleccionados, True)
        meta = blocks_world.hechos_desde_posiciones(self.pos_objetivo, self.seleccionados, False)
        acciones = blocks_world.construir_acciones(self.seleccionados)

        plan, nodos, tiempo = blocks_world.resolver(estado_inicial, meta, acciones)
        self._mostrar_resultados(estado_inicial, meta, plan, nodos, tiempo)
        self._mostrar_pantalla_resultado()

    def _mostrar_resultados(self, estado_inicial, meta, plan, nodos, tiempo):
        for w in self.marco_resultados.winfo_children():
            w.destroy()

        bloques = self.seleccionados
        ancho_grande, alto_grande = tamano_canvas(bloques, alto_bloque=30, ancho_bloque=30)
        ancho_chico, alto_chico = tamano_canvas(bloques, alto_bloque=20, ancho_bloque=20)

        t = Tarjeta(self.marco_resultados)
        t.pack(fill='x', padx=20, pady=8)
        tk.Label(t, text='Estado inicial vs. objetivo', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 10))
        marco_diag = tk.Frame(t, bg=PANEL)
        marco_diag.pack(anchor='w', padx=18, pady=(0, 16))

        sub_ini = tk.Frame(marco_diag, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        sub_ini.pack(side='left', padx=(0, 12))
        tk.Label(sub_ini, text='ESTADO INICIAL', font=('Segoe UI', 8, 'bold'), fg=MUTED, bg=PANEL_2).pack(anchor='w', padx=10, pady=(8, 0))
        canvas_ini = tk.Canvas(sub_ini, width=ancho_grande, height=alto_grande, bg=PANEL_2, highlightthickness=0)
        canvas_ini.pack(padx=8, pady=8)
        canvas_ini.bind('<Configure>', lambda e, c=canvas_ini, s=estado_inicial: dibujar_estado(c, s, bloques))

        sub_obj = tk.Frame(marco_diag, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        sub_obj.pack(side='left')
        tk.Label(sub_obj, text='OBJETIVO', font=('Segoe UI', 8, 'bold'), fg=MUTED, bg=PANEL_2).pack(anchor='w', padx=10, pady=(8, 0))
        canvas_obj = tk.Canvas(sub_obj, width=ancho_grande, height=alto_grande, bg=PANEL_2, highlightthickness=0)
        canvas_obj.pack(padx=8, pady=8)
        canvas_obj.bind('<Configure>', lambda e, c=canvas_obj, s=frozenset(meta): dibujar_estado(c, s, bloques))

        if plan is None:
            t2 = Tarjeta(self.marco_resultados)
            t2.pack(fill='x', padx=20, pady=8)
            tk.Label(t2, text='No se encontró un plan válido.', fg=ERR, bg=PANEL, font=F_CUERPO).pack(padx=18, pady=14)
            return

        t3 = Tarjeta(self.marco_resultados)
        t3.pack(fill='x', padx=20, pady=8)
        tk.Label(t3, text='Resumen de la búsqueda', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 10))
        marco_stats = tk.Frame(t3, bg=PANEL)
        marco_stats.pack(anchor='w', padx=18, pady=(0, 16))
        self._stat(marco_stats, str(len(plan)), 'Pasos en el plan')
        self._stat(marco_stats, str(nodos), 'Estados explorados')
        self._stat(marco_stats, f'{tiempo*1000:.3f} ms', 'Tiempo de búsqueda')

        t4 = Tarjeta(self.marco_resultados)
        t4.pack(fill='x', padx=20, pady=8)
        tk.Label(t4, text='La secuencia encontrada', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 8))

        marco_scroll_pasos = tk.Frame(t4, bg=PANEL)
        marco_scroll_pasos.pack(fill='x', padx=18, pady=(0, 16))
        canvas_scroll = tk.Canvas(marco_scroll_pasos, height=alto_chico + 30, bg=PANEL, highlightthickness=0)
        barra_h = ttk.Scrollbar(marco_scroll_pasos, orient='horizontal', command=canvas_scroll.xview)
        marco_tira = tk.Frame(canvas_scroll, bg=PANEL)
        marco_tira.bind('<Configure>', lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all')))
        canvas_scroll.create_window((0, 0), window=marco_tira, anchor='nw')
        canvas_scroll.configure(xscrollcommand=barra_h.set)
        canvas_scroll.pack(fill='x')
        barra_h.pack(fill='x')

        estados_por_paso = [estado_inicial]
        estado_actual = estado_inicial
        for accion in plan:
            estado_actual = blocks_world.aplicar_accion(estado_actual, accion)
            estados_por_paso.append(estado_actual)

        self._agregar_paso_a_tira(marco_tira, estado_inicial, 'Inicio', 0, bloques, ancho_chico, alto_chico)
        for i, accion in enumerate(plan, start=1):
            tk.Label(marco_tira, text='→', font=('Segoe UI', 14), fg=LINE, bg=PANEL).grid(row=0, column=(i * 2) - 1, padx=2)
            self._agregar_paso_a_tira(marco_tira, estados_por_paso[i], f'{i}. {accion["nombre"]}', i * 2, bloques, ancho_chico, alto_chico)

        t5 = Tarjeta(self.marco_resultados)
        t5.pack(fill='x', padx=20, pady=8)
        tk.Label(t5, text='Cómo se hizo — detalle de cada paso', font=F_SUBTITULO, fg=INK, bg=PANEL).pack(anchor='w', padx=18, pady=(14, 2))
        tk.Label(t5, text='Abre cada paso para ver qué precondiciones se revisaron y qué hechos cambiaron en la mesa.',
                 font=F_CUERPO, fg=MUTED, bg=PANEL, wraplength=650, justify='left').pack(anchor='w', padx=18, pady=(0, 10))

        marco_acordeon = tk.Frame(t5, bg=PANEL)
        marco_acordeon.pack(fill='x', padx=18, pady=(0, 16))
        for i, accion in enumerate(plan, start=1):
            item = PasoAccordion(marco_acordeon, i, accion)
            item.pack(fill='x', pady=4)

    def _stat(self, marco, numero, etiqueta):
        caja = tk.Frame(marco, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        caja.pack(side='left', padx=(0, 12))
        tk.Label(caja, text=numero, font=('Segoe UI', 16, 'bold'), fg=LINE, bg=PANEL_2).pack(padx=16, pady=(8, 0))
        tk.Label(caja, text=etiqueta, font=('Segoe UI', 8), fg=MUTED, bg=PANEL_2).pack(padx=16, pady=(0, 8))

    def _agregar_paso_a_tira(self, marco_tira, estado, etiqueta, columna, bloques, ancho, alto):
        sub = tk.Frame(marco_tira, bg=PANEL)
        sub.grid(row=0, column=columna, padx=5)
        canvas = tk.Canvas(sub, width=ancho, height=alto, bg=PANEL_2, highlightbackground=LINE_SOFT, highlightthickness=1)
        canvas.pack()
        canvas.bind('<Configure>', lambda e, c=canvas, s=estado: dibujar_estado(c, s, bloques, alto_bloque=20, ancho_bloque=20))
        tk.Label(sub, text=etiqueta, font=('Segoe UI', 8), fg=INK, bg=PANEL, wraplength=ancho, justify='center').pack(pady=(5, 0))

    def reiniciar(self):
        self.seleccionados = ['A', 'B', 'C']
        self.pos_inicial = {}
        self.pos_objetivo = {}
        self._dibujar_chips()
        self._refrescar_grids()
        self.etiqueta_error.config(text='')
        for w in self.marco_resultados.winfo_children():
            w.destroy()

if __name__ == '__main__':
    ventana = tk.Tk()
    app = Simulador(ventana)
    ventana.mainloop()