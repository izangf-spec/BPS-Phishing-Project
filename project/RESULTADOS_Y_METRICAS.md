# Resultados y métricas: entrega 2 (modelo de URL, PhishVN)

Fuente única: la ejecución final de `project/project-model.ipynb` (salidas guardadas, 0 errores, 279 s de cálculo). Todas las cifras de este documento proceden de esa ejecución. Las cifras de versiones anteriores se han retirado.

**Advertencia principal.** El conjunto de test no está limpio: una versión anterior lo leyó y reportó el mismo modelo, umbral y coste. Las cifras de test de la sección 4 son una comprobación contaminada, no una evaluación independiente. No hay muestra nueva en el repositorio.

## 1. Modelo final y umbral

- **Configuración:** LR-B (regresión logística sobre `url_len`, `num_dots`, `num_subdomains`, `has_at` y `tld`), C = 10, calibración isotónica, umbral 0,22.
- **Hiperparámetros elegidos dentro de cada pliegue interior:** C = 10, 10 y 1.
- **Umbral:** mínimo coste sobre las predicciones fuera de muestra (OOF) anidadas de los 14.665 registros de desarrollo.
- **Coste OOF:** 7.213,4 EUR por 1.000 URL. Es optimista, porque el umbral se eligió sobre esas mismas predicciones.
- **Umbral teórico** con precios ilustrativos (falso positivo 30 EUR, falso negativo 100 EUR, verdadero positivo 5 EUR, verdadero negativo 0 EUR): 30 / (30 + 100 − 5) = 0,24.
- **Huella:** SHA-256 de `model.joblib` = `ae32a3385a5226fb…`, igual que en `model_config.json`.

## 2. Datos y particiones

| Conjunto | URL | Phishing | Nota |
|---|---|---|---|
| Desarrollo (train + validation oficiales; niveles gold y silver) | 14.665 | 2.100 (14,3 %) | Base de todas las decisiones de modelado. |
| Test (oficial) | 4.332 | 487 (11,2 %) | Todas fechadas entre 2023 y 2025. Leído en una versión anterior (sección 4). |
| Bronze | 34.119 | 29.510 | Excluido del benchmark; solo se describe. |

**Protocolos de validación:**

| Protocolo | Entrenamiento | Validación | Uso |
|---|---|---|---|
| T1 primario (corte 31-dic-2021, por dominio) | 9.975 URL (1.526 phishing) | 4.690 URL (574 phishing, 12,2 %) | Selección del modelo y del umbral. |
| T2 sensibilidad (corte 31-dic-2020) | 8.833 URL (389 phishing) | 5.832 URL (1.711 phishing, 29,3 %) | Comprobación de sensibilidad. |
| T3 sensibilidad (todos los dominios fechados) | 10.387 URL (1.526 phishing) | 4.278 URL (574 phishing, 13,4 %) | Comprobación de sensibilidad. |
| R referencia (5 pliegues aleatorios agrupados por dominio) | media 11.732 URL | media 2.933 URL (media 420 phishing) | Referencia sin orden temporal. |

**Regla del corte.** Los dominios se asignan completos a un lado de la partición. Un dominio va a validación si su primera URL de phishing es igual o posterior al 31-dic-2021. Por eso 4 URL con fecha 31-dic-2021 quedan en validación y 4 URL de 2022 quedan en entrenamiento (figura fig_05_1).

## 3. Comparación de modelos en validación primaria (T1)

| Configuración | Calibración | Umbral | VP | FP | FN | VN | Precisión | Recall | FPR | Coste EUR por 1.000 | AUC | Brier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **LR-B** | isotónica | 0,25 | 417 | 167 | 157 | 3.949 | 0,714 | 0,726 | 0,041 | **4.860,3** | 0,940 | 0,048 |
| HGB-B | sigmoide | 0,24 | 462 | 517 | 112 | 3.599 | 0,472 | 0,805 | 0,126 | 6.187,6 | 0,935 | 0,055 |
| LR-A | isotónica | 0,30 | 241 | 40 | 333 | 4.076 | 0,858 | 0,420 | 0,010 | 7.613,0 | 0,839 | 0,066 |
| HGB-A | sigmoide | 0,34 | 212 | 40 | 362 | 4.076 | 0,841 | 0,369 | 0,010 | 8.200,4 | 0,840 | 0,071 |
| Basal: siempre benigno | — | — | 0 | 0 | 574 | 4.116 | — | 0,000 | 0,000 | 12.238,8 | — | — |
| Basal: has_at = 1 | — | — | 0 | 1 | 574 | 4.115 | 0,000 | 0,000 | 0,000 | 12.245,2 | — | — |

- LR-B es la configuración más barata en validación primaria y es la que pasa a la fase final.
- En validación primaria, LR-B con umbral 0,25 envía a revisión 584 de 4.690 URL (417 phishing y 167 benignas).
- Las dos basales son referencias técnicas. No son la regla actual de la organización, que no está documentada.

**Sensibilidad del coste por protocolo (EUR por 1.000 URL, configuración de cada modelo):**

| Protocolo | LR-A | LR-B | HGB-A | HGB-B |
|---|---|---|---|---|
| T1 primario | 7.613,0 | **4.860,3** | 8.200,4 | 6.187,6 |
| T2 (corte 2020) | **20.378,1** | 26.405,2 | 27.478,6 | 28.666,0 |
| T3 (todos los dominios) | 8.353,2 | **5.379,9** | 8.997,2 | 8.080,9 |
| R (5 pliegues aleatorios) | 10.331,4 | **7.023,2** | 10.255,4 | 7.370,3 |

LR-B no gana en T2, que tiene menos fechas de phishing de entrenamiento. Esa diferencia se declara; no se ha cambiado la selección.

## 4. Resultado final en test (contaminado)

Umbral 0,22, modelo final entrenado con todos los datos de desarrollo.

| Modelo | VP | FP | FN | VN | Precisión | Recall | FPR | AUC | Coste EUR por 1.000 |
|---|---|---|---|---|---|---|---|---|---|
| **LR-B final** | 171 | 52 | 316 | 3.793 | 0,767 | **0,351** | 0,014 | 0,911 | **7.852,0** |
| Siempre benigno | 0 | 0 | 487 | 3.845 | — | 0,000 | 0,000 | — | 11.241,9 |
| has_at = 1 | 0 | 2 | 487 | 3.843 | 0,000 | 0,000 | 0,001 | — | 11.255,8 |

- **Recall** del modelo final: 0,351 (intervalo de confianza del 95 % de Wilson: 0,310 a 0,395).
- **Por cada 1.000 URL:** unos 39 phishing llegan primero a un analista, 12 benignas se revisan sin necesidad y 73 phishing no se detectan. Son proporciones de la matriz con precios ilustrativos.
- **Frente a no hacer nada,** el coste baja un 30 % (7.852 frente a 11.242 EUR por 1.000 URL). La mejora frente a la regla actual no se puede cuantificar, porque esa regla no está documentada.
- **Recall por año de primera aparición** (test, post hoc): 2023 0,272 (n = 114); 2024 0,380 (n = 334); 2025 0,333 (n = 39).
- **Recall por TLD** (test, post hoc): `.vn` 0,000 (n = 37 phishing); otros TLD 0,380 (n = 450 phishing).
- **Calibración global:** prevalencia observada en test 11,24 %; probabilidad media predicha 7,98 %; URL marcadas 5,15 %. En desarrollo (OOF): prevalencia 14,32 %, probabilidad media 14,32 %, marcadas 10,60 %. El modelo subestima la prevalencia en test.

## 5. Errores por grupo (equidad)

Grupos: dominios `.vn` frente a otros TLD. Intervalos de Wilson del 95 % entre corchetes.

| Evaluación | Grupo | URL | Phishing | FPR | Recall | Coste EUR por 1.000 |
|---|---|---|---|---|---|---|
| Aleatoria (R) | `.vn` | 7.243 | 59 | 0,0024 [0,0015; 0,0038] | 0,000 [0,000; 0,061] | 885,0 |
| Aleatoria (R) | otros TLD | 7.422 | 2.041 | 0,0572 [0,0513; 0,0638] | 0,602 [0,581; 0,623] | 13.013,3 |
| Temporal (T1) | `.vn` | 2.470 | 7 | 0,0000 [0,0000; 0,0016] | 0,000 [0,000; 0,354] | 283,4 |
| Temporal (T1) | otros TLD | 2.220 | 567 | 0,1010 [0,0874; 0,1165] | 0,735 [0,698; 0,770] | 9.952,7 |

- Ningún phishing `.vn` se detecta en ninguna evaluación. El grupo `.vn` es pequeño, así que el intervalo es amplio.
- De los 325 falsos positivos de la validación aleatoria, 266 proceden de la fuente Tranco, 30 de `tinnhiem_web`, 29 de `tinnhiem_org`, y 1 cae en un dominio `.gov.vn`.

## 6. Interpretación

**Importancia por permutación** (LR-B, 5 pliegues de validación; aumento del Brier y caída del AUC):

| Entrada | Aumento del Brier (media, DE) | Caída del AUC (media) |
|---|---|---|
| `num_dots` | 0,175 (0,034) | 0,295 |
| `num_subdomains` | 0,164 (0,017) | 0,194 |
| `tld` | 0,074 (0,007) | 0,246 |
| `url_len` | 0,001 (0,001) | 0,004 |
| `has_at` | 0,000 (0,000) | 0,000 |

**Tres predicciones individuales** (pliegue 0 de la validación aleatoria, umbral 0,31, solo entradas; no se muestran URL):

| Caso | Probabilidad | `url_len` | Puntos | Subdominios | TLD |
|---|---|---|---|---|---|
| Verdadero positivo | 1,000 | 19 | 5 | 4 | `bar` |
| Falso negativo | 0,001 | 13 | 2 | 0 | `vn` |
| Falso positivo | 0,965 | 24 | 1 | 0 | `top` |

Las importancias describen el comportamiento de la puntuación, no por qué una URL es peligrosa: los puntos, los subdominios y el TLD son fáciles de cambiar para un atacante.

## 7. Costes y umbral

| Coste FP (EUR) | Coste FN (EUR) | Umbral teórico | Umbral óptimo en OOF aleatorio | Coste en validación primaria con umbral congelado (EUR por 1.000) |
|---|---|---|---|---|
| 15 | 50 | 0,25 | 0,25 | 2.652,5 |
| **30** | **100** | **0,24** | **0,21** | **4.860,3** (caso base) |
| 60 | 200 | 0,24 | 0,21 | 9.276,1 |

El umbral depende de los precios. Los precios son ilustrativos y deben sustituirse por los de la organización antes de cualquier cálculo de negocio. El umbral congelado (0,25 en T1) se aplica a validación una sola vez.

## 8. Comprobaciones de la ejecución final

| Comprobación | Resultado |
|---|---|
| Notebook: celdas | 58 (28 de código, 30 Markdown) |
| Notebook: errores y celdas sin ejecutar | 0 y 0 |
| Notebook: imágenes PNG visibles | 8 |
| Tiempo de cálculo | 279 s |
| Diferencias respecto a la ejecución anterior de la revisión | Ninguna, salvo las líneas de tiempo |
| `test_saved_model.py` (proceso independiente) | 21 comprobaciones, código de salida 0 |
| Palabras Markdown visibles | 2.477 |

## 9. Límites

- **Test contaminado.** Se leyó en una versión anterior y en diagnósticos posteriores. No hay muestra nueva ni independiente.
- **Sin regla actual documentada.** No se puede medir la mejora frente a la regla que la organización usa hoy.
- **Costes ilustrativos.** Las cifras en euros dependen de precios no reales.
- **Generalización limitada.** Los datos son vietnamitas y de fuentes concretas. No hay evidencia para otras regiones, idiomas ni para el tráfico actual.
- **`.vn` sin detecciones.** Ningún phishing `.vn` se detecta en ninguna evaluación.
- **Recall reciente bajo.** En phishing de 2023 a 2025 el recall es 0,35. El modelo encuentra menos de la mitad.
- **Etiquetas no verificadas.** Según el editor, 12 de 99 etiquetas de phishing resolubles son legítimas (12,1 %) y 2 de 50 benignas son abusivas (4,0 %) (Nguyen Vu, 2026, sección 4). Esto no se ha verificado aquí.
- **Feed sin fechas recientes.** La última detección fechada del feed NCSC es del 18-feb-2025.
- **Outliers conservados.** Hay 109 URL de desarrollo por encima del umbral de 36 caracteres (máximo 70); se mantienen.
