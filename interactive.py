import zipfile
from xml.dom.minidom import parse, parseString

path_to_zip_file = input("[1] Enter path to Polygon zip file (default ./polygon.zip): ") or "./polygon.zip"
directory_to_extract = input("[2] Enter directory to extract to (default ./problem_polygon): ") or "./problem_polygon/"


with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract)

document = parse(f"{directory_to_extract}/problem.xml")
print(f"+ Parsed {directory_to_extract}/problem.xml")
problem_name = document.getElementsByTagName("problem")[0].getAttribute("short-name")

print(f"+ Generating your {problem_name} config...")

names: dict[str, str] = {} # language: name
