import sys
import io
from difflib import SequenceMatcher

from termcolor import colored
from pprint import pprint

VERBOSE = False

class ListStream:
    def __init__(self):
        self.data = ''
    def write(self, s):
        self.data += s
    def flush(self):
        self.data = ''

def stdout_output(func):
    def wrapper(*args, **kwargs):
        sys.stdout = x = ListStream()

        output = func(*args, **kwargs)

        sys.stdout = sys.__stdout__

        if VERBOSE:
            print(x.data)

        return x.data
    return wrapper

class InputPipe:
    def __init__(self, inputs=[]):
        self.inputs = inputs

    def __call__(self, prompt):
        send_value = self.inputs.pop(0)
        print(prompt + f'{send_value}')
        return send_value

class BaseScript:
    def __init__(self, code, question, student, inputs=[]):
        self.code = code
        self.question = question
        self.student  = student
        self.inputs = inputs

    def __repr__(self):
        return f'{self.student}: {self.question}'

    @stdout_output
    def run(self):
        try:
            return exec(self.code, {'input': InputPipe(self.inputs)})
        except Exception as e:
            if VERBOSE:
                print(f'ERROR OCCURRED: {e}')

class PyScript(BaseScript):
    def __init__(self, path, question, student, inputs=[]):
        with open(path) as f:
            code = f.read()

        super().__init__(code, question, student, inputs)


class Grader:

    def __init__(self, correct_threshold=0.85):
        self.correct_threshold = correct_threshold

    def evaluate(self, script, testcase):

        output = script.run()
        similarity = self._get_similarity(output, testcase.expected)

        if VERBOSE:
            color = 'green' if similarity >= self.correct_threshold else 'red'
            colored_text = colored(similarity, color, attrs=["bold"])

            print(f'Script output vs Expected output: {colored_text}')

        return similarity >= self.correct_threshold

    def _get_similarity(self, output, testcase):
        return SequenceMatcher(None, output, testcase).ratio()  


class TestCase:
    def __init__(self, pipe_inputs, expected):
        self.inputs = pipe_inputs
        self.expected = expected

def evaluate(students_scripts, tests, script_path_to_question):
    grader = Grader()

    students_scores = {}

    for student, script_paths in students_scripts.items():

        students_scores[student] = {}

        for script_path in script_paths:

            question_num = script_path_to_question(script_path)

            if VERBOSE:
                print(colored(f"          {student} :: {question_num}          ", 'blue', attrs=['bold', 'underline']))

            testcases = tests[question_num]

            students_scores[student][question_num] = []

            for i, testcase in enumerate(testcases):

                if VERBOSE:
                    print(colored(f'\n[TESTCASE {i + 1}]', 'magenta'))

                script = PyScript(script_path, question_num, student, testcase.inputs)
                passed = grader.evaluate(script, testcase)

                score = 1 if passed else 0 
                students_scores[student][question_num].append(score)

    if VERBOSE:
        print(colored('                                ', color='cyan', attrs=['underline']))
        print()
        print(colored('           FINISHED    ...🐌      ', color='cyan', attrs=['bold']))
        print(colored('                                ', color='cyan', attrs=['underline']))

    print()
    pprint(students_scores)