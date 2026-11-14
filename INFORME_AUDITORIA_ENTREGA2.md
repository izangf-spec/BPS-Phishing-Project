# Informe de auditoría: entrega 2 (Unit 17, modelo de URL)

**Fecha:** 13-nov-2026. **Revisión final:** 14-nov-2026. **Ámbito:** repositorio `BPS_Phishing_Project`, carpeta `project/` y documentación, contra `PROJECT_BRIEF_2.md` (lección 09; documento del curso, no incluido en el repositorio, cuyo brief del alumno es `project/project-brief.md`) y el encargo de revisión final.

**Método.** (1) Checklist con el estado real antes de modificar nada. (2) Correcciones. (3) Ejecución completa y comprobaciones. (4) Estado final de cada requisito con su evidencia. Ningún requisito se marca como CUMPLE sin evidencia reproducible en el paquete.

Estados: **CUMPLE** (evidencia reproducible en el paquete); **NO CUMPLE** (el requisito falta o no se cumple tal como está escrito); **NO VERIFICABLE** (no puede comprobarse con el repositorio ni con las fuentes disponibles).

## 1. Resumen

- 72 requisitos: **59 CUMPLE**, **3 NO CUMPLE**, **10 NO VERIFICABLE**. Los tres NO CUMPLE (S8.2, T2, T3) se deben al test no independiente y a la falta de muestra nueva.
- El notebook se ejecuta de principio a fin en un proceso nuevo: 279 s de cálculo, 0 errores y 8 gráficos visibles. Las salidas coinciden con la ejecución anterior, salvo las líneas de tiempo.
- **No cumple por diseño:** el test no está virgen y no hay muestra nueva independiente (S8.2, T2, T3). No se puede arreglar sin datos nuevos; queda declarado.
- **No verificable:** la regla actual de la organización (no existe en la documentación) y la comprobación completa de las referencias.
- Ningún requisito de forma queda sin resolver (sección 5.2).

## 2. Cambios en esta revisión

- **Datos:** movidos a `project/data/`, con rutas relativas (antes, `data/` en la raíz y `../data/` en el notebook).
- **Gráficos:** 8 PNG estáticos con matplotlib, visibles en GitHub, además del HTML de Plotly. Etiquetas de eje con unidades en todos los gráficos Plotly. Anotaciones n en fig_10_1. Kaleido descartado porque necesita Chrome instalado.
- **Sección 1 y 5:** baseline ingenua puntuada en validación (antes solo en test). Regla actual declarada como no documentada. Partición por dominio explicada, con el corte «igual o posterior al 31-dic-2021» (el texto anterior decía «posterior»).
- **Sección 8:** test declarado como no cumplido. No se afirma que sea virgen.
- **Sección 6:** validación anidada descrita en el texto y verificada en el código.
- **Referencias:** apellido del editor corregido a «Nguyen Vu», según su ficha CFF (antes «Vu»). Referencia de Gebru retirada por no verificable. DOI de Wilson (1927) añadido tras comprobarlo.
- **Palabras:** 2.477 en la revisión final (antes 2.346 en la anterior y 2.481 en la primera). Textos ajustados en las secciones 2, 4, 5, 7, 8 y 9, sin cambios en los resultados.
- **Dependencias:** `matplotlib==3.11.2` añadido a `requirements.txt`, con el motivo.
- **Documentación:** README (raíz y proyecto), RESULTADOS_Y_METRICAS.md y CHECKLIST_REQUISITOS.md reescritos desde la ejecución final. Este informe es nuevo.
- **Sin cambios:** modelo, umbral (0,22), métricas y coste (7.852,0 EUR por 1.000 URL en test).

### Revisión final (14-nov-2026)

- **H2 (sección 3):** estado «Supported», como exige el formato del brief. Antes «Supported in silver; refuted in gold». La explicación se mantiene: diferencias significativas (p < 0,001) con dirección que varía entre tiers; no se afirma una regla universal.
- **Bloques de stakeholder:** añadidos al final de la sección 0 y de la sección 13.
- **P5:** párrafo «Tools in the triage workflow» al final de la sección 6 sobre Python, scikit-learn, joblib y Plotly/matplotlib. No se afirma integración con un SOC.
- **Palabras:** 2.477, dentro del rango 1.200 a 2.500 del encargo. Supera el objetivo anterior de 2.350 (T7). Para compensar los bloques se eliminaron tres frases repetidas: la de limpieza en el bloque de la sección 2, la de «regla actual» en la sección 5 y una frase del bloque de la sección 11.
- **Sin cambios:** modelo, hiperparámetros, umbral (0,22), métricas, coste y resultados. Las celdas de código no se han modificado.
- **Documentos actualizados:** esta auditoría, `project/CHECKLIST_REQUISITOS.md`, `project/RESULTADOS_Y_METRICAS.md`, `project/README.md` y `README.md`.

## 3. Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| Ejecución completa del notebook en un proceso nuevo (nbconvert) | 58 celdas (28 de código); 0 errores; 0 celdas sin ejecutar; 8 imágenes; 279 s de cálculo |
| Diferencias entre la ejecución anterior y la final, sin líneas de tiempo | Ninguna (salidas de las 28 celdas de código comparadas) |
| `test_saved_model.py` en proceso independiente | 21 de 21 comprobaciones; código de salida 0 |
| `scripts/validate_project.py` | 35/35 comprobaciones superadas |
| `count_markdown_words.py` sobre el notebook ejecutado | 2.477 palabras |
| SHA-256 de `model.joblib` frente a `model_config.json` | Coinciden (`ae32a338…757`) |
| Rutas absolutas en el código del notebook | 0 |
| Tamaño de los datos en `project/data/` | Mayor fichero 11,3 MB; todos por debajo de 50 MB |
| Versiones de `requirements.txt` frente al entorno instalado | 12 de 12 coinciden |
| Referencias citadas en el texto (por apellido u organización) | 20 de 20 |
| Cifras antiguas en los documentos | Ninguna (ver K10) |

## 4. Tabla de requisitos oficiales y del encargo

Cada fila reúne el estado, la evidencia y la explicación. Las secciones coinciden con `project/CHECKLIST_REQUISITOS.md`.

### A. Entregable y requisitos técnicos (brief §1)

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| E1 | Notebook construido desde la plantilla oficial resources/project-model-template.ipynb | **NO VERIFICABLE** | La plantilla no está en el repositorio. Los encabezados siguen los apartados 0 a 13 del brief (§3). | No puedo comparar la estructura con la plantilla. Depende de que subas el archivo. |
| E2 | Notebook en project/, junto a project-brief.md | **CUMPLE** | project/project-model.ipynb; project/project-brief.md. | — |
| E3 | Enlace de GitHub al notebook enviado al profesor | **NO VERIFICABLE** | No se ha hecho push (instrucción del usuario). | Depende del usuario: subir el repositorio y enviar el enlace. |
| E4 | Entrega antes de la fecha y de forma individual | **NO VERIFICABLE** | La fecha no aparece en los documentos del proyecto. | Depende del usuario. La autoría individual es una declaración del alumno. |
| E5 | Markdown entre 1.200 y 2.500 palabras visibles (el código no cuenta) | **CUMPLE** | 2.477 palabras con count_markdown_words.py sobre el notebook ejecutado; dentro de 1.200 a 2.500. | El recuento incluye tablas y referencias. |
| E6 | Se ejecuta de principio a fin en kernel limpio, en menos de 10 minutos, con requirements.txt | **CUMPLE** | Ejecución con nbconvert en un proceso nuevo: 279 s de cálculo, 0 errores, 0 celdas sin ejecutar. | Probado en Linux con Python 3.13.18, en el entorno de verificación, no en el equipo del usuario. |
| E7 | Paquetes adicionales en la primera celda de código, con motivo | **CUMPLE** | matplotlib es el único paquete extra. Está en requirements.txt y la primera celda explica el motivo. | Interpretación: el entorno del curso es requirements.txt, así que no hay celda de instalación. |
| E8 | Datos en project/data/ (CSV o Parquet de menos de 50 MB) o URL estable; sin rutas absolutas | **CUMPLE** | project/data/: 6 ficheros; el mayor pesa 11,3 MB. El notebook usa rutas relativas (data/dataset_url.csv). | Escaneo de rutas absolutas en el notebook: 0 coincidencias. |
| E9 | Reproducible: random_state fijado en todo | **CUMPLE** | SEED = 42 en los componentes con azar. Dos ejecuciones de la revisión dan salidas idénticas salvo las líneas de tiempo. | — |
| E10 | Salidas guardadas en el notebook, para verlas sin ejecutarlo | **CUMPLE** | 28 celdas de código ejecutadas y guardadas; 8 imágenes PNG visibles en el notebook. | Los gráficos Plotly interactivos no se ven en GitHub; por eso hay PNG (ver T8). |
| E11 | Gráficos con Plotly, con título y ejes etiquetados con unidades | **CUMPLE** | Los 8 gráficos se construyen con Plotly. Todos tienen título y etiquetas de eje con unidades (recuento, %, caracteres o adimensional). | Las copias PNG (matplotlib) llevan las mismas etiquetas (ver T6). |
| E12 | Modelo final como un único pipeline scikit-learn con joblib, de columnas crudas a predicción, en project/model.joblib | **CUMPLE** | project/model.joblib: pipeline de URL cruda a probabilidad calibrada. Su SHA-256 coincide con model_config.json. | Necesita url_features.py y psl/ en la misma carpeta; está declarado en project/README.md. |
| E13 | Modelo incluido en el repositorio si pesa menos de 50 MB | **CUMPLE** | 379.808 bytes. | — |

### B. Secciones 0 a 13 del brief (§3)

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| S0.1 | Resumen ejecutivo de cinco líneas: pregunta, modelo, comparación con la regla actual, acción y límite principal | **CUMPLE** | Sección 0: cinco viñetas. | — |
| S0.2 | El resumen indica cuánto mejora el modelo frente a la regla actual | **NO VERIFICABLE** | No hay regla actual documentada (T1). | El resumen compara con no hacer nada (11.242 frente a 7.852 EUR por 1.000 URL, con precios ilustrativos) y lo declara. |
| S1.1 | Tabla del brief convertida en tarea de ML completa | **CUMPLE** | Sección 1: decisión, tarea y etiqueta, grano y momento, entradas, regla actual, métrica y traducción de negocio. | — |
| S1.2 | Fila de la regla actual de hoy, con su valor | **NO VERIFICABLE** | La fila indica que la regla no está documentada (T1). | Se usan dos basales ingenuas como referencia técnica, sin afirmar que sean la regla. |
| S1.3 | Qué cambió respecto al brief y por qué | **CUMPLE** | Sección 1: hipótesis, KPI y etiqueta se mantienen; validación temporal; bronze excluido; cruce con Tranco no ejecutado. | — |
| S2 | Datos y calidad: carga, resumen de la ficha del dataset y limpieza con cifras | **CUMPLE** | Sección 2: 53.116 URL; 0 filas eliminadas; 0 duplicados; 4 columnas vacías sin rellenar; 109 outliers conservados (umbral de 36 caracteres). | — |
| S3.1 | Distribución del objetivo y entre 2 y 4 gráficos que importan al modelo | **CUMPLE** | Sección 3: fig_03_1 a fig_03_4 (etiquetas por nivel, mezcla de escenarios, indicadores léxicos, longitud por escenario). | — |
| S3.2 | Tabla de hipótesis con cada una marcada como supported, refuted o not testable yet | **CUMPLE** | H2 pasa a «Supported», la escala del brief. H1 también usa la escala. | H3 mantiene «Supported (dated phishing only)»: la aclaración entre paréntesis no está en la escala; no se cambia por encargo. H2 conserva la explicación: diferencias significativas, con dirección que varía entre tiers. |
| S4 | Features: construcción, motivo por el que deberían ayudar y comprobación de fugas | **CUMPLE** | Sección 4: tabla con «Why it should help» y concordancia con la columna del dataset; comprobación de fugas en la celda 20. | — |
| S5.1 | Partición que respeta el tiempo (entrenar con el pasado y evaluar con el futuro) | **CUMPLE** | Validación primaria: dominios cuya primera URL de phishing es igual o posterior al 31-dic-2021. Test: URL de 2023 a 2025. | La partición es por dominio: 4 URL con fecha 31-dic-2021 quedan en validación y 4 de 2022 en entrenamiento (sección 5 lo explica). |
| S5.2 | Basal ingenua (mayoría o regla simple) con sus puntuaciones | **CUMPLE** | Validación primaria (4.690 URL): siempre benigno 12.238,8 EUR por 1.000; has_at = 1: 12.245,2 EUR. | — |
| S5.3 | Regla actual con sus puntuaciones | **NO VERIFICABLE** | No hay regla documentada (T1). | Depende del usuario. |
| S6 | Al menos dos modelos (uno simple y uno ensemble) como pipelines, con tabla comparativa en validación | **CUMPLE** | LR-A, LR-B (regresión logística) y HGB-A, HGB-B (gradient boosting), todos como Pipeline; tabla en la sección 6 y en RESULTADOS_Y_METRICAS.md. | — |
| S7.1 | Métrica principal justificada para la decisión | **CUMPLE** | Sección 7: coste esperado por 1.000 URL con precios ilustrativos, junto con precisión y recall. La exactitud se descarta. | Los precios son ilustrativos (ver D2). |
| S7.2 | Matriz de confusión leída en términos de negocio y umbral elegido | **CUMPLE** | Sección 7: matriz en validación primaria (umbral 0,25). Sección 8: matriz de test (umbral 0,22). Umbral teórico 0,24. | — |
| S8.1 | Validación cruzada adecuada a los datos, búsqueda de hiperparámetros y CV temporal si hay fechas | **CUMPLE** | GridSearchCV dentro de cada pliegue; CV agrupada por dominio (anidada); protocolos temporales T1 a T3. | — |
| S8.2 | Una única evaluación final en test, que no se tocó antes | **NO CUMPLE** | La versión anterior leyó el test y reportó el mismo modelo y coste. Hay diagnósticos posteriores sobre el test (sección 8). | Declarado en la sección 8. Ver T2 y T3. |
| S9.1 | Importancia de variables (permutation importance o SHAP) | **CUMPLE** | Sección 9 y fig_09_1: num_dots 0,175; num_subdomains 0,164; tld 0,074 (aumento del Brier). | — |
| S9.2 | Dos o tres predicciones individuales explicadas | **CUMPLE** | Sección 9: un verdadero positivo (1,000), un falso negativo (0,001) y un falso positivo (0,965), del pliegue 0. | — |
| S9.3 | Si los factores coinciden con las hipótesis | **CUMPLE** | Sección 9: H2 y H3 solo se reflejan en parte. | — |
| S10.1 | Errores comparados en al menos un grupo relevante | **CUMPLE** | Sección 10 y fig_10_1: dominios .vn frente a otros TLD, con intervalos de Wilson, en validación aleatoria y temporal. | El grupo .vn es pequeño (59 y 7 phishing); el intervalo es amplio y se indica. |
| S10.2 | Datos personales o sensibles implicados y cómo se protegen | **CUMPLE** | Sección 10: el editor declara datos personales redactados (Nguyen Vu, 2026). El proyecto no almacena URL fuera del dataset. Se cita el RGPD. | La redacción la declara el editor; no se ha auditado. |
| S10.3 | Qué sale mal si el modelo se equivoca y para quién | **CUMPLE** | Sección 10: tabla de riesgos con quién sufre cada error y su mitigación. | — |
| S11.1 | Decisión, condiciones de no confianza, próximos pasos y qué añade el bloque 4 | **CUMPLE** | Sección 11: ordenar la revisión sin bloquear; no usar en tráfico .vn; próximos pasos; bloque 4. | — |
| S11.2 | Mejora frente a la regla actual, traducida a KPI o a dinero | **NO VERIFICABLE** | Sin regla actual no hay comparación posible (T1). | Mejora frente a no hacer nada: de 11.242 a 7.852 EUR por 1.000 URL (ilustrativo). |
| S12 | Modelo guardado en project/model.joblib, recargado, con una predicción y versiones impresas | **CUMPLE** | Sección 12; celda 54 (recarga y dos predicciones); celda 55 (versiones); test_saved_model.py en proceso independiente: 21 comprobaciones, código 0. | — |
| S13.1 | Referencias en formato APA, con todas las fuentes usadas | **CUMPLE** | Sección 13: 20 entradas en formato APA; cada autor o organización aparece citado en el texto. | Las citas de software usan el nombre de equipo habitual; ver S13.2. |
| S13.2 | Fuentes verificadas; sin DOI, autores, títulos ni fechas inventados | **NO VERIFICABLE** | Crossref no responde desde el entorno de verificación. Wilson (1927) se comprobó en Scilit en la revisión anterior. El título de Brier (1950) tiene dos versiones en fuentes secundarias. Los autores de software no se han contrastado con la cita oficial de cada proyecto, ni el año 2026 de las versiones. La ficha CFF del editor indica versión 3.1.0 con el DOI de la versión 4. | No he encontrado indicios de invención, pero no todas las fuentes pueden comprobarse. Ver pendientes. |
| S-BLK.1 | Cada sección termina con un bloque «What this means for the stakeholder» de dos o tres frases | **CUMPLE** | Presente en las secciones 1 a 12. | — |
| S-BLK.2 | Lo mismo en las secciones 0 y 13 | **CUMPLE** | Bloque «What this means for the stakeholder» al final de la sección 0 (celda 1) y de la sección 13 (celda 57). | Añadido en la revisión final. |

### C. Criterios Pearson (brief §4)

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| P5 | Discutir cómo las herramientas y tecnologías apoyan el proceso de negocio | **CUMPLE** | Sección 6, «Tools in the triage workflow»: Python y scikit-learn (reentrenar y revisar el modelo con cada lote), joblib (pipeline en un único archivo), Plotly y matplotlib (gráficos de seguimiento). | Explica el apoyo al proceso. No se afirma integración con un SOC: no está implementada. |
| P6, P7 | Diseñar e implementar la solución de extremo a extremo | **CUMPLE** | Ejecución completa del notebook, validate_project.py y test_saved_model.py. | — |
| M3, M4 | Evaluar las ventajas y justificar las recomendaciones | **CUMPLE** | Comparación con basales ingenuas y entre cuatro modelos; recomendación limitada a ordenar la revisión. | La ventaja frente a la regla actual no es verificable (S11.2). |
| D2 | Evaluar la solución frente a las necesidades del negocio y del usuario | **CUMPLE** | Secciones 7, 10 y 11: métrica, costes, límites y uso previsto. | Los costes son ilustrativos. |
| D1 | Implicaciones éticas y organizativas | **CUMPLE** | Sección 10: riesgos, grupos afectados, privacidad y quién asume el error. Sección 11: revisión humana. | — |

### D. Requisitos del encargo de revisión

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| T1 | Baseline empresarial real: regla actual de la organización documentada | **NO VERIFICABLE** | No aparece en project-brief.md ni en la documentación del repositorio (búsqueda por «rule», «current», «today», «regla», «manual», «blocklist» y «baseline»). | Depende del usuario. Sin ella no hay mejora cuantificada frente a la regla. |
| T2 | Test no tocado antes de la evaluación final | **NO CUMPLE** | La versión anterior leyó el test; hay diagnósticos posteriores. La sección 8 lo declara. | No se afirma que el test sea virgen. |
| T3 | Muestra nueva e independiente en el repositorio | **NO CUMPLE** | No existe. No se ha simulado. | Depende del usuario: obtener URL etiquetadas posteriores a la extracción de PhishVN. |
| T4 | Validación anidada: hiperparámetros dentro de cada pliegue; calibración y umbral solo desde OOF; test sin intervención | **CUMPLE** | Código (celdas 29 a 37): GridSearchCV dentro de cada pliegue, con C elegido por pliegue [10, 10, 1]; calibración y umbral desde OOF; test abierto solo en la celda 38. Las secciones 6 y 8 lo describen. | El coste de selección (7.213,4 EUR por 1.000 URL) se marca como optimista. |
| T5 | Referencias verificadas; sin DOI, autores, títulos ni fechas inventados | **NO VERIFICABLE** | Ver S13.2. | — |
| T6 | Gráficos: título, ejes con unidades, leyendas, valores y porcentajes correctos y escalas no engañosas | **CUMPLE** | Los 8 gráficos revisados uno a uno y comparados con las tablas de salida (por ejemplo, la matriz de test 3.793 / 52 / 316 / 171). Correcciones: unidades en ejes, explicación de fig_05_1 y anotaciones n en fig_10_1. | Los valores .vn son cero con intervalos amplios; las anotaciones n lo indican. |
| T7 | Palabras visibles entre 1.200 y 2.500 y 13 secciones conservadas | **CUMPLE** | 2.477 palabras. Secciones 0 a 13 presentes. | El rango del encargo es 1.200 a 2.500. El objetivo anterior de 2.200 a 2.350 ya no se cumple: los bloques pedidos superan ese tope. |
| T8 | Gráficos estáticos PNG visibles en GitHub | **CUMPLE** | 8 imágenes PNG como salida de celda; project/figures/ contiene PNG y HTML. | — |
| T9 | Carpetas project/data/ y project/figures/; dependencias declaradas | **CUMPLE** | project/data/ y project/figures/ existen; project/requirements.txt fija 12 versiones, todas comprobadas contra el entorno. | — |

### E. Procedimiento de comprobación final

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| K1 | Kernel limpio en menos de 10 minutos | **CUMPLE** | 279 s de cálculo (menos de 5 min). | — |
| K2 | Salidas guardadas | **CUMPLE** | 0 errores; 28 celdas de código ejecutadas; 8 imágenes. | — |
| K3 | test_saved_model.py en proceso independiente | **CUMPLE** | 21 comprobaciones; código de salida 0. | — |
| K4 | validate_project.py | **CUMPLE** | 35/35 comprobaciones superadas. | — |
| K5 | Recuento de palabras | **CUMPLE** | 2.477 palabras. | — |
| K6 | Rutas relativas (escaneo de rutas absolutas) | **CUMPLE** | 0 rutas absolutas en el notebook; sin coincidencias en los documentos. | — |
| K7 | Dependencias sin declarar | **CUMPLE** | Todos los paquetes de terceros importados por el notebook están en requirements.txt. | IPython llega como dependencia de ipykernel, que está fijado en requirements.txt. |
| K8 | SHA-256 de model.joblib frente a model_config.json | **CUMPLE** | ae32a3385a5226fb5d2e3e5819579e0789a6f02162ff6f51f34f158ebb14d757 en ambos. | — |
| K9 | ZIP descomprimido en carpeta nueva y comprobado | **CUMPLE** | Se descomprime en carpeta nueva y se repiten K3, K4, K5 y K8 allí, con los mismos resultados. | — |
| K10 | README, checklist, resultados y auditoría sin cifras antiguas ni contradicciones | **CUMPLE** | Búsqueda de cifras antiguas (2.481, 2.648, 288 s, 57 celdas, 18 comprobaciones, ../data) sin coincidencias en los documentos. | Kaleido aparece solo en la explicación de su descarte. |

### F. Restricciones del encargo

| ID | Requisito | Estado | Evidencia | Explicación |
|---|---|---|---|---|
| F1 | No cambiar modelo, umbral ni métricas sin razón metodológica | **CUMPLE** | Salidas de la revisión idénticas a la ejecución anterior (solo cambian los tiempos). Umbral 0,22; LR-B; C = 10; calibración isotónica. | Los cambios son de texto, figuras, referencias y documentación. |
| F2 | No hacer push a GitHub sin autorización | **CUMPLE** | No se ha hecho push. | — |
| F3 | No inventar reglas de negocio | **CUMPLE** | La regla actual no existe en la documentación. Los costes son ilustrativos y están marcados como tales. | — |
| F4 | No afirmar que el test es virgen; no ocultar limitaciones; no eliminar secciones exigidas | **CUMPLE** | Sección 8 y apartado de límites. Secciones 0 a 13 presentes. | — |
| F5 | Preguntas al usuario solo las imprescindibles | **CUMPLE** | Cuatro pendientes, los mínimos necesarios (sección 5). | — |

## 5. Pendientes

### 5.1 Depende del usuario

1. **T1, S0.2, S5.3, S11.2:** la descripción de la regla operativa actual para revisar URL (cómo se decide hoy) y sus resultados, si existen. Con ellos se calcula la mejora real frente a la regla.
2. **T2, T3, S8.2:** una muestra nueva de URL etiquetadas posteriores a la extracción de PhishVN, si puedes conseguirla. Si no, la limitación se mantiene declarada.
3. **E1:** el archivo resources/project-model-template.ipynb, para comparar la estructura con la plantilla oficial.
4. **E3, E4:** el enlace de GitHub y la fecha límite. El push a GitHub requiere tu autorización expresa.

### 5.2 Decisiones del alumno

Ninguna abierta. S3.2, S-BLK.2 y P5 se resolvieron en la revisión final (sección 2).

### 5.3 Límites de esta auditoría

- La ejecución y las comprobaciones se han hecho en Linux con Python 3.13.18, no en el equipo del usuario ni en GitHub.
- Crossref no respondió desde el entorno de verificación; las referencias no se han contrastado con el registro de origen.
- `data_docs/docs/datasheet.md` (documentación del editor) cita a Gebru et al. (2021). Esa cita no forma parte de las referencias del notebook.
- Los costes en euros son ilustrativos.
