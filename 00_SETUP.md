# 🚀 Azure AI Foundry - Setup Automático

## Opción 1: Setup Automático (Recomendado) ⭐

### Requisitos previos:
- PowerShell (Windows)
- [Azure CLI](https://aka.ms/azurecli) instalado
- Cuenta de Azure con cuota de OpenAI disponible

### Pasos:

1. **Obtén tu Azure Subscription ID:**
   ```powershell
   az account list --output table
   ```
   Copia el `SubscriptionId`

2. **Edita `.env.setup`:**
   - Pega tu `AZURE_SUBSCRIPTION_ID`
   -Elige un `AZURE_RESOURCE_GROUP` (nombre del grupo de recursos)
   - Elige una `AZURE_REGION` (ej: `northeurope`, `eastus`, `westeurope`)
   - Personaliza nombres de recursos si quieres

3. **Ejecuta el script de setup:**
   ```powershell
   .\setup.ps1
   ```

4. **El script automáticamente:**
   - ✅ Crea grupo de recursos
   - ✅ Crea recurso Azure OpenAI
   - ✅ Despliega un modelo (gpt-4o)
   - ✅ Crea archivos `.env` y `requirements.txt`

5. **Instala dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Autentica con Azure:**
   ```powershell
   az login
   ```

7. **Ejecuta los notebooks:**
   ```powershell
   jupyter notebook
   ```

---

## Opción 2: Setup Manual

Si ya tienes un recurso Azure OpenAI creado:

1. Copia `.env.example` a `.env`
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edita `.env` con tus valores reales:
   ```
   AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com
   DEPLOYMENT_NAME=tu-deployment
   AZURE_OPENAI_API_VERSION=2024-03-01-preview
   ```

3. Instala y ejecuta como en la Opción 1 (pasos 5-7)

---

## 📁 Archivos en esta carpeta

| Archivo | Descripción |
|---------|-------------|
| `setup.ps1` | Script PowerShell que crea todos los recursos |
| `.env.setup` | Archivo de configuración inicial (RELLENAR) |
| `.env.example` | Ejemplo con instrucciones |
| `.env` | **Credenciales reales (NO SUBIR A GIT)** |
| `requirements.txt` | Dependencias Python |
| `.gitignore` | Archivos a ignorar en Git |
| `01_text_json_guardrails.ipynb` | Notebook 1: Text, JSON, Guardrails |
| `02_reasoning_function_calling.ipynb` | Notebook 2: Reasoning, Function Calling |
| `03_multimodal_images_audio.ipynb` | Notebook 3: Multimodal (Imágenes, Audio) |

---

## ⚡ Verificación Rápida

Después del setup, verifica que funciona:

```powershell
# 1. Autentica
az login

# 2. Entra al ambiente Python
python

# 3. En Python, prueba:
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
client = OpenAI(base_url=f"{endpoint}/openai/v1", api_key=token_provider())

response = client.chat.completions.create(
    model=os.getenv("DEPLOYMENT_NAME"),
    messages=[{"role": "user", "content": "Hola, ¿funciona?"}]
)
print(response.choices[0].message.content)
```

---

## 🔒 Seguridad

⚠️ **IMPORTANTE:**
- El archivo `.env` contiene credenciales reales
- **NUNCA** lo commits a Git
- El `.gitignore` ya lo protege, pero ten cuidado

---

## 🆘 Solución de Problemas

### "Azure CLI no encontrado"
- Descarga e instala desde: https://aka.ms/azurecli

### "No tienes cuota de OpenAI"
- Verifica en Azure Portal → Quotas
- O contacta a soporte de Azure

### "Error de autenticación en setup.ps1"
- Ejecuta: `az login`
- Luego intenta `.\setup.ps1` de nuevo

### Los notebooks no ven las variables de entorno
- Asegúrate de tener `.env` en la misma carpeta
- Reinicia la terminal/kernel de Jupyter
- O establece manualmente: `$env:AZURE_OPENAI_ENDPOINT="..."`

---

## 📚 Documentación Relacionada

- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [Python OpenAI SDK](https://github.com/openai/openai-python)

---

**¿Preguntas?** Revisa los comentarios dentro de cada notebook 📓
