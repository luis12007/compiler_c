# Implementación de un Compilador de C

## Introducción
Este proyecto es un compilador básico para el lenguaje C, diseñado para procesar, analizar y generar código en múltiples etapas. Cada fase de la compilación, desde el análisis léxico hasta la generación de código intermedio y código objeto, está implementada en Python. El proyecto procesa código fuente en C y genera resultados intermedios, verifica errores semánticos y produce código objeto.

## Etapas de Compilación

### 1. Análisis Léxico
El **lexer** procesa el código fuente de entrada y lo convierte en una lista de tokens, categorizando identificadores, palabras reservadas, operadores y literales. Los tokens se formatean como `Token(tipo, valor, linea)`, incluyendo el tipo, valor y número de línea.

- **Archivo:** `lexer.py`
- **Ejemplo de Entrada:**
  ```c
  int factorial(int n) { 
      int result = 1; 
  }
  ```
- **Ejemplo de Salida:**
  ```
  Token(Tipo de dato int, int, Linea: 2)
  Token(ID, factorial, Linea: 2)
  Token(Inicio de paréntesis, (, Linea: 2)
  Token(ID, n, Linea: 2)
  Token(Fin de paréntesis, ), Linea: 2)
  Token(Inicio de llave, {, Linea: 2)
  Token(Tipo de dato int, int, Linea: 3)
  Token(ID, result, Linea: 3)
  Token(Igual, =, Linea: 3)
  Token(NUMERO, 1, Linea: 3)
  Token(Punto y coma, ;, Linea: 3)
  Token(Fin de llave, }, Linea: 4)
  ```

### 2. Análisis Sintáctico
El **parser** verifica que los tokens sigan la estructura gramatical definida en las reglas de la gramática, contenida en `parse_table`. Asegura la corrección sintáctica del código fuente y construye una estructura que representa declaraciones y expresiones válidas.

- **Archivo:** `parser.py`
- **Gramática:** Definida en `Current Grammar LL1.txt`, con reglas como:
  ```
  SOURCE -> INCLUDEBLOCK DEFINEBLOCK FUNCTIONBLOCK MAINFUNCTION
  ```
- **Ejemplo de Salida:**
  ```
  Parsing completed successfully: Syntax correct.
  ```

### 3. Análisis Semántico
El **Analizador Semántico** verifica la corrección semántica del código. Comprueba los tipos de datos, variables no declaradas y asignaciones incorrectas.

- **Archivo:** `SemanticAnalyzer.py`
- **Verificaciones:** Verifica que los tipos de datos asignados coincidan con los tipos declarados y que las variables estén declaradas antes de su uso.
- **Ejemplo de Tabla de Símbolos:**
  ```
  Variable result: {"tipo": "int", "initialized": True}
  ```

### 4. Generación de Código Intermedio
El **Generador de Código Intermedio** traduce las estructuras analizadas en un código intermedio, a menudo en formato de código de tres direcciones, para facilitar la transición hacia la generación de código objeto. Este es un nivel de abstracción cercano al lenguaje ensamblador.

- **Archivo:** `code_generator.py`
- **Ejemplo de Código Intermedio:**
  ```
  T1 = 1
  T2 = result * i
  ```

### 5. Generación de Código Objeto
El **Generador de Código Objeto** produce instrucciones en código objeto, representaciones de bajo nivel de las operaciones del programa, típicamente adecuadas para una máquina virtual o lenguaje ensamblador.

- **Archivo:** `object_code_generator.py`
- **Ejemplo de Código Objeto:**
  ```
  MOV result, 1
  MUL result, i
  ```

### Ejecución del Compilador
Para ejecutar el compilador:

1. Coloque su código fuente en C en `source_code.c`.
2. Ejecute `main.py` para iniciar el proceso de compilación, que invocará secuencialmente cada fase y mostrará los resultados y registros:
   ```bash
   python main.py
   ```
3. Las salidas incluyen tablas de tokens, resultados del análisis sintáctico, reportes de errores semánticos y código generado.

