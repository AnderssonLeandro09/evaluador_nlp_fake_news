import httpx
import time
import asyncio

# Configuración del servidor
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/evaluate"
TEXT_TO_EVALUATE = "Esta es una noticia de prueba para validar la concurrencia del sistema."

async def test_concurrency():
    print("🚀 Iniciando prueba de concurrencia arquitectónica...")
    print(f"Enviando petición a: {BASE_URL}{ENDPOINT}\n")

    try:
        async with httpx.AsyncClient() as client:
            start_time = time.perf_counter()
            
            response = await client.post(
                ENDPOINT, 
                json={"text": TEXT_TO_EVALUATE, "label": 1},
                base_url=BASE_URL
            )
            
            end_time = time.perf_counter()
            
            if response.status_code != 200:
                print(f"❌ Error en la petición: {response.status_code}")
                print(response.text)
                return

            data = response.json()
            
            beto_time = data["beto_result"]["time_ms"]
            mbert_time = data["mbert_result"]["time_ms"]
            total_response_time = (end_time - start_time) * 1000
            
            print("--- Resultados de la Inferencia ---")
            print(f"Tiempo BETO:   {beto_time:.2f} ms")
            print(f"Tiempo mBERT:  {mbert_time:.2f} ms")
            print(f"Suma Lineal:   {beto_time + mbert_time:.2f} ms")
            print("-" * 30)
            print(f"TIEMPO TOTAL DE RESPUESTA: {total_response_time:.2f} ms")
            print("-" * 30)

            # Análisis Matemático de Concurrencia
            if total_response_time < (beto_time + mbert_time):
                print("\n✅ ÉXITO: Procesamiento Concurrente Demostrado.")
                print(f"Ahorro de tiempo: { (beto_time + mbert_time) - total_response_time:.2f} ms")
                print("Explicación: El tiempo total es menor que la suma de los tiempos individuales,")
                print("lo que prueba que BETO y mBERT fueron ejecutados en paralelo gracias a")
                print("asyncio.gather y asyncio.to_thread.")
            else:
                print("\n⚠️ ADVERTENCIA: El procesamiento parece ser secuencial.")
                print("El tiempo total es igual o mayor que la suma de los tiempos individuales.")

    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")

if __name__ == "__main__":
    asyncio.run(test_concurrency())
