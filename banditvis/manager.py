from multiprocessing import Process
from pprint import pprint
import sys
import time

from .parse import Parse
from .plot import HistPlot, VarPlot
from .data import HistData, VarData
from .animation import HistAnimation, EllipseAnimation

def banditvis():
    start_time = time.clock()

    try:
        if sys.argv[1].endswith('.txt'):
            input_file = sys.argv[1]
        else:
            sys.exit("ERROR: You need input a .txt file.")
    except IndexError:
        sys.exit("ERROR: You need to specify a file.")
    try:
        core_dict = Parse("Input/{}".format(input_file))  # builds an initial dictionary of values
    except FileNotFoundError:
        sys.exit("ERROR: The file you tried to input doesn't exist in the current directory.")

    print("\n\n--Completed core_dict--\n\n")
    pprint(core_dict)
    print("--\n\n")

    if core_dict['init'] == 'Histogram':
        p1 = Process(target=HistData, args=(core_dict, ))
        p1.start()
        if core_dict['Animate']:
            HistAnimation(core_dict)
        p1.join()  # holds main() until p1 is done
        HistPlot(core_dict)


    elif core_dict['init'] == 'Variable':
        p1 = Process(target=VarData, args=(core_dict, ))
        p1.start()
        p1.join()
        VarPlot(core_dict)

    elif core_dict['init'] == 'Visualize':
        from Build.Plot.Animation import ConfAnimation
        if core_dict['visual'] == 'ellipse':
            EllipseAnimation(core_dict)
        elif core_dict['visual'] == 'confidence':
            ConfAnimation(core_dict)

    stop_time = time.clock()
    m, s = divmod(stop_time - start_time, 60)
    h, m = divmod(m, 60)
    print ("\nRuntime: {:d}h {:d}m {:.3f}s".format(int(h), int(m), s))