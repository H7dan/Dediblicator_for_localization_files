import os

# Prompts the user to enter a search value (e.g., a string to find in YAML files)
def get_search_value():
    return input("Enter value to search: ").strip()

# Searches through all .yaml files in the parent directory for keys that match the given value
def find_value_in_yamls(target_value):
    found_keys = set()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for filename in os.listdir(base_dir):
        if filename.endswith('.yaml'):
            file_path = os.path.join(base_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if ':' in line and not line.startswith('#'):
                            key, val = line.split(':', 1)
                            cleaned_val = val.strip().strip("'\"")
                            if cleaned_val == target_value:
                                found_keys.add(key.strip())
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")
    return found_keys

# Main function: asks user for a value and prints matching keys found in YAML files
def main():
    target = get_search_value()
    unique_keys = find_value_in_yamls(target)

    if not unique_keys:
        print(f"\nAll clear: '{target}' not found")
    else:
        print(f"\nFound {len(unique_keys)} key(s):")
        for key in sorted(unique_keys):
            print(f"- {key}")

if __name__ == "__main__":
    main()
