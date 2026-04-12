#!/usr/bin/env python3
"""
Script de Chat CLI Interactivo con gpt-4o en Azure Foundry
Mantiene memoria a corto plazo (contexto de conversación)
Guarda conversación en archivo .txt con diferenciación clara
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


class ChatBot:
    """Chatbot interactivo con memoria de conversación y persistencia en archivo"""
    
    def __init__(self, model: str = "gpt-4o", log_file: str = "chat_history.txt"):
        """
        Inicializa el chatbot.
        
        Args:
            model: Nombre del deployment en Azure Foundry
            log_file: Ruta del archivo para guardar conversación
        """
        # Cargar variables de entorno
        load_dotenv()
        
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.model = os.getenv("DEPLOYMENT_NAME", model)
        
        if not self.endpoint or not self.api_key:
            raise ValueError("❌ AZURE_OPENAI_ENDPOINT y AZURE_OPENAI_API_KEY no configurados en .env")
        
        # Crear cliente OpenAI
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.api_key
        )
        
        # Historial de conversación (memoria a corto plazo)
        self.conversation_history = []
        
        # Configuración de archivo de log
        self.log_file = Path(log_file)
        self._initialize_log_file()
        
        # Sistema prompt
        self.system_prompt = """Eres un asistente IA útil, amable y profesional. 
Responde en español a menos que se te indique lo contrario.
Sé conciso pero informativo en tus respuestas."""
    
    def _initialize_log_file(self):
        """Inicializa el archivo de log con encabezado"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"CONVERSACIÓN CON CHATBOT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Modelo: {self.model}\n")
            f.write(f"Endpoint: {self.endpoint[:50]}...\n")
            f.write("=" * 80 + "\n\n")
    
    def _save_to_log(self, role: str, content: str):
        """Guarda un mensaje en el archivo de log"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if role == "user":
                f.write(f"[{timestamp}] USUARIO:\n")
            else:
                f.write(f"[{timestamp}] MODELO:\n")
            
            f.write(f"{content}\n")
            f.write("-" * 80 + "\n\n")
    
    def _print_welcome(self):
        """Muestra mensaje de bienvenida"""
        print("\n" + "=" * 80)
        print("🤖 CHATBOT INTERACTIVO CON gpt-4o")
        print("=" * 80)
        print(f"Modelo: {self.model}")
        print(f"Archivo de log: {self.log_file}")
        print("\nComandos especiales:")
        print("  /salir     - Terminar conversación")
        print("  /limpiar   - Borrar historial (nueva conversación)")
        print("  /historial - Mostrar conversación actual")
        print("=" * 80 + "\n")
    
    def _print_separator(self):
        """Imprime separador visual"""
        print("-" * 80)
    
    def get_response(self, user_message: str) -> str:
        """
        Obtiene respuesta del modelo manteniendo contexto.
        
        Args:
            user_message: Mensaje del usuario
            
        Returns:
            Respuesta del modelo
        """
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Llamar al modelo con historial completo
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history,
                max_tokens=1024,
                temperature=0.7
            )
            
            # Extraer respuesta
            assistant_message = response.choices[0].message.content
            
            # Agregar respuesta al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            error_msg = f"❌ Error al conectar con el modelo: {str(e)}"
            print(error_msg)
            return None
    
    def show_history(self):
        """Muestra el historial de conversación actual"""
        if not self.conversation_history:
            print("\n📝 Historial vacío. Comienza a escribir para iniciar conversación.")
            return
        
        print("\n" + "=" * 80)
        print("📝 HISTORIAL DE CONVERSACIÓN ACTUAL")
        print("=" * 80)
        
        for i, msg in enumerate(self.conversation_history, 1):
            role = "USUARIO" if msg["role"] == "user" else "MODELO"
            print(f"\n[{i}] {role}:")
            print(f"    {msg['content'][:100]}..." if len(msg['content']) > 100 else f"    {msg['content']}")
        
        print("\n" + "=" * 80)
        print(f"Total de mensajes: {len(self.conversation_history)}")
        print("=" * 80 + "\n")
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
        print("\n✓ Historial borrado. Nueva conversación iniciada.\n")
        
        # Registrar en log
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("[NOTA] Historial borrado - Nueva conversación\n")
            f.write("-" * 80 + "\n\n")
    
    def run(self):
        """Inicia el bucle interactivo del chatbot"""
        self._print_welcome()
        
        while True:
            try:
                # Solicitar entrada del usuario
                user_input = input("👤 Tú: ").strip()
                
                # Procesar comandos especiales
                if not user_input:
                    print("⚠️  Por favor, escribe algo.\n")
                    continue
                
                if user_input.lower() == "/salir":
                    print("\n✓ ¡Gracias por usar el chatbot! Conversación guardada en:", self.log_file)
                    print("=" * 80 + "\n")
                    break
                
                if user_input.lower() == "/limpiar":
                    self.clear_history()
                    continue
                
                if user_input.lower() == "/historial":
                    self.show_history()
                    continue
                
                # Guardar entrada del usuario
                self._save_to_log("user", user_input)
                
                # Obtener respuesta del modelo
                print("\n🤖 Modelo (procesando...)  ", end="", flush=True)
                response = self.get_response(user_input)
                
                if response:
                    # Limpiar la línea de procesamiento
                    print("\r" + " " * 50 + "\r", end="")
                    
                    # Mostrar respuesta
                    print(f"🤖 Modelo:\n{response}\n")
                    
                    # Guardar respuesta del modelo
                    self._save_to_log("assistant", response)
                    
                    # Mostrar información de tokens
                    print(f"📊 [{len(self.conversation_history)} mensajes en historial]\n")
                
                self._print_separator()
            
            except KeyboardInterrupt:
                print("\n\n✓ Conversación interrumpida. Contenido guardado en:", self.log_file)
                print("=" * 80 + "\n")
                break
            
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                self._print_separator()


def main():
    """Punto de entrada principal"""
    try:
        # Crear instancia del chatbot
        chatbot = ChatBot(
            model="gpt-4o",
            log_file="chat_history.txt"
        )
        
        # Iniciar conversación
        chatbot.run()
    
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n⚠️  Asegúrate de que tu archivo .env contiene:")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - DEPLOYMENT_NAME (opcional)")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
