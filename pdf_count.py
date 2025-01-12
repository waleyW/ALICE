import os
from pathlib import Path

def count_pdf_files(directory='.'):
    """
    Count PDF files in the specified directory and its subdirectories
    
    Args:
        directory (str): Directory path to search, defaults to current directory
        
    Returns:
        tuple: (total number of PDF files, list of PDF files)
    """
    pdf_count = 0
    pdf_files = []
    
    # Use Path object for directory traversal
    for path in Path(directory).rglob('*.pdf'):
        if path.is_file():  # Ensure it's a file, not a directory
            pdf_count += 1
            pdf_files.append(str(path))
    
    return pdf_count, pdf_files

def main():
    # Get current directory
    current_dir = os.getcwd()
    
    # Count PDF files
    count, files = count_pdf_files(current_dir)
    
    # Print results
    print(f"\nFound {count} PDF files in directory '{current_dir}' and its subdirectories:")
    
    if count > 0:
        print("\nFile list:")
        for file in files:
            print(f"- {file}")
    else:
        print("No PDF files found.")

if __name__ == "__main__":
    main()