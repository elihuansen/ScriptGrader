from ScriptGrader import TestCase, evaluate
import ScriptGrader
ScriptGrader.VERBOSE = True

tests = {
    'q1': [
        TestCase(pipe_inputs = ['1', '2', '3', '4'],
                 expected = ('Initial Deposit: 1\n'
                             'Annual Interest Rate (in %): 2\n'
                             'Annual Compound Frequency (1-12): 3\n'
                             'Num Years: 4\n'
                             'Amount after 4 years is 1.08')),

        TestCase(pipe_inputs = ['5', '5', '1', '20'],
                 expected = ('Initial Deposit: 5\n'
                             'Annual Interest Rate (in %): 5\n'
                             'Annual Compound Frequency (1 - 12): 1\n'
                             'Num Years: 20\n'
                             'Amount after 20 years is 13.27')),
    ]
}

# TODO: Dynamically generate this 🥴
students_scripts = {
    'monty': ['scripts/monty/q1.py']
}

def get_question_num_from(path):
    if path.endswith('.py'):
        return path[path.rfind('q'):].replace('.py', '')

evaluate(
    students_scripts, 
    tests, 
    script_path_to_question=get_question_num_from
)
