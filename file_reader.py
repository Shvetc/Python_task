import argparse
import os.path
import sys

class PersonInfo:
    def __init__(self, name, surname, age, job_name):
        self.name_ = name
        self.surname_ = surname
        self.surname_ = surname
        self.job_name_ = job_name
        self.age_ = age
    def get_name(self):
        return self.name_
    def surname(self):
        return self.surname_
    def age(self):
        return self.age_
    def job_name(self):
        return self.job_name_

class JobNameCondition:
    def __init__(self, job_name):
        self.job_name_ = job_name
    def __call__(self, person_info):
        if person_info.job_name() == self.job_name_:
            return True
        else:
            return False

class AgeCondition:
    def __init__(self, age):
        self.age_ = age
    def __call__(self, person_info):
        if int(person_info.age()) > self.age_:
            return True
        else:
            return False

class EmptyCondition:
    def __init__(self, condition_operand):
        self.condition_operand = 0
    def __call__(self, person_info):
        return True

def simple_printer(data, dst=sys.stdout):
    print(data, file=dst)

def json_printer(data, dst=sys.stdout):
    # need to be implemented to support json format
    simple_printer(data, dst)

def get_printer(args):
    if args.print_format == 'simple':
        return simple_printer
    if args.print_format == 'json':
        return json_printer

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', required=True, help="Provide file name")
    # to be flexible several formats are possible, but now only simple print is implemented
    parser.add_argument('--print_format', required=False, choices=['simple', 'json', 'csv'], default='simple',  help="Choose print format")
    args = parser.parse_args()
    return args

def print_all_persons_with_specific_condition(persons_data, condition=EmptyCondition(0), printer=simple_printer):
    person_id = 0
    for person_info in persons_data:
        #person_info = person.split(';')
        if condition(person_info):
            printer("{} person:\n    Name: {}\n    Surname: {}\n    Age: {}\n    Job: {}\n".format(person_id, person_info.get_name(), person_info.surname(), person_info.age(), person_info.job_name() ))
        person_id += 1

def write_to_file_all_person_with_job(file_name, persons_data, condition=JobNameCondition('none'), printer=simple_printer):
    f = open(file_name, 'w')
    printer("Name;Surname;Age;Job", dst=f)
    for person_info in persons_data:
        #person_info = person.split(';')
        if not condition(person_info):
            printer(data = "{};{};{};{}".format(person_info.get_name(), person_info.surname(), person_info.age(), person_info.job_name() ), dst=f)

def remove_person_with_none_job(persons_data, condition=JobNameCondition('none')):
    for person_info in persons_data:
        if condition(person_info):
            persons_data.remove(person_info)

def main():
    # parse arguments
    args = parse_argument()
    # get file name
    file_name = args.file_name
    printer = get_printer(args)
    # check is file exist
    if os.path.isfile(file_name):
        f = open(file_name, 'r')
        print("file_name:", args.file_name)
        persons_data = []#cretion list 
        for line in f:
            # read line and remove '\n' symbol
            line = line[:-1]
            #print(line)
            person_info = line.split(';')
            person_info = PersonInfo(person_info[0],
                                     person_info[1],
                                     person_info[2],
                                     person_info[3])
            persons_data.append(person_info)
            
        # save and remove header
        #header = persons_data[0]
        del persons_data[0]

        # print all persons without any conditions, format can be specified by user
        print("All persons without any conditions:")
        print_all_persons_with_specific_condition(persons_data)

        # print all persons with specific job name
        print("All persons with job == managers:")
        print_all_persons_with_specific_condition(persons_data, JobNameCondition('manager'), printer)

        # print all persons with specific job name
        print("All persons with age > 22:")
        print_all_persons_with_specific_condition(persons_data, AgeCondition(22), printer)

        # write to file
        write_to_file_all_person_with_job('out.log', persons_data)

        # delete from common list
        remove_person_with_none_job(persons_data)
        print_all_persons_with_specific_condition(persons_data)
    else:
        print("File was not found")

if __name__ == '__main__':
    main()
