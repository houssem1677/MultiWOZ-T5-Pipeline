# MultiWOZ Dialogue Data Processing Pipeline

This repository provides a pipeline for processing and augmenting dialogue data from the [MultiWOZ dataset](https://github.com/budzianowski/multiwoz) for natural language processing (NLP) tasks, specifically for intent and slot prediction with T5 models. The pipeline converts dialogues, analyzes intent and slot distributions, augments emergency-related intents to address data imbalance, and merges all datasets into a unified file for comprehensive analysis or training.

## Repository Structure

- **Directories**:
  - `train/`: Training data (JSON/JSONL files) from MultiWOZ.
  - `dev/`: Development/validation data (JSON/JSONL files) from MultiWOZ.
  - `test/`: Test data (JSON/JSONL files) from MultiWOZ.

- **Scripts**:
  - `convert_for_t5.py`: Converts MultiWOZ JSON dialogues into JSONL format for T5 training.
  - `analyze_intent_slots.py`: Analyzes intent, slot, and slot value distributions in JSONL files.
  - `augment_emergency_data.py`: Generates synthetic samples for emergency intents (`find_hospital`, `find_police`, `find_pharmacy`, `find_embassy`).
  - `merge_jsonl.py`: Merges multiple JSONL files into a single file.

- **Data Files**:
  - 9 JSON/JSONL files across `train`, `dev`, and `test` directories, containing raw or processed MultiWOZ dialogue data.
  - Processed files: `t5_train.jsonl`, `t5_dev.jsonl`, `t5_test.jsonl`.
  - Augmented files: `augmented_find_hospital.jsonl`, `augmented_find_police.jsonl`, `augmented_find_pharmacy.jsonl`, `augmented_find_embassy.jsonl`.
  - Merged output: `merged_all.jsonl`.

## Prerequisites

- Python 3.6+
- No external dependencies (uses standard libraries: `json`, `argparse`, `collections`, `random`, `glob`).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/houssem1677/MultiWOZ-T5-Pipeline.git
   cd your-repo-name
   ```

2. Verify Python version:
   ```bash
   python --version
   ```

## Usage

Follow this pipeline to process and augment MultiWOZ data:

### 1. Convert MultiWOZ Data for T5
Converts MultiWOZ JSON dialogues from `train`, `dev`, and `test` directories into JSONL format, extracting intents and slots for T5 model training.

```bash
python convert_for_t5.py train/*.json t5_train.jsonl
python convert_for_t5.py dev/*.json t5_dev.jsonl
python convert_for_t5.py test/*.json t5_test.jsonl
```

**Output Example** (from `t5_train.jsonl`):
```json
{"input": "USER: i need a place to dine in the center thats expensive", "target": "intents: find_restaurant|find_hotel; slots: restaurant-area=centre; restaurant-pricerange=expensive"}
{"input": "USER: i need a place to dine in the center thats expensive SYSTEM: I have several options for you; do you prefer African, Asian, or British food? USER: Any sort of food would be fine, as long as it is a bit expensive. Could I get the phone number for your recommendation?", "target": "intents: find_restaurant|find_hotel; slots: restaurant-area=centre; restaurant-pricerange=expensive"}
{"input": "USER: i need a place to dine in the center thats expensive SYSTEM: I have several options for you; do you prefer African, Asian, or British food? USER: Any sort of food would be fine, as long as it is a bit expensive. Could I get the phone number for your recommendation? SYSTEM: There is an Afrian place named Bedouin in the centre. How does that sound? USER: Sounds good, could I get that phone number? Also, could you recommend an expensive hotel?", "target": "intents: find_restaurant|find_hotel; slots: restaurant-area=centre; restaurant-name=bedouin; restaurant-pricerange=expensive; hotel-pricerange=expensive; hotel-type=hotel"}
```

### 2. Analyze Intent and Slot Distributions
Analyzes the distribution of intents, slots, and slot values in the converted JSONL files to identify imbalances.

```bash
python analyze_intent_slots.py t5_train.jsonl
```

**Example Output** (abridged from `t5_train.jsonl`):
```
=== Intent Distribution ===
find_restaurant: 10773
find_hotel: 10540
find_train: 9594
find_attraction: 8133
book_restaurant: 4409
book_hotel: 4403
find_taxi: 3695
book_train: 2409
find_hospital: 707
find_police: 477
find_bus: 8

=== Slot Distribution ===
restaurant-area: 13995
hotel-area: 8694
attraction-area: 4800
...
hospital-department: 334
...
bus-departure: 25
bus-destination: 10
```

**Observation**: Emergency intents (`find_hospital`, `find_police`, `find_bus`) and their slots (e.g., `hospital-department`, `bus-departure`) are significantly underrepresented compared to non-emergency intents like `find_restaurant` and `find_hotel`. For example, `find_hospital` has only 707 instances in `train` (vs. 10,773 for `find_restaurant`), and `find_bus` has just 8. This imbalance can lead to poor model performance on emergency-related queries, which are critical for real-world dialogue systems.

### 3. Augment Emergency Data
Generates synthetic samples for emergency intents (`find_hospital`, `find_police`, `find_pharmacy`, `find_embassy`) to address data imbalance, targeting 12,500 samples per intent to match the scale of dominant intents.

```bash
python augment_emergency_data.py
```

**Why Augmentation?** The analysis shows emergency intents are severely underrepresented (e.g., `find_hospital`: 707 in `train`, 8 in `dev`, 12 in `test`; `find_police`: 477 in `train`, 0 in `dev`, 5 in `test`; `find_bus`: 8 in `train`, 0 in `dev`/`test`). Augmentation ensures sufficient training data for these critical intents, improving model performance and generalization for emergency queries.

**Output**: `augmented_find_hospital.jsonl`, `augmented_find_police.jsonl`, `augmented_find_pharmacy.jsonl`, `augmented_find_embassy.jsonl` with synthetic dialogue samples.

### 4. Merge JSONL Files
Combines the converted (`t5_train.jsonl`, `t5_test.jsonl`, `t5_dev.jsonl`) and augmented JSONL files into a single file for comprehensive dataset analysis or training.

```bash
python merge_jsonl.py merged_all.jsonl t5_train.jsonl t5_test.jsonl t5_dev.jsonl augmented_find_hospital.jsonl augmented_find_police.jsonl augmented_find_pharmacy.jsonl augmented_find_embassy.jsonl
```

**Output Example** (from `merged_all.jsonl`):
```json
{"input": "USER: I need train reservations from norwich to cambridge", "target": "intents: find_train; slots: train-departure=norwich; train-destination=cambridge"}
{"input": "USER: I need train reservations from norwich to cambridge SYSTEM: I have 133 trains matching your request. Is there a specific day and time you would like to travel? USER: I'd like to leave on Monday and arrive by 18:00.", "target": "intents: find_train; slots: train-arriveby=18:00; train-day=monday; train-departure=norwich; train-destination=cambridge"}
{"input": "USER: I need train reservations from norwich to cambridge SYSTEM: I have 133 trains matching your request. Is there a specific day and time you would like to travel? USER: I'd like to leave on Monday and arrive by 18:00. SYSTEM: There are 12 trains for the day and time you request. Would you like to book it now? USER: Before booking, I would also like to know the travel time, price, and departure time please.", "target": "intents: find_train; slots: train-arriveby=18:00; train-day=monday; train-departure=norwich; train-destination=cambridge"}
{"input": "USER: I need train reservations from norwich to cambridge SYSTEM: I have 133 trains matching your request. Is there a specific day and time you would like to travel? USER: I'd like to leave on Monday and arrive by 18:00. SYSTEM: There are 12 trains for the day and time you request. Would you like to book it now? USER: Before booking, I would also like to know the travel time, price, and departure time please. SYSTEM: There are 12 trains meeting your needs with the first leaving at 05:16 and the last one leaving at 16:16. Do you want to book one of these? USER: No hold off on booking for now. Can you help me find an attraction called cineworld cinema?", "target": "intents: find_attraction; slots: attraction-name=cineworld cinema; train-arriveby=18:00; train-day=monday; train-departure=norwich; train-destination=cambridge"}
{"input": "USER: I need train reservations from norwich to cambridge SYSTEM: I have 133 trains matching your request. Is there a specific day and time you would like to travel? USER: I'd like to leave on Monday and arrive by 18:00. SYSTEM: There are 12 trains for the day and time you request. Would you like to book it now? USER: Before booking, I would also like to know the travel time, price, and departure time please. SYSTEM: There are 12 trains meeting your needs with the first leaving at 05:16 and the last one leaving at 16:16. Do you want to book one of these? USER: No hold off on booking for now. Can you help me find an attraction called cineworld cinema? SYSTEM: Yes it is a cinema located in the south part of town what information would you like on it? USER: Yes, that was all I needed. Thank you very much!", "target": "intents: NONE; slots: attraction-name=cineworld cinema; train-arriveby=18:00; train-day=monday; train-departure=norwich; train-destination=cambridge"}
```

**Purpose of Merging**: The `merged_all.jsonl` file combines `train`, `dev`, `test`, and augmented emergency datasets into a single file, enabling comprehensive analysis or training on a balanced dataset that includes sufficient emergency intent samples. Note: For typical machine learning workflows, keep `dev` and `test` separate to avoid data leakage during evaluation.

## Data Format

JSONL files contain:
- `input`: Dialogue history (USER and SYSTEM turns).
- `target`: Intents (separated by `|`) and slots (separated by `;`) in the format `intents: <intent1>|<intent2>; slots: <slot_name>=<slot_value>`.

## Contributing

1. Fork the repository.
2. Create a branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contact

Open an issue on GitHub or contact [your-email@example.com](mailto:your-email@example.com) for questions.