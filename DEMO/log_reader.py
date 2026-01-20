import argparse
import sys

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

# If any new error pops-up which was not there with the baseline run, the current comparision will be marked as failed.
# If there are no new errors, but also none of the errors are marked solved, then no change will be the result.
# If atleast 1 error is solved, and no new errors are being introduced, then only pass will be forwarded.
# We know that effort matters more than results, but as the errors keep being solved will eventually result in a finished product that meets expectations, so this tough verdicts.
    
def analyzer(new_run,base_line_run,summary_only_mode):
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
            new_errors[error_string]=nr_error
            new_errors_count+=nr_error

    if not summary_only_mode:
        print("================== Regression Comparison ===================")
        print("Baseline File:",base_line_run)
        print("New Run File:",new_run)

        print("\n[New Errors]")
        if new_errors:
            for key in new_errors:
                print('\t',key,':',new_errors[key])
        else:
            print('\t(none)')

        print("\n[Solved Errors]")
        if solved_errors:
            for key in solved_errors:
                print('\t',key,':',solved_errors[key])
        else:
            print('\t(none)')

        print("\n[Unchanged Errors]")
        if persistent_error:
            for key in persistent_error:
                print('\t',key,':',persistent_error[key])
        else:
            print('\t(none)')

    print("\n\n------------- FINAL VERDICT ---------------")

    if new_errors_count>0:
        print('Result : FAIL')
        return 1
    elif solved_errors_count==0:
        print('Result : NO CHANGE')
        return 2
    else:
        print('Result : PASS')
        return 0

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Analyze new runs alongside the older benchmark run.')
    
    parser.add_argument("--baseline",required=True,help='Enter the benchmark run log file with correct path.')
    parser.add_argument("--newrun",required=True,help='Enter the new run log file with correct path.')
    parser.add_argument("--summary",action='store_true',help='Show only final verdict.')

    args = parser.parse_args()

    baseline_run = args.baseline
    new_run = args.newrun
    summary_only = args.summary

    exit_code = analyzer(new_run,baseline_run,summary_only)
    sys.exit(exit_code)
