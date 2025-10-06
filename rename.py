import os
# building a interface with tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from tkinter import ttk

class FileRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.directory_var = tk.StringVar()
        self.extensions_var = tk.StringVar(value=".pdf")
        self.suffix_var = tk.StringVar(value="suffix")
        self.prefix_var = tk.StringVar(value="prefix")
        self.keyword_var = tk.StringVar(value="keyword")
        self.add_folder_name_var = tk.BooleanVar(value=False)
        self.case_sensitive_var = tk.BooleanVar(value=False)
        self.ignores_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(10, weight=1)  # Make output row expandable
        
        # Title
        title_label = ttk.Label(main_frame, text="File Renamer Tool", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)
        
        # Directory selection
        ttk.Label(main_frame, text="Working Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        dir_entry = ttk.Entry(main_frame, textvariable=self.directory_var, width=50)
        dir_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_directory).grid(row=1, column=2, pady=5, sticky=tk.W)
        
        # Current directory button
        ttk.Button(main_frame, text="Use Current Directory", command=self.use_current_directory).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Prefix input
        ttk.Label(main_frame, text="File Prefix:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.prefix_var, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Suffix input
        ttk.Label(main_frame, text="File Suffix:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.suffix_var, width=50).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        # Keyword input
        ttk.Label(main_frame, text="Keyword to Search:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.keyword_var, width=50).grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        # Extensions input
        ttk.Label(main_frame, text="File Extensions:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.extensions_var, width=10).grid(row=6, column=1, sticky=tk.W, pady=5, padx=(5, 0))

        # Checkbox to add folder name in the suffix
        ttk.Checkbutton(main_frame, text="Add Folder Name to Suffix", variable=self.add_folder_name_var).grid(row=7, column=0, sticky=tk.W, pady=5)

        # Case sensitive checkbox
        ttk.Checkbutton(main_frame, text="Case Sensitive", variable=self.case_sensitive_var).grid(row=7, column=1, sticky=tk.W, pady=5)
        self.case_sensitive_var.set(True)  # Default to checked

        # Ignore folders input
        ttk.Label(main_frame, text="Folders to Ignore:").grid(row=8, column=0, sticky=tk.W, pady=5)
        ignore_frame = ttk.Frame(main_frame)
        ignore_frame.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ignore_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(ignore_frame, textvariable=self.ignores_var, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Label(ignore_frame, text="(comma-separated)", font=("Arial", 8)).grid(row=1, column=0, sticky=tk.W, padx=(5, 0))
        
        # Buttons frame for better layout
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Preview button
        ttk.Button(button_frame, text="Preview Changes", command=self.preview_changes).grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Execute button
        ttk.Button(button_frame, text="Execute Rename", command=self.execute_rename).grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=10, column=0, sticky=(tk.W, tk.N), pady=(10, 0))

        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=10, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(output_frame, height=12, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Make sure the output expands with window resize
        main_frame.rowconfigure(10, weight=1)
        main_frame.columnconfigure(1, weight=1)
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        
        # Set initial directory to current working directory
        self.use_current_directory()
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)
    
    def use_current_directory(self):
        self.directory_var.set(os.getcwd())
    
    def log_output(self, message):
        """Add message to output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def get_config(self):
        """Get current configuration from GUI inputs"""
        return {
            "case_sensitive": self.case_sensitive_var.get()
        }
    
    def get_ignores_list(self):
        """Parse the ignores string into a list"""
        ignores_str = self.ignores_var.get().strip()
        if not ignores_str:
            return []
        return [item.strip() for item in ignores_str.split(",") if item.strip()]
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.directory_var.get():
            messagebox.showerror("Error", "Please select a directory.")
            return False
        
        if not os.path.exists(self.directory_var.get()):
            messagebox.showerror("Error", "Selected directory does not exist.")
            return False
        
        if not self.keyword_var.get():
            messagebox.showerror("Error", "Please enter a keyword to search for.")
            return False
        
        return True
    
    def preview_changes(self):
        """Preview what files would be renamed without actually renaming them"""
        if not self.validate_inputs():
            return
        
        self.clear_output()
        self.log_output("=== PREVIEW MODE ===")
        self.log_output("The following changes would be made:")
        self.log_output("")
        
        # Simulate the rename operation
        self.simulate_rename_operation()
    
    
# verify if exists another file with the same name
# if true add counter to the name
# else keep the new name

    def get_new_filename(self, directory_path, proposed_name):
        """Generate a new filename based on the proposed name, avoiding conflicts"""
        full_path = os.path.join(directory_path, proposed_name)
        
        # If file doesn't exist, use the proposed name
        if not os.path.exists(full_path):
            return proposed_name
            
        # If file exists, add counter
        name, ext = os.path.splitext(proposed_name)
        counter = 1
        while True:
            new_name = f"{name} ({counter}){ext}"
            new_path = os.path.join(directory_path, new_name)
            if not os.path.exists(new_path):
                return new_name
            counter += 1

    def simulate_rename_operation(self):
        """Simulate the rename operation for preview"""
        directory = self.directory_var.get()
        prefix = self.prefix_var.get()
        keyword = self.keyword_var.get()
        config = self.get_config()
        ignores = self.get_ignores_list()
        base_suffix = self.suffix_var.get()

        def to_lower_case_if_needed(s):
            if not config['case_sensitive']:
                return s.lower()
            return s
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(directory)
            self.log_output(f"Working directory: {directory}")
            
            list_of_folders_to_ignore = ignores if ignores else []
            changes_found = False
            
            # Iterate through files if has no folders
            if not any(os.path.isdir(os.path.join(directory, f)) for f in os.listdir(directory)):
                self.log_output("No folders found, processing files directly.")
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        self.log_output(f"Processing file: {filename}")
                        extension = os.path.splitext(filename)[1]
                        allowed_extensions = self.extensions_var.get().split(',')
                        allowed_extensions = [ext.strip() for ext in allowed_extensions]
                        if extension in allowed_extensions:
                            if to_lower_case_if_needed(keyword) in to_lower_case_if_needed(filename):
                                # check if add folder name is true
                                if self.add_folder_name_var.get():
                                    folder_name = os.path.basename(directory)
                                    new_filename = f'{prefix} {base_suffix} {folder_name}{extension}'
                                else:
                                    new_filename = f'{prefix} {base_suffix}{extension}'
                                new_filename = self.get_new_filename(directory, new_filename)
                                self.log_output(f"  -> Would rename to: {new_filename}")
                                changes_found = True
                            else:
                                self.log_output(f"  -> Keyword '{keyword}' not found in filename.")
                        else:
                            self.log_output(f"  -> Extension '{extension}' not in allowed extensions: {allowed_extensions}")
                if not changes_found:
                    self.log_output("No files found matching the criteria.")
                return
            
            # Iterate through folders and files
            for folder in os.listdir(directory):
                if folder not in list_of_folders_to_ignore:
                    folder_path = os.path.join(directory, folder)
                    if os.path.isdir(folder_path):
                        self.log_output(f"Processing folder: {folder}")

                        # Determine suffix for this folder
                        if self.add_folder_name_var.get():
                            #verify if folder is empty
                            if folder == "" or folder is None:
                                # if true get the current folder name
                                folder = os.path.basename(folder_path)
                            suffix = f"{base_suffix} {folder}"
                        else:
                            suffix = base_suffix

                        for filename in os.listdir(folder_path):
                            file_path = os.path.join(folder_path, filename)
                            if os.path.isfile(file_path):
                                self.log_output(f"  Checking file: {filename}")
                                
                                # Check extension
                                extension = os.path.splitext(filename)[1]
                                allowed_extensions = self.extensions_var.get().split(',')
                                allowed_extensions = [ext.strip() for ext in allowed_extensions]
                                
                                if extension in allowed_extensions:
                                    # Check if keyword matches
                                    if to_lower_case_if_needed(keyword) in to_lower_case_if_needed(filename):
                                        new_filename = f'{prefix} {suffix}{extension}'
                                        new_filename = self.get_new_filename(folder_path, new_filename)
                                        
                                        self.log_output(f"    -> Would rename to: {new_filename}")
                                        changes_found = True
                                    else:
                                        self.log_output(f"    -> Keyword '{keyword}' not found in filename")
                                else:
                                    self.log_output(f"    -> Extension '{extension}' not in allowed extensions: {allowed_extensions}")
            
            if not changes_found:
                self.log_output("No files found matching the criteria.")
                
        except Exception as e:
            self.log_output(f"Error during preview: {str(e)}")
        finally:
            os.chdir(original_cwd)
    
    def execute_rename(self):
        """Execute the actual rename operation"""
        if not self.validate_inputs():
            return
        
        # Confirm with user
        result = messagebox.askyesno("Confirm", 
                                   "Are you sure you want to rename the files? This action cannot be undone.")
        if not result:
            return
        
        self.clear_output()
        self.log_output("=== EXECUTING RENAME OPERATION ===")
        
        # Change to selected directory and execute
        original_cwd = os.getcwd()
        
        try:
            os.chdir(self.directory_var.get())
            
            # Execute the rename function with GUI parameters
            self.execute_rename_operation()
            
            self.log_output("")
            self.log_output("=== RENAME OPERATION COMPLETED ===")
            messagebox.showinfo("Success", "File renaming completed successfully!")
            
        except Exception as e:
            error_msg = f"Error during rename operation: {str(e)}"
            self.log_output(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            os.chdir(original_cwd)
    
    def execute_rename_operation(self):
        """Execute the actual rename operation with logging"""
        prefix = self.prefix_var.get()
        base_suffix = self.suffix_var.get()
        keyword = self.keyword_var.get()
        config = self.get_config()
        ignores = self.get_ignores_list()
        
        def to_lower_case_if_needed(s):
            if not config['case_sensitive']:
                return s.lower()
            return s
        
        directory = os.getcwd()
        list_of_folders_to_ignore = ignores if ignores else []
        self.log_output(f"Current working directory: {directory}")
        # Iterate through files if has no folders
        if not any(os.path.isdir(os.path.join(directory, f)) for f in os.listdir(directory)):
            self.log_output("No folders found, processing files directly.")
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    self.log_output(f"Processing file: {filename}")
                    extension = os.path.splitext(filename)[1]
                    allowed_extensions = self.extensions_var.get().split(',')
                    allowed_extensions = [ext.strip() for ext in allowed_extensions]
                    if extension in allowed_extensions:
                        if to_lower_case_if_needed(keyword) in to_lower_case_if_needed(filename):
                            new_filename = f'{prefix} {base_suffix}{extension}'
                            new_filename = self.get_new_filename(directory, new_filename)
                            self.log_output(f"Renaming to: {new_filename}")
                            os.rename(
                                os.path.join(directory, filename),
                                os.path.join(directory, new_filename)
                            )
                        else:
                            self.log_output(f"Keyword '{keyword}' not found in filename.")
                    # Perform file renaming logic here
            return

        # Iterate through folders and files
        for folders in os.listdir(directory):
            if folders not in list_of_folders_to_ignore:
                folder_path = os.path.join(directory, folders)
                if os.path.isdir(folder_path):
                    self.log_output(f"Processing folder: {folders}")                    
                    # Determine suffix for this folder
                    if self.add_folder_name_var.get():
                        suffix = f"{base_suffix} {folders}"
                    else:
                        suffix = base_suffix
                    
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)
                        if os.path.isfile(file_path):
                            self.log_output(f"Original filename: {filename}")
                            
                            # Check extension
                            extension = os.path.splitext(filename)[1]
                            allowed_extensions = self.extensions_var.get().split(',')
                            allowed_extensions = [ext.strip() for ext in allowed_extensions]
                            
                            if extension in allowed_extensions:
                                # Check if the filename contains the keyword (case insensitive if specified)
                                if to_lower_case_if_needed(keyword) in to_lower_case_if_needed(filename):
                                    new_filename = f'{prefix} {suffix}{extension}'
                                    new_filename = self.get_new_filename(folder_path, new_filename)
                                    self.log_output(f"Renaming to: {new_filename}")
                                    
                                    os.rename(
                                        os.path.join(directory, folders, filename),
                                        os.path.join(directory, folders, new_filename)
                                    )

def main():
    root = tk.Tk()
    app = FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


