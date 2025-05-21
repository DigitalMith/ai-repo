import subprocess
import sys

def run_preview():
    print("\n[🔎] Running preview enhancer...")
    subprocess.run([sys.executable, "preview_enhancer.py"])

def run_batch():
    print("\n[⚙️] Running batch processor...")
    subprocess.run([sys.executable, "smart_batch_process.py"])

def main():
    print("""
📸 Smart Batch Image Enhancer
Choose an option:

1. Run preview enhancer (analyze & recommend settings)
2. Run batch processor (apply enhancements)
3. Exit
""")
    
    choice = input("Enter choice [1-3]: ").strip()

    if choice == "1":
        run_preview()
    elif choice == "2":
        run_batch()
    elif choice == "3":
        print("Exiting.")
    else:
        print("Invalid input. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
