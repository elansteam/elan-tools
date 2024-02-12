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
        original_tests = [
            test for test in os.listdir(
                f"{polygon_dir}/statement-sections/{language}"
            ) if test.startswith("example") and not test.endswith(".a")
        ]
        tests: list[ElanProblemExampleTest] = []
        os.makedirs(f"{elan_dir}/statements/{language}/examples")
        for test in original_tests:
            test_input = f"{polygon_dir}/statement-sections/{language}/{test}"
            test_output = f"{polygon_dir}/statement-sections/{language}/{test}.a"
            if not os.path.exists(test_output):
                raise InvalidProblem(f"Output file not found for test {test_input}")
            test_num = test.split("example.", maxsplit=1)[-1]
            shutil.copy(test_input, f"{elan_dir}/statements/{language}/examples/{test_num}")
            shutil.copy(test_output, f"{elan_dir}/statements/{language}/examples/{test_num}.a")
            tests.append(ElanProblemExampleTest(
                input=f"{elan_dir}/statements/{language}/examples/{test_num}",
                output=f"{elan_dir}/statements/{language}/examples/{test_num}.a"
            ))
        files = [
            "name", "legend", "input", "output", "scoring", "notes", "tutorial"
        ]
        required_files = [
            "input", "output"
        ]
        elan_statements_kwargs = {}
        for file in files:
            if os.path.exists(f"{polygon_dir}/statement-sections/{language}/{file}.tex"):
                shutil.copy(
                    f"{polygon_dir}/statement-sections/{language}/{file}.tex",
                    f"{elan_dir}/statements/{language}/{file}.mdx"
                )
                elan_statements_kwargs[file] = f"{elan_dir}/statements/{language}/{file}.mdx"
            elif file in required_files:
                raise InvalidProblem(f"Required statement file not found (bad Polygon archive?): {polygon_dir}/statement-sections/{language}/{file}.tex")
        statements[language] = ElanProblemStatements(
            name=elan_statements_kwargs.get("name", None),
            legend=elan_statements_kwargs.get("legend", None),
            input=elan_statements_kwargs.get("input"),
            output=elan_statements_kwargs.get("output"),
            scoring=elan_statements_kwargs.get("scoring", None),
            tests=tests,
            notes=elan_statements_kwargs.get("notes", None),
            tutorial=elan_statements_kwargs.get("tutorial", None)
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