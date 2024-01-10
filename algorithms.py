import random
import time
import heapq
import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions


class BFSAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state=initial_state
        toVisit = []
        visited = set()
        toVisit.append([state, []])
        while 1:
            state, actionList = toVisit.pop(0)
            legal_actions = self.get_legal_actions(state)
            if state == goal_state:
                break
            for action in legal_actions:
                new_state = self.apply_action(state, action)
                if new_state not in visited:
                    toVisit.append([new_state, actionList + [action]])
                    visited.add(new_state)

        return actionList


class BestFirstAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        toVisit = []
        visited = set()
        evaluation = self.heuristic.get_evaluation(state)
        heapq.heappush(toVisit, (evaluation, state, []))

        while toVisit:
            eval, state, action_list= heapq.heappop(toVisit)

            if state == goal_state:
                return action_list

            if state not in visited:
                visited.add(state)
                legal_actions = self.get_legal_actions(state)

                for action in legal_actions:
                    new_state = self.apply_action(state, action)
                    new_evaluation = self.heuristic.get_evaluation(new_state)

                    if new_state not in visited:
                        heapq.heappush(toVisit, (new_evaluation, new_state, action_list + [action]))

        return []

class AStarAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        toVisit = []
        visited = set()
        eval = self.heuristic.get_evaluation(state)
        heapq.heappush(toVisit, (eval,0, state, []))
        while 1:
            eval,cost, state, actionList = heapq.heappop(toVisit)
            legal_actions = self.get_legal_actions(state)
            if state == goal_state:
                break
            for action in legal_actions:
                new_state = self.apply_action(state, action)
                if new_state not in visited:
                    price=cost+1
                    eval = self.heuristic.get_evaluation(new_state)
                    heapq.heappush(toVisit,(eval+price,price,new_state,actionList + [action]))
                    visited.add(new_state)

        return actionList


