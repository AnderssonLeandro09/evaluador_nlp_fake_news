# Backlog de Desarrollo

## Tareas de Entorno (Docker)
- [x] 1.1 Crear Dockerfile base para Python 3.11 con dependencias optimizadas (20 min)
- [x] 1.2 Configurar docker-compose.yml para servicios de API y volumen de persistencia SQLite (20 min)
- [x] 1.3 Configurar volúmenes para caché de modelos HuggingFace para persistencia entre contenedores (15 min)

## Tareas de Lógica (Python - FastAPI y Pydantic)
- [x] 2.1 Configurar estructura básica de proyecto FastAPI y endpoints vacíos (20 min)
- [x] 2.2 Definir esquemas Pydantic estrictos para Request (entrada) y Response (salida) (30 min)
- [x] 2.3 Implementar validación de esquemas en los endpoints usando Pydantic (25 min)

## Tareas de Lógica (Python - Inferencia Asíncrona)
- [x] 3.1 Implementar service layer asíncrono para carga y ejecución del modelo BETO (30 min)
- [x] 3.2 Implementar service layer asíncrono para carga y ejecución del modelo mBERT (30 min)
- [x] 3.3 Desarrollar orquestador para ejecutar ambas inferencias de forma concurrente con `asyncio.gather` (30 min)

## Tareas de Lógica (Python - Persistencia)
- [x] 4.1 Diseñar esquema de tabla `evaluation_results` en SQLite (20 min)
- [x] 4.2 Implementar acceso a datos asíncrono seguro para persistencia (25 min)
- [ ] 4.3 Desarrollar lógica de cálculo de métricas (accuracy, F1-score) en el service layer (30 min)
