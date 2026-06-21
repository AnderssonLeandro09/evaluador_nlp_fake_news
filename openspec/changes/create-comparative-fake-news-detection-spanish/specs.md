# Especificaciones (Criterios de Aceptación)

## 1. Evaluación de Modelos

### Escenario: Evaluación asíncrona exitosa
**Dado** que tengo un texto en español para evaluar y el sistema está activo
**Cuando** envío el texto al endpoint `/api/v1/evaluate`
**Entonces** el sistema realiza la inferencia de forma asíncrona con ambos modelos (BETO y mBERT)
**Y** retorna un JSON con las predicciones, los tiempos de inferencia en milisegundos y las métricas calculadas

### Escenario: Validación de entrada con Pydantic
**Dado** que envío una petición con datos incompletos o formatos inválidos
**Cuando** llamo al endpoint `/api/v1/evaluate`
**Entonces** el sistema no ejecuta la inferencia
**Y** FastAPI retorna un error 422 indicando explícitamente los campos requeridos faltantes definidos en el esquema de Pydantic

## 2. Gestión de Persistencia

### Escenario: Almacenamiento de resultados
**Dado** que la inferencia ha finalizado exitosamente
**Cuando** el sistema procesa la respuesta
**Entonces** los datos (texto, etiquetas, predicciones, tiempos) se almacenan de manera persistente en la base de datos SQLite
**Y** se confirma el guardado correcto antes de responder al cliente
