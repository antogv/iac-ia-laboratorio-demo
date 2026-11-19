# Laboratorio de IaC e IA · empieza por aquí

Este repositorio contiene **un único proyecto ficticio**, `portal-demo`. Vas a trabajar en **una copia propia** del repositorio durante todos los ejercicios. Cada ejercicio amplía lo que hiciste en el anterior. Al principio solo existe el código necesario para el ejercicio 1; los demás archivos aparecerán cuando tú los crees.

## Tu primer paso

1. Descarga y abre la [Guía del ejercicio 1 (Word)](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1). Léela desde el principio: incluye los botones para crear tu copia y comprobarla.
2. En esta página pulsa **Use this template → Create a new repository**. En **Owner** elige tu usuario, deja **Include all branches** desmarcado y crea un repositorio público con otro nombre. **Hazlo una sola vez.**
3. Comprueba que la URL de tu copia empieza por `https://github.com/TU_USUARIO/`. A partir de aquí, todos tus cambios irán a esa copia.
4. Abre **Actions** en tu copia. Si aparece **Validacion IaC → Commit inicial → comprobar** en verde, el laboratorio ya ejecutó OpenTofu en GitHub. La guía explica qué hacer si no aparece.
5. Continúa la guía del ejercicio 1: abre **tu copia** en `github.dev`, cambia `variables.tf`, confirma y publica el cambio, y consulta la nueva ejecución de Actions.

**No necesitas instalar GitHub Actions, OpenTofu, Git ni VS Code en tu equipo para la ruta de navegador.** GitHub Actions es una pestaña de GitHub; el workflow instala OpenTofu en un ejecutor temporal. `github.dev` es el editor web. Abre ChatGPT o Copilot Chat en **otra pestaña** para preguntar, predecir y revisar. Usa solo datos ficticios.

## Las cinco guías

| Orden | Guía Word | Qué harás en la misma copia |
| --- | --- | --- |
| 1 | [Puesta en marcha, IA y primer plan](GUIAS/Guia_Alumnado_Ejercicio_1.docx?raw=1) | Crear la copia, comprender tres archivos, cambiar un entorno y leer el resultado. |
| 2 | [Dos escenarios](GUIAS/Guia_Alumnado_Ejercicio_2.docx?raw=1) | Parametrizar la configuración y comparar dos planes. |
| 3 | [Revisión y gobierno](GUIAS/Guia_Alumnado_Ejercicio_3.docx?raw=1) | Crear una rama, añadir validaciones y revisar un pull request. |
| 4 | [Automatización y evidencias](GUIAS/Guia_Alumnado_Ejercicio_4.docx?raw=1) | Mejorar el workflow y diagnosticar un fallo real de la práctica. |
| 5 | [Módulo reutilizable](GUIAS/Guia_Alumnado_Ejercicio_5.docx?raw=1) | Crear un módulo local y usarlo para dos fichas ficticias. |

**El ejercicio 2 empieza donde dejaste el 1**; no crees otra copia. Sigue el mismo principio para los siguientes. Las guías están en `GUIAS/` para poder descargarlas; el código que editarás está en la raíz y en `.github/workflows/`.

## Qué son los archivos iniciales

| Archivo | Función |
| --- | --- |
| `variables.tf` | Declara el entorno, inicialmente `desarrollo`. |
| `main.tf` | Describe una ficha ficticia con `terraform_data`. |
| `outputs.tf` | Define el resumen del plan. |
| `.github/workflows/validacion.yml` | Instala OpenTofu y ejecuta las comprobaciones en GitHub Actions. |

El workflow calcula un plan, **no ejecuta `tofu apply`** y no crea una web ni infraestructura comercial. Si tu equipo permite VS Code local, puedes usarlo con **esa misma copia**: el código y la comprobación en Actions son los mismos. La ruta principal, explicada paso a paso en los Word, funciona desde el navegador.

## Arquitectura ficticia

- **Necesidad:** representar el portal principal (`portal-demo` por defecto) y una ficha de ayuda (`portal-ayuda`) como datos de ejemplo. No son aplicaciones web ni servicios desplegados.
- **Reutilización:** las instancias `portal` y `ayuda`, declaradas en `main.tf`, usan el mismo módulo local `./modulo_ficha`. El módulo define una ficha mediante `terraform_data` y expone sus datos con el output `resumen`.
- **Entradas:** cada instancia recibe `nombre` y `entorno`. El módulo exige que el nombre empiece por `portal-` y que el entorno sea `desarrollo`, `pruebas` o `integracion`. La raíz usa `portal-demo` y `pruebas` por defecto; la ficha de ayuda usa `portal-ayuda` y comparte el entorno seleccionado.
- **Escenarios:** el plan predeterminado usa los valores por defecto. `escenario-integracion.tfvars` cambia el portal a `portal-interno` y el entorno a `integracion`; ambos planes recorren las mismas instancias y el mismo módulo.
- **Evidencias:** el workflow de GitHub Actions instala OpenTofu 1.13.9 y ejecuta `init` sin backend, comprobación recursiva de formato, `validate` y dos planes (predeterminado e integración). Resume sus resultados en el resumen de Actions y publica `evidencia.txt` como artefacto.
- **Limitación:** no se ejecuta `apply` ni se crean servidores, redes u otros recursos cloud reales. `terraform_data` solo representa datos para el plan, por lo que este ejercicio no genera infraestructura ni costes cloud.

## Política del laboratorio

La política permite únicamente dos fichas ficticias: `module.portal.terraform_data.ficha` y `module.ayuda.terraform_data.ficha`. Ambas deben ser recursos `terraform_data` con una única acción de creación, tener nombres que empiecen por `portal-` (la ayuda debe llamarse exactamente `portal-ayuda`) y compartir un entorno conocido, no sensible y permitido: `desarrollo`, `pruebas` o `integracion`.

`tofu validate` comprueba si la configuración es válida para OpenTofu; no determina si los cambios previstos cumplen estas reglas del laboratorio. La política analiza el JSON de cada plan y responde a esa pregunta de negocio antes de cualquier aplicación.

Los resultados aparecen en los pasos de plan y política de GitHub Actions, en el resumen de la ejecución y en el artefacto `evidencia.txt`. El workflow no ejecuta `tofu apply`: las fichas usan `terraform_data` y no despliegan infraestructura. Es un control didáctico y limitado, no una garantía de gobierno de producción ni una autorización para desplegar cambios reales.
