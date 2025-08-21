import json
import glob
import argparse
import os

def extract_intents_and_slots(frames):
    intents = []
    slots = []
    for frame in frames:
        intent = frame["state"]["active_intent"]
        if intent and intent != "NONE":
            intents.append(intent)

        for slot_name, slot_values in frame["state"]["slot_values"].items():
            for value in slot_values:
                slots.append(f"{slot_name}={value.lower()}")

    intents = list(dict.fromkeys(intents))
    slots = list(dict.fromkeys(slots))
    return intents, slots

def process_dialogue(dialogue):
    history = []
    results = []

    for turn in dialogue["turns"]:
        speaker = turn["speaker"]
        utt = turn["utterance"].strip()
        history.append(f"{speaker.upper()}: {utt}")

        if speaker.upper() == "USER":
            intents, slots = extract_intents_and_slots(turn.get("frames", []))
            target_intents = "|".join(intents) if intents else "NONE"
            target_slots = "; ".join(slots) if slots else ""

            results.append({
                "dialogue_id": dialogue.get("dialogue_id", ""),
                "turn_id": turn.get("turn_id", ""),
                "input": " ".join(history),
                "target": f"intents: {target_intents}; slots: {target_slots}"
            })

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs="+", help="Input JSON dialogue files (glob allowed)")
    parser.add_argument("output_file", help="Output JSONL file")
    args = parser.parse_args()

    all_results = []
    files = []
    for pattern in args.input_files:
        files.extend(glob.glob(pattern))

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                for dialogue in data:
                    all_results.extend(process_dialogue(dialogue))
            else:
                all_results.extend(process_dialogue(data))

    with open(args.output_file, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(json.dumps({
                "input": r["input"],
                "target": r["target"]
            }, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
