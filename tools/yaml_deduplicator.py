import os
import re

from model import Statistics

# Exceptions for skipping specific keys or values
KEY_EXCEPTIONS = {}
VALUE_EXCEPTIONS = {'%'}

STATS = []
csv_header = ['Filename', 'Total keys', 'Unique values', 'Duplicated values']
input_dir = ".."
endswith_yaml = ".yaml"

# Folder names
all_new_yaml = "all_new_yaml"
output_dir = "../new"

# YAML file names
value_to_keys_file = "value_to_keys.yaml"
replacement_file = "replacement.yaml"
# Statistics file name
statistics = "statistics.csv"


# Loads a flat YAML file and returns a list of (key, value) pairs
def load_flat_yaml(filepath):
    parsed = []
    with open(filepath, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            try:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip("'").strip('"')
                parsed.append((key, value))
            except ValueError:
                continue
    return parsed


# Groups keys by their associated values
def group_keys_by_values(pairs):
    value_to_keys = {}
    for key, value in pairs:
        if value not in value_to_keys:
            value_to_keys[value] = []
        value_to_keys[value].append(key)
    return value_to_keys


# Escapes special characters in a YAML string
def escape_yaml_string(value):
    return re.sub(
        r'([\\\n\r\t"])', lambda m: {
            '\\': r'\\\\',
            '\n': r'\\n',
            '\r': r'\\r',
            '\t': r'\\t',
            '"': r'\\"'
        }[m.group()], value)


# Writes keys grouped by their values (only values with more than one key)
def write_grouped_keys(value_to_keys, output_path):
    filtered = {
        value: keys
        for value, keys in value_to_keys.items()
        if len(keys) > 1
    }

    def get_sort_group(value):
        words = value.split()
        if len(value) == 1:
            return 0
        elif len(words) == 1:
            return 1
        elif len(words) == 2:
            return 2
        elif len(words) == 3:
            return 3
        else:
            return 4

    sorted_items = sorted(filtered.items(), key=lambda x: (get_sort_group(x[0]), x[0]))

    with open(output_path, "w", encoding="utf-8") as f:
        for value, keys in sorted_items:
            escaped = escape_yaml_string(value)
            f.write(f'"{escaped}":\n')
            for key in keys:
                f.write(f"- {key}\n")


# Writes a map of duplicate keys (one representative key mapped to all duplicates)
def write_duplicates_keys_map(value_to_keys, output_path):
    duplicates = {}
    for value, keys in value_to_keys.items():
        if (
            len(keys) > 1
            and len(value) != 1
            and value not in VALUE_EXCEPTIONS
            and all(k not in KEY_EXCEPTIONS for k in keys)
        ):
            duplicates[keys[0]] = keys

    with open(output_path, "w", encoding="utf-8") as f:
        for key, keys in duplicates.items():
            formatted_line = ", ".join(keys)
            f.write(f"{key}: {formatted_line}\n")


# Writes a cleaned YAML file, removing duplicate values unless explicitly allowed
def write_cleaned_yaml(pairs, output_path):
    seen_values = set()
    cleaned_pairs = []
    for key, value in pairs:
        if value in VALUE_EXCEPTIONS or value not in seen_values:
            cleaned_pairs.append((key, value))
            seen_values.add(value)
        elif key in KEY_EXCEPTIONS:
            cleaned_pairs.append((key, value))

    with open(output_path, "w", encoding="utf-8") as f:
        for key, value in cleaned_pairs:
            f.write(f"{key}: '{value}'\n")


# Writes collected statistics to a CSV file
def write_statistics(stats, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\t'.join(csv_header) + '\n')
        for stat in stats:
            f.write(stat.get_csv_line())


# Collects statistical information from the YAML data
def collect_statistics(filename, pairs, value_to_keys):
    total_keys = len(set(k for k, _ in pairs))
    unique_values = len(set(v for _, v in pairs))
    duplicated_values = sum(1 for keys in value_to_keys.values() if len(keys) > 1)

    STATS.append(Statistics(
        filename=filename,
        total_keys=total_keys,
        unique_values=unique_values,
        duplicated_values=duplicated_values
    ))


# Processes a single YAML file and writes grouped, duplicate, and cleaned outputs
def process_yaml_file(filepath, output_base):
    filename = os.path.basename(filepath)
    filename_no_ext = os.path.splitext(filename)[0]

    output_folder = os.path.join(output_base, filename_no_ext)
    os.makedirs(output_folder, exist_ok=True)

    pairs = load_flat_yaml(filepath)
    value_to_keys = group_keys_by_values(pairs)

    collect_statistics(filename, pairs, value_to_keys)

    write_grouped_keys(value_to_keys, os.path.join(output_folder, value_to_keys_file))
    write_duplicates_keys_map(value_to_keys, os.path.join(output_folder, replacement_file))
    write_cleaned_yaml(pairs, os.path.join(output_folder, filename))

    all_yaml_path = os.path.join(output_base, all_new_yaml)
    os.makedirs(all_yaml_path, exist_ok=True)
    write_cleaned_yaml(pairs, os.path.join(all_yaml_path, filename))


# Main function: processes all YAML files and saves results
def main():
    output_base = os.path.join(output_dir)
    os.makedirs(output_base, exist_ok=True)

    yaml_files = [f for f in os.listdir(input_dir) if f.endswith(endswith_yaml)]

    for yaml_file in yaml_files:
        process_yaml_file(os.path.join(input_dir, yaml_file), output_base)

    write_statistics(STATS, os.path.join(output_base, statistics))

    print(f"Processing complete. Statistics saved to {statistics}.")


if __name__ == "__main__":
    main()
