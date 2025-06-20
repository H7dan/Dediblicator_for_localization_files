# Tools for Localization File Deduplication and Analysis

This repository contains 2 scripts and 1 model located in the `tools` directory. These tools help identify and handle duplicate values in localization `.yaml` files.

## Contents

- `yaml_deduplicator.py` — finds all duplicate values in localization files and generates cleaned files and statistics.
- `finder.py` — checks if a given value already exists before adding a new key-value pair.
- `model.py` — used internally for collecting statistics.

---

## 📄 Script Descriptions

### `yaml_deduplicator.py`

This script scans localization `.yaml` files for duplicate values. It performs the following actions:

- Creates a `new` folder in the root directory.
- Inside `new`, it creates:
  - A folder containing **deduplicated versions** of the original files (only the first occurrence of each value is kept).
  - For each original localization file, a separate folder with:
    - A deduplicated version of the file.
    - A `value_to_keys.yaml` file mapping each duplicate value to all keys that shared it.
    - A `replacement.yaml` file mapping each preserved key to keys that referred to the same value.
- Additionally, a `statistics.csv` file is generated with an overview of:
  - Total number of keys.
  - Unique values.
  - Number of duplicated values found in each file.

#### Notable features:
- You can define **exceptions** — specific keys or values that should not be changed, even if they are duplicates.
- Values consisting of only **one character** are ignored by default.

---

### `finder.py`

This utility helps to **avoid inserting duplicate values** manually.

- Prompts the user to input a value.
- Searches all `.yaml` files in the parent directory.
- If the value already exists, it returns the corresponding `KEY: VALUE` pair(s).
- If not found, it notifies the user that the value is new.

---

### `model.py`

A technical support module used by `yaml_deduplicator.py` to **gather and store statistical data** during execution.

---

## 🛠️ How to Use

1. Place the `tools` directory in the **same directory as your localization `.yaml` files**.
2. Run the script you need:
   - `yaml_deduplicator.py` for full deduplication and reporting.
   - `finder.py` for checking if a value already exists before adding.





teasting 
try to add reviewer in pull request 
я вспомнил что нужно добавить тех папку с видом как будет выглядеьб рез работы кода