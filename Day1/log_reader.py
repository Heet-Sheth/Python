def log_reader(filename):
    count=0
    error=0
    warning=0

    with open(filename,"r") as f:
        for line in f:
            count+=1

            if "[ERROR]" in line:
                error+=1
            elif "[WARNING]" in line:
                warning+=1

    f.close()

    print("Read",filename)
    print("Errors:",error)
    print("Warnings:",warning)
    print("Read",count,"lines in total")

if __name__ == "__main__":
    log_reader('logs/sample.log')