import subprocess
import os 
import json
# Define the part of the code to run in the global environment
for i in range(15):
    def run_in_global1():
        print("Running part of the code in the global environment...")
        
        # Define the script for the global environment
        global_script = "D:\models\english\content_creator\global_script.py"  # Make sure this script exists and contains your global code
        import os

        # Folder path
        folder_path = r"D:\models\english\photos"

        # Check if the folder exists
        if os.path.exists(folder_path):
            # List all files in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # Check if it's a file and delete it
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted filD: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
        else:
            print("The folder does not exist.")

        # Run the global environment script using the global Python interpreter
        result = subprocess.run(
            [r"C:\\Users\\suraj\\AppData\\Local\\Programs\\Python\\Python310\\python.exe", global_script],
            capture_output=True, text=True
        )
        
        # Check if the process was successful
        if result.returncode == 0:
            print("Global environment result:", result.stdout)
        else:
            print("Error in global environment:", result.stderr)

    def run_in_global2():
        print("Running part of the code in the global environment...")
        
        # Define the script for the global environment
        global_script = r"D:\models\english\content_creator\global_script2.py"  # Make sure this script exists and contains your global code
        
        # Run the global environment script using the global Python interpreter
        result = subprocess.run(
            [r"C:\\Users\\suraj\\AppData\\Local\\Programs\\Python\\Python310\\python.exe", global_script],
            capture_output=True, text=True
        )
        
        # Check if the process was successful
        if result.returncode == 0:
            print("Global environment result:", result.stdout)
        else:
            print("Error in global environment:", result.stderr)

    # Define the part of the code to run in the virtual environment
    def run_in_virtualenv():
        print("Running part of the code in the virtual environment...")
        
        # Define the script for the virtual environment
        virtual_script = r"D:\models\english\content_creator\virtual_script.py"  # Make sure this script exists and contains your virtual environment code
        
        output_final_path = r'D:\models\models_used\english\output\final_output.wav'
        if os.path.exists(output_final_path):
            os.remove(output_final_path)
        # Run the virtual environment script using the virtualenv Python interpreter
        result = subprocess.run(
            [r"D:\F5-TTS\FTTS\Scripts\python.exe", virtual_script],
            capture_output=True, text=True
        )
        
        # Check if the process was successful
        if result.returncode == 0:
            print("Virtual environment result:", result.stdout)
        else:
            print("Error in virtual environment:", result.stderr)

    def del_():
        print("Performing pop...")

        with open(r'D:\models\english\content_creator\prompts.json','r') as f:
            prompts=json.load(f)
            prompts.pop(0)
        with open(r'D:\models\english\content_creator\prompts.json','w') as f:
            json.dump(prompts,f)

        with open(r'D:\models\english\content_creator\script.json','r') as f:
            script=json.load(f)
            script.pop(0)
        with open(r'D:\models\english\content_creator\script.json','w') as f:
            json.dump(script,f)
        
    if __name__ == "__main__":
        # Running both parts
        run_in_global1()
        run_in_virtualenv()
        run_in_global2()

        del_()
