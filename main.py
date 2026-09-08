from pid import Pid
from plot import Plot

def main():
    pid = Pid(target=300, start=0, kp=16, ki=0.2, kd=0.1)
    plt = Plot(pid)
    plt.begin()


if __name__ == "__main__":
    main()