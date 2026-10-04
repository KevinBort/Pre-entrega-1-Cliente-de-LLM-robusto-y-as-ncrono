# Pre-entrega 1 - Cliente de LLM robusto y asincrono

Cliente asincrono que permite hablar con distintos proveedores de LLM (OpenAI, Anthropic, Gemini) usando una misma interfaz.

## Pasos para correrlo

1. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar las variables de entorno en un archivo `.env`:
   ```
   LLM_PROVIDER=gemini
   LLM_MODEL=gemini-3.8-flash

   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GEMINI_API_KEY=...
   ```

4. Ejecutar el script:
   ```bash
   python main.py
   ```

## Temperatura

La temperatura controla qué tan creativa o determinista es la respuesta (rango valido: `0.0` a `2.0`). Por defecto es `0.3`.

Para probarla con otro valor, sin tocar el codigo, pasa la variable `LLM_TEMPERATURE` al ejecutar:

```bash
LLM_TEMPERATURE=0.7 python main.py
```

También podés barrer varios valores de una:

```bash
for t in 0.0 0.5 1.0 1.5 2.0; do
  echo "=== temperature=$t ==="
  LLM_TEMPERATURE=$t python main.py
done
```

O fijar un valor por defecto agregando `LLM_TEMPERATURE=0.3` al `.env`.

Para temperatura 1 me dio esto :

En física, es la magnitud que mide la energía no utilizable de un sistemay la cantidad de microestados posibles (desorden molecular).
En teoría de la información, cuantifica el grado de incertidumbre o sorpresa inherente a una variable aleatoria o mensaje.
Rige la segunda ley de la termodinámica, estableciendo que los sistemas cerrados evolucionan irreversiblemente hacia el equilibrio térmico y el caos.

Para temperatura 0.1 esto: 

En termodinámica, es la magnitud física que mide el grado de desorden molecular y la energía no aprovechable de un sistema cerrado.
En teoría de la información, cuantifica la incertidumbre y la tasa promedio de información producida por una fuente estocástica.
En ambos casos, representa una medida estadística del número de microestados posibles o la pérdida de predictibilidad.