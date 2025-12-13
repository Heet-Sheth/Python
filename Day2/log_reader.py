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

    sorted_errors = sorted(errors.items(), key = lambda x:x[1], reverse=True)

    for (error,count) in sorted_errors:
        print(error,':',count)
    print("---------------")

    print("Unique errors:",len(errors))
 
    print("---------------")
    print(total,"lines read.")

if __name__ == "__main__":
    log_reader('logs/sample.log')