import json
from collections import Counter, defaultdict
import argparse

def analyze_distribution(file_path):
    intent_counter = Counter()
    slot_counter = Counter()
    slot_values_counter = defaultdict(Counter)  

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)

            target = record["target"]
            parts = target.split(";")
            intents_part = parts[0].replace("intents:", "").strip()
            slots_part = parts[1].replace("slots:", "").strip() if len(parts) > 1 else ""

            if intents_part != "NONE" and intents_part:
                for intent in intents_part.split("|"):
                    intent_counter[intent.strip()] += 1

            if slots_part:
                for slot in slots_part.split(";"):
                    slot = slot.strip()
                    if slot:
                        if "=" in slot:
                            slot_name, slot_value = slot.split("=", 1)
                            slot_name = slot_name.strip()
                            slot_value = slot_value.strip()
                            slot_counter[slot_name] += 1
                            slot_values_counter[slot_name][slot_value] += 1
                        else:
                            slot_counter[slot] += 1

    print("\n=== Intent Distribution ===")
    for intent, count in intent_counter.most_common():
        print(f"{intent}: {count}")

    print("\n=== Slot Distribution ===")
    for slot, count in slot_counter.most_common():
        print(f"{slot}: {count}")

    print("\n=== Slot Values Distribution (Top 10 for each slot) ===")
    for slot_name, values_counter in slot_values_counter.items():
        print(f"\nSlot: {slot_name}")
        for value, count in values_counter.most_common(10):
            print(f"  {value}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to JSONL file")
    args = parser.parse_args()

    analyze_distribution(args.file)
