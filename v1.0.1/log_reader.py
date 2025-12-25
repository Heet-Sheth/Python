import argparse

def extract_error(line):
    current_error = line.split(']',1)
    return current_error[1].strip()

def log_reader(filename):
    lineCount = 0
    extracted_errors={}

    try:
        with open(filename,'r') as f:
            for line in f:
                lineCount+=1

                if line.startswith('[ERROR]'):
                    errorString = extract_error(line)
                    extracted_errors[errorString]=extracted_errors.get(errorString,0)+1

        if lineCount == 0:
            raise RuntimeError('Empty File.')
        elif len(extracted_errors) == 0:
            print('[INFO] No errors found in',filename,'. Have a great day.')
        
        return extracted_errors
    
    except FileNotFoundError:
        print("[ERROR] File",filename,'not found.')
        return {}
    except RuntimeError:
        print('[INFO]',filename,'is empty. Nothing to analyze')
        return {}
    except Exception as e:
        print('[ERROR]:',e)
        return {}
    
def analyzer(new_run,base_line_run):
    errors_file_1 = log_reader(base_line_run)
    errors_file_2 = log_reader(new_run)

    solved_errors={}
    new_errors={}
    persistent_error={}

    solved_errors_count=0
    new_errors_count=0
    persistent_error_count=0

    for error_string in errors_file_1:
        blr_error = errors_file_1[error_string]
        nr_error = errors_file_2.get(error_string,0)

        if nr_error>blr_error:
            new_errors[error_string]=nr_error-blr_error
            new_errors_count+=nr_error-blr_error
        elif blr_error>nr_error:
            solved_errors[error_string]=blr_error-nr_error
            solved_errors_count+=blr_error-nr_error
        else:
            persistent_error[error_string]=blr_error
            persistent_error_count+=blr_error


    for error_string in errors_file_2:
        nr_error=errors_file_2[error_string]
        blr_error=errors_file_1.get(error_string,0)

        if blr_error==0:
            new_errors[nr_error]=nr_error
            new_errors_count+=nr_error

    print("\n\nComparison Report")
    print('-------------------')

    print("\nNew Error:")
    for key in new_errors:
        print('\t',key,':',new_errors[key])

    print("\nSolved Errors:")
    for key in solved_errors:
        print('\t',key,':',solved_errors[key])

    print("\nUnchanged Errors:")
    for key in persistent_error:
        print('\t',key,':',persistent_error[key])

    print("\n\nFINAL VERDICT")
    print('---------------')

    if new_errors_count>0:
        print('FAIL')
    elif solved_errors_count==0:
        print('NO CHANGE')
    else:
        print('PASS')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Analyze new runs alongside the older benchmark run.')
    
    parser.add_argument("--baseline",required=True,help='Enter the benchmark run log file with correct path.')
    parser.add_argument("--newrun",required=True,help='Enter the new run log file with correct path.')

    args = parser.parse_args()

    baseline_run = args.baseline
    new_run = args.newrun

    analyzer(new_run,baseline_run)
