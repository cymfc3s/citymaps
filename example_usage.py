#!/usr/bin/env python3
"""
Example usage script for generating maps for Fusion 360
"""

import subprocess
import sys

def run_example():
    """Run example map generation commands."""
    
    examples = [
        {
            "description": "San Francisco - Feature Based Theme",
            "command": [
                sys.executable, "create_map_poster.py",
                "-c", "San Francisco",
                "-C", "USA",
                "-t", "feature_based",
                "-d", "10000",
                "-f", "svg"
            ]
        },
        {
            "description": "Barcelona - Noir Theme",
            "command": [
                sys.executable, "create_map_poster.py",
                "-c", "Barcelona",
                "-C", "Spain",
                "-t", "noir",
                "-d", "8000",
                "-f", "svg"
            ]
        },
        {
            "description": "Venice - Blueprint Theme",
            "command": [
                sys.executable, "create_map_poster.py",
                "-c", "Venice",
                "-C", "Italy",
                "-t", "blueprint",
                "-d", "4000",
                "-f", "svg"
            ]
        }
    ]
    
    print("Map Poster Generator - Examples")
    print("=" * 50)
    print("\nChoose an example to run:\n")
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}")
    
    print("0. Run all examples")
    print("\nOr run manually:")
    print('python create_map_poster.py -c "Your City" -C "Your Country" -t feature_based -d 10000')
    
    choice = input("\nEnter choice (0-3): ").strip()
    
    if choice == "0":
        # Run all examples
        for example in examples:
            print(f"\n{'='*50}")
            print(f"Running: {example['description']}")
            print('='*50)
            subprocess.run(example['command'])
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        # Run selected example
        example = examples[int(choice) - 1]
        print(f"\nRunning: {example['description']}")
        subprocess.run(example['command'])
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    run_example()
