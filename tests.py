from functions.run_python_file import run_python_file


def main():
    output = [
        run_python_file('calculator', 'main.py'),
        run_python_file('calculator', 'tests.py'),
        run_python_file('calculator', '../main.py'),
        run_python_file('calculator', 'nonexistent.py')
    ]
    print('\n\n'.join(output))


if __name__ == '__main__':
    main()
