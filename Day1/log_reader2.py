def log_reader(filename):
    total = 0
    warning = 0
    error = 0

    with open(filename,"r") as f:
        for line in f:
            total+=1

            if "[ERROR]" in line:
                error+=1
            elif "[WARNING]" in line:
                warning+=1

    print("Read "+filename+" .")
    print(error,"errors found.")
    print(warning,"warnings found.")
    print("Total",total,'lines read.')

if __name__ == "__main__":
    log_reader('./sample.log')