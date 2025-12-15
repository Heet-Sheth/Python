def extract_exact_error(log_line):
    current_error = log_line.split(']',1)   #split string at 1st occurance of ] (closing bracket indicating warnnin gor error)
    return current_error[1].strip() #remove unnecsary leading & trailing spaces 

def log_reader(filename):
    errors={}   #dictionary

    with open(filename,'r') as f:   #open file for reading only (to avoid accidental modifications!!!)
        for line in f:  #read line by line
            if line.startswith('[ERROR]'):  #error representation format as of now.
                current_error = extract_exact_error(line)
                errors[current_error] = errors.get(current_error,0) +1  #increase current unique error count by 1

    return errors

def compare_logs(new_run_logfile,baseline_logfile):
    log_new = log_reader(new_run_logfile)   #old or baseline file
    log_old = log_reader(baseline_logfile)  #new or current file

    solved_errors={}
    new_errors={}
    persistant={}

    total_new_error=0
    total_solved_error=0
    total_persistant_error=0

    for key in log_new:
        new_count = log_new[key]
        old_count = log_old.get(key,0)  #default to 0 if key not found

        if new_count>old_count: #new errors that weren't there with old log
            new_errors[key]=new_count-old_count
            total_new_error+=(new_count-old_count)
        elif new_count==old_count:  #errors with frequency same as that in old files
            persistant[key]=old_count
            total_persistant_error+=old_count

    for key in log_old: #to check old errors that are not there in new file
        new_count = log_new.get(key,0)
        old_count = log_old.get(key,0)

        if old_count>new_count: #if newer run dosen't show or shows less errors than older run
            solved_errors[key]=old_count-new_count
            total_solved_error+=(old_count-new_count)

    print('### - Comparision Report - ###')

    print("Solved Errors:",solved_errors)
    print("New Errors:",new_errors)
    print("Not Changed:",persistant)

    print("### - FINAL VERDICT - ###")

    if total_new_error>0:
        print("FAIL")
    elif total_solved_error==0:
        print("NO CHANGE")
    else:
        print("PASS")


if __name__ == "__main__":
    compare_logs('./logs/new_line.log','./logs/sample.log')