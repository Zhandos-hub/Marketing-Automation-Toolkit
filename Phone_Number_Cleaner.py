"""
Phone Number Cleaner (for mailing)

This script reads a list of phone numbers from 'a.txt', removes all
non-numeric characters, filters out duplicates and error data,
and saves the sorted, clean list to 'output.txt'.
"""

import sys

def clean_phone(raw: str) -> str:
    """Removes all non-digit characters."""
    # Use a generator expression to filter for digits and join them
    return "".join(char for char in raw if char.isdigit())

def main():
    try:
        with open("a.txt", "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"File read error: {e}", file=sys.stderr)
        return

    # Use a set comprehension for efficiency and automatic de-duplication
    cleaned_numbers = {
        clean_phone(line) for line in lines
    }
    
    # Filter the set for valid numbers (non-empty and >= 10 digits)
    valid_numbers = {
        num for num in cleaned_numbers if num and len(num) >= 10
    }

    # Sort the final set
    sorted_list = sorted(valid_numbers)

    try:
        with open("output.txt", "w", encoding="utf-8") as out:
            # Use .join() for fast writing
            out.write("\n".join(sorted_list))
            out.write("\n") # Add final newline
            
    except Exception as e:
        print(f"File write error: {e}", file=sys.stderr)
        return

    print(f"✅ Done. Saved {len(sorted_list)} numbers to output.txt")

if __name__ == "__main__":
    main()