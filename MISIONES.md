# Misión: rescate del modelo de fuga

**El caso.** Son el equipo de Data Science de un banco. El modelo que predice la fuga de clientes llegó a un AUC de **0.92**, pero después de varios cambios que nadie registró cayó a **0.65**. Su misión: poner el proyecto bajo control de versiones, colaborar sin pisarse y encontrar el cambio que lo rompió.

**Cómo trabajamos**
- Parejas: **Persona A** y **Persona B**.
- **Piloto y navegante:** quien hace la misión comparte pantalla y escribe; la otra persona lee los pasos y guía. Cambian de rol en cada misión.
- **Semáforo** (reacciones de Zoom): verde = misión completa · amarillo = avanzando con dudas · rojo = bloqueados más de 5 minutos.

---

## Misión 1 · Toma el control (Persona A) · ~8 min

1. Descarga esta carpeta como ZIP (botón **Code → Download ZIP**) y descomprímela. *Importante: no la clones; queremos crear el repositorio desde cero.*
2. Abre la carpeta en PyCharm o VS Code (o tu editor de preferencia) y abre la terminal.
3. Inicializa el repositorio y mira el estado:
   ```bash
   git init
   git status
   ```
4. Hay un archivo `.env` con credenciales. **Nunca** debe subirse. Crea un archivo `.gitignore` con este contenido:
   ```
   .env
   models/
   __pycache__/
   .venv/
   ```
5. Vuelve a ejecutar `git status`: ¿desapareció `.env` de la lista?
6. Guarda el primer commit:
   ```bash
   git add .
   git commit -m "Agrega proyecto base del modelo de fuga"
   ```

✅ **Listo cuando:** `git log --oneline` muestra 1 commit y `.env` no aparece en `git status`.

## Misión 2 · Experimenta (Persona A) · ~10 min

1. Ejecuta `python train.py` y anota el AUC.
2. Haz **3 experimentos**: en cada uno cambia algún valor de `config.json` (`n_estimators`, `max_depth`, `min_samples_leaf`), ejecuta el script y **haz un commit por experimento**, con el AUC en el mensaje:
   ```bash
   git add config.json
   git commit -m "Sube max_depth a 8"
   ```
   *Ideas:* `n_estimators` 100 → 200, `max_depth` 3 → 5 → 8.
3. Revisa tu historial: `git log --oneline`.
4. Usa `git show <id>` sobre uno de tus commits: ¿ves exactamente qué valor cambió?

✅ **Listo cuando:** tienes al menos 4 commits.

## Misión 3 · Publica (Persona A) · ~8 min

1. En GitHub, crea un repositorio **vacío** (sin README ni .gitignore) en la organización del curso (utec-curso-mlops-2026-2), llamado `churn-<id-GitHub>`.
2. Conecta y sube:
   ```bash
   git remote add origin <url-de-tu-repo>
   git branch -M main
   git push -u origin main
   ```
3. Refresca la página en GitHub: ¿aparece tu código? ¿Aparece `.env`? (no debería).
4. Si el repo no está en la organización, invita a tu pareja: **Settings → Collaborators → Add people**.

✅ **Listo cuando:** ves tus commits en GitHub (pestaña **Commits**).

## Misión 4 · Colabora (Persona B) · ~8 min

1. Clona el repositorio de tu pareja:
   ```bash
   git clone <url-del-repo>
   cd <carpeta-del-repo>
   ```
2. En `README.md`, sección **Equipo**, agrega sus dos nombres.
3. Guarda y sube:
   ```bash
   git add README.md
   git commit -m "Agrega integrantes del equipo al README"
   git push
   ```
4. **Persona A:** trae el cambio a tu computadora con `git pull` y verifica el README.

✅ **Listo cuando:** ambos ven el mismo `git log --oneline`.

## Misión 5 · Sabotaje (Persona B) · ~5 min

🤫 **Persona A: no mires esta sección. Persona B: deja de compartir pantalla.**

Lee la sección **"Solo para la Persona B"** al final de este archivo y sigue las instrucciones.

## Misión 6 · Rescate (Persona A) · ~10 min

1. Trae los últimos cambios y ejecuta el modelo:
   ```bash
   git pull
   python train.py
   ```
   ¿Qué pasó con el AUC? 😱
2. Investiga sin preguntarle a tu pareja:
   ```bash
   git log --oneline
   git show <id>      # revisa los commits recientes uno por uno
   ```
   Pista: **los mensajes de commit pueden mentir; el diff no.**
3. Cuando encuentres al culpable, deshazlo de forma segura:
   ```bash
   git revert <id>
   python train.py   # ¿volvió el AUC?
   git push
   ```

✅ **Listo cuando:** el AUC volvió a su valor anterior y el commit de revert está en GitHub. Pega el link de tu repo en el chat.

---

## Retos extra (para quienes terminen antes)

- `git blame config.json`: ¿quién cambió cada línea y en qué commit?
- Marca la versión buena del modelo: `git tag v1.0` y `git push origin v1.0`.
- En GitHub, abre `config.json` y usa el botón **History**: recorre el historial desde la web.
- Mejora tus mensajes de commit: ¿responden a "si aplico este commit, este commit…"?

---
---
---

## Solo para la Persona B

Elige **una** opción, haz el cambio, ejecuta `python train.py` para comprobar que el AUC empeoró, y haz commit con un **mensaje engañoso**:

**Opción fácil (cambio en la configuración):** en `config.json` cambia `"label_noise": 0.0` por `"label_noise": 0.45`.

**Opción difícil (cambio en el código):** en `train.py`, dentro de `main()`, cambia `predict_proba(X_test)[:, 1]` por `predict_proba(X_test)[:, 0]`.

Luego:
```bash
git add .
git commit -m "Actualiza comentarios y formato"
git push
```

Avísale a tu pareja que ya puede empezar la Misión 6. Durante el rescate solo puedes responder "sí" o "no". 😉
