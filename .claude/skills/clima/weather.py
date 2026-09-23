#!/usr/bin/env python3
"""Clima desde la terminal usando Open-Meteo (gratis, sin API key).

Uso:
    python weather.py "Madrid"
    python weather.py "Buenos Aires" --dias 5
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Códigos WMO -> descripción en español
WMO = {
    0: "despejado", 1: "mayormente despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla con escarcha",
    51: "llovizna ligera", 53: "llovizna moderada", 55: "llovizna intensa",
    56: "llovizna helada ligera", 57: "llovizna helada intensa",
    61: "lluvia ligera", 63: "lluvia moderada", 65: "lluvia intensa",
    66: "lluvia helada ligera", 67: "lluvia helada intensa",
    71: "nieve ligera", 73: "nieve moderada", 75: "nieve intensa", 77: "granos de nieve",
    80: "chubascos ligeros", 81: "chubascos moderados", 82: "chubascos violentos",
    85: "chubascos de nieve ligeros", 86: "chubascos de nieve intensos",
    95: "tormenta", 96: "tormenta con granizo ligero", 99: "tormenta con granizo fuerte",
}


def fetch_json(url, params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{query}", timeout=15) as resp:
        return json.load(resp)


def geocode(place):
    data = fetch_json(GEOCODE_URL, {"name": place, "count": 1, "language": "es"})
    results = data.get("results")
    if not results:
        sys.exit(f"No se encontró la ubicación: {place!r}")
    r = results[0]
    label = ", ".join(filter(None, [r.get("name"), r.get("admin1"), r.get("country")]))
    return r["latitude"], r["longitude"], label


def main():
    parser = argparse.ArgumentParser(description="Clima con Open-Meteo")
    parser.add_argument("lugar", help="Ciudad o ubicación")
    parser.add_argument("--dias", type=int, default=3, help="Días de pronóstico (1-7)")
    args = parser.parse_args()

    lat, lon, label = geocode(args.lugar)
    dias = max(1, min(7, args.dias))

    data = fetch_json(FORECAST_URL, {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                   "wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                 "precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": dias,
    })

    cur = data["current"]
    print(f"Clima en {label}")
    print(f"  Ahora: {cur['temperature_2m']}°C "
          f"(sensación {cur['apparent_temperature']}°C), "
          f"{WMO.get(cur['weather_code'], 'desconocido')}")
    print(f"  Humedad {cur['relative_humidity_2m']}% | "
          f"Viento {cur['wind_speed_10m']} km/h")

    daily = data["daily"]
    print(f"\n  Pronóstico ({dias} días):")
    for i, day in enumerate(daily["time"]):
        print(f"    {day}: "
              f"{daily['temperature_2m_min'][i]}°–{daily['temperature_2m_max'][i]}°C, "
              f"{WMO.get(daily['weather_code'][i], 'desconocido')}, "
              f"lluvia {daily['precipitation_probability_max'][i]}%")


if __name__ == "__main__":
    main()
