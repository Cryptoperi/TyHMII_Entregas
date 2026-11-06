# Módulo 3: Taller de Fotografía Técnica

> 📷 **Pendiente: tomar y cargar las fotos.** La estructura del informe y el generador automático ya están listos.

## Descripción
La fotografía se aplica como **instrumento de registro técnico** para inspección, análisis de fallas y mantenimiento industrial, siguiendo el curso [Fotografía Digital para ingenieros](https://github.com/ricardorpalma/Fotograf-a_Digital) de la cátedra. La consigna central: una foto técnica no se edita ni lleva filtros, y tiene que permitir **ubicar, ver y medir** el defecto.

## Contenidos aplicados
1. **La imagen como documento técnico:** sin filtros, sin mejoras por IA, sin zoom digital, con los metadatos (EXIF) conservados.
2. **Encuadre estructurado:** regla de los tercios con la cuadrícula activada y la secuencia de 3 planos (contexto → componente → detalle).
3. **Iluminación técnica:** luz rasante (lateral) para revelar grietas, rayas y corrosión; luz frontal sin reflejos para placas y códigos; balance de blancos correcto.
4. **Escalas:** testigo métrico (regla o calibre) paralelo al plano de la falla y toma perpendicular para evitar el paralaje.
5. **Sensor en manual:** ISO 100–400, diafragma f/8–f/11 para tener profundidad de campo y velocidad ≥ 1/250 s si hay vibración.

## Plan de tomas (12 fotos)

| N.º | Archivo sugerido | Qué fotografiar | Técnica |
|---|---|---|---|
| 01 | `01_contexto_<objeto>.jpg` | Equipo o instalación completa (tablero, máquina, estructura) | Tercios, f/8, ISO 100–200 |
| 02 | `02_componente_<objeto>.jpg` | El componente donde está el defecto | Plano medio, cuadrícula |
| 03 | `03_detalle_<defecto>.jpg` | El defecto en primer plano | Punto crítico en una intersección de los tercios |
| 04 | `04_frontal_<defecto>.jpg` | La misma superficie con luz frontal | Muestra que la luz frontal "aplana" la textura |
| 05 | `05_rasante_<defecto>.jpg` | La misma superficie con linterna a 10–20° | Luz rasante: la textura se ve |
| 06 | `06_escala_<defecto>.jpg` | El defecto con una regla al lado | Cámara perpendicular, regla en el mismo plano |
| 07 | `07_contexto_<objeto2>.jpg` | Segundo caso: corrosión o desgaste en exterior | Luz difusa (día nublado o sombra) |
| 08 | `08_detalle_<defecto2>.jpg` | Detalle del segundo caso | f/11, ISO bajo |
| 09 | `09_escala_<defecto2>.jpg` | Segundo caso con escala | Toma perpendicular |
| 10 | `10_frontal_<placa>.jpg` | Placa de identificación o código de barras | Luz frontal sin reflejos (ángulo leve) |
| 11 | `11_antes_<tarea>.jpg` | Antes de una tarea de mantenimiento o limpieza | Mismo encuadre que la 12 |
| 12 | `12_despues_<tarea>.jpg` | Después de la tarea | Mismo encuadre que la 11 |

Ideas de objetos en casa o en la facultad: tablero eléctrico, un perfil o caño oxidado, una pieza metálica rayada, una soldadura, una rueda o engranaje gastado, una pared con fisuras, la placa de un motor o electrodoméstico.

## Cómo generar el informe
1. Copiar las fotos **originales del celular o la cámara** (sin pasar por WhatsApp, que borra los EXIF) a la carpeta `Modulo 3/fotos/`, con los nombres del plan.
2. Ejecutar desde la carpeta `Modulo 3`:
   ```bash
   python generar_informe.py
   ```
3. El script lee los EXIF (ISO, diafragma, velocidad, cámara, fecha) y marca las tomas que no cumplen la checklist (ISO > 400, flash, zoom digital, velocidad lenta). Además genera las copias livianas para la web en `fotos_web/` y el PDF del informe.
4. Completar la sección de conclusiones del informe y pegar en este README la tabla de `tabla_fotos.md`.

## 📥 Descargas
El informe en PDF se publicará en esta carpeta una vez cargadas las fotos.
