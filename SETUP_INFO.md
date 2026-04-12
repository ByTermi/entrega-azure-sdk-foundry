# ✅ CONFIGURACIÓN COMPLETADA

He creado un sistema automático para que solo tengas que rellenar tu información de Azure y ejecutar un script.

## 📋 Nuevos archivos creados:

### 1. **setup.ps1** ← EL ARCHIVO PRINCIPAL
Script PowerShell que **automatiza TODO**:
- ✅ Crea grupo de recursos en Azure
- ✅ Crea cuenta Azure OpenAI
- ✅ Despliega modelo (gpt-4o)
- ✅ Genera archivo `.env` con credenciales reales
- ✅ Crea `requirements.txt`

### 2. **.env.setup** ← RELLENA EST
Archivo de configuración que TÚ completas con:
- Tu **AZURE_SUBSCRIPTION_ID** (obtén con `az account list`)
- Nombre del grupo de recursos
- Región de Azure
- Nombres de recursos

### 3. **.env.example**
Archivo de referencia que muestra qué variables se necesitan

### 4. **.env**
Se crea automáticamente al ejecutar `setup.ps1` con credenciales reales

### 5. **00_SETUP.md**
Instrucciones completas paso a paso

### 6. **.gitignore**
Protege que `.env` no se suba a Git (seguridad)

---

## 🚀 CÓMO USAR (3 pasos):

### Paso 1: Edita `.env.setup`
Abre el archivo y rellena:
```
AZURE_SUBSCRIPTION_ID=tu-id-aqui
AZURE_RESOURCE_GROUP=mi-grupo-ia
AZURE_REGION=northeurope  # o tu región
```

**Obtén tu ID de suscripción:**
```powershell
az account list --output table
```

### Paso 2: Ejecuta el script
```powershell
.\setup.ps1
```
El script hará TODO automáticamente:
- Autentica en Azure (te pide `az login`)
- Crea recursos
- Actualiza `.env` con credenciales

### Paso 3: Instala y ejecuta
```powershell
pip install -r requirements.txt
az login
jupyter notebook
```

---

## 📁 Estructura final:

```
foundry_notebooks/
├── setup.ps1                              ← Script automático (EJECUTA ESTO)
├── .env.setup                             ← Tu configuración (RELLENA ESTO)
├── .env.example                           ← Ejemplo (referencia)
├── .env                                   ← Credenciales (se crea automáticamente, NO SUBIR A GIT)
├── requirements.txt                       ← Dependencias Python (creado automáticamente)
├── .gitignore                             ← Protege .env en Git
├── 00_SETUP.md                            ← Instrucciones detalladas
├── 01_text_json_guardrails.ipynb          ← Notebook 1
├── 02_reasoning_function_calling.ipynb    ← Notebook 2
└── 03_multimodal_images_audio.ipynb       ← Notebook 3
```

---

## ⚡ RESUMEN RÁPIDO:

| Tarea | Comando | Archivo |
|-------|---------|---------|
| Rellenar mi Azure ID | (manual) | `.env.setup` |
| Crear todos los recursos | `.\setup.ps1` | `setup.ps1` |
| Ver instrucciones | (leer) | `00_SETUP.md` |
| Ver qué necesito rellenar | (leer) | `.env.setup` |
| Instalar dependencias | `pip install -r requirements.txt` | `requirements.txt` |
| Ejecutar notebooks | `jupyter notebook` | `*.ipynb` |

---

## 🔒 Seguridad:

- ✅ El `.env` con credenciales NUNCA se verá en Git (protegido por `.gitignore`)
- ✅ `setup.ps1` valida que hayas rellenado los valores antes de continuar
- ✅ Las credenciales se cargan desde `.env` automáticamente en los notebooks
- ✅ Se recomienda usar `az login` (DefaultAzureCredential) en lugar de meter API Key

---

## ❓ Preguntas comunes:

**P: ¿Necesito tener un grupo de recursos ya creado?**
A: No, `setup.ps1` lo crea automáticamente.

**P: ¿Esto me cuesta dinero?**
A: Azure OpenAI tiene costos. Verifica https://aka.ms/openai/pricing

**P: ¿Dónde obtengo el SUBSCRIPTION_ID?**
A: Ejecuta: `az account list --output table` y copia la columna `SubscriptionId`

**P: ¿Qué región debo usar?**
A: Usa donde tengas cuota disponible. Comunes: `northeurope`, `eastus`, `westeurope`

**P: ¿Funciona en Linux/Mac?**
A: El script.ps1 es PowerShell. En Linux/Mac puedes hacer el setup manual siguiendo `00_SETUP.md`

---

## 🎯 PRÓXIMO PASO:

**Abre `.env.setup` → Rellena tu Azure ID → Ejecuta `.\setup.ps1`**

Eso es todo. El script hace el resto automáticamente ✨
