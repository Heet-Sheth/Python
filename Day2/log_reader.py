def extract_exact_error(errorLine):
    currentError = errorLine.split(']')[1].strip()

    return currentError

def log_reader(filename):
    errors={}
    total = 0

    with open(filename,"r") as f:
        for line in f:
            total+=1

            if line.startswith('[ERROR]'):
                currentError = extract_exact_error(line)

                errors[currentError] = errors.get(currentError, 0)+1

    for key in errors:
        print(key,':',errors[key])

    print("---------------")
    print(total,"lines read.")

if __name__ == "__main__":
    log_reader('logs/sample.log')