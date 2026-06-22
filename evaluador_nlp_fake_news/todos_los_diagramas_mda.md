# Modelado MDA: Plataforma de Evaluación de Fake News (BETO vs mBERT)

Este archivo contiene la documentación visual del sistema desglosada según los niveles MDA (CIM, PIM, PSM).

---

## NIVEL CIM (Negocio)

### Diagrama 1: Flujo de Proceso de Negocio
```mermaid
graph TD
    A[Investigador] --> B[Ingresar Texto/Dataset]
    B --> C{Evaluación Paralela}
    C --> D[Inferencia BETO]
    C --> E[Inferencia mBERT]
    D --> F[Consolidación de Resultados]
    E --> F
    F --> G[Reporte Comparativo]
    G --> H[Resultado Final]
```

### Diagrama 2: Casos de Uso
```mermaid
usecaseDiagram
    actor "Investigador" as Inv
    usecase "Evaluar Texto" as UC1
    usecase "Consultar Historial" as UC2
    usecase "Exportar Resultados" as UC3
    
    Inv --> UC1
    Inv --> UC2
    Inv --> UC3
```

---

## NIVEL PIM (Lógico)

### Diagrama 3: Clases Conceptual (Dominio)
```mermaid
classDiagram
    class Investigador {
        +string nombre
    }
    class Evaluacion {
        +string texto
        +datetime fecha
    }
    class ModeloNLP {
        +string nombre
        +ejecutarInferencia()
    }
    class ResultadoMetrica {
        +float accuracy
        +float f1_score
    }
    
    Investigador "1" -- "0..*" Evaluacion : realiza
    Evaluacion "1" *-- "2" ModeloNLP : utiliza
    Evaluacion "1" *-- "2" ResultadoMetrica : genera
```

### Diagrama 4: Secuencia "Evaluar Texto"
```mermaid
sequenceDiagram
    participant I as Investigador
    participant G as GestorEvaluacion
    participant M as ModeloNLP
    participant DB as Persistencia
    
    I->>G: Solicitar Evaluación(texto)
    G->>M: Ejecutar Inferencia(texto)
    M-->>G: Resultado
    G->>DB: Guardar Resultado(datos)
    DB-->>G: Confirmación
    G-->>I: Retornar Predicciones
```

### Diagrama 5: Actividad de Consolidación
```mermaid
activityDiagram
    start
    :Recibir predicciones BETO y mBERT;
    :Calcular métricas individuales;
    :Consolidar tiempos de inferencia;
    :Comparar rendimiento;
    :Generar objeto consolidado;
    stop
```

---

## NIVEL PSM (Específico de Plataforma)

### Diagrama 6: Clases Tecnológico (PSM)
```mermaid
classDiagram
    class FastAPIEndpoint {
        <<FastAPI>>
        +post_evaluate()
    }
    class PydanticSchema {
        <<Pydantic>>
        +str text
        +int label
    }
    class SQLiteDB {
        <<SQLite>>
        +INSERT evaluation_results
    }
    
    FastAPIEndpoint ..> PydanticSchema : valida
    FastAPIEndpoint ..> SQLiteDB : persistencia
```

### Diagrama 7: Componentes Tecnológicos
```mermaid
graph LR
    subgraph REST_API
        API[FastAPI Endpoint]
    end
    subgraph NLP_Engine
        TRANS[Transformers/PyTorch]
    end
    subgraph Database
        DB[(SQLite)]
    end
    
    API --> TRANS
    API --> DB
```

### Diagrama 8: Despliegue
```mermaid
graph TD
    subgraph Servidor_Host
        subgraph Docker_Container
            App[FastAPI + NLP Engine]
        end
        Vol[SQLite Volume]
    end
    
    App --> Vol
```
