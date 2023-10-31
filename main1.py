import subprocess

def install_requirements(requirements_file):
    with open(requirements_file, 'r') as file:
        requirements = file.readlines()
    
    for requirement in requirements:
        package = requirement.strip()
        subprocess.run(['pip', 'install', package])

if __name__ == "__main__":
    requirements_file = "requirements.txt"
    install_requirements(requirements_file)
