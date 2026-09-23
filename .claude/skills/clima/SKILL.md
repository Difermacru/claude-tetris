---
name: clima
description: Obtiene información del clima actual y pronóstico para una ciudad o ubicación. Úsala cuando el usuario pida el clima, el tiempo, la temperatura, si va a llover, el pronóstico, o mencione "clima en <lugar>". Funciona en local sin API key.
---

# Clima

Consulta el clima actual y el pronóstico de cualquier lugar desde la terminal, sin necesidad de API key.

## Cuándo usarla

- "¿Qué clima hace en Madrid?"
- "Dame el tiempo de Buenos Aires"
- "¿Va a llover mañana en Santiago?"
- "Temperatura actual en Ciudad de México"

Si el usuario no indica ciudad, usa `wttr.in` sin lugar (detecta por IP) o pregúntale.

## Método principal: wttr.in (rápido, texto)

Servicio gratuito sin API key. Funciona con `curl`.

Clima resumido de una ciudad (1 línea):

```bash
curl -s "wttr.in/Madrid?format=3"
```

Vista actual + pronóstico 3 días, en español y unidades métricas:

```bash
curl -s "wttr.in/Madrid?lang=es&m"
```

Formato personalizado (temp, sensación, humedad, viento):

```bash
curl -s "wttr.in/Buenos+Aires?format=%l:+%c+%t+(sensacion+%f)+humedad+%h+viento+%w&lang=es"
```

Notas:
- Sustituye espacios en el nombre por `+` (ej. `Ciudad+de+Mexico`).
- Sin lugar (`curl -s wttr.in`) detecta ubicación por IP.
- Códigos de formato útiles: `%c` icono, `%t` temperatura, `%f` sensación térmica, `%h` humedad, `%w` viento, `%l` lugar.

## Método alternativo: Open-Meteo (JSON, robusto)

Si wttr.in falla o se quiere datos estructurados, usa el script Python con Open-Meteo (también gratis, sin key). Requiere Python (ya disponible en el proyecto).

```bash
python .claude/skills/clima/weather.py "Madrid"
python .claude/skills/clima/weather.py "Buenos Aires" --dias 5
```

## Cómo presentar el resultado

- Responde en español, breve y directo.
- Da la temperatura actual, sensación térmica y condición (soleado, lluvia, etc.).
- Si el usuario pregunta por el pronóstico, incluye los próximos días con máxima/mínima y probabilidad de lluvia.
- No inventes datos: si el comando falla, díselo al usuario y ofrece reintentar o cambiar de fuente.
