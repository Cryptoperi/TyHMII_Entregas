"""
Genera el informe del Taller de Fotografía Técnica (Módulo 3) a partir de las fotos de la carpeta fotos/.

Uso (desde la carpeta "Modulo 3"):
    python generar_informe.py

Las fotos se nombran con la convención  NN_plano_descripcion.jpg  (ver README), por ejemplo:
    01_contexto_tablero-electrico.jpg
    02_componente_tablero-electrico.jpg
    03_detalle_borne-oxidado.jpg

El script:
  1. Lee los datos EXIF de cada foto (fecha, cámara, ISO, diafragma, velocidad, distancia focal).
  2. Verifica la checklist de la cátedra (ISO <= 400, sin zoom digital, etc.) y marca advertencias.
  3. Genera copias reducidas para la web (fotos_web/, máx. 1600 px) y la tabla para el README.
  4. Arma el informe HTML y lo imprime a PDF con Microsoft Edge (sin instalar nada).
"""
import html, os, re, subprocess, sys
from datetime import datetime
from PIL import Image, ExifTags

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS, WEB = os.path.join(AQUI, "fotos"), os.path.join(AQUI, "fotos_web")
PDF = os.path.join(AQUI, "TP3 - Taller de Fotografia Tecnica - TyHMII - Glasner.pdf")
TAGS = {v: k for k, v in ExifTags.TAGS.items()}
PLANOS = {"contexto": "Plano de contexto", "componente": "Plano medio (componente)", "detalle": "Primer plano (detalle)",
          "rasante": "Luz rasante", "frontal": "Luz frontal", "escala": "Testigo métrico", "antes": "Antes", "despues": "Después"}


def exif(img):
    raw = img.getexif()
    d = {ExifTags.TAGS.get(k, k): v for k, v in raw.items()}
    try:
        d.update({ExifTags.TAGS.get(k, k): v for k, v in raw.get_ifd(0x8769).items()})
    except Exception:
        pass
    def num(v):
        try: return float(v)
        except Exception: return None
    t = num(d.get("ExposureTime"))
    return {
        "fecha": str(d.get("DateTimeOriginal") or d.get("DateTime") or "s/d"),
        "camara": " ".join(str(d.get(k, "")).strip() for k in ("Make", "Model")).strip() or "s/d",
        "iso": d.get("ISOSpeedRatings") or d.get("PhotographicSensitivity"),
        "f": num(d.get("FNumber")),
        "t": t,
        "focal": num(d.get("FocalLength")),
        "zoom": num(d.get("DigitalZoomRatio")),
        "flash": d.get("Flash"),
    }


def velocidad(t):
    if not t: return "s/d"
    return f"1/{round(1 / t)} s" if t < 1 else f"{t:g} s"


def chequeos(e):
    avisos = []
    iso = e["iso"][0] if isinstance(e["iso"], (tuple, list)) else e["iso"]
    if iso and int(iso) > 400: avisos.append(f"ISO {iso} > 400: puede haber ruido que tape microfisuras.")
    if e["t"] and e["t"] > 1 / 30: avisos.append("Velocidad lenta (> 1/30 s): riesgo de foto movida si no hubo apoyo o trípode.")
    if e["zoom"] and e["zoom"] > 1: avisos.append("Zoom digital activado: pierde resolución real.")
    if e["flash"] and int(e["flash"]) & 1: avisos.append("Flash disparado: puede aplanar texturas.")
    return avisos


def main():
    if not os.path.isdir(FOTOS) or not [f for f in os.listdir(FOTOS) if f.lower().endswith((".jpg", ".jpeg", ".png"))]:
        sys.exit("No hay fotos en la carpeta fotos/. Copiá ahí tus fotos con la convención NN_plano_descripcion.jpg")
    os.makedirs(WEB, exist_ok=True)
    filas, bloques = [], []
    for n in sorted(os.listdir(FOTOS)):
        if not n.lower().endswith((".jpg", ".jpeg", ".png")): continue
        img = Image.open(os.path.join(FOTOS, n)); e = exif(img)
        m = re.match(r"(\d+)_([a-z]+)_(.+)\.\w+$", n.lower())
        plano = PLANOS.get(m.group(2), m.group(2)) if m else "—"
        desc = m.group(3).replace("-", " ") if m else n
        web = os.path.splitext(n)[0] + ".jpg"
        w = img.convert("RGB"); w.thumbnail((1600, 1600)); w.save(os.path.join(WEB, web), quality=85)
        iso = e["iso"][0] if isinstance(e["iso"], (tuple, list)) else e["iso"]
        params = f"ISO {iso or 's/d'} · f/{e['f']:g} · {velocidad(e['t'])}" if e["f"] else f"ISO {iso or 's/d'} · {velocidad(e['t'])}"
        avisos = chequeos(e)
        filas.append(f"| {n} | {plano} | {desc} | {params} | {'⚠️ ' + ' '.join(avisos) if avisos else '✅'} |")
        bloques.append(f"""<div class="foto"><img src="fotos_web/{html.escape(web)}"><div class="pie"><b>{html.escape(plano)}</b>: {html.escape(desc)}<br>
          <span>{html.escape(params)} · {html.escape(e['camara'])} · {html.escape(e['fecha'])}</span>
          {'<div class="aviso">' + '<br>'.join(map(html.escape, avisos)) + '</div>' if avisos else ''}</div></div>""")
    tabla = "| Archivo | Plano / técnica | Descripción | Parámetros (EXIF) | Checklist |\n|---|---|---|---|---|\n" + "\n".join(filas)
    open(os.path.join(AQUI, "tabla_fotos.md"), "w", encoding="utf-8").write(tabla + "\n")
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>TP3 Fotografía Técnica</title><style>
      @page {{ size: A4; margin: 18mm; }} body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; color: #1d2733; }}
      h1 {{ color: #123a5c; font-size: 18pt; margin-bottom: 2px; }} h2 {{ color: #123a5c; border-bottom: 2px solid #2a7ab0; font-size: 13pt; }}
      .foto {{ page-break-inside: avoid; margin: 10px 0 16px; }} .foto img {{ width: 100%; max-height: 150mm; object-fit: contain; background: #f4f4f4; }}
      .pie {{ font-size: 9.5pt; margin-top: 4px; }} .pie span {{ color: #556; }} .aviso {{ color: #a35a00; margin-top: 3px; }}
      li {{ margin-bottom: 3px; }}</style></head><body>
      <h1>Trabajo Práctico N.º 3 – Taller de Fotografía Técnica</h1>
      <div>Técnicas y Herramientas Modernas II – UNCuyo – Grupo 2 (Grupo λ) – Raimundo Glasner – {datetime.now():%d/%m/%Y}</div>
      <h2>Objetivo</h2><p>Aplicar la fotografía como instrumento de registro técnico para inspección y mantenimiento industrial:
      encuadre por tercios, secuencia de tres planos, iluminación rasante para revelar texturas, testigo métrico para dimensionar y
      configuración manual del sensor (ISO bajo, diafragma y velocidad adecuados), sin filtros ni edición.</p>
      <h2>Checklist aplicada en cada toma</h2><ol><li>¿Activé la cuadrícula (regla de los tercios)?</li>
      <li>¿Hice los 3 planos (contexto → componente → detalle)?</li><li>¿La luz revela la textura del fallo o la oculta?</li>
      <li>¿Coloqué la referencia métrica, paralela al plano de la falla?</li><li>¿ISO ≤ 400 y velocidad suficiente para no mover la foto?</li></ol>
      <h2>Registro fotográfico</h2>{''.join(bloques)}
      <h2>Conclusiones</h2><p>[Completar: qué técnica aportó más información, qué falla o detalle se pudo dimensionar, qué se haría distinto.]</p>
      </body></html>"""
    src = os.path.join(AQUI, "informe_fotografia.html")
    open(src, "w", encoding="utf-8").write(doc)
    import tempfile
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    with tempfile.TemporaryDirectory() as perfil:
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={perfil}",
                        f"--print-to-pdf={PDF}", "file:///" + src.replace("\\", "/")], check=False, capture_output=True)
    if not os.path.exists(PDF):
        print("No se pudo generar el PDF automáticamente: abrí informe_fotografia.html en el navegador e imprimilo como PDF.")
    print(f"Listo: {len(filas)} fotos.\n  PDF:   {PDF}\n  Tabla: tabla_fotos.md (pegala en el README)")


if __name__ == "__main__":
    main()
