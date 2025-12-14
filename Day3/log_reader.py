def extract_error(log_line):
    current_error = log_line.split(']')
    return current_error[1].strip()

def log_reader(filename):
    errors={}

    with open(filename,'r') as f:
        for line in f:
            if line.startswith('[ERROR]'):
                current_error = extract_error(line)
                errors[current_error] = errors.get(current_error,0) +1

    return errors

def compare_logs(new_run_logfile,baseline_logfile):
    log_new = log_reader(new_run_logfile)
    log_old = log_reader(baseline_logfile)

    print("New Errors...")

    for key in log_new:
        current_count = log_new[key]
        old_count = log_old.get(key,0)

        if current_count>old_count:
            print(key,':',current_count-old_count)

    print("Solved Errors...")

    for key in log_old:
        old_count = log_old[key]
        current_count = log_new.get(key,0)

        if current_count==0:
            print(key,': all')
        elif current_count<old_count:
            print(key,':',old_count-current_count)


if __name__ == "__main__":
    compare_logs('./logs/new_line.log','./logs/sample.log')