import random
import json

current_counts = {
    "find_hospital": 727,
    "find_police": 482,
    "find_pharmacy": 200,
    "find_embassy": 200
}

target_count = 12500

intent_slots = {
    "find_hospital": {
        "hospital-department": [
            "emergency department", "neurology", "infectious diseases",
            "cardiology", "paediatric clinic", "intensive care unit"
        ],
        "hospital-name": [
            "addenbrookes hospital", "cambridge general hospital",
            "queen mary hospital", "st john's hospital"
        ]
    },
    "find_police": {
        "police-station": [
            "cambridge police station", "central police station",
            "north district police", "west end police office"
        ]
    },
    "find_pharmacy": {
        "pharmacy-name": [
            "boots pharmacy", "cambridge pharmacy", "healthplus",
            "city centre pharmacy", "green cross pharmacy"
        ],
        "pharmacy-area": [
            "centre", "north", "south", "east", "west"
        ]
    },
    "find_embassy": {
        "embassy-country": [
            "france", "germany", "italy", "spain", "usa", "canada"
        ],
        "embassy-city": [
            "london", "manchester", "birmingham", "leeds"
        ]
    }
}

templates = {
    "find_hospital": [
        "I need information about the {hospital-department} at {hospital-name}",
        "Where is the {hospital-department} in {hospital-name}?",
        "Find the {hospital-department} department in {hospital-name}",
        "Tell me about {hospital-name}'s {hospital-department}"
    ],
    "find_police": [
        "Where is the {police-station}?",
        "Find the nearest {police-station}",
        "I need the address of {police-station}",
        "Locate {police-station}"
    ],
    "find_pharmacy": [
        "Find a pharmacy named {pharmacy-name} in the {pharmacy-area}",
        "Where is {pharmacy-name} pharmacy in the {pharmacy-area} area?",
        "Locate {pharmacy-name} pharmacy around {pharmacy-area}",
        "I need directions to {pharmacy-name} in {pharmacy-area}"
    ],
    "find_embassy": [
        "Where is the {embassy-country} embassy in {embassy-city}?",
        "Find the {embassy-country} embassy located in {embassy-city}",
        "I need contact info for the {embassy-country} embassy at {embassy-city}",
        "Locate the {embassy-country} embassy in {embassy-city}"
    ]
}

def generate_sample(intent):
    slot_values = {}
    for slot, values in intent_slots[intent].items():
        slot_values[slot] = random.choice(values)

    template = random.choice(templates[intent])
    input_text = template.format(**slot_values)
    slots_str = "; ".join([f"{k}={v}" for k, v in sorted(slot_values.items())])
    target_text = f"intents: {intent}; slots: {slots_str}"

    return {"input": f"USER: {input_text}", "target": target_text}

def main():
    for intent, current_count in current_counts.items():
        to_generate = target_count - current_count
        print(f"Generating {to_generate} samples for intent '{intent}'")
        with open(f"augmented_{intent}.jsonl", "w", encoding="utf-8") as f_out:
            for _ in range(to_generate):
                sample = generate_sample(intent)
                f_out.write(json.dumps(sample, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
