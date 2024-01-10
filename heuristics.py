import math

class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0

class HammingHeuristic(Heuristic):
    def get_evaluation(self, state):
        sum=0
        for i in range (0,len(state)):
            if(state[i]==0):
                continue
            if(state[i]!=(i+1)%len(state)):
                sum=sum+1
        return sum


class ManhattanHeuristic(Heuristic):
    def get_evaluation(self, state):
        sum=0
        for i in range (0,len(state)):
            if(state[i]==0):
                continue
            dim=math.sqrt(len(state))
            i1=i//dim
            j1=i%dim
            i2=((state[i]-1)%len(state))//dim
            j2=((state[i]-1)%len(state))%dim
            sum=sum+abs(i1-i2)+abs(j1-j2)
        return sum


