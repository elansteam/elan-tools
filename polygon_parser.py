import os
import zipfile
import shutil
from xml.dom.minidom import parse, parseString
from typings import ElanProblem, ElanProblemExampleTest, ElanProblemLocalized, ElanProblemStatements, InvalidProblem

def unzip(path_to_zip_file: str, directory_to_extract: str):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract)

def parse_polygon(polygon_dir: str, elan_dir: str):
    # elan dir looks like "/elan/problems/problem{id}"
    problem_id = int(elan_dir.split("problem")[-1])
    
    document = parse(f"{polygon_dir}/problem.xml")
    print(f"+ Parsed {polygon_dir}/problem.xml")
    problem_name = document.getElementsByTagName("problem")[0].getAttribute("short-name")

    print(f"+ Generating your {problem_name} config...")

    names: dict[str, str] = {
        name.getAttribute("language"): name.getAttribute("value") for name in document.getElementsByTagName("name")
    }
    
    time_limit = int(document.getElementsByTagName('time-limit')[0].firstChild.nodeValue)
    memory_limit = int(document.getElementsByTagName('memory-limit')[0].firstChild.nodeValue)
    
    
    # Parsing statements
    statements: dict[str, ElanProblemStatements] = {}
    for language in names.keys():
        os.makedirs(f"{elan_dir}/statements/{language}")
        tests = [
            ElanProblemExampleTest(
                input=open(f"{polygon_dir}/statement-sections/{language}/{test}").read().strip(),
                output=open(f"{polygon_dir}/statement-sections/{language}/{test}.a").read().strip()
            ) for test in [
                test for test in os.listdir(
                    f"{polygon_dir}/statement-sections/{language}"
                ) if test.startswith("example") and not test.endswith(".a")
            ]
        ]
        files = [
            "name", "legend", "input", "output", "scoring", "notes", "tutorial"
        ]
        required_files = [
            "input", "output"
        ]
        elan_statements_kwargs = {}
        for file in files:
            if os.path.exists(f"{polygon_dir}/statement-sections/{language}/input.tex"):
                shutil.copy(
                    f"{polygon_dir}/statement-sections/{language}/{file}.tex",
                    f"{elan_dir}/statements/{language}/{file}.mdx"
                )
                elan_statements_kwargs[file] = f"{elan_dir}/statements/{language}/{file}.mdx"
            elif file in required_files:
                raise InvalidProblem(f"Required statement file not found (bad Polygon archive?): {polygon_dir}/statement-sections/{language}/{file}.tex")
        statements[language] = ElanProblemStatements(
            **elan_statements_kwargs,
            tests=tests
        )
    
    variants: dict[str, ElanProblemLocalized] = {}
    for language in names.keys():
        variants[language] = ElanProblemLocalized(
            problem_id=problem_id,
            problem_short_name=problem_name,
            name=names[language],
            statements=statements[language]
        )
    return ElanProblem(
        problem_id=problem_id,
        problem_short_name=problem_name,
        time_limit=time_limit,
        memory_limit=memory_limit,
        variants=variants
    )

unzip("./birthday-mex-4.zip", "./problem_polygon")
print(parse_polygon("./problem_polygon", "./problem1"))