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

    solved_errors={}
    new_errors={}
    persistant={}

    total_new_error=0
    total_solved_error=0
    total_persistant_error=0

    for key in log_new:
        new_count = log_new[key]
        old_count = log_old.get(key,0)

        if new_count>old_count:
            new_errors[key]=new_count-old_count
            total_new_error+=(new_count-old_count)
        elif new_count==old_count:
            persistant[key]=old_count
            total_persistant_error+=old_count

    for key in log_old:
        new_count = log_new.get(key,0)
        old_count = log_old.get(key,0)

        if old_count>new_count:
            solved_errors[key]=old_count-new_count
            total_solved_error+=(old_count-new_count)

    print("Solved Errors:",solved_errors)
    print("New Errors:",new_errors)
    print("Not Changed:",persistant)

    print("FINAL VERDICT")

    if total_new_error>total_solved_error:
        print("FAIL")
    elif total_new_error<total_solved_error:
        print("PASS")
    else:
        print("NO CHANGE")


if __name__ == "__main__":
    compare_logs('./logs/new_line.log','./logs/sample.log')