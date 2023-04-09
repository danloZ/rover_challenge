import logging 
from utils import *

INPUT = "test_input"
OUTPUT = "test_output"
ROVER_NUMBER = 2

logging.basicConfig(level=logging.INFO,format="%(levelname)s | %(asctime)s | %(message)s")

def read_instructions(test_input_source,test_output_source):

    rover_conf = []
    plateau_limit = None

    with open(test_input_source) as instructions:
        try:
            content = instructions.readline()
            max_x, max_y = content.split(' ')
            plateau_limit = (int(max_x), int(max_y))
            logging.info("Plateau size read {x} {y}".format(x=max_x, y=max_y))
        except Exception as e:
            logging.exception("Error while reading input file")
            raise Exception(e.msg)

        for i in range(1,ROVER_NUMBER+1):
            conf = {"plateau_limit":plateau_limit}
            try:
                content = instructions.readline()
                x, y, orientation = content.split()
                conf["rover_start_position"] = (int(x),int(y))
                conf["rover_start_orientation"] = orientation
                logging.info("Rover{n} start position read {x} {y} {o}".format(n=i,x=x,y=y,o=orientation))
            except Exception as e:
                logging.exception("Error while reading input file")
                raise Exception(e.msg)

            try:
                content = instructions.readline()
                instruction_sequence = content.split()
                conf["rover_instruction_set"] = instruction_sequence
                logging.info("Rover{n} instructions read".format(n=i))
            except Exception as e:
                logging.exception("Error while reading input file")
                raise Exception(e.msg)
            
            rover_conf.append(conf)
        
        with open(test_output_source) as output_file:
            for i in range(0, ROVER_NUMBER):
                content = output_file.readline()
                test_sequence = content.split()
                rover_conf[i]["expected_position"]=' '.join(test_sequence)

    return rover_conf

def run_rover(rover_name,rover_conf):
    #create new rover
    new_rover = rover(rover_name, rover_conf["rover_start_position"], rover_conf["rover_start_orientation"], rover_conf["plateau_limit"])
    #run the rover following input instructions
    final_position = new_rover(rover_conf["rover_instruction_set"])
    #check final position is equal to expected one
    assert(final_position == rover_conf["expected_position"])
    logging.info("ROVER {name} REACHED EXPECTED DESTINATION, TEST SUCCEDED!".format(name=rover_name))
    del new_rover
    return


def main():
    rover_conf_set = read_instructions(INPUT, OUTPUT)
    logging.info("Input reading completed")
    for i in range(1,ROVER_NUMBER+1):
        run_rover("rover{n}".format(n=i),rover_conf_set[i-1])
    logging.info("Run {n} rovers".format(n=i))
    

if __name__ == '__main__':
    main()
