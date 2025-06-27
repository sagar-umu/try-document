import os
import subprocess

# Define the parent directory where you want to scan for subdirectories
parent_directory = './docs'  # Parent directory where we scan for subdirectories

# Function to get the list of files in a specific directory (ignores untracked files)
def get_files_from_repo(directory):
    # Run `git ls-files` to get all tracked files in the given directory
    result = subprocess.run(['git', 'ls-files', directory], stdout=subprocess.PIPE)
    files = result.stdout.decode().splitlines()
    
    # Filter out .md files and get only file names (not the full paths)
    files_to_include = [file.split(os.sep)[-1] for file in files if not file.endswith('.md')]  # Get only file name
    
    # Convert to markdown file list format
    markdown_list = [f"- [{file}]({file})" for file in files_to_include]
    
    return markdown_list

# Function to generate file_list.md for each subdirectory inside the parent directory
def generate_file_list_for_subdirectories():
    # Loop through all subdirectories inside the parent_directory
    for subdir in os.listdir(parent_directory):
        subdir_path = os.path.join(parent_directory, subdir)
        
        # Only process directories, skip files
        if os.path.isdir(subdir_path):
            # Get list of files for this subdirectory (excluding .md files)
            file_list = get_files_from_repo(subdir_path)
            
            # Create a file_list.md inside each subdirectory
            file_list_path = os.path.join(subdir_path, 'file_list.md')
            with open(file_list_path, 'w') as f:
                f.write(f"# List of Files in the {subdir} Directory (excluding .md files)\n\n")
                f.write("\n".join(file_list))

# Run the function to generate file lists
if __name__ == "__main__":
    generate_file_list_for_subdirectories()
