
# MultiWOZ Dialogue Data Processing Pipeline

This repository provides a pipeline for processing and augmenting dialogue data from the [MultiWOZ dataset](https://github.com/budzianowski/multiwoz) for NLP tasks, specifically for **intent and slot prediction** with T5 models. The pipeline converts dialogues, analyzes intent and slot distributions, augments emergency-related intents, and merges datasets for comprehensive analysis or training.

---

## Repository Structure

- **Directories:**
  - `train/`: Training data (JSON files) from MultiWOZ.
  - `dev/`: Development/validation data (JSON files) from MultiWOZ.
  - `test/`: Test data (JSON files) from MultiWOZ.

- **Scripts:**
  - `convert_for_t5.py`: Converts MultiWOZ JSON dialogues into JSONL format for T5 training.
  - `analyze_intent_slots.py`: Analyzes intent, slot, and slot value distributions in JSONL files.
  - `augment_emergency_data.py`: Generates synthetic samples for emergency intents (find_hospital, find_police, find_pharmacy, find_embassy).
  - `merge_jsonl.py`: Merges multiple JSONL files into a single file.

- **Data Files:**
  - Processed files: `t5_train.jsonl`, `t5_dev.jsonl`, `t5_test.jsonl`.
  - Augmented files: `augmented_find_hospital.jsonl`, `augmented_find_police.jsonl`, `augmented_find_pharmacy.jsonl`, `augmented_find_embassy.jsonl`.
  - Merged output: `merged_all.jsonl`.
  - notebook : `t5-travelmate.ipynb` Jupyter notebooks for experiments and fine-tuning

---

## Prerequisites

- Python 3.6+
- No external dependencies (standard libraries: `json`, `argparse`, `collections`, `random`, `glob`).

---

## Installation

```bash
git clone https://github.com/houssem1677/MultiWOZ-T5-Pipeline.git
cd MultiWOZ-T5-Pipeline
python --version
```

---

## Pipeline Overview

### 1. Convert MultiWOZ Data for T5

Converts MultiWOZ JSON dialogues into JSONL format for T5 model training.

```bash
python convert_for_t5.py train/*.json t5_train.jsonl
python convert_for_t5.py dev/*.json t5_dev.jsonl
python convert_for_t5.py test/*.json t5_test.jsonl
```

**Output Example:**

```json
{"input": "USER: i need a place to dine in the center thats expensive", "target": "intents: find_restaurant|find_hotel; slots: restaurant-area=centre; restaurant-pricerange=expensive"}
```

---

### 2. Analyze Intent and Slot Distributions

Analyzes distributions to identify underrepresented intents like emergency queries.

```bash
python analyze_intent_slots.py t5_train.jsonl
```

**Observation:**  
Emergency intents (e.g., `find_hospital`, `find_police`) are significantly underrepresented compared to standard intents like `find_restaurant`.

---

### 3. Augment Emergency Data

Generates synthetic samples to balance emergency intents (target: ~12,500 per intent).

```bash
python augment_emergency_data.py
```

**Output:**  
`augmented_find_hospital.jsonl`, `augmented_find_police.jsonl`, `augmented_find_pharmacy.jsonl`, `augmented_find_embassy.jsonl`.

---

### 4. Merge JSONL Files

Combine all data for a balanced dataset:

```bash
python merge_jsonl.py merged_all.jsonl t5_train.jsonl t5_test.jsonl t5_dev.jsonl augmented_find_hospital.jsonl augmented_find_police.jsonl augmented_find_pharmacy.jsonl augmented_find_embassy.jsonl
```

**Output Example:**

```json
{"input": "USER: I need train reservations from norwich to cambridge", "target": "intents: find_train; slots: train-departure=norwich; train-destination=cambridge"}
```

---

### 5. Fine-Tuning T5 for TravelMate

This notebook demonstrates **training a T5 model on the merged dataset** (`merged_all.jsonl`) for the TravelMate project, including emergency and normal dialogue intents.

- **Notebook:** `t5-travelmate.ipynb`
- **Steps:**
  1. Load `merged_all.jsonl` dataset.
  2. Preprocess data for T5 input and target formatting.
  3. Fine-tune a T5 model (e.g., `t5-small`) for **intent and slot prediction**.
  4. Evaluate on a validation set.

---

## Data Format

JSONL files contain:

- `input`: Dialogue history (USER + SYSTEM turns).  
- `target`: Intents (pipe-separated `|`) and slots (semicolon-separated `;`) in the format:  
`intents: <intent1>|<intent2>; slots: <slot_name>=<slot_value>`

---

## Contributing

1. Fork the repository.  
2. Create a branch: `git checkout -b feature-branch`.  
3. Commit changes: `git commit -m "Add feature"`.  
4. Push: `git push origin feature-branch`.  
5. Open a pull request.

---

## Contact

Open an issue on GitHub or contact [mohamedhoussem45@gmail.com](mailto:mohamedhoussem45@gmail.com).
