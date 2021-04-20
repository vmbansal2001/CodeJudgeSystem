import sys
import os
import time
from subprocess import Popen, PIPE, TimeoutExpired
from multiprocessing import Pool, Process
import tabulate

def run(input_file, correct_output, python_file, test_case_no):
    input_data = open(input_file).read()
    init_time = time.time()
    process = Popen([sys.executable, python_file], stdin = PIPE, stdout = PIPE, stderr = PIPE)

    try:
        output, error = process.communicate(input_data.encode("utf-8"), timeout=5)
    except TimeoutExpired:
        process.kill()
        return(test_case_no, "Timeout", time.time() - init_time)

    final_time = time.time()

    if process.returncode !=0:
        return(test_case_no, "Run Error", error.decode("utf-8"))

    output = output.decode("utf-8")
    output = output.replace("\r", "")


    k = output.rfind("\n")
    new_string = output[:k] + "" + output[k+1:]
    output = new_string

    runningtime = final_time - init_time
    correct_output = open(correct_output).read()

    result = "Wrong Ans"
    if runningtime<1.0 and correct_output == output:
        result = "Pass"

    elif runningtime>1.0:
        result = "TLE"

    return(test_case_no, result, runningtime)

if(__name__ == "__main__"):
    problemName = sys.argv[1]
    testCaseDir = os.path.join(os.getcwd(), "TestCases", problemName)
    args = []

    for test_case_no in os.listdir(testCaseDir):
        root = os.path.join(testCaseDir,test_case_no)
        problemfiledir = os.path.join(os.getcwd(), "ProgramNames",problemName)+".py"
        arg = (os.path.join(root,"input.txt"),os.path.join(root,"correctOutput.txt"),problemfiledir, test_case_no)
        args.append(arg)

    p = Pool(min(len(args),3))

    results = p.starmap(run, args)
    passCount = 0
    for result in results:
        if result[1] == "Pass":
            passCount+=1

    print(f"{passCount} of {len(results)} Test Cases Passed")
    print(tabulate.tabulate(sorted(results), headers=["Test Case", "Result", "Time Taken/Error Description"],tablefmt="grid"))
