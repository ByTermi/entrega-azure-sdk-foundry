## 🚀 SETUP SIMPLIFICADO - Ya tienes Foundry

Como ya tienes un Foundry con **gpt-4o-mini** desplegado, el setup es **MUCHO más simple**:

### ⚡ 3 pasos (30 segundos):

#### Paso 1️⃣ : Obtén 2 valores de tu Foundry

Ve a: https://ai.azure.com → Tu Proyecto → **Endpoints and Keys**

Copia estos 2 valores:
```
ENDPOINT: https://tu-recurso-openai.openai.azure.com
DEPLOYMENT: gpt-4o-mini (o el nombre que uses)
```

#### Paso 2️⃣ : Rellena `.env.setup`
Abre el archivo y completa:
```
AZURE_OPENAI_ENDPOINT=https://tu-endpoint.openai.azure.com
DEPLOYMENT_NAME=gpt-4o-mini
```

Opcionalmente, si quieres usar API Key en lugar de `az login`:
```
AZURE_OPENAI_API_KEY=tu-api-key-aqui
```

#### Paso 3️⃣ : Ejecuta el script
```powershell
.\setup.ps1
```

**Listo.** El script crea automáticamente:
- ✅ `.env` con tus credenciales
- ✅ `requirements.txt`

---

### 📝 Después del setup:

```powershell
# Instala dependencias
pip install -r requirements.txt

# Autentica con Azure (si no usas API Key)
az login

# Ejecuta los notebooks
jupyter notebook
```

---

**¡Eso es todo! Los notebooks ya funcionarán.**
