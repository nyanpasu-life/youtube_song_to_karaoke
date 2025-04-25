import subprocess
import os

def run_amt_script():
  try:
    # Construct the path to the script
    script_path = "run_amt.py"  # Relative path since cwd will be amt/src

    # Define the working directory for the subprocess
    working_directory = "amt/src"

    # Execute the script using subprocess.run, setting the cwd
    process = subprocess.run(["python", script_path], capture_output=True, text=True, check=True, cwd=working_directory)

    # Print the standard output and standard error from the subprocess
    print("Standard Output:")
    print(process.stdout)
    print("Standard Error:")
    print(process.stderr)

    print("Script execution completed successfully.")

  except subprocess.CalledProcessError as e:
    # Handle errors that occurred during script execution
    print(f"Error executing script: {e}")
    print("Standard Output:")
    print(e.stdout)
    print("Standard Error:")
    print(e.stderr)
  except FileNotFoundError:
    print("Error: run_amt.py not found in amt/src directory or amt/src directory does not exist.")
  except Exception as e:
      print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
  run_amt_script()