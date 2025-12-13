def extract_exact_error(error_string):
    current_error = error_string.split(']')[1]
    return current_error.strip()

def log_reader(filename):
    errors = {}
    total = 0

    with open(filename,'r') as f:
        for line in f:
            total+=1

            if line.startswith('[ERROR]'):
                current_error = extract_exact_error(line)
                errors[current_error] = errors.get(current_error,0)+1

        sorted_errors = sorted(
            errors.items(),
            key= lambda x:x[1]
        )

        for (error,freq) in sorted_errors:
            print(error,':',freq)

        print("-----------------------")
        print("Unique errors:",len(errors))
        print("-----------------------")
        print(total,"lines read")

if __name__ == "__main__":
    log_reader('logs/sample.log')