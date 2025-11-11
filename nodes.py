from .tools import get_weather, get_crypto_price
from .memory import save_to_memory, get_from_memory
from .llm_client import classify_intent_and_extract_entities, llm_generate_answer

def run_agent(user_input: str) -> str:
    parsed = classify_intent_and_extract_entities(user_input)
    intent = parsed.get("intent")
    entities = parsed.get("entities", [])
    timeframe = parsed.get("timeframe")

    if not intent or intent == "unknown":
        return "Sorry, I couldn't understand your request."

    if intent in ["weather", "compare_weather"]:
        city_string = ", ".join(entities)
        cached = get_from_memory("weather", city_string)
        if cached:
            data = cached
        else:
            data = get_weather.run(city_string)
            save_to_memory("weather", city_string, data)
    elif intent in ["crypto", "compare_crypto"]:
        token_string = ", ".join(entities)
        date_str = timeframe
        key_mem = f"{token_string}_{date_str or 'current'}"
        cached = get_from_memory("crypto", key_mem)
        if cached:
            data = cached
        else:
            data = get_crypto_price.run(token_string, date=date_str)
            save_to_memory("crypto", key_mem, data)
    else:
        return "Sorry, I can currently provide info only on weather and cryptocurrency."

    return llm_generate_answer(intent, data, entities, timeframe)
